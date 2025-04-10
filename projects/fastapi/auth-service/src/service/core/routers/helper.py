from fastapi import (
    APIRouter,
)

from service.core.settings import settings

router = APIRouter(
    tags=["Helper"],
    responses={404: {"description": "Not found"}},
)


@router.get("/__healthcheck__/", response_model=dict)
async def health():
    """Health check endpoint, this is used to check if the service is up and running."""
    return {"status": "ok"}


@router.get("/__version__/", response_model=str)
async def version():
    """Version endpoint, this is used to check the version of the service."""
    return settings.release_version


@router.get("/__commithash__/", response_model=str)
async def commithash():
    """
    Commit hash endpoint, this is used to check the commit hash of the service.
    Based on the commit hash, you can identify the version of the service from git.
    """
    return settings.commit_hash
