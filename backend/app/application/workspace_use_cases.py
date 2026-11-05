from backend.app.domain.workspace import Workspace, WorkspaceSummary, normalize_workspace_name, parse_workspace_id
from backend.app.ports.workspace_store import WorkspaceStore


class CreateWorkspace:
    def __init__(self, store: WorkspaceStore) -> None:
        self._store = store

    def execute(self, name: str) -> Workspace:
        return self._store.create(normalize_workspace_name(name))


class ListWorkspaces:
    def __init__(self, store: WorkspaceStore) -> None:
        self._store = store

    def execute(self) -> list[WorkspaceSummary]:
        return self._store.list()


class GetWorkspace:
    def __init__(self, store: WorkspaceStore) -> None:
        self._store = store

    def execute(self, workspace_id: str) -> Workspace:
        return self._store.get(parse_workspace_id(workspace_id))
