from backend.app.domain.metadata import WorkbenchMetadata
from backend.app.ports.ontology_catalog import OntologyCatalog


class GetWorkbenchMetadata:
    def __init__(self, ontology_catalog: OntologyCatalog) -> None:
        self._ontology_catalog = ontology_catalog

    def execute(self) -> WorkbenchMetadata:
        return self._ontology_catalog.get_metadata()
