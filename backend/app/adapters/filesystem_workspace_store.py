"""Private, manifest-backed storage for local workspaces."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import errno
import json
import os
from pathlib import Path
import re
import shutil
import stat
from typing import Any
from uuid import uuid4

from backend.app.domain.workspace import (
    InvalidWorkspaceName,
    Workspace,
    WorkspaceNotFound,
    WorkspaceStatus,
    WorkspaceStorageUnavailable,
    WorkspaceSummary,
    WorkspaceUnavailable,
    normalize_workspace_name,
    parse_workspace_id,
)


MANIFEST_FILE = "manifest.json"
MAX_MANIFEST_BYTES = 64 * 1024
_MANIFEST_KEYS = {
    "schemaVersion",
    "workspaceId",
    "name",
    "createdAt",
    "activeSnapshotId",
}
_CREATING_PREFIX = ".creating-"
_SUPPORTS_DIRECTORY_HANDLES = (
    hasattr(os, "O_DIRECTORY")
    and hasattr(os, "O_NOFOLLOW")
    and all(
        operation in os.supports_dir_fd
        for operation in (os.open, os.link, os.stat, os.unlink, os.mkdir, os.rmdir)
    )
    and os.listdir in os.supports_fd
)
_RFC3339_UTC = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)$"
)


class _InvalidManifest(ValueError):
    pass


def _path_from_override(value: str, home: Path, cwd: Path) -> Path:
    if value == "~":
        path = home
    elif value.startswith("~/") or value.startswith("~\\"):
        path = home / value[2:]
    else:
        path = Path(value)
        if not path.is_absolute():
            path = cwd / path
    return path.resolve(strict=False)


def resolve_data_root(
    environ: Mapping[str, str],
    platform_name: str,
    home: Path,
    cwd: Path,
) -> Path:
    """Resolve the configured local data directory without performing I/O writes."""
    override = environ.get("SDLC_QE_DATA_DIR", "")
    if override:
        return _path_from_override(override, home, cwd)

    if platform_name == "darwin":
        return (home / "Library/Application Support/SDLC-QE Ontology Workbench").resolve(
            strict=False
        )

    if platform_name in {"win32", "cygwin"}:
        local_app_data = environ.get("LOCALAPPDATA", "")
        if local_app_data:
            local_path = Path(local_app_data)
            if local_path.is_absolute():
                return (local_path / "SDLC-QE Ontology Workbench").resolve(strict=False)
        return (home / "AppData/Local/SDLC-QE Ontology Workbench").resolve(strict=False)

    xdg_data_home = environ.get("XDG_DATA_HOME", "")
    if xdg_data_home:
        xdg_path = Path(xdg_data_home)
        if xdg_path.is_absolute():
            return (xdg_path / "sdlc-qe-ontology-workbench").resolve(strict=False)
    return (home / ".local/share/sdlc-qe-ontology-workbench").resolve(strict=False)


def _duplicate_rejecting_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _InvalidManifest("duplicate key")
        result[key] = value
    return result


def _parse_created_at(value: object) -> datetime:
    if not isinstance(value, str) or not _RFC3339_UTC.fullmatch(value):
        raise _InvalidManifest("invalid timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        raise _InvalidManifest("invalid timestamp") from None
    if parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise _InvalidManifest("timestamp is not UTC")
    return parsed.astimezone(timezone.utc)


def _format_created_at(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z"
    )


def _parse_manifest(raw: bytes, expected_id: str) -> Workspace:
    try:
        decoded = raw.decode("utf-8")
        payload = json.loads(decoded, object_pairs_hook=_duplicate_rejecting_object)
    except (UnicodeDecodeError, ValueError, RecursionError):
        raise _InvalidManifest("invalid JSON") from None

    if not isinstance(payload, dict) or set(payload) != _MANIFEST_KEYS:
        raise _InvalidManifest("invalid manifest shape")

    schema_version = payload["schemaVersion"]
    if isinstance(schema_version, bool) or not isinstance(schema_version, int) or schema_version != 1:
        raise _InvalidManifest("unsupported schema version")
    if payload["workspaceId"] != expected_id:
        raise _InvalidManifest("workspace ID mismatch")
    if payload["activeSnapshotId"] is not None:
        raise _InvalidManifest("snapshot is not supported")

    name = payload["name"]
    try:
        normalized_name = normalize_workspace_name(name)
    except InvalidWorkspaceName:
        raise _InvalidManifest("invalid name") from None
    if name != normalized_name:
        raise _InvalidManifest("name is not normalized")

    created_at = payload["createdAt"]
    parsed_created_at = _parse_created_at(created_at)
    return Workspace(
        workspace_id=expected_id,
        name=normalized_name,
        created_at=_format_created_at(parsed_created_at),
    )


def _is_directory(path: Path) -> bool:
    try:
        return stat.S_ISDIR(path.lstat().st_mode)
    except FileNotFoundError:
        return False


def _ensure_directory(path: Path) -> None:
    """Create a directory tree privately without chmodding any existing directory."""
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        parent = path.parent
        if parent != path:
            _ensure_directory(parent)
        try:
            path.mkdir(mode=0o700)
        except FileExistsError:
            pass
        metadata = path.lstat()
    if not stat.S_ISDIR(metadata.st_mode):
        raise WorkspaceStorageUnavailable


def _path_exists(path: Path) -> bool:
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    return True


def _remove_reservation(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        pass


class FilesystemWorkspaceStore:
    """A lazy local workspace store using one atomic manifest per workspace."""

    def __init__(self, data_root: Path) -> None:
        try:
            self._data_root = Path(data_root).expanduser().resolve(strict=False)
        except (OSError, RuntimeError):
            raise WorkspaceStorageUnavailable from None
        self._workspaces_root = self._data_root / "workspaces"

    def create(self, name: str) -> Workspace:
        normalized_name = normalize_workspace_name(name)
        if os.name != "nt":
            return self._create_posix(normalized_name)

        return self._create_windows(normalized_name)

    def _create_posix(self, normalized_name: str) -> Workspace:
        if not _SUPPORTS_DIRECTORY_HANDLES:
            raise WorkspaceStorageUnavailable

        try:
            _ensure_directory(self._data_root)
            data_fd = self._open_data_root(create=False)
            if data_fd is None:
                raise WorkspaceStorageUnavailable
            try:
                workspaces_fd = self._open_workspaces_root(data_fd, create=True)
            except BaseException:
                os.close(data_fd)
                raise
            if workspaces_fd is None:
                os.close(data_fd)
                raise WorkspaceStorageUnavailable
        except WorkspaceStorageUnavailable:
            raise
        except OSError:
            raise WorkspaceStorageUnavailable from None

        try:
            for _ in range(10):
                workspace_id = str(uuid4())
                reservation_name = f"{_CREATING_PREFIX}{workspace_id}"
                try:
                    reservation_fd = os.open(
                        reservation_name,
                        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                        0o600,
                        dir_fd=workspaces_fd,
                    )
                except FileExistsError:
                    continue

                reservation_stat = os.fstat(reservation_fd)
                staging_name = f".staging-{workspace_id}"
                staging_fd: int | None = None
                final_fd: int | None = None
                manifest_stat: os.stat_result | None = None
                try:
                    try:
                        os.mkdir(staging_name, mode=0o700, dir_fd=workspaces_fd)
                    except FileExistsError:
                        self._unlink_if_owned(
                            workspaces_fd,
                            reservation_name,
                            reservation_stat,
                        )
                        continue
                    staging_fd = self._open_child_directory(workspaces_fd, staging_name)
                    created_at = _format_created_at(datetime.now(timezone.utc))
                    manifest = {
                        "schemaVersion": 1,
                        "workspaceId": workspace_id,
                        "name": normalized_name,
                        "createdAt": created_at,
                        "activeSnapshotId": None,
                    }
                    manifest_stat = self._write_manifest_at(staging_fd, manifest)
                    try:
                        os.mkdir(workspace_id, mode=0o700, dir_fd=workspaces_fd)
                    except FileExistsError:
                        self._remove_manifest_if_owned(staging_fd, manifest_stat)
                        self._remove_child_directory_if_owned(
                            workspaces_fd,
                            staging_name,
                            staging_fd,
                        )
                        self._unlink_if_owned(
                            workspaces_fd,
                            reservation_name,
                            reservation_stat,
                        )
                        continue
                    final_fd = self._open_child_directory(workspaces_fd, workspace_id)
                    self._publish_manifest_at(
                        staging_fd,
                        final_fd,
                        expected_manifest=manifest_stat,
                    )
                    if not self._directory_entry_matches(
                        workspaces_fd,
                        workspace_id,
                        final_fd,
                    ):
                        raise OSError("workspace directory changed during create")
                    if not self._storage_handles_match(data_fd, workspaces_fd):
                        raise OSError("workspace storage root changed during create")
                    self._remove_manifest_if_owned(staging_fd, manifest_stat)
                    self._remove_child_directory_if_owned(
                        workspaces_fd,
                        staging_name,
                        staging_fd,
                    )
                    self._unlink_if_owned(
                        workspaces_fd,
                        reservation_name,
                        reservation_stat,
                    )
                    return Workspace(workspace_id, normalized_name, created_at)
                except OSError:
                    if final_fd is not None and manifest_stat is not None:
                        self._remove_manifest_if_owned(final_fd, manifest_stat)
                    if final_fd is not None:
                        self._remove_child_directory_if_owned(
                            workspaces_fd,
                            workspace_id,
                            final_fd,
                        )
                    if staging_fd is not None:
                        if manifest_stat is not None:
                            self._remove_manifest_if_owned(staging_fd, manifest_stat)
                        self._remove_child_directory_if_owned(
                            workspaces_fd,
                            staging_name,
                            staging_fd,
                        )
                    self._unlink_if_owned(
                        workspaces_fd,
                        reservation_name,
                        reservation_stat,
                    )
                    raise WorkspaceStorageUnavailable from None
                finally:
                    for descriptor in (staging_fd, final_fd, reservation_fd):
                        if descriptor is not None:
                            os.close(descriptor)

            raise WorkspaceStorageUnavailable
        except WorkspaceStorageUnavailable:
            raise
        except OSError:
            raise WorkspaceStorageUnavailable from None
        finally:
            os.close(workspaces_fd)
            os.close(data_fd)

    def _create_windows(self, normalized_name: str) -> Workspace:
        try:
            _ensure_directory(self._data_root)
            self._ensure_workspaces_root(create=True)

            for _ in range(10):
                workspace_id = str(uuid4())
                final_dir = self._workspaces_root / workspace_id
                if _path_exists(final_dir):
                    continue

                reservation = self._workspaces_root / f"{_CREATING_PREFIX}{workspace_id}"
                try:
                    reservation_fd = os.open(
                        reservation,
                        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                        0o600,
                    )
                except FileExistsError:
                    continue
                try:
                    os.close(reservation_fd)
                except OSError:
                    _remove_reservation(reservation)
                    raise

                temp_dir = self._workspaces_root / f".staging-{workspace_id}"
                try:
                    temp_dir.mkdir(mode=0o700)
                except FileExistsError:
                    _remove_reservation(reservation)
                    continue
                except OSError:
                    _remove_reservation(reservation)
                    raise

                try:
                    created_at = _format_created_at(datetime.now(timezone.utc))
                    manifest = {
                        "schemaVersion": 1,
                        "workspaceId": workspace_id,
                        "name": normalized_name,
                        "createdAt": created_at,
                        "activeSnapshotId": None,
                    }
                    self._write_manifest(temp_dir / MANIFEST_FILE, manifest)
                    try:
                        os.rename(temp_dir, final_dir)
                    except FileExistsError:
                        self._remove_owned_temp_dir(temp_dir)
                        _remove_reservation(reservation)
                        continue
                    _remove_reservation(reservation)
                    return Workspace(workspace_id, normalized_name, created_at)
                except OSError:
                    self._remove_owned_temp_dir(temp_dir)
                    _remove_reservation(reservation)
                    raise WorkspaceStorageUnavailable from None

            raise WorkspaceStorageUnavailable
        except WorkspaceStorageUnavailable:
            raise
        except OSError:
            raise WorkspaceStorageUnavailable from None

    def list(self) -> list[WorkspaceSummary]:
        if os.name != "nt":
            return self._list_posix()

        return self._list_windows()

    def _list_posix(self) -> list[WorkspaceSummary]:
        if not _SUPPORTS_DIRECTORY_HANDLES:
            raise WorkspaceStorageUnavailable
        try:
            data_fd = self._open_data_root(create=False)
            if data_fd is None:
                return []
            try:
                workspaces_fd = self._open_workspaces_root(data_fd, create=False)
            except BaseException:
                os.close(data_fd)
                raise
            if workspaces_fd is None:
                os.close(data_fd)
                return []

            summaries: list[WorkspaceSummary] = []
            try:
                for entry_name in os.listdir(workspaces_fd):
                    try:
                        workspace_id = parse_workspace_id(entry_name)
                    except WorkspaceNotFound:
                        continue
                    directory = self._workspaces_root / workspace_id
                    try:
                        metadata = os.stat(
                            workspace_id,
                            dir_fd=workspaces_fd,
                            follow_symlinks=False,
                        )
                    except FileNotFoundError:
                        continue
                    if not stat.S_ISDIR(metadata.st_mode):
                        summaries.append(self._corrupt_summary(workspace_id))
                        continue
                    try:
                        directory_fd = self._open_child_directory(
                            workspaces_fd,
                            workspace_id,
                        )
                    except OSError as error:
                        if error.errno in {errno.ELOOP, errno.ENOTDIR, errno.ENOENT}:
                            summaries.append(self._corrupt_summary(workspace_id))
                            continue
                        raise
                    try:
                        if self._entry_exists(workspaces_fd, f"{_CREATING_PREFIX}{workspace_id}"):
                            try:
                                os.stat(
                                    MANIFEST_FILE,
                                    dir_fd=directory_fd,
                                    follow_symlinks=False,
                                )
                            except FileNotFoundError:
                                continue
                        try:
                            workspace = self._read_workspace(
                                directory,
                                workspace_id,
                                directory_fd=directory_fd,
                                workspaces_fd=workspaces_fd,
                            )
                        except _InvalidManifest:
                            summaries.append(self._corrupt_summary(workspace_id))
                        else:
                            summaries.append(
                                WorkspaceSummary(
                                    workspace_id=workspace.workspace_id,
                                    name=workspace.name,
                                    created_at=workspace.created_at,
                                    status=WorkspaceStatus.EMPTY,
                                )
                            )
                    finally:
                        os.close(directory_fd)

                if not self._storage_handles_match(data_fd, workspaces_fd):
                    raise WorkspaceStorageUnavailable
            finally:
                os.close(workspaces_fd)
                os.close(data_fd)

            return self._sort_summaries(summaries)
        except WorkspaceStorageUnavailable:
            raise
        except OSError:
            raise WorkspaceStorageUnavailable from None

    def _list_windows(self) -> list[WorkspaceSummary]:
        try:
            if not _path_exists(self._data_root):
                return []
            if not _is_directory(self._data_root):
                raise WorkspaceStorageUnavailable
            if not _path_exists(self._workspaces_root):
                return []
            self._ensure_workspaces_root(create=False)

            summaries: list[WorkspaceSummary] = []
            with os.scandir(self._workspaces_root) as entries:
                for entry in entries:
                    try:
                        workspace_id = parse_workspace_id(entry.name)
                    except WorkspaceNotFound:
                        continue
                    directory = self._workspaces_root / workspace_id
                    reservation = self._workspaces_root / f"{_CREATING_PREFIX}{workspace_id}"
                    manifest_path = directory / MANIFEST_FILE
                    if _path_exists(reservation) and not _path_exists(manifest_path):
                        continue
                    try:
                        metadata = directory.lstat()
                    except FileNotFoundError:
                        continue
                    if not stat.S_ISDIR(metadata.st_mode):
                        summaries.append(self._corrupt_summary(workspace_id))
                        continue
                    try:
                        workspace = self._read_workspace(directory, workspace_id)
                    except _InvalidManifest:
                        summaries.append(self._corrupt_summary(workspace_id))
                    else:
                        summaries.append(
                            WorkspaceSummary(
                                workspace_id=workspace.workspace_id,
                                name=workspace.name,
                                created_at=workspace.created_at,
                                status=WorkspaceStatus.EMPTY,
                            )
                        )

            return self._sort_summaries(summaries)
        except WorkspaceStorageUnavailable:
            raise
        except OSError:
            raise WorkspaceStorageUnavailable from None

    def get(self, workspace_id: str) -> Workspace:
        canonical_id = parse_workspace_id(workspace_id)
        if os.name != "nt":
            return self._get_posix(canonical_id)

        return self._get_windows(canonical_id)

    def _get_posix(self, workspace_id: str) -> Workspace:
        if not _SUPPORTS_DIRECTORY_HANDLES:
            raise WorkspaceStorageUnavailable
        data_fd: int | None = None
        workspaces_fd: int | None = None
        try:
            data_fd = self._open_data_root(create=False)
            if data_fd is None:
                raise WorkspaceNotFound
            workspaces_fd = self._open_workspaces_root(data_fd, create=False)
            if workspaces_fd is None:
                raise WorkspaceNotFound
            try:
                directory_fd = self._open_child_directory(workspaces_fd, workspace_id)
            except FileNotFoundError:
                raise WorkspaceNotFound from None
            except OSError as error:
                if error.errno in {errno.ELOOP, errno.ENOTDIR}:
                    raise WorkspaceUnavailable from None
                raise
            try:
                try:
                    workspace = self._read_workspace(
                        self._workspaces_root / workspace_id,
                        workspace_id,
                        directory_fd=directory_fd,
                        workspaces_fd=workspaces_fd,
                    )
                except _InvalidManifest:
                    raise WorkspaceUnavailable from None
                if not self._storage_handles_match(data_fd, workspaces_fd):
                    raise WorkspaceStorageUnavailable
                return workspace
            finally:
                os.close(directory_fd)
        except (WorkspaceNotFound, WorkspaceUnavailable, WorkspaceStorageUnavailable):
            raise
        except OSError:
            raise WorkspaceStorageUnavailable from None
        finally:
            if workspaces_fd is not None:
                os.close(workspaces_fd)
            if data_fd is not None:
                os.close(data_fd)

    def _get_windows(self, workspace_id: str) -> Workspace:
        try:
            if not _path_exists(self._data_root):
                raise WorkspaceNotFound
            if not _is_directory(self._data_root):
                raise WorkspaceStorageUnavailable
            if not _path_exists(self._workspaces_root):
                raise WorkspaceNotFound
            self._ensure_workspaces_root(create=False)
            directory = self._workspaces_root / workspace_id
            try:
                metadata = directory.lstat()
            except FileNotFoundError:
                raise WorkspaceNotFound from None
            if not stat.S_ISDIR(metadata.st_mode):
                raise WorkspaceUnavailable
            try:
                return self._read_workspace(directory, workspace_id)
            except _InvalidManifest:
                raise WorkspaceUnavailable from None
        except (WorkspaceNotFound, WorkspaceUnavailable, WorkspaceStorageUnavailable):
            raise
        except OSError:
            raise WorkspaceStorageUnavailable from None

    def _ensure_workspaces_root(self, *, create: bool) -> None:
        if create:
            _ensure_directory(self._workspaces_root)
        try:
            metadata = self._workspaces_root.lstat()
        except FileNotFoundError:
            raise WorkspaceNotFound
        if not stat.S_ISDIR(metadata.st_mode):
            raise WorkspaceStorageUnavailable

    def _open_data_root(self, *, create: bool) -> int | None:
        if create:
            _ensure_directory(self._data_root)
        try:
            metadata = self._data_root.lstat()
        except FileNotFoundError:
            return None
        if not stat.S_ISDIR(metadata.st_mode):
            raise WorkspaceStorageUnavailable
        descriptor = os.open(
            self._data_root,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
        )
        opened = os.fstat(descriptor)
        if (
            not stat.S_ISDIR(opened.st_mode)
            or opened.st_dev != metadata.st_dev
            or opened.st_ino != metadata.st_ino
            or not self._directory_handle_matches(self._data_root, descriptor)
        ):
            os.close(descriptor)
            raise WorkspaceStorageUnavailable
        return descriptor

    def _open_workspaces_root(self, data_fd: int, *, create: bool) -> int | None:
        if create:
            try:
                os.mkdir("workspaces", mode=0o700, dir_fd=data_fd)
            except FileExistsError:
                pass
        try:
            metadata = os.stat("workspaces", dir_fd=data_fd, follow_symlinks=False)
        except FileNotFoundError:
            return None
        if not stat.S_ISDIR(metadata.st_mode):
            raise WorkspaceStorageUnavailable
        descriptor = self._open_child_directory(data_fd, "workspaces")
        if not self._directory_handle_matches(self._workspaces_root, descriptor):
            os.close(descriptor)
            raise WorkspaceStorageUnavailable
        return descriptor

    @staticmethod
    def _open_child_directory(parent_fd: int, name: str) -> int:
        descriptor = os.open(
            name,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
            dir_fd=parent_fd,
        )
        if not FilesystemWorkspaceStore._directory_entry_matches(
            parent_fd,
            name,
            descriptor,
        ):
            os.close(descriptor)
            raise OSError(errno.ELOOP, "directory entry changed")
        return descriptor

    @staticmethod
    def _directory_entry_matches(parent_fd: int, name: str, descriptor: int) -> bool:
        try:
            named = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            opened = os.fstat(descriptor)
        except OSError:
            return False
        return (
            stat.S_ISDIR(named.st_mode)
            and named.st_dev == opened.st_dev
            and named.st_ino == opened.st_ino
        )

    def _storage_handles_match(self, data_fd: int, workspaces_fd: int) -> bool:
        return (
            self._directory_handle_matches(self._data_root, data_fd)
            and self._directory_entry_matches(data_fd, "workspaces", workspaces_fd)
            and self._directory_handle_matches(self._workspaces_root, workspaces_fd)
        )

    @staticmethod
    def _entry_exists(directory_fd: int, name: str) -> bool:
        try:
            os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            return True
        except FileNotFoundError:
            return False

    @staticmethod
    def _write_manifest_at(
        directory_fd: int,
        manifest: dict[str, Any],
    ) -> os.stat_result:
        descriptor = os.open(
            MANIFEST_FILE,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
            dir_fd=directory_fd,
        )
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(manifest, stream, ensure_ascii=False, separators=(",", ":"))
            stream.flush()
            os.fsync(stream.fileno())
            return os.fstat(stream.fileno())

    @staticmethod
    def _publish_manifest_at(
        source_directory_fd: int,
        destination_directory_fd: int,
        *,
        expected_manifest: os.stat_result,
    ) -> None:
        source = os.stat(
            MANIFEST_FILE,
            dir_fd=source_directory_fd,
            follow_symlinks=False,
        )
        if (
            not stat.S_ISREG(source.st_mode)
            or source.st_dev != expected_manifest.st_dev
            or source.st_ino != expected_manifest.st_ino
        ):
            raise OSError("staged manifest changed during create")
        os.link(
            MANIFEST_FILE,
            MANIFEST_FILE,
            src_dir_fd=source_directory_fd,
            dst_dir_fd=destination_directory_fd,
            follow_symlinks=False,
        )
        published = os.stat(
            MANIFEST_FILE,
            dir_fd=destination_directory_fd,
            follow_symlinks=False,
        )
        if (
            not stat.S_ISREG(published.st_mode)
            or published.st_dev != expected_manifest.st_dev
            or published.st_ino != expected_manifest.st_ino
        ):
            raise OSError("published manifest changed during create")
        os.fsync(destination_directory_fd)
        published_after_sync = os.stat(
            MANIFEST_FILE,
            dir_fd=destination_directory_fd,
            follow_symlinks=False,
        )
        if (
            published_after_sync.st_dev != expected_manifest.st_dev
            or published_after_sync.st_ino != expected_manifest.st_ino
        ):
            raise OSError("published manifest changed during create")

    @staticmethod
    def _unlink_if_owned(
        directory_fd: int,
        name: str,
        expected: os.stat_result,
    ) -> None:
        try:
            current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            if current.st_dev == expected.st_dev and current.st_ino == expected.st_ino:
                os.unlink(name, dir_fd=directory_fd)
        except OSError:
            pass

    @classmethod
    def _remove_manifest_if_owned(
        cls,
        directory_fd: int,
        expected: os.stat_result,
    ) -> None:
        cls._unlink_if_owned(directory_fd, MANIFEST_FILE, expected)

    @staticmethod
    def _remove_child_directory_if_owned(
        parent_fd: int,
        name: str,
        descriptor: int,
    ) -> None:
        try:
            if FilesystemWorkspaceStore._directory_entry_matches(
                parent_fd,
                name,
                descriptor,
            ):
                os.rmdir(name, dir_fd=parent_fd)
        except OSError:
            pass

    @staticmethod
    def _corrupt_summary(workspace_id: str) -> WorkspaceSummary:
        return WorkspaceSummary(
            workspace_id=workspace_id,
            name=None,
            created_at=None,
            status=WorkspaceStatus.CORRUPT,
            issue_code="workspace_manifest_unavailable",
        )

    @staticmethod
    def _sort_summaries(
        summaries: list[WorkspaceSummary],
    ) -> list[WorkspaceSummary]:
        valid = [summary for summary in summaries if summary.created_at is not None]
        corrupt = [summary for summary in summaries if summary.created_at is None]
        valid.sort(key=lambda item: item.workspace_id)
        valid.sort(key=lambda item: _parse_created_at(item.created_at or ""), reverse=True)
        corrupt.sort(key=lambda item: item.workspace_id)
        return valid + corrupt

    @staticmethod
    def _write_manifest(path: Path, manifest: dict[str, Any]) -> None:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        descriptor = os.open(path, flags, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(manifest, stream, ensure_ascii=False, separators=(",", ":"))
            stream.flush()
            os.fsync(stream.fileno())

    @staticmethod
    def _directory_handle_matches(path: Path, descriptor: int) -> bool:
        try:
            named = path.lstat()
        except OSError:
            return False
        opened = os.fstat(descriptor)
        return (
            stat.S_ISDIR(named.st_mode)
            and named.st_dev == opened.st_dev
            and named.st_ino == opened.st_ino
        )

    @staticmethod
    def _read_workspace(
        directory: Path,
        workspace_id: str,
        *,
        directory_fd: int | None = None,
        workspaces_fd: int | None = None,
    ) -> Workspace:
        try:
            if directory_fd is not None:
                metadata = os.stat(
                    MANIFEST_FILE,
                    dir_fd=directory_fd,
                    follow_symlinks=False,
                )
            else:
                directory_metadata = directory.lstat()
                if not stat.S_ISDIR(directory_metadata.st_mode):
                    raise _InvalidManifest("workspace directory unavailable")
                metadata = (directory / MANIFEST_FILE).lstat()
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_MANIFEST_BYTES:
                raise _InvalidManifest("manifest unavailable")

            flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            try:
                if directory_fd is None:
                    descriptor = os.open(directory / MANIFEST_FILE, flags)
                else:
                    descriptor = os.open(MANIFEST_FILE, flags, dir_fd=directory_fd)
            except OSError as error:
                if error.errno in {errno.ELOOP, errno.ENOTDIR, errno.ENOENT}:
                    raise _InvalidManifest("manifest unavailable") from None
                raise
            with os.fdopen(descriptor, "rb") as stream:
                opened_manifest = os.fstat(stream.fileno())
                if (
                    not stat.S_ISREG(opened_manifest.st_mode)
                    or opened_manifest.st_dev != metadata.st_dev
                    or opened_manifest.st_ino != metadata.st_ino
                ):
                    raise _InvalidManifest("manifest unavailable")
                raw = stream.read(MAX_MANIFEST_BYTES + 1)
            if len(raw) > MAX_MANIFEST_BYTES:
                raise _InvalidManifest("manifest too large")
            if directory_fd is not None:
                if workspaces_fd is not None and not FilesystemWorkspaceStore._directory_entry_matches(
                    workspaces_fd,
                    directory.name,
                    directory_fd,
                ):
                    raise _InvalidManifest("workspace directory changed")
            else:
                current_directory_metadata = directory.lstat()
                if (
                    not stat.S_ISDIR(current_directory_metadata.st_mode)
                    or current_directory_metadata.st_dev != directory_metadata.st_dev
                    or current_directory_metadata.st_ino != directory_metadata.st_ino
                ):
                    raise _InvalidManifest("workspace directory changed")
            return _parse_manifest(raw, workspace_id)
        except FileNotFoundError:
            raise _InvalidManifest("manifest missing") from None

    @staticmethod
    def _remove_owned_temp_dir(path: Path) -> None:
        try:
            metadata = path.lstat()
        except FileNotFoundError:
            return
        if stat.S_ISDIR(metadata.st_mode):
            shutil.rmtree(path)
        else:
            path.unlink()
