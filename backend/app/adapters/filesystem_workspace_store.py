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

                claimed_final_dir = False
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
                        final_dir.mkdir(mode=0o700)
                    except FileExistsError:
                        self._remove_owned_temp_dir(temp_dir)
                        _remove_reservation(reservation)
                        continue
                    claimed_final_dir = True
                    os.rename(temp_dir / MANIFEST_FILE, final_dir / MANIFEST_FILE)
                    claimed_final_dir = False
                    try:
                        temp_dir.rmdir()
                    except OSError:
                        pass
                    _remove_reservation(reservation)
                    return Workspace(workspace_id, normalized_name, created_at)
                except OSError:
                    if claimed_final_dir:
                        try:
                            final_dir.rmdir()
                        except OSError:
                            pass
                    self._remove_owned_temp_dir(temp_dir)
                    _remove_reservation(reservation)
                    raise WorkspaceStorageUnavailable from None

            raise WorkspaceStorageUnavailable
        except WorkspaceStorageUnavailable:
            raise
        except OSError:
            raise WorkspaceStorageUnavailable from None

    def list(self) -> list[WorkspaceSummary]:
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

            valid = [summary for summary in summaries if summary.created_at is not None]
            corrupt = [summary for summary in summaries if summary.created_at is None]
            valid.sort(key=lambda item: item.workspace_id)
            valid.sort(key=lambda item: _parse_created_at(item.created_at or ""), reverse=True)
            corrupt.sort(key=lambda item: item.workspace_id)
            return valid + corrupt
        except WorkspaceStorageUnavailable:
            raise
        except OSError:
            raise WorkspaceStorageUnavailable from None

    def get(self, workspace_id: str) -> Workspace:
        canonical_id = parse_workspace_id(workspace_id)
        try:
            if not _path_exists(self._data_root):
                raise WorkspaceNotFound
            if not _is_directory(self._data_root):
                raise WorkspaceStorageUnavailable
            if not _path_exists(self._workspaces_root):
                raise WorkspaceNotFound
            self._ensure_workspaces_root(create=False)
            directory = self._workspaces_root / canonical_id
            try:
                metadata = directory.lstat()
            except FileNotFoundError:
                raise WorkspaceNotFound from None
            if not stat.S_ISDIR(metadata.st_mode):
                raise WorkspaceUnavailable
            try:
                return self._read_workspace(directory, canonical_id)
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
    def _write_manifest(path: Path, manifest: dict[str, Any]) -> None:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        descriptor = os.open(path, flags, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(manifest, stream, ensure_ascii=False, separators=(",", ":"))
            stream.flush()
            os.fsync(stream.fileno())

    @staticmethod
    def _read_workspace(directory: Path, workspace_id: str) -> Workspace:
        manifest_path = directory / MANIFEST_FILE
        try:
            metadata = manifest_path.lstat()
        except FileNotFoundError:
            raise _InvalidManifest("manifest missing") from None
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_MANIFEST_BYTES:
            raise _InvalidManifest("manifest unavailable")

        flags = os.O_RDONLY
        no_follow = getattr(os, "O_NOFOLLOW", 0)
        flags |= no_follow
        try:
            descriptor = os.open(manifest_path, flags)
        except OSError as error:
            if error.errno == errno.ELOOP:
                raise _InvalidManifest("manifest unavailable") from None
            raise
        with os.fdopen(descriptor, "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise _InvalidManifest("manifest unavailable")
            raw = stream.read(MAX_MANIFEST_BYTES + 1)
        if len(raw) > MAX_MANIFEST_BYTES:
            raise _InvalidManifest("manifest too large")
        return _parse_manifest(raw, workspace_id)

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
