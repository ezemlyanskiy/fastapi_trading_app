from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate


router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


@router.get('/')
async def get_specific_operations(
    operation_type: str,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(operation).where(
        operation.c.type == operation_type
    )
    result = await session.execute(query)
    return result.all()


@router.post('/')
async def add_specific_operations(
    new_operation: OperationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(operation).values(**new_operation.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}
