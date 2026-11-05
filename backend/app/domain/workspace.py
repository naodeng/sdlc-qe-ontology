from dataclasses import dataclass
from enum import StrEnum
import unicodedata
from uuid import UUID


class WorkspaceStatus(StrEnum):
    EMPTY = "empty"
    CORRUPT = "corrupt"


class InvalidWorkspaceName(ValueError):
    pass


class WorkspaceNotFound(LookupError):
    pass


class WorkspaceUnavailable(RuntimeError):
    pass


class WorkspaceStorageUnavailable(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class Workspace:
    workspace_id: str
    name: str
    created_at: str
    status: WorkspaceStatus = WorkspaceStatus.EMPTY
    active_snapshot_id: None = None


@dataclass(frozen=True, slots=True)
class WorkspaceSummary:
    workspace_id: str
    name: str | None
    created_at: str | None
    status: WorkspaceStatus
    issue_code: str | None = None


def normalize_workspace_name(name: str) -> str:
    if not isinstance(name, str):
        raise InvalidWorkspaceName

    normalized = name.strip()
    if not normalized or len(normalized) > 80:
        raise InvalidWorkspaceName
    if any(unicodedata.category(character) in {"Cc", "Cs"} for character in normalized):
        raise InvalidWorkspaceName
    return normalized


def parse_workspace_id(value: str) -> str:
    try:
        parsed = UUID(value)
    except (AttributeError, TypeError, ValueError):
        raise WorkspaceNotFound from None

    canonical = str(parsed)
    if value != canonical:
        raise WorkspaceNotFound
    return canonical
