import os
import pytest
from unittest.mock import patch
from services.factory import get_service
from services.supabase_service import SupabaseService
from services.mock_supabase_service import MockSupabaseService

def test_get_service_real():
    """Test that get_service returns SupabaseService when MOCK_MODE is false."""
    # We need to ensure SUPABASE vars are present for SupabaseService init
    env_vars = {
        "MOCK_MODE": "False",
        "SUPABASE_URL": "https://example.supabase.co",
        "SUPABASE_KEY": "fake-key"
    }
    with patch.dict(os.environ, env_vars):
        service = get_service()
        assert isinstance(service, SupabaseService)

def test_get_service_mock():
    """Test that get_service returns MockSupabaseService when MOCK_MODE is true."""
    with patch.dict(os.environ, {"MOCK_MODE": "True"}):
        service = get_service()
        assert isinstance(service, MockSupabaseService)

def test_get_service_mock_singleton():
    """Test that the mock service is a singleton."""
    with patch.dict(os.environ, {"MOCK_MODE": "True"}):
        service1 = get_service()
        service2 = get_service()
        assert service1 is service2
