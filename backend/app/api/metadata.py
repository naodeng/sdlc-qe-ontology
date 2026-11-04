from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from backend.app.application.get_workbench_metadata import GetWorkbenchMetadata
from backend.app.domain.metadata import WorkbenchMetadata


class WorkbenchMetaResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    snapshot_id: str
    ontology_version: str
    validation: str
    triple_count: int
    class_count: int
    property_count: int
    data_source: str


def create_metadata_router(use_case: GetWorkbenchMetadata) -> APIRouter:
    router = APIRouter(prefix="/api/v1")

    @router.get("/health", tags=["meta"])
    def get_health() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/meta", response_model=WorkbenchMetaResponse, tags=["meta"])
    def get_meta() -> WorkbenchMetaResponse:
        metadata = use_case.execute()
        return _to_response(metadata)

    return router


def _to_response(metadata: WorkbenchMetadata) -> WorkbenchMetaResponse:
    return WorkbenchMetaResponse(
        snapshot_id=metadata.snapshot_id,
        ontology_version=metadata.ontology_version,
        validation=metadata.validation.value,
        triple_count=metadata.triple_count,
        class_count=metadata.class_count,
        property_count=metadata.property_count,
        data_source=metadata.data_source,
    )
