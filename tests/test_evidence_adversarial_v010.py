import unittest
from pathlib import Path
from rdflib import Graph, Namespace
ROOT=Path(__file__).resolve().parents[1]
EX=Namespace("https://example.org/sdlc-qe/")
class AdversarialEvidenceTests(unittest.TestCase):
    def rows(self, fixture, query):
        g=Graph().parse(ROOT/"ontology/fixtures"/fixture,format="turtle")
        return [tuple(r) for r in g.query((ROOT/"ontology/queries"/query).read_text())]
    def test_mixed_pass_and_fail_retains_valid_evidence_only(self):
        fixture="evidence-mixed-outcomes-v010.ttl"
        self.assertEqual(self.rows(fixture,"cq09_qualified_evidence.rq"),[(EX["release-checkout"],EX["obligation-checkout"],EX["evidence-checkout"])])
        self.assertEqual(self.rows(fixture,"cq10_unqualified_obligations.rq"),[])
    def test_adversarial_cases_are_not_qualified(self):
        for issue in ("missing-execution","late-only","empty-digest","wrong-evidence-link","missing-cutoff","missing-build-environment","missing-status"):
            with self.subTest(issue=issue):
                fixture=f"evidence-{issue}-v010.ttl"
                self.assertEqual(self.rows(fixture,"cq09_qualified_evidence.rq"),[])
                # Missing cutoff or build env means the release does not enter CQ10's candidate set.
                expected=[] if issue in ("missing-cutoff","missing-build-environment") else [(EX["release-checkout"],EX["obligation-checkout"])]
                self.assertEqual(self.rows(fixture,"cq10_unqualified_obligations.rq"),expected)
    def test_all_adversarial_fixtures_parse(self):
        for path in (ROOT/"ontology/fixtures").glob("*-v010.ttl"):
            with self.subTest(path=path.name): self.assertGreater(len(Graph().parse(path,format="turtle")),0)
if __name__=="__main__": unittest.main()
