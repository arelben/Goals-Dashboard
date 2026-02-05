from typing import List, Optional
from uuid import UUID
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
from models.goal import Goal, GoalCreate, Milestone, MilestoneCreate
from services.base_service import BaseService
import os

# Cargar variables de entorno
load_dotenv()

class SupabaseService(BaseService):
    def __init__(self):
        self.url: str = os.getenv("SUPABASE_URL")
        self.key: str = os.getenv("SUPABASE_KEY")
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
        self.client: Client = create_client(self.url, self.key)

    # --- Authentication ---

    def sign_up(self, email: str, password: str, metadata: Optional[dict] = None):
        """Crea un nuevo usuario en Supabase con metadata opcional."""
        options = {"data": metadata} if metadata else None
        return self.client.auth.sign_up({"email": email, "password": password, "options": options})

    def sign_in(self, email: str, password: str):
        """Inicia sesión con un usuario existente."""
        return self.client.auth.sign_in_with_password({"email": email, "password": password})

    def sign_out(self):
        """Cierra la sesión actual."""
        return self.client.auth.sign_out()

    def get_session(self):
        """Recupera la sesión actual."""
        return self.client.auth.get_session()

    # --- Goals ---

    def get_goals(self, user_id: UUID) -> List[Goal]:
        """Recupera todos los objetivos de un usuario, incluyendo sus hitos."""
        response = self.client.table("goals").select("*, milestones(*)").eq("user_id", str(user_id)).execute()
        return [Goal(**item) for item in response.data]

    def create_goal(self, goal: GoalCreate) -> Goal:
        """Crea un nuevo objetivo en la base de datos."""
        # model_dump(mode='json') convierte el objeto Pydantic a un diccionario compatible con JSON
        data = goal.model_dump(mode='json')
        response = self.client.table("goals").insert(data).execute()
        
        # Supabase devuelve una lista, tomamos el primer elemento
        if response.data:
            return Goal(**response.data[0])
        raise Exception("Error creating goal")

    def delete_goal(self, goal_id: UUID) -> None:
        """Elimina un objetivo por su ID."""
        self.client.table("goals").delete().eq("id", str(goal_id)).execute()

    def update_goal(self, goal_id: UUID, data: dict) -> Goal:
        """Actualiza un objetivo existente."""
        response = self.client.table("goals").update(data).eq("id", str(goal_id)).execute()
        if response.data:
            return Goal(**response.data[0])
        raise Exception("Error updating goal")

    def update_goal_status(self, goal_id: UUID, status: str) -> Goal:
        """Actualiza el estado de un objetivo."""
        return self.update_goal(goal_id, {"status": status})

    # --- Milestones ---

    def add_milestone(self, milestone: MilestoneCreate) -> Milestone:
        """Añade un hito a un objetivo existente."""
        data = milestone.model_dump(mode='json')
        response = self.client.table("milestones").insert(data).execute()
        if response.data:
            return Milestone(**response.data[0])
        raise Exception("Error creating milestone")

    def toggle_milestone(self, milestone_id: UUID, is_completed: bool) -> Milestone:
        """Marca un hito como completado o pendiente."""
        response = self.client.table("milestones").update({"is_completed": is_completed}).eq("id", str(milestone_id)).execute()
        if response.data:
            return Milestone(**response.data[0])
        raise Exception("Error toggling milestone")

    def delete_milestone(self, milestone_id: UUID) -> None:
        """Elimina un hito."""
        self.client.table("milestones").delete().eq("id", str(milestone_id)).execute()
