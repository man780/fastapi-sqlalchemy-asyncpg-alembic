from uuid import UUID

import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "payload, status_code",
    (
        (
            {"title": "motorhead", "content": "we play rock and roll"},
            status.HTTP_201_CREATED,
        ),
    ),
)
async def test_add_car(client: AsyncClient, payload: dict, status_code: int):
    response = await client.post("/car", json=payload)
    assert response.status_code == status_code
    assert payload["title"] == response.json()["title"]


@pytest.mark.parametrize(
    "payload, status_code",
    (
        (
            {"title": "motorhead", "content": "we play rock and roll"},
            status.HTTP_200_OK,
        ),
    ),
)
async def test_get_car(client: AsyncClient, payload: dict, status_code: int):
    await client.post("/car", json=payload)
    title = payload["title"]
    response = await client.get(f"/car/{title}")
    assert response.status_code == status_code
    assert payload["title"] == response.json()["title"]
    assert UUID(response.json()["id"])


@pytest.mark.parametrize(
    "payload, status_code",
    (
        (
            {"title": "motorhead", "content": "we play rock and roll"},
            status.HTTP_200_OK,
        ),
    ),
)
async def test_delete_car(client: AsyncClient, payload: dict, status_code: int):
    response = await client.post("/car", json=payload)
    title = response.json()["title"]
    response = await client.delete(f"/car/{title}")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload, status_code",
    (
        (
            {"title": "motorhead", "content": "we play rock and roll"},
            status.HTTP_200_OK,
        ),
    ),
)
@pytest.mark.parametrize(
    "patch_payload, patch_status_code",
    (
        (
            {"title": "motorhead", "content": "we play loud"},
            status.HTTP_200_OK,
        ),
    ),
)
async def test_update_car(
    client: AsyncClient,
    payload: dict,
    status_code: int,
    patch_payload: dict,
    patch_status_code: int,
):
    await client.post("/car", json=payload)
    title = payload["title"]
    response = await client.patch(f"/car/{title}", json=patch_payload)
    assert response.status_code == patch_status_code
    response = await client.get(f"/car/{title}")
    assert patch_payload["content"] == response.json()["content"]
