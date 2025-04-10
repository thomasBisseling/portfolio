from fastapi import Query
from pydantic import BaseModel


class OffsetLimitQueryModel(BaseModel):
    """Offset limit query model."""

    offset: int = Query(default=0, ge=0)
    limit: int = Query(default=100, le=100)
    count: int = 0
