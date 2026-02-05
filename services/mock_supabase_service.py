from typing import List, Optional, Dict
from uuid import UUID, uuid4
from datetime import datetime
from services.base_service import BaseService
from models.goal import Goal, GoalCreate, Milestone, MilestoneCreate

class MockSupabaseService(BaseService):
    def __init__(self):
        self.users: Dict[str, dict] = {}  # email -> user_data
        self.sessions: Dict[str, dict] = {} # user_id -> session_data
        self.goals: Dict[str, Goal] = {} # goal_id -> Goal
        self.milestones: Dict[str, Milestone] = {} # milestone_id -> Milestone
        self._current_user_id: Optional[str] = None

        # Pre-seed some data
        self._seed_data()

    def _seed_data(self):
        # Fake user
        mock_user_id = str(uuid4())
        self.users["test@example.com"] = {
            "id": mock_user_id,
            "email": "test@example.com",
            "password": "password",
            "metadata": {"first_name": "Mock", "last_name": "User"}
        }
        
        # Seed Goals
        goal1_id = uuid4()
        self.goals[str(goal1_id)] = Goal(
            id=goal1_id,
            user_id=UUID(mock_user_id),
            title="Learn Reflex",
            description="Master the Reflex framework for building web apps in Python.",
            status="in_progress",
            progress=40,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            deadline=datetime(2025, 12, 31)
        )
        
        goal2_id = uuid4()
        self.goals[str(goal2_id)] = Goal(
            id=goal2_id,
            user_id=UUID(mock_user_id),
            title="Run a Marathon",
            description="Train for 6 months and complete a full marathon.",
            status="pending",
            progress=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            category="Health"
        )

    # --- Authentication ---

    def sign_up(self, email: str, password: str, metadata: Optional[dict] = None):
        if email in self.users:
             # Simulate error
            class MockError:
                message = "User already registered"
            raise Exception(MockError.message)
            
        user_id = str(uuid4())
        self.users[email] = {
            "id": user_id,
            "email": email,
            "password": password,
            "metadata": metadata or {}
        }
        
        # Auto login
        self._current_user_id = user_id
        
        # Mock Response object expecting a .user attribute
        class MockResponse:
            class User:
                def __init__(self, id, email, metadata):
                    self.id = id
                    self.email = email
                    self.user_metadata = metadata
            
            def __init__(self, user_data):
                self.user = self.User(user_data["id"], user_data["email"], user_data["metadata"])

        return MockResponse(self.users[email])

    def sign_in(self, email: str, password: str):
        user = self.users.get(email)
        if not user or user["password"] != password:
            raise Exception("Invalid credentials")
            
        self._current_user_id = user["id"]
        
        class MockResponse:
            class User:
                def __init__(self, id, email):
                    self.id = id
                    self.email = email
            
            def __init__(self, user_data):
                self.user = self.User(user_data["id"], user_data["email"])
                self.session = "mock-session-token"

        return MockResponse(user)

    def sign_out(self):
        self._current_user_id = None

    def get_session(self):
        if self._current_user_id:
             # Find user email by ID (inefficient but fine for mock)
             user = next((u for u in self.users.values() if u["id"] == self._current_user_id), None)
             if user:
                 class MockSessionResponse:
                    class User:
                        def __init__(self, id, email):
                            self.id = id
                            self.email = email
                    def __init__(self, user_data):
                        self.user = self.User(user_data["id"], user_data["email"])
                 
                 return MockSessionResponse(user)
        return None

    # --- Goals ---

    def get_goals(self, user_id: UUID) -> List[Goal]:
        user_goals = [g for g in self.goals.values() if str(g.user_id) == str(user_id)]
        # Attach milestones
        for goal in user_goals:
            goal.milestones = [m for m in self.milestones.values() if str(m.goal_id) == str(goal.id)]
        return user_goals

    def create_goal(self, goal: GoalCreate) -> Goal:
        if not self._current_user_id:
            raise Exception("Not authenticated")
            
        new_id = uuid4()
        new_goal = Goal(
            id=new_id,
            user_id=UUID(self._current_user_id),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            **goal.dict()
        )
        self.goals[str(new_id)] = new_goal
        return new_goal

    def delete_goal(self, goal_id: UUID) -> None:
        if str(goal_id) in self.goals:
            del self.goals[str(goal_id)]
            # Cascade delete milestones
            to_delete = [mid for mid, m in self.milestones.items() if str(m.goal_id) == str(goal_id)]
            for mid in to_delete:
                del self.milestones[mid]

    def update_goal(self, goal_id: UUID, data: dict) -> Goal:
        if str(goal_id) not in self.goals:
             raise Exception("Goal not found")
        
        goal = self.goals[str(goal_id)]
        # Update attributes
        for key, value in data.items():
            if hasattr(goal, key):
                setattr(goal, key, value)
        
        goal.updated_at = datetime.now()
        return goal

    def update_goal_status(self, goal_id: UUID, status: str) -> Goal:
        return self.update_goal(goal_id, {"status": status})

    # --- Milestones ---

    def add_milestone(self, milestone: MilestoneCreate) -> Milestone:
        new_id = uuid4()
        new_milestone = Milestone(
            id=new_id,
            created_at=datetime.now(),
            is_completed=False,
            **milestone.dict()
        )
        self.milestones[str(new_id)] = new_milestone
        return new_milestone

    def toggle_milestone(self, milestone_id: UUID, is_completed: bool) -> Milestone:
        if str(milestone_id) not in self.milestones:
            raise Exception("Milestone not found")
            
        milestone = self.milestones[str(milestone_id)]
        milestone.is_completed = is_completed
        return milestone

    def delete_milestone(self, milestone_id: UUID) -> None:
        if str(milestone_id) in self.milestones:
            del self.milestones[str(milestone_id)]
