import os
from dotenv import load_dotenv
from services.base_service import BaseService
from services.supabase_service import SupabaseService
from services.mock_supabase_service import MockSupabaseService

load_dotenv()

def get_service() -> BaseService:
    """Returns an instance of BaseService based on the MOCK_MODE env var."""
    mock_mode = os.getenv("MOCK_MODE", "False").lower() == "true"
    
    if mock_mode:
        print("Using MockSupabaseService")
        # Singleton pattern for mock service could be useful here to persist data in memory across calls
        # For simplicity, we'll instantiate it fresh, but in a real app, a singleton is better for stateful mocks.
        # But since Reflex State persists per session, maybe it's fine? 
        # Actually reflex runs backend in python, so a global variable here would work for simple persistence?
        return _get_mock_instance() 
    else:
        return SupabaseService()

# Simple singleton for mock service to keep data alive during the session
_mock_instance = None

def _get_mock_instance():
    global _mock_instance
    if _mock_instance is None:
        _mock_instance = MockSupabaseService()
    return _mock_instance
