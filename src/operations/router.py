import asyncio

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/long_operation")
@cache(expire=30)
async def get_long_op():
    await asyncio.sleep(2)
    return "Lots of data were calculated lots of time"


@router.get("")
async def get_specific_operations(
        operation_type: str,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception as exc:
        # Send error to the developers
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        }) from exc


@router.post("")
async def add_specific_operations(
    new_operation: OperationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/main")
async def main(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(1))
    return result.all()
