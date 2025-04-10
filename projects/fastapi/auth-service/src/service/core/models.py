import inspect
from datetime import datetime
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from pydantic import GetCoreSchemaHandler, PrivateAttr
from pydantic_core import core_schema
from sqlalchemy import distinct, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    declared_attr,
)
from sqlmodel import Field, Session, SQLModel, create_engine, select


class BaseSQLModel(SQLModel):
    """Base SQLModel class."""

    id: int = Field(primary_key=True, default=None)

    def __str__(self) -> str:
        """String representation of the model."""
        return f"{self.__class__.__name__}({self.id})"

    def __repr__(self):
        """String representation of the model for debugging."""
        return f"<{self.__class__.__name__} {self.__str__()}>"

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        """Table name for the model."""

        class_name = cls.__name__

        # convert CamelCase to snake_case
        return "".join(
            ["_" + i.lower() if i.isupper() else i for i in class_name]
        ).lstrip("_")

    @classmethod
    def cast_dict(cls, data: dict):
        """Cast a dictionary to a model."""

        if isinstance(data, cls):
            data = data.__dict__
        return {k: v for k, v in data.items() if k in inspect.signature(cls).parameters}


class Datetime(datetime):
    """Custom datetime field for SQLModel"""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ):
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value)  # ISO 8601 strings are supported
        raise ValueError(f"Invalid datetime format: {value}")
