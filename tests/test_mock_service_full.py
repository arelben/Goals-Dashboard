
import pytest
from uuid import uuid4
from datetime import datetime
from services.mock_supabase_service import MockSupabaseService
from models.goal import GoalCreate, MilestoneCreate

@pytest.fixture
def mock_service():
    return MockSupabaseService()

def test_auth_flow(mock_service):
    # Sign Up
    email = f"test_{uuid4()}@example.com"
    password = "password123"
    response = mock_service.sign_up(email, password, {"name": "Test"})
    assert response.user.email == email
    assert mock_service._current_user_id is not None
    
    # Sign Out
    mock_service.sign_out()
    assert mock_service._current_user_id is None
    
    # Sign In
    response = mock_service.sign_in(email, password)
    assert response.user.email == email
    assert mock_service._current_user_id is not None
    
    # Get Session
    session = mock_service.get_session()
    assert session is not None
    assert session.user.email == email

def test_auth_errors(mock_service):
    # Duplicate email
    email = "test@example.com" # Already seeded
    with pytest.raises(Exception, match="User already registered"):
        mock_service.sign_up(email, "password", {})
        
    # Invalid login
    with pytest.raises(Exception, match="Invalid credentials"):
        mock_service.sign_in(email, "WRONG_PASSWORD")

def test_goal_management(mock_service):
    # Login first
    mock_service.sign_in("test@example.com", "password")
    user_id = mock_service._current_user_id
    
    # Create Goal
    goal_data = GoalCreate(
        title="New Goal",
        description="Desc",
        deadline=datetime.now(),
        category="Work",
        user_id=user_id # Required by model
    )
    new_goal = mock_service.create_goal(goal_data)
    assert new_goal.title == "New Goal"
    assert str(new_goal.id) in mock_service.goals
    
    # Get Goals
    goals = mock_service.get_goals(user_id)
    assert len(goals) >= 1
    assert any(g.id == new_goal.id for g in goals)
    
    # Update Goal
    updated_goal = mock_service.update_goal(new_goal.id, {"title": "Updated Title"})
    assert updated_goal.title == "Updated Title"
    
    # Delete Goal
    mock_service.delete_goal(new_goal.id)
    assert str(new_goal.id) not in mock_service.goals

def test_milestone_management(mock_service):
    mock_service.sign_in("test@example.com", "password")
    user_id = mock_service._current_user_id
    
    # Create Goal for milestone
    goal = mock_service.create_goal(GoalCreate(title="G", description="D", user_id=user_id))
    
    # Add Milestone
    milestone_data = MilestoneCreate(
        goal_id=goal.id,
        title="M1"
        # due_date is missing in my previous code? Let's check model. No, model has title only in Base.
        # Wait, MilestoneCreate inherits MilestoneBase which has title, is_completed.
        # It also has goal_id.
    )
    # Re-reading model: MilestoneBase has title, is_completed. MilestoneCreate(MilestoneBase) has goal_id.
    # So title and goal_id are required.
    
    milestone = mock_service.add_milestone(milestone_data)
    assert milestone.title == "M1"
    assert str(milestone.id) in mock_service.milestones
    
    # Check if attached to goal
    fetched_goals = mock_service.get_goals(mock_service._current_user_id)
    target_goal = next(g for g in fetched_goals if g.id == goal.id)
    assert len(target_goal.milestones) == 1
    
    # Toggle Milestone
    updated = mock_service.toggle_milestone(milestone.id, True)
    assert updated.is_completed is True
    
    # Delete Milestone
    mock_service.delete_milestone(milestone.id)
    assert str(milestone.id) not in mock_service.milestones

def test_unauthenticated_create_goal(mock_service):
    mock_service.sign_out()
    # We need a dummy user_id to satisfy the model validation, even if service will reject because not auth
    goal_data = GoalCreate(title="G", description="D", user_id=uuid4())
    with pytest.raises(Exception, match="Not authenticated"):
        mock_service.create_goal(goal_data)

def test_update_missing_goal(mock_service):
    with pytest.raises(Exception, match="Goal not found"):
        mock_service.update_goal(uuid4(), {})
