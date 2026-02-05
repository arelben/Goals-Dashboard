import pytest
from unittest.mock import MagicMock, patch
from services.supabase_service import SupabaseService

@pytest.fixture
def mock_supabase():
    with patch("services.supabase_service.create_client") as mock_create:
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        service = SupabaseService()
        yield service, mock_client

def test_sign_up(mock_supabase):
    service, mock_client = mock_supabase
    email = "test@example.com"
    password = "password123"
    metadata = {"first_name": "John", "last_name": "Doe"}
    
    service.sign_up(email, password, metadata=metadata)
    
    expected_options = {"data": metadata}
    mock_client.auth.sign_up.assert_called_once_with({
        "email": email, 
        "password": password, 
        "options": expected_options
    })

def test_sign_in(mock_supabase):
    service, mock_client = mock_supabase
    email = "test@example.com"
    password = "password123"
    
    service.sign_in(email, password)
    
    mock_client.auth.sign_in_with_password.assert_called_once_with({"email": email, "password": password})

def test_sign_out(mock_supabase):
    service, mock_client = mock_supabase
    
    service.sign_out()
    
    mock_client.auth.sign_out.assert_called_once()

def test_get_session(mock_supabase):
    service, mock_client = mock_supabase
    
    service.get_session()
    
    mock_client.auth.get_session.assert_called_once()
