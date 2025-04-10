import inspect
from typing import List, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlmodel import select, update

from service.core.models import BaseSQLModel
from service.models import User


class Service:
    """
    Base class for all services.
    """

    model = None

    def __init__(self, session: AsyncSession | Session, skip_model_check: bool = False):
        self.session = session

        if not skip_model_check:
            if self.model is None:
                raise ValueError(f"{self.__class__.__name__} must have a model.")
            elif not inspect.isclass(self.model):
                raise ValueError(f"{self.__class__.__name__} must have a model class.")
            elif not issubclass(self.model, BaseSQLModel):
                raise ValueError(
                    f"{self.__class__.__name__} must have a model class that is a subclass of BaseSQLModel."
                )

    async def execute(self, stmt):
        """
        Execute a statement.
        """

        if isinstance(self.session, AsyncSession):
            return await self.session.execute(stmt)
        return self.session.execute(stmt)

    async def save(self):
        """
        Save an object to the database.
        """

        if isinstance(self.session, AsyncSession):
            await self.session.commit()
        else:
            self.session.commit()

    async def flush(self):
        """
        Flush the session.
        """
        if isinstance(self.session, AsyncSession):
            await self.session.flush()
        else:
            self.session.flush()

    async def create(self, object_data: dict | List[dict]):
        """
        Create a new object.

        To save to the database, you must call the .save() method.
        """
        if isinstance(object_data, list):
            objects = [self.model(**obj) for obj in object_data]
            self.session.add_all(objects)
            await self.flush()
            return objects

        obj = self.model(**object_data)
        self.session.add(obj)
        await self.flush()
        return obj

    async def get_by_id(self, object_id: int) -> dict | None:
        """
        Get a object by its ID.
        """
        stmt = select(self.model).where(getattr(self.model, "id") == object_id)
        result = await self.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, object_data: BaseSQLModel | List[BaseSQLModel]):
        """
        Delete a user by its ID.
        """

        if isinstance(object_data, list):
            for obj in object_data:
                await self.session.delete(obj)
        else:
            await self.session.delete(object_data)
        await self.session.commit()
