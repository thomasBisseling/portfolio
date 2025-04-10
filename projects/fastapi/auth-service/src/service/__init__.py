from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware

from service.core.database import db_connection
from service.core.routers.helper import router as helper_router
from service.core.settings import settings
from service.routers import router as all_routers


@asynccontextmanager
async def lifespan(*args, **kwargs):
    """Initialize and close resources."""

    # Check if system can connect with the database
    session = db_connection.get_sync_session()
    try:
        session.execute(text("SELECT 1"))
    except Exception as e:
        print(f"Unable to connect with database: {e}")
        raise e
    finally:
        session.close()
    yield
    await db_connection.dispose()
    print("Database connection disposed.")


description = """
This is the API for the Plan Service. \n
It is responsible for managing plans and their associated data.
"""

app = FastAPI(
    docs_url=None,
    redoc_url="/docs",
    title="Auth Service",
    openapi_url="/openapi.json",
    description=description,
    version=settings.release_version,
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"message": str(exc)})


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(helper_router)  # no prefix for helper router
app.include_router(all_routers)
