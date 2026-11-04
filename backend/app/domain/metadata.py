from dataclasses import dataclass
from enum import StrEnum


class ValidationStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    NOT_RUN = "not_run"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class WorkbenchMetadata:
    snapshot_id: str
    ontology_version: str
    validation: ValidationStatus
    triple_count: int
    class_count: int
    property_count: int
    data_source: str
