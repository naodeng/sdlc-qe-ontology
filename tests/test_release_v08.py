import unittest
from pathlib import Path
from rdflib import Graph, Namespace
ROOT=Path(__file__).resolve().parents[1]
EX=Namespace('https://example.org/sdlc-qe/')
class ReleaseEvidenceTests(unittest.TestCase):
    def query(self, fixture, filename):
        graph=Graph().parse(ROOT/'ontology/fixtures'/fixture,format='turtle')
        return [tuple(row) for row in graph.query((ROOT/'ontology/queries'/filename).read_text())]
    def test_release_evidence_positive(self):
        rows=self.query('delivery-release-v08.ttl','cq07_release_evidence.rq')
        self.assertEqual(rows,[(EX['release-checkout'],EX['pr-checkout'],EX['req-checkout'],EX['obligation-checkout'],EX['evidence-checkout'])])
    def test_gap_fixture_does_not_invent_evidence(self):
        self.assertEqual(self.query('delivery-release-gap-v08.ttl','cq07_release_evidence.rq'),[])
    def test_release_gap_is_detected(self):
        self.assertEqual(self.query('delivery-release-gap-v08.ttl','cq08_release_obligation_gaps.rq'),[(EX['release-gap'],EX['obligation-gap'])])
    def test_complete_release_has_no_gap(self):
        self.assertEqual(self.query('delivery-release-v08.ttl','cq08_release_obligation_gaps.rq'),[])
    def test_ontology_parses(self):
        self.assertGreater(len(Graph().parse(ROOT/'ontology/models/baseline.ttl',format='turtle')),0)
if __name__=='__main__':unittest.main()
