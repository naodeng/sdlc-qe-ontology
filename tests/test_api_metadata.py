import asyncio

import httpx

from backend.app.main import create_app


def get(app: object, path: str, headers: dict[str, str] | None = None) -> httpx.Response:
    async def send_request() -> httpx.Response:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1",
        ) as client:
            return await client.get(path, headers=headers)

    return asyncio.run(send_request())


def test_meta_describes_bundled_candidate_without_claiming_validation() -> None:
    response = get(create_app(), "/api/v1/meta")

    assert response.status_code == 200
    payload = response.json()
    assert payload["snapshotId"].startswith("demo-")
    assert payload["ontologyVersion"] == "unversioned-candidate"
    assert payload["validation"] == "not_run"
    assert payload["dataSource"] == "bundled-example-fixture"
    assert payload["tripleCount"] > 0
    assert payload["classCount"] > 0
    assert payload["propertyCount"] > 0


def test_health_endpoint_is_available() -> None:
    response = get(create_app(), "/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_untrusted_host_is_rejected() -> None:
    response = get(create_app(), "/api/v1/meta", headers={"host": "attacker.example"})

    assert response.status_code == 400


def test_untrusted_browser_origin_is_rejected() -> None:
    response = get(
        create_app(),
        "/api/v1/meta",
        headers={"origin": "https://attacker.example"},
    )

    assert response.status_code == 403
