from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class MilestoneBase(BaseModel):
    title: str
    is_completed: bool = False

class MilestoneCreate(MilestoneBase):
    goal_id: UUID

class Milestone(MilestoneBase):
    id: UUID
    goal_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: str = "pending"
    progress: int = 0
    category: Optional[str] = None

class GoalCreate(GoalBase):
    user_id: UUID

class Goal(GoalBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    milestones: List[Milestone] = []

    class Config:
        from_attributes = True
