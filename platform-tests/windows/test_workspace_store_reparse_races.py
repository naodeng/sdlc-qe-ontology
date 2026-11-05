import json
from pathlib import Path
import subprocess

import pytest

from backend.app.adapters import filesystem_workspace_store as store_module
from backend.app.domain.workspace import WorkspaceStorageUnavailable, WorkspaceUnavailable


def _create_junction(link: Path, target: Path) -> None:
    result = subprocess.run(
        ["cmd.exe", "/c", "mklink", "/J", str(link), str(target)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"junction creation failed: {result.stderr.strip()}")


def _write_manifest(directory: Path, workspace_id: str, name: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "manifest.json").write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "workspaceId": workspace_id,
                "name": name,
                "createdAt": "2026-11-05T00:00:00Z",
                "activeSnapshotId": None,
            }
        ),
        encoding="utf-8",
    )


def test_create_does_not_write_through_replaced_staging_junction(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = store_module.FilesystemWorkspaceStore(tmp_path / "data")
    outside = tmp_path / "outside"
    outside.mkdir()
    moved_staging: Path | None = None
    replaced_path: Path | None = None
    real_open_lock = store_module._open_windows_directory_lock
    replaced = False

    def open_after_junction_swap(path: Path, **kwargs) -> int:
        nonlocal moved_staging, replaced_path, replaced
        if path.name.startswith(".staging-") and not replaced:
            moved_staging = path.with_name(f"{path.name}-moved")
            path.rename(moved_staging)
            _create_junction(path, outside)
            replaced_path = path
            replaced = True
        return real_open_lock(path, **kwargs)

    monkeypatch.setattr(
        store_module,
        "_open_windows_directory_lock",
        open_after_junction_swap,
    )

    try:
        with pytest.raises(WorkspaceStorageUnavailable):
            store.create("Project")
        assert replaced
        assert list(outside.iterdir()) == []
    finally:
        if replaced_path is not None and replaced_path.exists():
            replaced_path.rmdir()
        if moved_staging is not None and moved_staging.exists():
            import shutil

            shutil.rmtree(moved_staging)


def test_get_does_not_read_through_replaced_workspace_junction(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = store_module.FilesystemWorkspaceStore(tmp_path / "data")
    workspace = store.create("Project")
    workspace_dir = tmp_path / "data/workspaces" / workspace.workspace_id
    outside = tmp_path / "outside"
    _write_manifest(outside, workspace.workspace_id, "Outside secret")
    moved_workspace = workspace_dir.with_name("moved-workspace")
    replaced = False
    real_open_lock = store_module._open_windows_directory_lock

    def open_after_junction_swap(path: Path, **kwargs) -> int:
        nonlocal replaced
        if path == workspace_dir and not replaced:
            workspace_dir.rename(moved_workspace)
            _create_junction(workspace_dir, outside)
            replaced = True
        return real_open_lock(path, **kwargs)

    monkeypatch.setattr(
        store_module,
        "_open_windows_directory_lock",
        open_after_junction_swap,
    )

    try:
        with pytest.raises(WorkspaceUnavailable):
            store.get(workspace.workspace_id)
        assert replaced
    finally:
        if workspace_dir.exists():
            workspace_dir.rmdir()
        if moved_workspace.exists():
            moved_workspace.rename(workspace_dir)
