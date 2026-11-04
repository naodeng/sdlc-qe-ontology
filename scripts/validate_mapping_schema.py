"""Validate the bundled mapping profile and one required-field negative case."""

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "ontology/mappings/v1/mapping-profile-v1.schema.json"
EXAMPLE_PATH = ROOT / "ontology/mappings/v1/example-requirement-mapping.json"


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    profile = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    errors = sorted(validator.iter_errors(profile), key=lambda error: list(error.path))
    if errors:
        for error in errors:
            print(f"FAIL: example mapping: {error.message}")
        return 1

    invalid_profile = deepcopy(profile)
    del invalid_profile["idField"]
    if not list(validator.iter_errors(invalid_profile)):
        print("FAIL: schema accepted a profile without its required idField")
        return 1

    print("PASS: mapping profile schema, positive example, and required-field negative case")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
