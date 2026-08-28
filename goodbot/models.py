from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def now() -> datetime:
    return datetime.now(timezone.utc)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class ActorKind(str, Enum):
    HUMAN = "human"
    AGENT = "agent"


class Actor(BaseModel):
    id: str = Field(default_factory=lambda: new_id("act"))
    kind: ActorKind
    name: str
    owner_id: str | None = None  # agente aponta para humano dono
    verified: bool = False
    reputation: float = 0.0
    created_at: datetime = Field(default_factory=now)


class SkillManifest(BaseModel):
    name: str
    description: str
    inputs: dict[str, str] = Field(default_factory=dict)
    side_effects: list[str] = Field(default_factory=list)
    requires_approval: bool = True


class AgentProfile(BaseModel):
    actor_id: str
    persona: str
    goals: list[str] = Field(default_factory=list)
    skills: list[SkillManifest] = Field(default_factory=list)
    memory: list[str] = Field(default_factory=list)


class Guild(BaseModel):
    id: str = Field(default_factory=lambda: new_id("gld"))
    name: str
    mission: str
    members: list[str] = Field(default_factory=list)
    created_by: str


class Post(BaseModel):
    id: str = Field(default_factory=lambda: new_id("pst"))
    guild_id: str
    author_id: str
    title: str
    body: str
    score: int = 0
    created_at: datetime = Field(default_factory=now)


class TaskStatus(str, Enum):
    OPEN = "open"
    RUNNING = "running"
    NEEDS_APPROVAL = "needs_approval"
    DONE = "done"
    FAILED = "failed"


class Task(BaseModel):
    id: str = Field(default_factory=lambda: new_id("tsk"))
    title: str
    assigned_to: str
    status: TaskStatus = TaskStatus.OPEN
    evidence: list[str] = Field(default_factory=list)
    audit: list[dict[str, Any]] = Field(default_factory=list)
