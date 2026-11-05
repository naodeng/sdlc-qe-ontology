import os
from pathlib import Path
import sys

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from backend.app.adapters.rdflib_catalog import RdflibOntologyCatalog
from backend.app.adapters.filesystem_workspace_store import (
    FilesystemWorkspaceStore,
    resolve_data_root,
)
from backend.app.api.metadata import create_metadata_router
from backend.app.api.workspaces import create_workspace_router
from backend.app.application.get_workbench_metadata import GetWorkbenchMetadata
from backend.app.ports.workspace_store import WorkspaceStore
from backend.app.ports.ontology_catalog import OntologyCatalog

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ALLOWED_ORIGINS = {
    "http://127.0.0.1:5174",
    "http://127.0.0.1:8000",
}
e2e_frontend_port = os.environ.get("E2E_FRONTEND_PORT", "")
if (
    e2e_frontend_port.isascii()
    and e2e_frontend_port.isdecimal()
    and 1 <= len(e2e_frontend_port) <= 5
    and 1 <= int(e2e_frontend_port) <= 65535
    and str(int(e2e_frontend_port)) == e2e_frontend_port
):
    ALLOWED_ORIGINS.add(f"http://127.0.0.1:{e2e_frontend_port}")


def create_app(
    ontology_catalog: OntologyCatalog | None = None,
    workspace_store: WorkspaceStore | None = None,
    data_root: Path | None = None,
) -> FastAPI:
    catalog = ontology_catalog or RdflibOntologyCatalog(
        ontology_path=REPOSITORY_ROOT / "ontology/models/baseline.ttl",
        fixture_path=REPOSITORY_ROOT / "ontology/fixtures/golden.ttl",
    )
    app = FastAPI(
        title="SDLC-QE Ontology Workbench API",
        version="0.1.0-bootstrap",
        docs_url="/api/docs",
        redoc_url=None,
    )
    app.include_router(create_metadata_router(GetWorkbenchMetadata(catalog)))
    if workspace_store is None:
        resolved_data_root = data_root
        if resolved_data_root is None:
            resolved_data_root = resolve_data_root(
                os.environ,
                sys.platform,
                Path.home(),
                Path.cwd(),
            )
        workspace_store = FilesystemWorkspaceStore(resolved_data_root)
    app.include_router(create_workspace_router(workspace_store))

    @app.middleware("http")
    async def reject_untrusted_origin(request: Request, call_next):
        origin = request.headers.get("origin")
        if request.method == "POST" and request.url.path == "/api/v1/workspaces" and not origin:
            return JSONResponse(
                status_code=403,
                content={"detail": {"code": "origin_required"}},
            )
        if origin and origin not in ALLOWED_ORIGINS:
            return JSONResponse(
                status_code=403,
                content={"detail": {"code": "origin_not_allowed"}},
            )
        return await call_next(request)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=sorted(ALLOWED_ORIGINS),
        allow_methods=["GET", "POST"],
        allow_headers=["content-type"],
        allow_credentials=False,
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["127.0.0.1", "localhost"],
    )
    return app


app = create_app()
