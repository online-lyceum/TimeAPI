import logging
from typing import Optional

from sqlalchemy import select, exc
from fastapi import status, HTTPException

from .base import BaseService
from time_api.db import tables
from time_api.schemas.classes import ClassCreate


logger = logging.getLogger(__name__)


class ClassService(BaseService):
    async def get_list(
            self,
            school_id: Optional[int] = None
    ) -> list[tables.Class]:
        query = select(tables.Class)

        if school_id is not None:
            query = query.filter_by(
                school_id=school_id
            )

        classes = list(await self.session.scalars(query))
        if not classes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        return classes

    async def get(
            self, *,
            class_id: Optional[int] = None,
            class_schema: ClassCreate = None
    ):
        query = select(tables.Class)

        if class_id is not None:
            query = query.filter_by(
                class_id=class_id
            )

        if class_schema is not None:
            query = query.filter_by(
                number=class_schema.number,
                letter=class_schema.letter
            )

        class_ = await self.session.scalar(query)
        if class_ is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        return class_

    async def create(self, class_schema: ClassCreate):
        try:
            new_class = tables.Class(**class_schema.dict())

            self.session.add(new_class)
            await self.session.commit()

        except exc.IntegrityError:
            await self.session.rollback()

            new_class = await self.get(
                class_schema=class_schema
            )

        return new_class
