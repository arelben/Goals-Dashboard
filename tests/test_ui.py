import pytest
import reflex as rx
from unittest.mock import patch, MagicMock
from goals_dashboard.goals_dashboard import State

def test_initial_state():
    """Test that the initial state is correct."""
    state = State()
    assert state is not None

def test_navigation_state():
    """Test that the state correctly handles navigation."""
    state = State()
    assert state.current_page == "home"
    
    state.set_current_page("goals")
    assert state.current_page == "goals"

def test_auth_state():
    """Test login and logout state transitions with mocked SupabaseService."""
    state = State()
    assert state.is_authenticated is False
    assert state.user_id == ""

    # Mock get_service
    with patch("goals_dashboard.goals_dashboard.get_service") as mock_get_service:
        mock_service = mock_get_service.return_value
        
        # Success case
        mock_response = MagicMock()
        # Ensure it's treated as a string or returns a string for the id
        mock_response.user.id = "real-user-123"
        mock_service.sign_in.return_value = mock_response
        
        # We need to mock the State instance correctly or just use the state object
        state.email = "test@example.com"
        state.password = "password"
        state.login()
        
        assert state.user_id == "real-user-123"
        assert state.is_authenticated is True
        assert state.error_message == ""

        # Logout
        state.logout()
        assert state.is_authenticated is False
        assert state.user_id == ""

def test_registration_flow():
    """Test that the state correctly handles registration with metadata."""
    state = State()
    assert state.show_registration is False
    
    # Toggle to registration
    state.toggle_registration()
    assert state.show_registration is True
    
    # Mock get_service
    with patch("goals_dashboard.goals_dashboard.get_service") as mock_get_service:
        mock_service = mock_get_service.return_value
        
        mock_response = MagicMock()
        mock_response.user.id = "new-user-123"
        mock_service.sign_up.return_value = mock_response
        
        state.first_name = "Jane"
        state.last_name = "Doe"
        state.email = "jane@example.com"
        state.password = "secure-pass"
        
        state.signup()
        
        # Verify metadata was passed
        mock_service.sign_up.assert_called_once_with(
            "jane@example.com", 
            "secure-pass", 
            metadata={"first_name": "Jane", "last_name": "Doe"}
        )
        assert state.is_authenticated is True
        assert state.user_id == "new-user-123"

    from goals_dashboard.goals_dashboard import index
    component = index()
    assert isinstance(component, rx.Component)

def test_load_goals():
    """Test loading goals into state."""
    from models.goal import Goal
    from uuid import uuid4
    from datetime import datetime
    
    state = State()
    state.user_id = str(uuid4())
    
    # Mock get_service
    with patch("goals_dashboard.goals_dashboard.get_service") as mock_get_service:
        mock_service = mock_get_service.return_value
        
        # Mock goals with real objects
        goal_id = uuid4()
        real_goal = Goal(
            id=goal_id,
            user_id=uuid4(),
            title="Test Goal",
            status="pending",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        mock_service.get_goals.return_value = [real_goal]
        
        state.load_goals()
        
        assert len(state.goals) == 1
        assert state.goals[0].title == "Test Goal"
        assert state.is_loading is False
