from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from models.goal import Goal, GoalCreate, Milestone, MilestoneCreate

class BaseService(ABC):
    
    # --- Authentication ---
    @abstractmethod
    def sign_up(self, email: str, password: str, metadata: Optional[dict] = None):
        pass

    @abstractmethod
    def sign_in(self, email: str, password: str):
        pass

    @abstractmethod
    def sign_out(self):
        pass

    @abstractmethod
    def get_session(self):
        pass

    # --- Goals ---
    @abstractmethod
    def get_goals(self, user_id: UUID) -> List[Goal]:
        pass

    @abstractmethod
    def create_goal(self, goal: GoalCreate) -> Goal:
        pass

    @abstractmethod
    def delete_goal(self, goal_id: UUID) -> None:
        pass

    @abstractmethod
    def update_goal(self, goal_id: UUID, data: dict) -> Goal:
        pass

    @abstractmethod
    def update_goal_status(self, goal_id: UUID, status: str) -> Goal:
        pass

    # --- Milestones ---
    @abstractmethod
    def add_milestone(self, milestone: MilestoneCreate) -> Milestone:
        pass

    @abstractmethod
    def toggle_milestone(self, milestone_id: UUID, is_completed: bool) -> Milestone:
        pass

    @abstractmethod
    def delete_milestone(self, milestone_id: UUID) -> None:
        pass
