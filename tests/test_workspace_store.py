import errno
import json
import os
import stat
from importlib import import_module
from pathlib import Path
from uuid import UUID

import pytest

from backend.app.domain.workspace import WorkspaceStatus, WorkspaceStorageUnavailable, WorkspaceUnavailable


def _load_store_module():
    try:
        return import_module("backend.app.adapters.filesystem_workspace_store")
    except ModuleNotFoundError as error:
        if error.name == "backend.app.adapters.filesystem_workspace_store":
            pytest.fail("filesystem workspace store is not implemented", pytrace=False)
        raise


def _manifest(
    workspace_id: str,
    *,
    name: str = "Project",
    created_at: str = "2026-11-05T00:00:00Z",
    schema_version: object = 1,
) -> dict[str, object]:
    return {
        "schemaVersion": schema_version,
        "workspaceId": workspace_id,
        "name": name,
        "createdAt": created_at,
        "activeSnapshotId": None,
    }


def _write_manifest(directory: Path, payload: dict[str, object]) -> bytes:
    directory.mkdir(parents=True, exist_ok=True)
    contents = json.dumps(payload).encode("utf-8")
    (directory / "manifest.json").write_bytes(contents)
    return contents


def test_resolve_data_root_uses_platform_default(tmp_path: Path) -> None:
    module = _load_store_module()
    home = tmp_path / "home"
    cwd = tmp_path / "app"

    assert module.resolve_data_root({}, "darwin", home, cwd) == (
        home / "Library/Application Support/SDLC-QE Ontology Workbench"
    )
    assert module.resolve_data_root(
        {"LOCALAPPDATA": str(tmp_path / "local")}, "win32", home, cwd
    ) == tmp_path / "local/SDLC-QE Ontology Workbench"
    assert module.resolve_data_root(
        {"XDG_DATA_HOME": str(tmp_path / "xdg")}, "linux", home, cwd
    ) == tmp_path / "xdg/sdlc-qe-ontology-workbench"
    assert module.resolve_data_root({}, "linux", home, cwd) == (
        home / ".local/share/sdlc-qe-ontology-workbench"
    )


def test_resolve_data_root_expands_home_and_resolves_relative_override(tmp_path: Path) -> None:
    module = _load_store_module()
    home = tmp_path / "home"
    cwd = tmp_path / "application"

    assert module.resolve_data_root(
        {"SDLC_QE_DATA_DIR": "~/private/workbench"}, "linux", home, cwd
    ) == home / "private/workbench"
    assert module.resolve_data_root(
        {"SDLC_QE_DATA_DIR": "../workbench-data"}, "linux", home, cwd
    ) == (cwd / "../workbench-data").resolve()


def test_empty_data_dir_uses_platform_default(tmp_path: Path) -> None:
    module = _load_store_module()

    result = module.resolve_data_root(
        {"SDLC_QE_DATA_DIR": ""}, "darwin", tmp_path / "home", tmp_path / "app"
    )

    assert result == tmp_path / "home/Library/Application Support/SDLC-QE Ontology Workbench"


def test_relative_xdg_data_home_uses_fallback(tmp_path: Path) -> None:
    module = _load_store_module()
    home = tmp_path / "home"

    result = module.resolve_data_root(
        {"XDG_DATA_HOME": "relative/data"}, "linux", home, tmp_path / "app"
    )

    assert result == home / ".local/share/sdlc-qe-ontology-workbench"


def test_list_does_not_create_data_root(tmp_path: Path) -> None:
    module = _load_store_module()
    data_root = tmp_path / "not-created"

    assert module.FilesystemWorkspaceStore(data_root).list() == []
    assert not data_root.exists()


def test_create_writes_v1_manifest_and_returns_workspace(tmp_path: Path) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")

    workspace = store.create("  项目 A  ")
    workspace_dir = tmp_path / "data/workspaces" / workspace.workspace_id
    manifest = json.loads((workspace_dir / "manifest.json").read_text(encoding="utf-8"))

    assert str(UUID(workspace.workspace_id)) == workspace.workspace_id
    assert manifest == {
        "schemaVersion": 1,
        "workspaceId": workspace.workspace_id,
        "name": "项目 A",
        "createdAt": workspace.created_at,
        "activeSnapshotId": None,
    }
    assert workspace.status is WorkspaceStatus.EMPTY
    assert workspace.active_snapshot_id is None
    assert store.get(workspace.workspace_id) == workspace
    assert not any(
        entry.name.startswith(".staging-")
        for entry in (tmp_path / "data/workspaces").iterdir()
    )


@pytest.mark.skipif(os.name == "nt", reason="directory fsync is POSIX-specific")
def test_create_fsyncs_parents_of_new_storage_directories(tmp_path: Path, monkeypatch) -> None:
    module = _load_store_module()
    data_root = tmp_path / "new-parent" / "nested" / "data"
    real_fsync = os.fsync
    real_mkdir = os.mkdir
    events: list[tuple[str, object]] = []

    def record_fsync(descriptor: int) -> None:
        metadata = os.fstat(descriptor)
        if stat.S_ISDIR(metadata.st_mode):
            events.append(("fsync", (metadata.st_dev, metadata.st_ino)))
        real_fsync(descriptor)

    def record_mkdir(path, mode=0o777, *, dir_fd=None) -> None:
        real_mkdir(path, mode, dir_fd=dir_fd)
        candidate = Path(path)
        created_data_dir = candidate in {
            tmp_path / "new-parent",
            tmp_path / "new-parent/nested",
            data_root,
        }
        if created_data_dir or (dir_fd is not None and candidate == Path("workspaces")):
            parent = os.fstat(dir_fd) if dir_fd is not None else candidate.parent.stat()
            parent_identity = (parent.st_dev, parent.st_ino)
            label = str(candidate)
            events.append(("mkdir", (label, parent_identity)))

    monkeypatch.setattr(module.os, "fsync", record_fsync)
    monkeypatch.setattr(module.os, "mkdir", record_mkdir)
    module.FilesystemWorkspaceStore(data_root).create("Project")

    new_data_dirs = [
        tmp_path / "new-parent",
        tmp_path / "new-parent/nested",
        data_root,
        data_root / "workspaces",
    ]
    for directory in new_data_dirs:
        parent = directory.parent.stat()
        parent_identity = (parent.st_dev, parent.st_ino)
        mkdir_event = ("mkdir", ("workspaces" if directory.name == "workspaces" else str(directory), parent_identity))
        mkdir_index = events.index(mkdir_event)
        fsync_index = events.index(("fsync", parent_identity), mkdir_index + 1)
        assert mkdir_index < fsync_index


def test_create_retries_uuid_collision_without_overwriting(tmp_path: Path, monkeypatch) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    existing_id = "7c1b7912-5702-4e5a-b017-25dbd1ca418c"
    existing_dir = tmp_path / "data/workspaces" / existing_id
    old_bytes = _write_manifest(existing_dir, _manifest(existing_id, name="Existing"))
    new_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    generated_ids = iter((UUID(existing_id), UUID(new_id)))
    monkeypatch.setattr(module, "uuid4", lambda: next(generated_ids))

    created = store.create("New workspace")

    assert created.workspace_id == new_id
    assert (existing_dir / "manifest.json").read_bytes() == old_bytes
    assert store.get(existing_id).name == "Existing"


def test_create_retries_collision_at_atomic_destination_claim(
    tmp_path: Path, monkeypatch
) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    existing_id = "7c1b7912-5702-4e5a-b017-25dbd1ca418c"
    existing_dir = tmp_path / "data/workspaces" / existing_id
    new_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    generated_ids = iter((UUID(existing_id), UUID(new_id)))
    monkeypatch.setattr(module, "uuid4", lambda: next(generated_ids))
    collision: dict[str, bytes | int | bool | None] = {"injected": False}

    def inject_existing_workspace() -> None:
        collision["injected"] = True
        collision["manifest"] = _write_manifest(
            existing_dir,
            _manifest(existing_id, name="Existing"),
        )
        collision["inode"] = existing_dir.stat().st_ino

    real_rename = os.rename

    def rename_with_late_collision(source: Path, destination: Path) -> None:
        if Path(destination) == existing_dir and not collision["injected"]:
            inject_existing_workspace()
        real_rename(source, destination)

    real_rename_no_replace = module._rename_directory_no_replace

    def renameat_with_late_collision(parent_fd, source_name, destination_name):
        if destination_name == existing_id and not collision["injected"]:
            inject_existing_workspace()
        real_rename_no_replace(parent_fd, source_name, destination_name)

    if os.name == "nt":
        monkeypatch.setattr(module.os, "rename", rename_with_late_collision)
    else:
        monkeypatch.setattr(module, "_rename_directory_no_replace", renameat_with_late_collision)

    created = store.create("New workspace")

    assert collision["injected"] is True
    assert created.workspace_id == new_id
    assert existing_dir.stat().st_ino == collision["inode"]
    assert (existing_dir / "manifest.json").read_bytes() == collision["manifest"]
    assert store.get(existing_id).name == "Existing"


def test_create_does_not_publish_into_replaced_destination_directory(
    tmp_path: Path, monkeypatch
) -> None:
    if os.name == "nt":
        pytest.skip("this race regression uses POSIX directory operations")
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    final_dir = tmp_path / "data/workspaces" / workspace_id
    moved_dir = final_dir.with_name("moved-workspace")
    replaced = False
    real_mkdir = os.mkdir
    monkeypatch.setattr(module, "uuid4", lambda: UUID(workspace_id))

    def mkdir_with_replacement(path, mode=0o777, *, dir_fd=None):
        nonlocal replaced
        if path == workspace_id and dir_fd is not None and not replaced:
            real_mkdir(path, mode, dir_fd=dir_fd)
            final_dir.rename(moved_dir)
            real_mkdir(path, mode, dir_fd=dir_fd)
            (final_dir / "preserve.txt").write_text("existing directory data", encoding="utf-8")
            replaced = True
        elif dir_fd is None:
            real_mkdir(path, mode)
        else:
            real_mkdir(path, mode, dir_fd=dir_fd)

    monkeypatch.setattr(module.os, "mkdir", mkdir_with_replacement)

    workspace = store.create("Project")

    assert not replaced
    assert workspace.workspace_id == workspace_id
    assert not (final_dir / "preserve.txt").exists()
    assert json.loads((final_dir / "manifest.json").read_text(encoding="utf-8"))[
        "workspaceId"
    ] == workspace_id


def test_create_does_not_publish_through_replaced_destination_symlink(
    tmp_path: Path, monkeypatch
) -> None:
    if os.name == "nt":
        pytest.skip("symlink creation may require elevated privileges on Windows")
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    final_dir = tmp_path / "data/workspaces" / workspace_id
    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    outside_manifest = outside_dir / "manifest.json"
    outside_manifest.write_bytes(b"preserve existing file")
    real_rename_no_replace = module._rename_directory_no_replace
    replaced = False
    monkeypatch.setattr(module, "uuid4", lambda: UUID(workspace_id))

    def rename_with_swap(parent_fd, source_name, destination_name):
        nonlocal replaced
        if destination_name == workspace_id and not replaced:
            final_dir.symlink_to(outside_dir, target_is_directory=True)
            replaced = True
        real_rename_no_replace(parent_fd, source_name, destination_name)

    monkeypatch.setattr(module, "_rename_directory_no_replace", rename_with_swap)

    try:
        with pytest.raises(WorkspaceStorageUnavailable):
            store.create("Project")
        assert replaced
        assert outside_manifest.read_bytes() == b"preserve existing file"
    finally:
        if final_dir.is_symlink():
            final_dir.unlink()


def test_list_ignores_workspace_with_active_creation_marker(tmp_path: Path) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    workspace_dir = tmp_path / "data/workspaces" / workspace_id
    workspace_dir.mkdir(parents=True)
    (workspace_dir.parent / f".creating-{workspace_id}").touch()

    assert store.list() == []


def test_create_failure_does_not_publish_partial_workspace(tmp_path: Path, monkeypatch) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")

    def fail_publication(*args, **kwargs):
        raise OSError("manifest publication failed")

    if os.name == "nt":
        monkeypatch.setattr(module.os, "rename", fail_publication)
    else:
        monkeypatch.setattr(module, "_rename_directory_no_replace", fail_publication)

    with pytest.raises(WorkspaceStorageUnavailable):
        store.create("Project")

    workspaces = tmp_path / "data/workspaces"
    assert [entry for entry in workspaces.iterdir() if not entry.name.startswith(".")] == []
    assert [entry for entry in workspaces.iterdir() if entry.name.startswith(".creating-")] == []


def test_duplicate_names_create_distinct_workspaces(tmp_path: Path) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")

    first = store.create("Same name")
    second = store.create("Same name")

    assert first.workspace_id != second.workspace_id
    assert [item.name for item in store.list()] == ["Same name", "Same name"]


def test_list_orders_newest_first_then_uuid(tmp_path: Path) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    first_id = "7c1b7912-5702-4e5a-b017-25dbd1ca418c"
    second_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    workspace_root = tmp_path / "data/workspaces"
    _write_manifest(
        workspace_root / first_id,
        _manifest(first_id, name="Older", created_at="2026-11-04T23:59:59Z"),
    )
    _write_manifest(
        workspace_root / second_id,
        _manifest(second_id, name="Newer", created_at="2026-11-05T00:00:00Z"),
    )

    assert [item.name for item in store.list()] == ["Newer", "Older"]


def test_list_reports_corrupt_manifest_and_continues(tmp_path: Path) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    valid = store.create("Valid")
    corrupt_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    corrupt_dir = tmp_path / "data/workspaces" / corrupt_id
    corrupt_dir.mkdir(parents=True)
    corrupt_bytes = b"{invalid json"
    (corrupt_dir / "manifest.json").write_bytes(corrupt_bytes)

    summaries = store.list()
    valid_summary = next(item for item in summaries if item.workspace_id == valid.workspace_id)
    corrupt_summary = next(item for item in summaries if item.workspace_id == corrupt_id)

    assert valid_summary.status is WorkspaceStatus.EMPTY
    assert corrupt_summary.status is WorkspaceStatus.CORRUPT
    assert corrupt_summary.name is None
    assert corrupt_summary.created_at is None
    assert corrupt_summary.issue_code == "workspace_manifest_unavailable"
    assert (corrupt_dir / "manifest.json").read_bytes() == corrupt_bytes


def test_list_reports_unsupported_manifest_as_corrupt(tmp_path: Path) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    _write_manifest(
        tmp_path / "data/workspaces" / workspace_id,
        _manifest(workspace_id, schema_version=2),
    )

    summary = store.list()[0]

    assert summary.workspace_id == workspace_id
    assert summary.status is WorkspaceStatus.CORRUPT
    assert summary.issue_code == "workspace_manifest_unavailable"


def test_manifest_workspace_id_must_match_directory(tmp_path: Path) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    directory_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    other_id = "7c1b7912-5702-4e5a-b017-25dbd1ca418c"
    _write_manifest(
        tmp_path / "data/workspaces" / directory_id,
        _manifest(other_id),
    )

    assert store.list()[0].status is WorkspaceStatus.CORRUPT


def test_manifest_rejects_naive_created_at(tmp_path: Path) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    _write_manifest(
        tmp_path / "data/workspaces" / workspace_id,
        _manifest(workspace_id, created_at="2026-11-05T00:00:00"),
    )

    assert store.list()[0].status is WorkspaceStatus.CORRUPT


def test_manifest_rejects_non_utc_created_at(tmp_path: Path) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    _write_manifest(
        tmp_path / "data/workspaces" / workspace_id,
        _manifest(workspace_id, created_at="2026-11-05T08:00:00+08:00"),
    )

    assert store.list()[0].status is WorkspaceStatus.CORRUPT


def test_manifest_rejects_boolean_schema_version(tmp_path: Path) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    _write_manifest(
        tmp_path / "data/workspaces" / workspace_id,
        _manifest(workspace_id, schema_version=True),
    )

    assert store.list()[0].status is WorkspaceStatus.CORRUPT


def test_manifest_rejects_duplicate_keys(tmp_path: Path) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    directory = tmp_path / "data/workspaces" / workspace_id
    directory.mkdir(parents=True)
    manifest = json.dumps(_manifest(workspace_id)).replace(
        '"schemaVersion": 1', '"schemaVersion": 1, "schemaVersion": 1'
    )
    (directory / "manifest.json").write_text(manifest, encoding="utf-8")

    assert store.list()[0].status is WorkspaceStatus.CORRUPT


def test_manifest_rejects_oversized_file(tmp_path: Path) -> None:
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    directory = tmp_path / "data/workspaces" / workspace_id
    directory.mkdir(parents=True)
    (directory / "manifest.json").write_bytes(b" " * (64 * 1024 + 1))

    assert store.list()[0].status is WorkspaceStatus.CORRUPT


def test_store_rejects_symlink_workspaces_root(tmp_path: Path) -> None:
    if os.name == "nt":
        pytest.skip("symlink creation may require elevated privileges on Windows")
    module = _load_store_module()
    data_root = tmp_path / "data"
    data_root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (data_root / "workspaces").symlink_to(outside, target_is_directory=True)

    with pytest.raises(WorkspaceStorageUnavailable):
        module.FilesystemWorkspaceStore(data_root).list()


def test_store_rejects_symlink_workspace_directory(tmp_path: Path) -> None:
    if os.name == "nt":
        pytest.skip("symlink creation may require elevated privileges on Windows")
    module = _load_store_module()
    data_root = tmp_path / "data"
    workspaces = data_root / "workspaces"
    workspaces.mkdir(parents=True)
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    outside = tmp_path / "outside"
    _write_manifest(outside, _manifest(workspace_id, name="Secret outside"))
    (workspaces / workspace_id).symlink_to(outside, target_is_directory=True)
    store = module.FilesystemWorkspaceStore(data_root)

    summary = store.list()[0]

    assert summary.status is WorkspaceStatus.CORRUPT
    assert summary.name is None
    with pytest.raises(WorkspaceUnavailable):
        store.get(workspace_id)


def test_list_does_not_follow_workspace_directory_replaced_with_symlink(
    tmp_path: Path, monkeypatch
) -> None:
    if os.name == "nt":
        pytest.skip("symlink creation may require elevated privileges on Windows")
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    workspace = store.create("Project")
    workspace_dir = tmp_path / "data/workspaces" / workspace.workspace_id
    moved_directory = workspace_dir.with_name("moved-workspace")
    outside_dir = tmp_path / "outside"
    _write_manifest(outside_dir, _manifest(workspace.workspace_id, name="Outside secret"))
    real_open = os.open
    replaced = False

    def open_after_directory_swap(path, flags, *args, **kwargs):
        nonlocal replaced
        if Path(path).name == "manifest.json" and not replaced:
            workspace_dir.rename(moved_directory)
            workspace_dir.symlink_to(outside_dir, target_is_directory=True)
            replaced = True
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(module.os, "open", open_after_directory_swap)

    try:
        summary = next(
            item for item in store.list() if item.workspace_id == workspace.workspace_id
        )
        assert replaced
        assert summary.status is WorkspaceStatus.CORRUPT
        assert summary.name is None
    finally:
        if workspace_dir.is_symlink():
            workspace_dir.unlink()


def test_list_rejects_workspaces_root_replaced_with_symlink(
    tmp_path: Path, monkeypatch
) -> None:
    if os.name == "nt":
        pytest.skip("symlink creation may require elevated privileges on Windows")
    module = _load_store_module()
    data_root = tmp_path / "data"
    workspaces_root = data_root / "workspaces"
    outside_root = tmp_path / "outside"
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    _write_manifest(outside_root / workspace_id, _manifest(workspace_id, name="Outside secret"))
    workspaces_root.mkdir(parents=True)
    moved_root = workspaces_root.with_name("moved-workspaces")
    replaced = False

    def replace_root() -> None:
        nonlocal replaced
        if not replaced:
            workspaces_root.rename(moved_root)
            workspaces_root.symlink_to(outside_root, target_is_directory=True)
            replaced = True

    real_scandir = os.scandir
    real_listdir = os.listdir

    def scandir_with_root_swap(path):
        if Path(path) == workspaces_root:
            replace_root()
        return real_scandir(path)

    def listdir_with_root_swap(path):
        if isinstance(path, int):
            replace_root()
        return real_listdir(path)

    monkeypatch.setattr(module.os, "scandir", scandir_with_root_swap)
    monkeypatch.setattr(module.os, "listdir", listdir_with_root_swap)

    try:
        with pytest.raises(WorkspaceStorageUnavailable):
            module.FilesystemWorkspaceStore(data_root).list()
        assert replaced
    finally:
        if workspaces_root.is_symlink():
            workspaces_root.unlink()


def test_create_does_not_write_through_replaced_workspaces_root_symlink(
    tmp_path: Path, monkeypatch
) -> None:
    if os.name == "nt":
        pytest.skip("symlink creation may require elevated privileges on Windows")
    module = _load_store_module()
    data_root = tmp_path / "data"
    workspaces_root = data_root / "workspaces"
    workspaces_root.mkdir(parents=True)
    outside_root = tmp_path / "outside"
    outside_root.mkdir()
    moved_root = workspaces_root.with_name("moved-workspaces")
    replaced = False
    real_open = os.open
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    monkeypatch.setattr(module, "uuid4", lambda: UUID(workspace_id))

    def open_with_root_swap(path, flags, *args, **kwargs):
        nonlocal replaced
        if Path(path).name == f".creating-{workspace_id}" and not replaced:
            workspaces_root.rename(moved_root)
            workspaces_root.symlink_to(outside_root, target_is_directory=True)
            replaced = True
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(module.os, "open", open_with_root_swap)

    try:
        with pytest.raises(WorkspaceStorageUnavailable):
            module.FilesystemWorkspaceStore(data_root).create("Project")
        assert replaced
        assert list(outside_root.iterdir()) == []
    finally:
        if workspaces_root.is_symlink():
            workspaces_root.unlink()


def test_store_rejects_symlink_manifest(tmp_path: Path) -> None:
    if os.name == "nt":
        pytest.skip("symlink creation may require elevated privileges on Windows")
    module = _load_store_module()
    data_root = tmp_path / "data"
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    workspace_dir = data_root / "workspaces" / workspace_id
    workspace_dir.mkdir(parents=True)
    outside_manifest = tmp_path / "outside-manifest.json"
    outside_manifest.write_text(json.dumps(_manifest(workspace_id, name="Secret")), encoding="utf-8")
    (workspace_dir / "manifest.json").symlink_to(outside_manifest)

    summary = module.FilesystemWorkspaceStore(data_root).list()[0]

    assert summary.status is WorkspaceStatus.CORRUPT
    assert summary.name is None


def test_list_reports_no_follow_eloop_as_corrupt_and_continues(
    tmp_path: Path, monkeypatch
) -> None:
    if os.name == "nt":
        pytest.skip("this race injection depends on POSIX directory descriptors")
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    valid = store.create("Valid")
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    manifest_path = tmp_path / "data/workspaces" / workspace_id / "manifest.json"
    _write_manifest(manifest_path.parent, _manifest(workspace_id))
    real_open = os.open
    real_fstat = os.fstat
    target_directory = manifest_path.parent.stat()

    def open_with_no_follow_race(path, flags, *args, **kwargs):
        is_target_manifest = Path(path) == manifest_path
        if path == "manifest.json" and kwargs.get("dir_fd") is not None:
            directory = real_fstat(kwargs["dir_fd"])
            is_target_manifest = (
                directory.st_dev == target_directory.st_dev
                and directory.st_ino == target_directory.st_ino
            )
        if is_target_manifest and flags & getattr(os, "O_NOFOLLOW", 0):
            raise OSError(errno.ELOOP, "too many levels of symbolic links")
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(module.os, "open", open_with_no_follow_race)

    summaries = store.list()

    valid_summary = next(item for item in summaries if item.workspace_id == valid.workspace_id)
    corrupt_summary = next(item for item in summaries if item.workspace_id == workspace_id)
    assert valid_summary.status is WorkspaceStatus.EMPTY
    assert corrupt_summary.status is WorkspaceStatus.CORRUPT


def test_get_rejects_manifest_replaced_with_fifo_without_blocking(
    tmp_path: Path,
    monkeypatch,
) -> None:
    if os.name == "nt" or not hasattr(os, "mkfifo"):
        pytest.skip("FIFO replacement is a POSIX-only race regression")
    module = _load_store_module()
    store = module.FilesystemWorkspaceStore(tmp_path / "data")
    workspace = store.create("Project")
    manifest_path = (
        tmp_path / "data/workspaces" / workspace.workspace_id / "manifest.json"
    )
    real_open = os.open
    replaced = False

    def open_after_fifo_swap(path, flags, *args, **kwargs):
        nonlocal replaced
        if path == "manifest.json" and kwargs.get("dir_fd") is not None and not replaced:
            manifest_path.unlink()
            os.mkfifo(manifest_path)
            replaced = True
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(module.os, "open", open_after_fifo_swap)

    with pytest.raises(WorkspaceUnavailable):
        store.get(workspace.workspace_id)

    assert replaced


def test_store_errors_never_include_storage_path(tmp_path: Path) -> None:
    module = _load_store_module()
    data_root = tmp_path / "not-a-directory"
    data_root.write_text("not a directory", encoding="utf-8")

    with pytest.raises(WorkspaceStorageUnavailable) as error:
        module.FilesystemWorkspaceStore(data_root).create("Project")

    assert str(data_root) not in str(error.value)


def test_created_storage_uses_private_posix_permissions(tmp_path: Path) -> None:
    if os.name == "nt":
        pytest.skip("POSIX mode bits are not used on Windows")
    module = _load_store_module()
    data_root = tmp_path / "private-data"
    workspace = module.FilesystemWorkspaceStore(data_root).create("Private")
    workspaces_dir = data_root / "workspaces"
    workspace_dir = workspaces_dir / workspace.workspace_id
    manifest_path = workspace_dir / "manifest.json"

    assert data_root.stat().st_mode & 0o777 == 0o700
    assert workspaces_dir.stat().st_mode & 0o777 == 0o700
    assert workspace_dir.stat().st_mode & 0o777 == 0o700
    assert manifest_path.stat().st_mode & 0o777 == 0o600
