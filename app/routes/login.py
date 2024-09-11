from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user_repository import check_username_and_email, create_user
from app.db.database import get_session
from app.security.security import authenticate_user, create_access_token
from app.security.pwd_crypt import get_hashed_password
from app.schemas.user import UserAuthentication, UserBase, UserCreate


loginrouter = APIRouter()


@loginrouter.post(
    '/users', response_model=UserBase, status_code=status.HTTP_201_CREATED
)
async def create_new_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
):
    user = await check_username_and_email(
        session, user_data.username, user_data.email
    )
    if user:
        if user.username == user_data.username:
            raise HTTPException(
                detail='Имя уже используется.',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        raise HTTPException(
            detail='Почта уже используется',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user_data.password = get_hashed_password(user_data.password)
    new_user = await create_user(session, user_data)

    return new_user


@loginrouter.post('/token/login', response_model=dict[str, str])
async def get_token(
    user_data: UserAuthentication, session: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(
        session, user_data.email, user_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(user)
    return {'access_token': access_token, 'token_type': 'Bearer'}
