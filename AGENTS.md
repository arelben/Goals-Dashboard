# Agent Rules - Goals Dashboard

Este documento define las reglas de oro y convenciones para el desarrollo del "Goals Dashboard".

## Critical Rules
- ALWAYS check Linear for active tasks before starting.
- NEVER commit keys or secrets to GitHub.
- ALWAYS use Spanish for user communication.
- ALWAYS work within a virtual environment (venv).
- ALWAYS maintain dependencies in 'requirements.txt'.

### Auto-invoke Skills

When performing these actions, ALWAYS invoke the corresponding skill FIRST:

| Action | Skill |
|--------|-------|
| After creating/modifying a skill | `skill-sync` |
| Creating new skills | `skill-creator` |
| Creating/modifying Reflex UI components | `reflex-ui` |
| Creating/modifying diagrams | `design-doc-mermaid` |
| Creating/modifying documentation | `documentation-specialist` |
| Creating/modifying git commits | `mastering-git-cli` |
| GitHub CLI commands | `mastering-github-cli` |
| Regenerate AGENTS.md Auto-invoke tables (sync.sh) | `skill-sync` |
| Setting up project memory | `project-memory` |
| Troubleshoot why a skill is missing from AGENTS.md auto-invoke | `skill-sync` |
| Writing Python code | `mastering-python-skill` |
| Writing Python tests with pytest | `pytest` |
| Writing TypeScript types/interfaces | `mastering-typescript` |
| creating/modifying PostgreSQL related code | `mastering-postgresql` |

## 🏗️ Estructura Genérica
- `models/`: Esquemas de datos (Pydantic).
- `services/`: Lógica de negocio e integración con Supabase.
- `states/`: Estados de Reflex y eventos.
- `pages/`: Vistas de la aplicación.
- `components/`: UI reutilizable.

## 🎨 Convenciones de Código
- **Nomenclatura**: `snake_case` para funciones/variables, `PascalCase` para Clases.
- **Tipado**: Type Hints OBLIGATORIOS en todas las funciones.
- **Testing**: Ciclo Red-Green-Refactor con Pytest.

Last synced: Wed Feb  4 19:52:14 -05 2026
