import unittest
from pathlib import Path
from rdflib import Graph, Namespace
ROOT=Path(__file__).resolve().parents[1]
EX=Namespace('https://example.org/sdlc-qe/')
class DeliveryFlowTest(unittest.TestCase):
    def test_gap_detection_has_ground_truth(self):
        graph=Graph().parse(ROOT/'ontology/fixtures/delivery-gap.ttl',format='turtle')
        query=(ROOT/'ontology/queries/cq05_obligations_without_tests.rq').read_text()
        self.assertEqual([row[0] for row in graph.query(query)], [EX['obligation-gap']])
    def test_complete_flow_has_no_obligation_gap(self):
        graph=Graph().parse(ROOT/'ontology/fixtures/delivery-flow.ttl',format='turtle')
        query=(ROOT/'ontology/queries/cq05_obligations_without_tests.rq').read_text()
        self.assertEqual(list(graph.query(query)),[])
    def test_evidence_provenance(self):
        graph=Graph().parse(ROOT/'ontology/fixtures/delivery-flow.ttl',format='turtle')
        query=(ROOT/'ontology/queries/cq06_evidence_provenance.rq').read_text()
        self.assertEqual([tuple(r) for r in graph.query(query)],[(EX['evidence-checkout'],EX['execution-checkout'],EX['test-checkout'])])
    def test_no_false_evidence_claim_for_gap(self):
        graph=Graph().parse(ROOT/'ontology/fixtures/delivery-gap.ttl',format='turtle')
        query=(ROOT/'ontology/queries/cq06_evidence_provenance.rq').read_text()
        self.assertEqual(list(graph.query(query)),[])
if __name__=='__main__': unittest.main()
