from typing import Protocol

from backend.app.domain.metadata import WorkbenchMetadata


class OntologyCatalog(Protocol):
    def get_metadata(self) -> WorkbenchMetadata: ...
