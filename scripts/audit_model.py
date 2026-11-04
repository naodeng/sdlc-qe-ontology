"""Static ontology and fixture audit. Not a SHACL or OWL reasoner."""
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL
ROOT = Path(__file__).resolve().parents[1]
EX = Namespace("https://example.org/sdlc-qe/")
SH = Namespace("http://www.w3.org/ns/shacl#")
PROV = Namespace("http://www.w3.org/ns/prov#")

def audit():
    ontology = Graph().parse(ROOT / "ontology/models/baseline.ttl", format="turtle")
    shapes = Graph().parse(ROOT / "ontology/shapes/baseline.shacl.ttl", format="turtle")
    gold = Graph().parse(ROOT / "ontology/fixtures/golden.ttl", format="turtle")
    negative = Graph().parse(ROOT / "ontology/fixtures/negative.ttl", format="turtle")
    errors = []
    for name in ("Requirement", "AcceptanceCriterion", "TestObligation", "TestCase", "TestExecution", "TestEvidence", "CodeChange", "Component", "QualityClaim"):
        node = EX[name]
        if (node, RDF.type, OWL.Class) not in ontology: errors.append(f"missing class {name}")
        for lang in ("en", "zh"):
            if not any(v.language == lang for v in ontology.objects(node, RDFS.label)):
                errors.append(f"missing {lang} label for {name}")
    for name in ("hasAcceptanceCriterion", "derivedFrom", "addresses", "executes", "modifies"):
        if (EX[name], RDF.type, OWL.ObjectProperty) not in ontology: errors.append(f"missing property {name}")
    if (EX.TestExecution, RDFS.subClassOf, PROV.Activity) not in ontology: errors.append("missing provenance alignment: TestExecution")
    if (EX.TestEvidence, RDFS.subClassOf, PROV.Entity) not in ontology: errors.append("missing provenance alignment: TestEvidence")
    for target in (EX.Requirement, EX.TestExecution):
        if not any((shape, SH.targetClass, target) in shapes for shape in shapes.subjects(RDF.type, SH.NodeShape)):
            errors.append(f"missing shape for {target}")
    if (EX.r1, RDF.type, EX.Requirement) not in gold: errors.append("golden fixture missing requirement")
    if (EX.brokenRequirement, RDF.type, EX.Requirement) not in negative: errors.append("negative fixture missing broken requirement")
    return errors

if __name__ == "__main__":
    problems = audit()
    if problems:
        for problem in problems: print("FAIL:", problem)
        raise SystemExit(1)
    print("PASS: structural audit (NOT SHACL validation)")
