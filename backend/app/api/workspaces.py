from typing import Literal

from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from backend.app.application.workspace_use_cases import (
    CreateWorkspace,
    GetWorkspace,
    ListWorkspaces,
)
from backend.app.domain.workspace import (
    InvalidWorkspaceName,
    Workspace,
    WorkspaceNotFound,
    WorkspaceStorageUnavailable,
    WorkspaceSummary,
    WorkspaceUnavailable,
)
from backend.app.ports.workspace_store import WorkspaceStore


class WorkspaceCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str


class WorkspaceResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    workspace_id: str
    name: str
    created_at: str
    status: Literal["empty"]
    active_snapshot_id: None


class CorruptWorkspaceResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    workspace_id: str
    name: None
    created_at: None
    status: Literal["corrupt"]
    issue_code: Literal["workspace_manifest_unavailable"]


class WorkspaceListResponse(BaseModel):
    workspaces: list[WorkspaceResponse | CorruptWorkspaceResponse]


class ErrorDetail(BaseModel):
    code: str


class ErrorResponse(BaseModel):
    detail: ErrorDetail


def _workspace_response(workspace: Workspace) -> WorkspaceResponse:
    return WorkspaceResponse(
        workspace_id=workspace.workspace_id,
        name=workspace.name,
        created_at=workspace.created_at,
        status=workspace.status.value,
        active_snapshot_id=workspace.active_snapshot_id,
    )


def _summary_response(summary: WorkspaceSummary) -> WorkspaceResponse | CorruptWorkspaceResponse:
    if summary.issue_code is not None:
        return CorruptWorkspaceResponse(
            workspace_id=summary.workspace_id,
            name=None,
            created_at=None,
            status="corrupt",
            issue_code="workspace_manifest_unavailable",
        )
    return WorkspaceResponse(
        workspace_id=summary.workspace_id,
        name=summary.name or "",
        created_at=summary.created_at or "",
        status=summary.status.value,
        active_snapshot_id=None,
    )


def _error(status_code: int, code: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": {"code": code}})


def create_workspace_router(store: WorkspaceStore) -> APIRouter:
    router = APIRouter(prefix="/api/v1/workspaces", tags=["workspaces"])
    create = CreateWorkspace(store)
    list_workspaces = ListWorkspaces(store)
    get_workspace = GetWorkspace(store)

    @router.post(
        "",
        response_model=WorkspaceResponse,
        status_code=201,
        responses={
            403: {"model": ErrorResponse, "description": "Origin is missing or not allowed."},
            503: {"model": ErrorResponse, "description": "Local workspace storage is unavailable."},
        },
    )
    def create_workspace(
        body: WorkspaceCreateRequest,
        _origin: str = Header(..., alias="Origin"),
    ) -> WorkspaceResponse | JSONResponse:
        try:
            return _workspace_response(create.execute(body.name))
        except InvalidWorkspaceName:
            return _error(422, "workspace_name_invalid")
        except WorkspaceStorageUnavailable:
            return _error(503, "workspace_storage_unavailable")

    @router.get(
        "",
        response_model=WorkspaceListResponse,
        responses={
            503: {"model": ErrorResponse, "description": "Local workspace storage is unavailable."},
        },
    )
    def get_workspaces() -> WorkspaceListResponse | JSONResponse:
        try:
            summaries = list_workspaces.execute()
        except WorkspaceStorageUnavailable:
            return _error(503, "workspace_storage_unavailable")
        return WorkspaceListResponse(workspaces=[_summary_response(item) for item in summaries])

    @router.get(
        "/{workspace_id}",
        response_model=WorkspaceResponse,
        responses={
            404: {"model": ErrorResponse, "description": "Workspace identifier is invalid or unknown."},
            409: {"model": ErrorResponse, "description": "Workspace manifest is corrupt or unavailable."},
            503: {"model": ErrorResponse, "description": "Local workspace storage is unavailable."},
        },
    )
    def get_workspace_detail(workspace_id: str) -> WorkspaceResponse | JSONResponse:
        try:
            return _workspace_response(get_workspace.execute(workspace_id))
        except WorkspaceNotFound:
            return _error(404, "workspace_not_found")
        except WorkspaceUnavailable:
            return _error(409, "workspace_manifest_unavailable")
        except WorkspaceStorageUnavailable:
            return _error(503, "workspace_storage_unavailable")

    return router
