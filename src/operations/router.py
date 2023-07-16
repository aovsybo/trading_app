import time

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Long data"


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": [dict(r._mapping) for r in result],
            "details": None,
        }
    except Exception:
        return {
            "status": "error",
            "data": None,
            "details": None,
        }


@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
