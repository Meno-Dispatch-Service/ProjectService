from pydantic import BaseModel
from typing import Optional, List


class SUser(BaseModel):
    id: int
    username: str
    email: str


class SCreateProjectRequest(BaseModel):
    title: str
    participants_id: Optional[list[int]] = None
    meeting_days: Optional[str] = None
    user_id: Optional[int] = None


class SProject(BaseModel):
    id: int
    user: Optional[SUser] = None
    participants: Optional[List[SUser]] = None
    meeting_days: Optional[str] = None


class SAppendParticipantsRequest(BaseModel):
    pk: int
    participants_id: int


class SAppendParticipantsResponse(BaseModel):
    id: int
    participants_id: list[int]


class SRemoveParticipantsRequest(SAppendParticipantsRequest):
    pass


class SRemoveParticipantsResponse(SAppendParticipantsResponse):
    pass
