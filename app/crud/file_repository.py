from typing import Optional
from uuid import UUID

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.file import File
from app.schemas.file import FileToDB


async def create_file_data(session: AsyncSession, file_data: FileToDB) -> File:
    file = File(**file_data.model_dump())
    session.add(file)
    await session.commit()
    return file


async def get_file_by_uuid(
    session: AsyncSession, unique_name: UUID
) -> Optional[File]:
    query = select(File).filter_by(unique_filename=unique_name)
    result = await session.execute(query)
    return result.scalar()


async def get_paginated_files(session: AsyncSession, params: Params):
    return await paginate(
        session, select(File).order_by(File.created_at), params
    )


async def get_user_paginated_files(
    session: AsyncSession, params: Params, user_id: int
):
    return await paginate(
        session,
        select(File).filter_by(user_id=user_id).order_by(File.created_at),
        params,
    )


async def delete_file_data(sesion: AsyncSession, file: File) -> None:
    await sesion.delete(file)
    await sesion.commit()
