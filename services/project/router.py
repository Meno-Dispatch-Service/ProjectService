from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependcies.dependcies import get_session, get_redis, get_current_user
from services.project.service import ProjectService
from services.project.scheme import (
    SUser,
    SCreateProjectRequest,
    SProject,
    SAppendParticipantsRequest,
    SAppendParticipantsResponse,
    SRemoveParticipantsResponse,
    SRemoveParticipantsRequest,
)
from typing import Annotated
from redis.asyncio import StrictRedis

project_router = APIRouter(
    tags=["Meno Dispatcher Project Service"], prefix="/project-service/api/v1"
)


@project_router.post(
    "/create-project/",
    response_model=SCreateProjectRequest,
    status_code=201,
    dependencies=[Depends(get_current_user), Depends(get_session)],
)
async def create_project(
    request: SCreateProjectRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[SUser, Depends(get_current_user)],
):
    service = ProjectService(session=session, current_user=current_user)
    return await service.create_project(request)


@project_router.get("/get-project/{pk}/", response_model=SProject)
async def get_project(
    pk: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    redis: Annotated[StrictRedis, Depends(get_redis)],
):
    service = ProjectService(session=session, redis=redis)
    return await service.get_project(pk)


@project_router.patch(
    "/append-participants/",
    response_model=SAppendParticipantsResponse,
    status_code=201,
    dependencies=[Depends(get_session), Depends(get_current_user), Depends(get_redis)],
)
async def append_participants(
    request: SAppendParticipantsRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[SUser, Depends(get_current_user)],
    redis: Annotated[StrictRedis, Depends(get_redis)],
):
    service = ProjectService(session=session, current_user=current_user, redis=redis)
    return await service.append_participants(request)


@project_router.delete(
    "/remove-participants/",
    response_model=SRemoveParticipantsResponse,
    status_code=200,
    dependencies=[Depends(get_redis), Depends(get_current_user)],
)
async def remove_participants(
    request: SRemoveParticipantsRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[SUser, Depends(get_current_user)],
    redis: Annotated[StrictRedis, Depends(get_redis)],
):
    service = ProjectService(session=session, redis=redis, current_user=current_user)
    return await service.remove_participants(request)
