"""Private, manifest-backed storage for local workspaces."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import ctypes
import errno
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
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
        for operation in (os.open, os.stat, os.unlink, os.mkdir, os.rmdir)
    )
    and os.listdir in os.supports_fd
)
_RFC3339_UTC = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)$"
)
_WINDOWS_FILE_ATTRIBUTE_DIRECTORY = 0x10
_WINDOWS_FILE_ATTRIBUTE_REPARSE_POINT = 0x400
_WINDOWS_FILE_SHARE_READ = 0x00000001
_WINDOWS_FILE_SHARE_WRITE = 0x00000002
_WINDOWS_FILE_SHARE_DELETE = 0x00000004
_WINDOWS_FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
_WINDOWS_FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
_WINDOWS_FILE_READ_ATTRIBUTES = 0x00000080
_WINDOWS_DELETE = 0x00010000


class _WindowsFileTime(ctypes.Structure):
    _fields_ = [("low", ctypes.c_uint32), ("high", ctypes.c_uint32)]


class _WindowsFileInformation(ctypes.Structure):
    _fields_ = [
        ("attributes", ctypes.c_uint32),
        ("creation_time", _WindowsFileTime),
        ("access_time", _WindowsFileTime),
        ("write_time", _WindowsFileTime),
        ("volume_serial", ctypes.c_uint32),
        ("file_size_high", ctypes.c_uint32),
        ("file_size_low", ctypes.c_uint32),
        ("number_of_links", ctypes.c_uint32),
        ("file_index_high", ctypes.c_uint32),
        ("file_index_low", ctypes.c_uint32),
    ]


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


def _new_workspace_manifest(
    workspace_id: str,
    name: str,
    created_at: str,
) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "workspaceId": workspace_id,
        "name": name,
        "createdAt": created_at,
        "activeSnapshotId": None,
    }


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


def _rename_directory_no_replace(
    parent_fd: int,
    source_name: str,
    destination_name: str,
) -> None:
    if sys.platform not in {"darwin", "linux"}:
        raise OSError(errno.ENOTSUP, "atomic no-replace directory rename is unavailable")

    try:
        libc = ctypes.CDLL(None, use_errno=True)
        rename = libc.renameatx_np if sys.platform == "darwin" else libc.renameat2
    except AttributeError:
        raise OSError(
            errno.ENOTSUP,
            "atomic no-replace directory rename is unavailable",
        ) from None

    rename.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    rename.restype = ctypes.c_int
    result = rename(
        parent_fd,
        os.fsencode(source_name),
        parent_fd,
        os.fsencode(destination_name),
        0x00000004 if sys.platform == "darwin" else 0x00000001,
    )

    if result != 0:
        error = ctypes.get_errno()
        if error == errno.EEXIST:
            raise FileExistsError(error, os.strerror(error), destination_name)
        raise OSError(error, os.strerror(error), destination_name)


def _windows_file_information(handle: int) -> _WindowsFileInformation:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    get_info = kernel32.GetFileInformationByHandle
    get_info.argtypes = [ctypes.c_void_p, ctypes.POINTER(_WindowsFileInformation)]
    get_info.restype = ctypes.c_int
    information = _WindowsFileInformation()
    if not get_info(ctypes.c_void_p(handle), ctypes.byref(information)):
        raise ctypes.WinError(ctypes.get_last_error())
    return information


def _windows_file_identity(handle: int) -> tuple[int, int, int]:
    information = _windows_file_information(handle)
    return (
        information.volume_serial,
        information.file_index_high,
        information.file_index_low,
    )


def _open_windows_directory_lock(
    path: Path,
    *,
    allow_delete_sharing: bool = False,
    desired_access: int = _WINDOWS_FILE_READ_ATTRIBUTES,
) -> int:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    create_file = kernel32.CreateFileW
    create_file.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
    ]
    create_file.restype = ctypes.c_void_p
    share_mode = _WINDOWS_FILE_SHARE_READ | _WINDOWS_FILE_SHARE_WRITE
    if allow_delete_sharing:
        share_mode |= _WINDOWS_FILE_SHARE_DELETE
    handle = create_file(
        str(path),
        desired_access,
        share_mode,
        None,
        3,  # OPEN_EXISTING
        _WINDOWS_FILE_FLAG_BACKUP_SEMANTICS
        | _WINDOWS_FILE_FLAG_OPEN_REPARSE_POINT,
        None,
    )
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())

    try:
        information = _windows_file_information(int(handle))
        if (
            not information.attributes & _WINDOWS_FILE_ATTRIBUTE_DIRECTORY
            or information.attributes & _WINDOWS_FILE_ATTRIBUTE_REPARSE_POINT
        ):
            raise OSError(errno.ELOOP, "storage path is not a plain directory")
    except BaseException:
        _close_windows_directory_lock(int(handle))
        raise
    return int(handle)


def _close_windows_directory_lock(handle: int) -> None:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel32.CloseHandle.restype = ctypes.c_int
    if not kernel32.CloseHandle(ctypes.c_void_p(handle)):
        raise ctypes.WinError(ctypes.get_last_error())


def _read_windows_file(path: Path) -> bytes:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    create_file = kernel32.CreateFileW
    create_file.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
    ]
    create_file.restype = ctypes.c_void_p
    handle = create_file(
        str(path),
        0x80000000 | _WINDOWS_FILE_READ_ATTRIBUTES,  # GENERIC_READ
        _WINDOWS_FILE_SHARE_READ,
        None,
        3,  # OPEN_EXISTING
        _WINDOWS_FILE_FLAG_OPEN_REPARSE_POINT,
        None,
    )
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())

    try:
        handle_value = int(handle)
        information = _windows_file_information(handle_value)
        if (
            information.attributes & _WINDOWS_FILE_ATTRIBUTE_REPARSE_POINT
            or information.attributes & _WINDOWS_FILE_ATTRIBUTE_DIRECTORY
        ):
            raise _InvalidManifest("manifest is not a plain file")
        size = (information.file_size_high << 32) | information.file_size_low
        if size > MAX_MANIFEST_BYTES:
            raise _InvalidManifest("manifest too large")

        read_file = kernel32.ReadFile
        read_file.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.c_void_p,
        ]
        read_file.restype = ctypes.c_int
        chunks: list[bytes] = []
        total = 0
        while total <= MAX_MANIFEST_BYTES:
            capacity = MAX_MANIFEST_BYTES + 1 - total
            buffer = ctypes.create_string_buffer(capacity)
            bytes_read = ctypes.c_uint32()
            if not read_file(
                ctypes.c_void_p(handle_value),
                buffer,
                capacity,
                ctypes.byref(bytes_read),
                None,
            ):
                raise ctypes.WinError(ctypes.get_last_error())
            if bytes_read.value == 0:
                break
            chunks.append(buffer.raw[: bytes_read.value])
            total += bytes_read.value
        raw = b"".join(chunks)
        if len(raw) > MAX_MANIFEST_BYTES:
            raise _InvalidManifest("manifest too large")
        return raw
    finally:
        _close_windows_directory_lock(int(handle))


def _set_windows_delete_disposition(handle: int) -> None:
    class _FileDispositionInfo(ctypes.Structure):
        _fields_ = [("delete_file", ctypes.c_ubyte)]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    set_info = kernel32.SetFileInformationByHandle
    set_info.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
    set_info.restype = ctypes.c_int
    information = _FileDispositionInfo(1)
    if not set_info(
        ctypes.c_void_p(handle),
        4,  # FileDispositionInfo
        ctypes.byref(information),
        ctypes.sizeof(information),
    ):
        raise ctypes.WinError(ctypes.get_last_error())


def _remove_windows_staging_directory(
    path: Path,
    expected_identity: tuple[int, int, int],
) -> None:
    directory_handle: int | None = None
    manifest_handle: int | None = None
    try:
        directory_handle = _open_windows_directory_lock(
            path,
            desired_access=_WINDOWS_FILE_READ_ATTRIBUTES | _WINDOWS_DELETE,
        )
        if _windows_file_identity(directory_handle) != expected_identity:
            return

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        create_file = kernel32.CreateFileW
        create_file.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_void_p,
        ]
        create_file.restype = ctypes.c_void_p
        handle = create_file(
            str(path / MANIFEST_FILE),
            _WINDOWS_DELETE | _WINDOWS_FILE_READ_ATTRIBUTES,
            _WINDOWS_FILE_SHARE_READ | _WINDOWS_FILE_SHARE_WRITE,
            None,
            3,  # OPEN_EXISTING
            _WINDOWS_FILE_FLAG_OPEN_REPARSE_POINT,
            None,
        )
        if handle != ctypes.c_void_p(-1).value:
            manifest_handle = int(handle)
            information = _windows_file_information(manifest_handle)
            if (
                information.attributes & _WINDOWS_FILE_ATTRIBUTE_REPARSE_POINT
                or information.attributes & _WINDOWS_FILE_ATTRIBUTE_DIRECTORY
            ):
                return
            _set_windows_delete_disposition(manifest_handle)
            _close_windows_directory_lock(manifest_handle)
            manifest_handle = None

        _set_windows_delete_disposition(directory_handle)
    except OSError:
        pass
    finally:
        if manifest_handle is not None:
            _close_windows_directory_lock(manifest_handle)
        if directory_handle is not None:
            _close_windows_directory_lock(directory_handle)


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
                manifest_stat: os.stat_result | None = None
                published = False
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
                    manifest = _new_workspace_manifest(
                        workspace_id,
                        normalized_name,
                        created_at,
                    )
                    manifest_stat = self._write_manifest_at(staging_fd, manifest)
                    os.fsync(staging_fd)
                    try:
                        _rename_directory_no_replace(
                            workspaces_fd,
                            staging_name,
                            workspace_id,
                        )
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
                    published = True
                    if not self._directory_entry_matches(
                        workspaces_fd,
                        workspace_id,
                        staging_fd,
                    ):
                        raise OSError("workspace directory changed during create")
                    if not self._storage_handles_match(data_fd, workspaces_fd):
                        raise OSError("workspace storage root changed during create")
                    self._unlink_if_owned(
                        workspaces_fd,
                        reservation_name,
                        reservation_stat,
                    )
                    os.fsync(workspaces_fd)
                    if not self._storage_handles_match(data_fd, workspaces_fd):
                        raise OSError("workspace storage root changed during create")
                    return Workspace(workspace_id, normalized_name, created_at)
                except OSError:
                    if staging_fd is not None and manifest_stat is not None:
                        self._remove_manifest_if_owned(staging_fd, manifest_stat)
                    if staging_fd is not None and published:
                        self._remove_child_directory_if_owned(
                            workspaces_fd,
                            workspace_id,
                            staging_fd,
                        )
                    elif staging_fd is not None:
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
                    for descriptor in (staging_fd, reservation_fd):
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
            root_locks = self._open_windows_root_locks()
            if root_locks is None:
                raise WorkspaceStorageUnavailable
            try:
                return self._create_windows_locked(normalized_name)
            finally:
                self._close_windows_root_locks(root_locks)
        except WorkspaceStorageUnavailable:
            raise
        except OSError:
            raise WorkspaceStorageUnavailable from None

    def _create_windows_locked(self, normalized_name: str) -> Workspace:
        try:

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
                    directory_lock: int | None = None
                    identity_handle: int | None = None
                    final_lock: int | None = None
                    expected_identity: tuple[int, int, int] | None = None
                    published = False
                    created_at = _format_created_at(datetime.now(timezone.utc))
                    manifest = _new_workspace_manifest(
                        workspace_id,
                        normalized_name,
                        created_at,
                    )

                    directory_lock = _open_windows_directory_lock(temp_dir)
                    identity_handle = _open_windows_directory_lock(
                        temp_dir,
                        allow_delete_sharing=True,
                    )
                    expected_identity = _windows_file_identity(directory_lock)
                    if _windows_file_identity(identity_handle) != expected_identity:
                        raise OSError(errno.ELOOP, "staging directory changed")

                    self._write_manifest(temp_dir / MANIFEST_FILE, manifest)
                    _close_windows_directory_lock(directory_lock)
                    directory_lock = None
                    try:
                        os.rename(temp_dir, final_dir)
                    except FileExistsError:
                        if expected_identity is not None:
                            _remove_windows_staging_directory(
                                temp_dir,
                                expected_identity,
                            )
                        _remove_reservation(reservation)
                        continue
                    published = True

                    final_lock = _open_windows_directory_lock(final_dir)
                    if _windows_file_identity(final_lock) != expected_identity:
                        raise OSError(errno.ELOOP, "published directory changed")
                    workspace = self._read_workspace(final_dir, workspace_id)
                    if workspace != Workspace(workspace_id, normalized_name, created_at):
                        raise OSError(errno.EINVAL, "published manifest changed")
                    _remove_reservation(reservation)
                    return workspace
                except OSError:
                    if final_lock is not None:
                        _close_windows_directory_lock(final_lock)
                        final_lock = None
                    if directory_lock is not None:
                        _close_windows_directory_lock(directory_lock)
                        directory_lock = None
                    if expected_identity is not None:
                        _remove_windows_staging_directory(
                            final_dir if published else temp_dir,
                            expected_identity,
                        )
                    _remove_reservation(reservation)
                    raise WorkspaceStorageUnavailable from None
                except _InvalidManifest:
                    if final_lock is not None:
                        _close_windows_directory_lock(final_lock)
                        final_lock = None
                    if directory_lock is not None:
                        _close_windows_directory_lock(directory_lock)
                        directory_lock = None
                    if expected_identity is not None:
                        _remove_windows_staging_directory(
                            final_dir if published else temp_dir,
                            expected_identity,
                        )
                    _remove_reservation(reservation)
                    raise WorkspaceStorageUnavailable from None
                finally:
                    for handle in (final_lock, directory_lock, identity_handle):
                        if handle is not None:
                            _close_windows_directory_lock(handle)

            raise WorkspaceStorageUnavailable
        except WorkspaceStorageUnavailable:
            raise
        except OSError:
            raise WorkspaceStorageUnavailable from None

    def list(self) -> list[WorkspaceSummary]:
        if os.name != "nt":
            return self._list_posix()

        root_locks = self._open_windows_root_locks()
        if root_locks is None:
            return []
        try:
            return self._list_windows()
        finally:
            self._close_windows_root_locks(root_locks)

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

        root_locks = self._open_windows_root_locks()
        if root_locks is None:
            raise WorkspaceNotFound
        try:
            return self._get_windows(canonical_id)
        finally:
            self._close_windows_root_locks(root_locks)

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

    def _open_windows_root_locks(self) -> list[int] | None:
        handles: list[int] = []
        try:
            if not _path_exists(self._data_root) or not _path_exists(
                self._workspaces_root
            ):
                return None
            handles.append(_open_windows_directory_lock(self._data_root))
            handles.append(_open_windows_directory_lock(self._workspaces_root))
            return handles
        except (OSError, AttributeError):
            self._close_windows_root_locks(handles)
            raise WorkspaceStorageUnavailable from None

    @staticmethod
    def _close_windows_root_locks(handles: list[int]) -> None:
        for handle in reversed(handles):
            _close_windows_directory_lock(handle)

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
            if os.name == "nt" and directory_fd is None:
                try:
                    directory_handle = _open_windows_directory_lock(directory)
                except OSError as error:
                    if error.errno in {errno.ELOOP, errno.ENOTDIR, errno.ENOENT}:
                        raise _InvalidManifest("workspace directory unavailable") from None
                    raise
                try:
                    raw = _read_windows_file(directory / MANIFEST_FILE)
                except FileNotFoundError:
                    raise _InvalidManifest("manifest missing") from None
                finally:
                    _close_windows_directory_lock(directory_handle)
                return _parse_manifest(raw, workspace_id)

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
            if os.name != "nt" and hasattr(os, "O_NONBLOCK"):
                flags |= os.O_NONBLOCK
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
