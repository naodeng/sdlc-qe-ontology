import hashlib
from pathlib import Path

from rdflib import Graph, OWL, RDF

from backend.app.domain.metadata import ValidationStatus, WorkbenchMetadata


class RdflibOntologyCatalog:
    def __init__(self, ontology_path: Path, fixture_path: Path) -> None:
        self._ontology_path = ontology_path
        self._fixture_path = fixture_path

    def get_metadata(self) -> WorkbenchMetadata:
        ontology = Graph().parse(self._ontology_path, format="turtle")
        fixture_bytes = self._fixture_path.read_bytes()
        fixture = Graph().parse(data=fixture_bytes, format="turtle")

        ontology_iri = next(ontology.subjects(RDF.type, OWL.Ontology), None)
        version = ontology.value(ontology_iri, OWL.versionInfo) if ontology_iri else None
        ontology_version = str(version or "unversioned-candidate")

        digest = hashlib.sha256(fixture_bytes).hexdigest()
        property_types = {OWL.ObjectProperty, OWL.DatatypeProperty}
        properties = set()
        for property_type in property_types:
            properties.update(ontology.subjects(RDF.type, property_type))

        return WorkbenchMetadata(
            snapshot_id=f"demo-{digest}",
            ontology_version=ontology_version,
            validation=ValidationStatus.NOT_RUN,
            triple_count=len(fixture),
            class_count=len(set(ontology.subjects(RDF.type, OWL.Class))),
            property_count=len(properties),
            data_source="bundled-example-fixture",
        )
