import pytest
import os
from uuid import uuid4
from services.supabase_service import SupabaseService
from models.goal import GoalCreate, MilestoneCreate

@pytest.mark.integration
class TestSupabaseServiceIntegration:
    @pytest.fixture(scope="class")
    def service(self):
        return SupabaseService()

    @pytest.fixture
    def test_user_id(self):
        # Usamos un UUID persistente para pruebas o uno aleatorio
        # Nota: Si hay RLS estricto, esto podría fallar si el UUID no existe en auth.users
        return uuid4()

    def test_goal_lifecycle(self, service, test_user_id):
        # 1. Crear
        new_goal = GoalCreate(
            user_id=test_user_id,
            title="Integration Test Goal",
            category="testing"
        )
        created = service.create_goal(new_goal)
        assert created.title == "Integration Test Goal"
        assert created.id is not None
        
        goal_id = created.id

        try:
            # 2. Leer
            goals = service.get_goals(test_user_id)
            assert any(g.id == goal_id for g in goals)

            # 3. Actualizar
            updated = service.update_goal_status(goal_id, "completed")
            assert updated.status == "completed"

            # 4. Gestionar Hitos
            milestone_data = MilestoneCreate(
                goal_id=goal_id,
                title="Integration Milestone"
            )
            milestone = service.add_milestone(milestone_data)
            assert milestone.title == "Integration Milestone"

            toggled = service.toggle_milestone(milestone.id, True)
            assert toggled.is_completed is True

            # 5. Borrado de hito
            service.delete_milestone(milestone.id)

        finally:
            # 6. Borrado de objetivo (Limpieza)
            service.delete_goal(goal_id)
            
            # Verificar borrado
            goals_after = service.get_goals(test_user_id)
            assert not any(g.id == goal_id for g in goals_after)
