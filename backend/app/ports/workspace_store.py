from typing import Protocol

from backend.app.domain.workspace import Workspace, WorkspaceSummary


class WorkspaceStore(Protocol):
    def create(self, name: str) -> Workspace: ...

    def list(self) -> list[WorkspaceSummary]: ...

    def get(self, workspace_id: str) -> Workspace: ...
