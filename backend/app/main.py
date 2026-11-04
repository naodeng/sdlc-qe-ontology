from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from backend.app.adapters.rdflib_catalog import RdflibOntologyCatalog
from backend.app.api.metadata import create_metadata_router
from backend.app.application.get_workbench_metadata import GetWorkbenchMetadata
from backend.app.ports.ontology_catalog import OntologyCatalog

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ALLOWED_ORIGINS = {
    "http://127.0.0.1:5174",
    "http://127.0.0.1:8000",
}


def create_app(ontology_catalog: OntologyCatalog | None = None) -> FastAPI:
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

    @app.middleware("http")
    async def reject_untrusted_origin(request: Request, call_next):
        origin = request.headers.get("origin")
        if origin and origin not in ALLOWED_ORIGINS:
            return JSONResponse(
                status_code=403,
                content={"detail": "Origin is not allowed by the local workbench"},
            )
        return await call_next(request)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=sorted(ALLOWED_ORIGINS),
        allow_methods=["GET"],
        allow_headers=[],
        allow_credentials=False,
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["127.0.0.1", "localhost"],
    )
    return app


app = create_app()
