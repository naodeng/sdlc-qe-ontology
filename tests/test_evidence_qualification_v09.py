import unittest
from pathlib import Path
from rdflib import Graph, Namespace
ROOT=Path(__file__).resolve().parents[1]
EX=Namespace('https://example.org/sdlc-qe/')
class EvidenceQualificationTests(unittest.TestCase):
    def run_query(self, fixture, query):
        graph=Graph().parse(ROOT/'ontology/fixtures'/fixture,format='turtle')
        return [tuple(row) for row in graph.query((ROOT/'ontology/queries'/query).read_text())]
    def test_qualified_evidence_positive(self):
        self.assertEqual(self.run_query('evidence-valid-v09.ttl','cq09_qualified_evidence.rq'),[(EX['release-checkout'],EX['obligation-checkout'],EX['evidence-checkout'])])
        self.assertEqual(self.run_query('evidence-valid-v09.ttl','cq10_unqualified_obligations.rq'),[])
    def test_negative_fixtures(self):
        for issue in ('failed','environment','stale','missing-digest','wrong-build'):
            with self.subTest(issue=issue):
                fixture=f'evidence-{issue}-v09.ttl'
                self.assertEqual(self.run_query(fixture,'cq09_qualified_evidence.rq'),[])
                self.assertEqual(self.run_query(fixture,'cq10_unqualified_obligations.rq'),[(EX['release-checkout'],EX['obligation-checkout'])])
    def test_ontology_and_fixtures_parse(self):
        self.assertTrue(len(Graph().parse(ROOT/'ontology/models/baseline.ttl',format='turtle')))
        for fixture in (ROOT/'ontology/fixtures').glob('evidence-*-v09.ttl'):
            with self.subTest(fixture=fixture.name):self.assertTrue(len(Graph().parse(fixture,format='turtle')))
if __name__=='__main__':unittest.main()
