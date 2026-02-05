import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from datetime import datetime
from services.supabase_service import SupabaseService
from models.goal import Goal, GoalCreate, Milestone, MilestoneCreate

@pytest.fixture
def mock_supabase_client():
    with patch("services.supabase_service.create_client") as mock_create:
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        yield mock_client

@pytest.fixture
def supabase_service(mock_supabase_client):
    # Mock environment variables to avoid ValueError
    with patch.dict("os.environ", {"SUPABASE_URL": "http://test.com", "SUPABASE_KEY": "test-key"}):
        return SupabaseService()

def test_get_goals(supabase_service, mock_supabase_client):
    user_id = uuid4()
    mock_data = [
        {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "title": "Test Goal",
            "description": "Desc",
            "status": "in_progress",
            "progress": 0,
            "category": "work",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "milestones": []
        }
    ]
    
    mock_supabase_client.table().select().eq().execute.return_value = MagicMock(data=mock_data)
    
    goals = supabase_service.get_goals(user_id)
    
    assert len(goals) == 1
    assert goals[0].title == "Test Goal"
    mock_supabase_client.table.assert_called_with("goals")

def test_create_goal(supabase_service, mock_supabase_client):
    goal_data = GoalCreate(
        user_id=uuid4(),
        title="New Goal",
        category="personal"
    )
    
    mock_response = {
        "id": str(uuid4()),
        "user_id": str(goal_data.user_id),
        "title": "New Goal",
        "category": "personal",
        "status": "pending",
        "progress": 0,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    mock_supabase_client.table().insert().execute.return_value = MagicMock(data=[mock_response])
    
    result = supabase_service.create_goal(goal_data)
    
    assert result.title == "New Goal"
    assert result.status == "pending"

def test_toggle_milestone(supabase_service, mock_supabase_client):
    milestone_id = uuid4()
    mock_response = {
        "id": str(milestone_id),
        "goal_id": str(uuid4()),
        "title": "Hito 1",
        "is_completed": True,
        "created_at": datetime.now().isoformat()
    }
    
    mock_supabase_client.table().update().eq().execute.return_value = MagicMock(data=[mock_response])
    
    result = supabase_service.toggle_milestone(milestone_id, True)
    
    assert result.is_completed is True
    mock_supabase_client.table().update.assert_called_with({"is_completed": True})

def test_delete_goal(supabase_service, mock_supabase_client):
    goal_id = uuid4()
    supabase_service.delete_goal(goal_id)
    mock_supabase_client.table().delete().eq.assert_called_with("id", str(goal_id))

def test_add_milestone(supabase_service, mock_supabase_client):
    milestone_data = MilestoneCreate(
        goal_id=uuid4(),
        title="New Milestone"
    )
    mock_response = {
        "id": str(uuid4()),
        "goal_id": str(milestone_data.goal_id),
        "title": "New Milestone",
        "is_completed": False,
        "created_at": datetime.now().isoformat()
    }
    mock_supabase_client.table().insert().execute.return_value = MagicMock(data=[mock_response])
    
    result = supabase_service.add_milestone(milestone_data)
    assert result.title == "New Milestone"

def test_update_goal_status(supabase_service, mock_supabase_client):
    goal_id = uuid4()
    mock_response = {
        "id": str(goal_id),
        "user_id": str(uuid4()),
        "title": "Goal",
        "status": "completed",
        "progress": 100,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    mock_supabase_client.table().update().eq().execute.return_value = MagicMock(data=[mock_response])
    
    result = supabase_service.update_goal_status(goal_id, "completed")
    assert result.status == "completed"

def test_delete_milestone(supabase_service, mock_supabase_client):
    milestone_id = uuid4()
    supabase_service.delete_milestone(milestone_id)
    mock_supabase_client.table().delete().eq.assert_called_with("id", str(milestone_id))

def test_create_goal_error(supabase_service, mock_supabase_client):
    mock_supabase_client.table().insert().execute.return_value = MagicMock(data=[])
    with pytest.raises(Exception, match="Error creating goal"):
        supabase_service.create_goal(GoalCreate(user_id=uuid4(), title="fail", category="work"))
