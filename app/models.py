from pydantic import BaseModel
from typing import Optional


class TopicRequest(BaseModel):
    topic: str
    context: Optional[str] = ""
    tone: str = "professional-personal"


class PostContent(BaseModel):
    content: str
    topic: str


class ScheduleRequest(BaseModel):
    post_content: str
    scheduled_time: str  # ISO 8601 format


class LinkedInToken(BaseModel):
    access_token: str
    expires_in: int
