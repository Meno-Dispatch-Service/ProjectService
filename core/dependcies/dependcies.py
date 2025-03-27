from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncContextManager, AsyncGenerator
from core.database.project import session_factory
from redis.asyncio import StrictRedis
from config.config import settings
from services.project.scheme import SUser
from utils.utils import request_to_url
from jose import jwt
from typing import Annotated
import json


oauth2 = OAuth2PasswordBearer("http://localhost:8081/auth-service/api/v1/auth/login/")


async def get_session() -> AsyncGenerator[AsyncContextManager, AsyncSession]:
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_redis():
    return await StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


async def get_current_user(
    token: Annotated[str, Depends(oauth2)],
    redis: Annotated[StrictRedis, Depends(get_redis)],
) -> SUser:

    payload = jwt.decode(
        token, key=settings.AUTH_SECRET_KEY.get_secret_value(), algorithms="HS256"
    )
    user_id: int = payload.get("sub")
    cached_data = await redis.get(f"get-current-user-{user_id}")
    if cached_data:
        if isinstance(cached_data, str):
            return SUser(**json.loads(cached_data))

    if user_id is None:
        raise HTTPException(detail="User id in token not found !", status_code=400)

    user_data = await request_to_url(
        url=f"http://localhost:8000/user-service/api/v1/get-user-by-id/{user_id}",
        method="get",
    )

    user = SUser.model_validate(user_data)

    await redis.setex(
        f"get-current-user-{user_id}", 500, json.dumps(user.dict(), default=str)
    )
    return user
