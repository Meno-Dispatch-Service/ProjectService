from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Optional
from services.project.scheme import SUser
from dataclasses import dataclass
from sqlalchemy import select
import logging

log = logging.getLogger(__name__)


@dataclass
class BaseDTO:
    session: AsyncSession
    model: Any
    current_user: Optional[SUser] = None

    async def create(self, request):
        obj = self.model(**request.__dict__)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, **filters):
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def append_or_remove(
        self, value: int, column_name: str, append: Optional[bool] = True, **filters
    ):
        stmt = await self.get(**filters)
        if not stmt:
            raise HTTPException(detail="Object Not Found", status_code=404)

        stmt_list = getattr(stmt, column_name)
        if stmt_list is None:
            stmt_list = []

        if append:
            log.info("Obj appened to ", stmt_list)
            if value in stmt_list:
                raise HTTPException(detail="Value All ready in list", status_code=400)
            
            stmt_list.append(value)
            setattr(stmt, column_name, stmt_list)
            await self.session.commit()
            await self.session.refresh(stmt)
            return stmt

        if value not in stmt_list:
            raise HTTPException(detail="Value Not Found in list", status_code=404)
        stmt_list.remove(value)
        log.info("Obj removed from this list %s", stmt_list)
        await self.session.commit()
        await self.session.refresh(stmt)
        return stmt
