from pathlib import Path
import unittest
from rdflib import Graph, Namespace, RDF, RDFS, OWL

ROOT = Path(__file__).resolve().parents[1]
EX = Namespace("https://example.org/sdlc-qe/")

class OntologyBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = Graph()
        cls.graph.parse(ROOT / "ontology/models/baseline.ttl", format="turtle")
        cls.graph.parse(ROOT / "ontology/fixtures/golden.ttl", format="turtle")

    def test_ontology_and_classes_parse(self):
        self.assertIn((EX.Requirement, RDF.type, OWL.Class), self.graph)
        self.assertIn((EX.TestExecution, RDFS.subClassOf, Namespace("http://www.w3.org/ns/prov#").Activity), self.graph)

    def test_cq_gold_results(self):
        expected = {"cq01": {EX.ac1}, "cq02": {EX.o2}, "cq03": {EX.component1}, "cq04": {EX.e1}}
        for name, gold in expected.items():
            with self.subTest(cq=name):
                q = (ROOT / "ontology/queries" / f"{name}.rq").read_text()
                result = {row[0] for row in self.graph.query(q)}
                self.assertEqual(result, gold)

    def test_negative_fixture_is_parseable(self):
        g = Graph().parse(ROOT / "ontology/fixtures/negative.ttl", format="turtle")
        self.assertIn((EX.brokenRequirement, RDF.type, EX.Requirement), g)

if __name__ == "__main__": unittest.main()
