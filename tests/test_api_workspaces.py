import asyncio
from pathlib import Path
from typing import Any

import httpx
import pytest

from backend.app.main import create_app


def request(
    app: object,
    method: str,
    path: str,
    *,
    headers: dict[str, str] | None = None,
    json_body: dict[str, Any] | None = None,
) -> httpx.Response:
    async def send_request() -> httpx.Response:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1",
        ) as client:
            return await client.request(method, path, headers=headers, json=json_body)

    return asyncio.run(send_request())


def _app(data_root: Path):
    return create_app(data_root=data_root)


def test_app_startup_and_read_routes_do_not_create_data_root(tmp_path: Path) -> None:
    data_root = tmp_path / "not-created"
    app = _app(data_root)

    assert not data_root.exists()
    assert request(app, "GET", "/api/v1/workspaces").json() == {"workspaces": []}
    assert request(app, "GET", "/api/v1/workspaces/6f35fb35-d617-44f2-926c-4029da7d7007").status_code == 404
    assert not data_root.exists()


def test_create_workspace_returns_201_and_never_returns_path(tmp_path: Path) -> None:
    data_root = tmp_path / "workspace-data"
    response = request(
        _app(data_root),
        "POST",
        "/api/v1/workspaces",
        headers={"origin": "http://127.0.0.1:5174"},
        json_body={"name": "项目 A"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["name"] == "项目 A"
    assert payload["status"] == "empty"
    assert payload["activeSnapshotId"] is None
    assert str(data_root) not in response.text
    assert set(payload) == {"workspaceId", "name", "createdAt", "status", "activeSnapshotId"}


def test_create_rejects_client_supplied_path(tmp_path: Path) -> None:
    data_root = tmp_path / "workspace-data"
    response = request(
        _app(data_root),
        "POST",
        "/api/v1/workspaces",
        headers={"origin": "http://127.0.0.1:5174"},
        json_body={"name": "Project", "path": str(tmp_path)},
    )

    assert response.status_code == 422
    assert not data_root.exists()


def test_list_and_get_return_empty_workspace(tmp_path: Path) -> None:
    app = _app(tmp_path / "workspace-data")
    created = request(
        app,
        "POST",
        "/api/v1/workspaces",
        headers={"origin": "http://127.0.0.1:5174"},
        json_body={"name": "Project"},
    ).json()

    listed = request(app, "GET", "/api/v1/workspaces").json()
    detail = request(app, "GET", f"/api/v1/workspaces/{created['workspaceId']}").json()

    assert listed == {"workspaces": [created]}
    assert detail == created


def test_corrupt_workspace_is_listed_but_detail_returns_409(tmp_path: Path) -> None:
    data_root = tmp_path / "workspace-data"
    workspace_id = "6f35fb35-d617-44f2-926c-4029da7d7007"
    workspace_dir = data_root / "workspaces" / workspace_id
    workspace_dir.mkdir(parents=True)
    (workspace_dir / "manifest.json").write_text("not json", encoding="utf-8")
    app = _app(data_root)

    listed = request(app, "GET", "/api/v1/workspaces").json()
    detail = request(app, "GET", f"/api/v1/workspaces/{workspace_id}")

    assert listed == {
        "workspaces": [
            {
                "workspaceId": workspace_id,
                "name": None,
                "createdAt": None,
                "status": "corrupt",
                "issueCode": "workspace_manifest_unavailable",
            }
        ]
    }
    assert detail.status_code == 409
    assert detail.json() == {"detail": {"code": "workspace_manifest_unavailable"}}


@pytest.mark.parametrize(
    "workspace_id",
    ["not-a-uuid", "6F35FB35-D617-44F2-926C-4029DA7D7007", "6f35fb35d61744f2-926c-4029da7d7007"],
)
def test_invalid_or_unknown_workspace_id_returns_404(
    tmp_path: Path, workspace_id: str
) -> None:
    response = request(_app(tmp_path / "workspace-data"), "GET", f"/api/v1/workspaces/{workspace_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": {"code": "workspace_not_found"}}


def test_invalid_workspace_name_returns_422_code(tmp_path: Path) -> None:
    response = request(
        _app(tmp_path / "workspace-data"),
        "POST",
        "/api/v1/workspaces",
        headers={"origin": "http://127.0.0.1:5174"},
        json_body={"name": " \n "},
    )

    assert response.status_code == 422
    assert response.json() == {"detail": {"code": "workspace_name_invalid"}}


def test_storage_failure_returns_503_code(tmp_path: Path) -> None:
    data_root = tmp_path / "not-a-directory"
    data_root.write_text("file", encoding="utf-8")
    response = request(
        _app(data_root),
        "POST",
        "/api/v1/workspaces",
        headers={"origin": "http://127.0.0.1:5174"},
        json_body={"name": "Project"},
    )

    assert response.status_code == 503
    assert response.json() == {"detail": {"code": "workspace_storage_unavailable"}}
    assert str(data_root) not in response.text


def test_create_rejects_missing_origin(tmp_path: Path) -> None:
    response = request(
        _app(tmp_path / "workspace-data"),
        "POST",
        "/api/v1/workspaces",
    )

    assert response.status_code == 403
    assert response.json() == {"detail": {"code": "origin_required"}}


def test_create_rejects_untrusted_origin(tmp_path: Path) -> None:
    response = request(
        _app(tmp_path / "workspace-data"),
        "POST",
        "/api/v1/workspaces",
        headers={"origin": "https://attacker.example"},
        json_body={"name": "Project"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": {"code": "origin_not_allowed"}}


@pytest.mark.parametrize(
    "path",
    [
        "/api/v1/health",
        "/api/v1/meta",
        "/api/v1/workspaces",
        "/api/v1/workspaces/6f35fb35-d617-44f2-926c-4029da7d7007",
    ],
)
def test_get_rejects_untrusted_origin_with_documented_error(
    tmp_path: Path,
    path: str,
) -> None:
    response = request(
        _app(tmp_path / "workspace-data"),
        "GET",
        path,
        headers={"origin": "https://attacker.example"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": {"code": "origin_not_allowed"}}


def test_create_accepts_allowed_origin(tmp_path: Path) -> None:
    response = request(
        _app(tmp_path / "workspace-data"),
        "POST",
        "/api/v1/workspaces",
        headers={"origin": "http://127.0.0.1:5174"},
        json_body={"name": "Project"},
    )

    assert response.status_code == 201


def test_create_trims_before_enforcing_workspace_name_limit(tmp_path: Path) -> None:
    name = "a" * 80
    response = request(
        _app(tmp_path / "workspace-data"),
        "POST",
        "/api/v1/workspaces",
        headers={"origin": "http://127.0.0.1:5174"},
        json_body={"name": f"  {name}  "},
    )

    assert response.status_code == 201
    assert response.json()["name"] == name


def test_untrusted_host_is_rejected_for_workspace_routes(tmp_path: Path) -> None:
    response = request(
        _app(tmp_path / "workspace-data"),
        "GET",
        "/api/v1/workspaces",
        headers={"host": "attacker.example"},
    )

    assert response.status_code == 400


def test_workspace_cors_preflight_allows_json_post(tmp_path: Path) -> None:
    response = request(
        _app(tmp_path / "workspace-data"),
        "OPTIONS",
        "/api/v1/workspaces",
        headers={
            "origin": "http://127.0.0.1:5174",
            "access-control-request-method": "POST",
            "access-control-request-headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5174"
    assert "POST" in response.headers["access-control-allow-methods"]
    assert "content-type" in response.headers["access-control-allow-headers"]
