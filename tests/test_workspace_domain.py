from importlib import import_module

import pytest


def _load_contract_module(name: str):
    try:
        return import_module(name)
    except ModuleNotFoundError as error:
        if error.name == name:
            pytest.fail(f"{name} is not implemented", pytrace=False)
        raise


def test_normalize_workspace_name_trims_unicode_whitespace() -> None:
    domain = _load_contract_module("backend.app.domain.workspace")

    assert domain.normalize_workspace_name(" \u3000项目 A 🚀\t") == "项目 A 🚀"


def test_normalize_workspace_name_rejects_blank_name() -> None:
    domain = _load_contract_module("backend.app.domain.workspace")

    with pytest.raises(domain.InvalidWorkspaceName):
        domain.normalize_workspace_name(" \u3000\t")


def test_normalize_workspace_name_rejects_control_characters() -> None:
    domain = _load_contract_module("backend.app.domain.workspace")

    with pytest.raises(domain.InvalidWorkspaceName):
        domain.normalize_workspace_name("project\nname")


def test_normalize_workspace_name_rejects_unpaired_surrogates() -> None:
    domain = _load_contract_module("backend.app.domain.workspace")

    with pytest.raises(domain.InvalidWorkspaceName):
        domain.normalize_workspace_name("project\ud800name")


def test_normalize_workspace_name_rejects_more_than_80_codepoints() -> None:
    domain = _load_contract_module("backend.app.domain.workspace")

    with pytest.raises(domain.InvalidWorkspaceName):
        domain.normalize_workspace_name("界" * 81)


def test_parse_workspace_id_requires_canonical_uuid() -> None:
    domain = _load_contract_module("backend.app.domain.workspace")
    workspace_id = "7c1b7912-5702-4e5a-b017-25dbd1ca418c"

    assert domain.parse_workspace_id(workspace_id) == workspace_id
    with pytest.raises(domain.WorkspaceNotFound):
        domain.parse_workspace_id("../7c1b7912-5702-4e5a-b017-25dbd1ca418c")
    with pytest.raises(domain.WorkspaceNotFound):
        domain.parse_workspace_id("7C1B7912-5702-4E5A-B017-25DBD1CA418C")


def test_create_use_case_passes_normalized_name_to_store() -> None:
    use_cases = _load_contract_module("backend.app.application.workspace_use_cases")

    class RecordingWorkspaceStore:
        received_name: str | None = None

        def create(self, name: str) -> object:
            self.received_name = name
            return self

    store = RecordingWorkspaceStore()

    result = use_cases.CreateWorkspace(store).execute("  项目 A  ")

    assert store.received_name == "项目 A"
    assert result is store
