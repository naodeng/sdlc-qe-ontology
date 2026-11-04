"""Strict release gate for Python tests and positive/negative SHACL fixtures."""

from pathlib import Path
import sys

from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]


class NoSkippedTests:
    skipped = 0

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config) -> None:
        self.skipped = len(terminalreporter.stats.get("skipped", []))


def main() -> int:
    try:
        from pyshacl import validate
    except ImportError:
        print(
            "BLOCKED: pySHACL is required for the release gate; "
            "install project validation dependencies.",
            file=sys.stderr,
        )
        return 2

    import pytest

    gate = NoSkippedTests()
    test_result = pytest.main([str(ROOT / "tests"), "-q"], plugins=[gate])
    if test_result != pytest.ExitCode.OK or gate.skipped:
        print("BLOCKED: tests failed or skipped", file=sys.stderr)
        return 1

    shapes = Graph().parse(ROOT / "ontology/shapes/baseline.shacl.ttl", format="turtle")
    ontology = Graph().parse(ROOT / "ontology/models/baseline.ttl", format="turtle")
    for filename, expected in [("golden.ttl", True), ("negative.ttl", False)]:
        data = Graph().parse(ROOT / "ontology/fixtures" / filename, format="turtle")
        conforms, _, report = validate(
            data_graph=data,
            shacl_graph=shapes,
            ont_graph=ontology,
            inference="rdfs",
        )
        if conforms != expected:
            print(
                f"BLOCKED: {filename} expected conforms={expected}, "
                f"got {conforms}: {report}",
                file=sys.stderr,
            )
            return 1

    print("PASS: Python tests, SPARQL CQs, and SHACL positive/negative fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
