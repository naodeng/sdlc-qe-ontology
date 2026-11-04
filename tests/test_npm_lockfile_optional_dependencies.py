import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def test_lockfile_contains_every_optional_dependency_for_all_platforms() -> None:
    lockfile = json.loads((REPOSITORY_ROOT / "package-lock.json").read_text())
    packages = lockfile["packages"]
    missing: list[str] = []

    for parent_path, package in packages.items():
        optional_dependencies = package.get("optionalDependencies", {})
        if not optional_dependencies or "node_modules/" not in parent_path:
            continue

        package_directory = parent_path.rsplit("node_modules/", maxsplit=1)[0] + "node_modules/"
        for dependency_name in optional_dependencies:
            dependency_path = package_directory + dependency_name
            if dependency_path not in packages:
                missing.append(f"{parent_path} -> {dependency_path}")

    assert not missing, "package-lock.json omits optional dependency records:\n" + "\n".join(missing)
