import asyncio
import os

from fastapi import FastAPI, Response, status
from fastapi.exceptions import ValidationException
from pydantic import ValidationError
import uvicorn

from app.db.database import init_models
from app.routes.login import loginrouter
from app.routes.files import filesrouter
from config import API_URL, UPLOAD_DIR


app = FastAPI()


app.include_router(loginrouter, prefix=f'{API_URL}/auth')
app.include_router(filesrouter, prefix=f'{API_URL}/files')


@app.exception_handler(ValidationException)
async def custom_pydantic_validation_exception_handler(request, exc):
    return Response(
        content={'detail': exc.errors()},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.exception_handler(ValidationError)
async def custom_pydantic_validation_error_handler(request, exc):
    return Response(
        content={'detail': exc.errors()},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.get('/')
async def index():
    return """
        File storage API, get documentation from 127.0.0.1:8000/docs
        """


def create_upload_directory():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)


if __name__ == '__main__':
    create_upload_directory()
    asyncio.run(init_models())
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000, reload=True)
