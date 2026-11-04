from pathlib import Path
import unittest
from rdflib import Graph
ROOT = Path(__file__).resolve().parents[1]
class SHACLTests(unittest.TestCase):
    def test_positive_and_negative(self):
        try:
            from pyshacl import validate
        except ImportError:
            self.fail('pySHACL missing: mandatory validation cannot be skipped')
        shapes = Graph().parse(ROOT / 'ontology/shapes/baseline.shacl.ttl', format='turtle')
        ontology = Graph().parse(ROOT / 'ontology/models/baseline.ttl', format='turtle')
        for filename, expected in [('golden.ttl', True), ('negative.ttl', False)]:
            with self.subTest(fixture=filename):
                data = Graph().parse(ROOT / 'ontology/fixtures' / filename, format='turtle')
                conforms, _, report = validate(data_graph=data, shacl_graph=shapes, ont_graph=ontology, inference='rdfs')
                self.assertEqual(conforms, expected, str(report))
