from sqlalchemy.ext.asyncio import AsyncSession
from dto.dto import ProjectDTO
from services.project.scheme import (
    SUser,
    SCreateProjectRequest,
    SProject,
    SAppendParticipantsRequest,
    SAppendParticipantsResponse,
    SRemoveParticipantsRequest,
    SRemoveParticipantsResponse,
)
from typing import Optional
from redis.asyncio import StrictRedis
from services.project.models import Project
from fastapi import HTTPException
from utils.utils import request_to_url
import asyncio
import json


class ProjectService:
    def __init__(
        self,
        session: AsyncSession,
        redis: Optional[StrictRedis] = None,
        current_user: Optional[SUser] = None,
    ):
        self.session = session
        self.redis = redis
        self.current_user = current_user

    async def create_project(self, request: SCreateProjectRequest):
        try:
            project_dto = ProjectDTO(session=self.session, model=Project)
            request.user_id = self.current_user.id
            project = await project_dto.create(request)
            response = SCreateProjectRequest(**project.__dict__)
            return response
        except Exception as e:
            raise HTTPException(detail=e, status_code=500)


    async def get_project(self, pk: int):
        cached_data = await self.redis.get(f"get-project-{pk}")
        if cached_data:
            return SProject(**json.loads(cached_data))

        project_dto = ProjectDTO(session=self.session, model=Project)
        project = await project_dto.get(id=pk)
        if not project:
            raise HTTPException(detail="Project Not Found", status_code=404)

        participants_ids = project.participants_id

        user_data = await request_to_url(
            f"http://localhost:8000/user-service/api/v1/get-user-by-id/{project.user_id}/",
            method="get",
        )

        participants_data = await asyncio.gather(
            *[
                request_to_url(
                    f"http://localhost:8000/user-service/api/v1/get-user-by-id/{participant_id}/",
                    method="get",
                )
                for participant_id in participants_ids
            ],
        )

        user = SUser.model_validate(user_data)
        participants = [
            SUser.model_validate(participants) for participants in participants_data
        ]

        response = SProject(**project.__dict__, user=user, participants=participants)
        await self.redis.setex(f"get-project-{pk}", 500, json.dumps(response.dict()))
        return response

    async def append_participants(self, request: SAppendParticipantsRequest):
        project_dto = ProjectDTO(session=self.session, model=Project)
        project = await project_dto.append_or_remove(
            value=request.participants_id,
            column_name="participants_id",
            id=request.pk,
            user_id=self.current_user.id,
        )

        await self.redis.delete(f"get-project-{request.pk}")
        await self.redis.save()
        return SAppendParticipantsResponse(**project.__dict__)

    async def remove_participants(self, request: SRemoveParticipantsRequest):
        project_dto = ProjectDTO(session=self.session, model=Project)
        project = await project_dto.append_or_remove(
            value=request.participants_id,
            column_name="participants_id",
            append=False,
            id=request.pk,
            user_id=self.current_user.id,
        )

        await self.redis.delete(f"get-project-{request.pk}")
        await self.redis.save()
        return SRemoveParticipantsResponse(**project.__dict__)
