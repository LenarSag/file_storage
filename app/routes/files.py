import os
from typing import Optional
import uuid

import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, status, UploadFile
from fastapi_pagination import Page, Params
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.file_repository import (
    create_file_data,
    delete_file_data,
    get_file_by_uuid,
    get_paginated_files,
    get_user_paginated_files,
)
from app.db.database import get_session
from app.models.user import User
from app.models.file import File as UserFile
from app.schemas.file import FileDB, FileToDB
from app.security.security import get_current_user
from app.utils.utils import get_file_path
from config import FILE_CHUNK_SIZE


filesrouter = APIRouter()


async def get_file_or_404(
    session: AsyncSession, filename: uuid.UUID
) -> Optional[UserFile]:
    file = await get_file_by_uuid(session, filename)
    if not file:
        raise HTTPException(
            detail='Файл не найден или удален.',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return file


@filesrouter.get('/me', response_model=Page[FileDB])
async def get_my_files_data(
    params: Params = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await get_user_paginated_files(session, params, current_user.id)
    result.items = [
        FileDB(
            id=file.id,
            unique_filename=file.unique_filename,
            filename=file.filename,
            size=file.size,
            content_type=file.content_type,
            created_at=file.created_at,
            user_id=file.user_id,
        )
        for file in result.items
    ]
    return result


@filesrouter.get('/', response_model=Page[FileDB])
async def get_files_data(
    params: Params = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await get_paginated_files(session, params)
    result.items = [
        FileDB(
            id=file.id,
            unique_filename=file.unique_filename,
            filename=file.filename,
            size=file.size,
            content_type=file.content_type,
            created_at=file.created_at,
            user_id=file.user_id,
        )
        for file in result.items
    ]
    return result


@filesrouter.get('/{filename}', response_model=FileDB)
async def get_file_data(
    filename: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    file = await get_file_or_404(session, filename)
    return file


@filesrouter.get('/{filename}/download')
async def download_file(
    filename: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    file = await get_file_or_404(session, filename)

    async def iterfile():
        # Отправляет файл порциями, по 1мб для экономии памяти
        async with aiofiles.open(file.path, 'rb') as f:
            while contents := await f.read(FILE_CHUNK_SIZE):
                yield contents

    headers = (
        {'Content-Disposition': f'attachment; filename="{file.filename}"'}
    )
    return StreamingResponse(
        iterfile(), headers=headers, media_type=f'{file.content_type}'
    )


@filesrouter.post(
        '/upload', response_model=FileDB, status_code=status.HTTP_201_CREATED
)
async def upload(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...),
):
    unique_name = uuid.uuid4()
    file_path = get_file_path(file.filename, unique_name)

    try:
        # Принимает файл порциями, по 1мб для экономии памяти
        async with aiofiles.open(file_path, 'wb') as f:
            while contents := await file.read(FILE_CHUNK_SIZE):
                await f.write(contents)

        file_data = FileToDB(
            unique_filename=unique_name,
            path=file_path,
            filename=file.filename,
            size=file.size,
            content_type=file.content_type,
            user_id=current_user.id,
        )

        new_file = await create_file_data(session, file_data)
        return new_file

    except Exception as e:
        raise HTTPException(
            detail={'message': f'Ошибка во время загрузки файла: {str(e)}'},
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
        )
    finally:
        await file.close()


@filesrouter.delete('/{filename}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    filename: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    file = await get_file_or_404(session, filename)
    if file.user_id != current_user.id:
        raise HTTPException(
            detail='Можно удалять только свои файлы',
            status_code=status.HTTP_403_FORBIDDEN,
        )

    if not os.path.exists(file.path):
        await delete_file_data(session, file)
        raise HTTPException(
            detail='Файл не найден.', status_code=status.HTTP_404_NOT_FOUND
        )

    try:
        os.remove(file.path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f'Ошибка во время удаления файла: {str(e)}',
        )
    await delete_file_data(session, file)
    return {'detail': 'Файл успешно удален.'}
