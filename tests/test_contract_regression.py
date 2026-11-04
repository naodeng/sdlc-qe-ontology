from pathlib import Path
import unittest
from rdflib import Graph, Namespace, RDF, OWL, RDFS
ROOT = Path(__file__).resolve().parents[1]
EX = Namespace('https://example.org/sdlc-qe/')
class ContractRegression(unittest.TestCase):
    def test_minimum_contract(self):
        g = Graph().parse(ROOT/'ontology/models/baseline.ttl',format='turtle')
        for name in ['Requirement','AcceptanceCriterion','TestObligation','TestCase','TestExecution','TestEvidence','CodeChange','Component','QualityClaim']:
            with self.subTest(class_name=name): self.assertIn((EX[name],RDF.type,OWL.Class),g)
        for name in ['hasAcceptanceCriterion','derivedFrom','addresses','executes','modifies']:
            with self.subTest(property_name=name): self.assertIn((EX[name],RDF.type,OWL.ObjectProperty),g)
    def test_labels_bilingual(self):
        g = Graph().parse(ROOT/'ontology/models/baseline.ttl',format='turtle')
        for c in g.subjects(RDF.type, OWL.Class):
            labels = list(g.objects(c,RDFS.label))
            with self.subTest(class_uri=str(c)):
                self.assertIn('en',[x.language for x in labels]); self.assertIn('zh',[x.language for x in labels])
