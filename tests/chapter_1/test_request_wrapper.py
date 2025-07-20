from unittest.mock import AsyncMock

import pytest
from httpx import Response, Request

from src.chapter_1.request_wrapper import RequestWrapper


@pytest.fixture(scope="module")
def wrapper():
    mock_client = AsyncMock()
    return RequestWrapper(client=mock_client)

async def test_request_happypath(wrapper):
    dummy_response = Response(
        status_code=200,
        request=Request("GET", "https://example.com/foo/bar")
    )
    wrapper._client.request = AsyncMock(return_value=dummy_response)

    response = await wrapper.request("GET", "https://example.com/foo/bar")

    assert response.status_code == 200
    assert wrapper._client.request.call_count == 1

async def test_request_retry(wrapper):
    dummy_response = Response(
        status_code=500,
        request=Request("GET", "https://example.com/foo/bar")
    )
    wrapper._client.request = AsyncMock(return_value=dummy_response)

    with pytest.raises(RuntimeError):
        await wrapper.request("GET", "https://example.com/foo/bar")

    assert wrapper._client.request.call_count == 3