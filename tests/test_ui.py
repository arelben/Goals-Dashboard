import pytest
import reflex as rx
from goals_dashboard.goals_dashboard import State

def test_initial_state():
    """Test that the initial state is correct."""
    state = State()
    # Aquí añadiremos variables de estado conforme las necesitemos
    assert state is not None

def test_navigation_state():
    """Test that the state correctly handles navigation."""
    state = State()
    assert state.current_page == "home"
    
    state.set_current_page("goals")
    assert state.current_page == "goals"

def test_auth_state():
    """Test login and logout state transitions."""
    state = State()
    assert state.is_authenticated is False
    assert state.user_id == ""
    
    # Mock login
    dummy_id = "user-123"
    state.login(dummy_id)
    assert state.is_authenticated is True
    assert state.user_id == dummy_id
    
    # Mock logout
    state.logout()
    assert state.is_authenticated is False
    assert state.user_id == ""

def test_index_component():
    """Test that the index component renders without error."""
    from goals_dashboard.goals_dashboard import index
    component = index()
    assert isinstance(component, rx.Component)
