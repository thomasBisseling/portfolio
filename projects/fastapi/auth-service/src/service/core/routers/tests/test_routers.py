import pytest  # noqa

from service.core.settings import settings  # noqa


@pytest.mark.asyncio
async def test_healthcheck_endpoint(client):
    """
    Test the health check endpoint. This will return a status of ok.
    """

    response = client.get("/__healthcheck__/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_version_endpoint(client):
    """
    Test the version endpoint. This will return the version of the service.
    """

    response = client.get("/__version__/")

    assert response.status_code == 200
    assert response.json() == settings.release_version


@pytest.mark.asyncio
async def test_commithash_endpoint(client):
    """
    Test the commit hash endpoint. This will return the commit hash of the service.
    """

    response = client.get("/__commithash__/")

    assert response.status_code == 200
    assert response.json() == settings.commit_hash
