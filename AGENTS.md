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
| Run pytest with coverage monitoring | `pytest-coverage-check` |
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

## Project Memory System

This project maintains institutional knowledge in `docs/project_notes/` for consistency across sessions.

### Memory Files

- **bugs.md** - Bug log with dates, solutions, and prevention notes
- **decisions.md** - Architectural Decision Records (ADRs) with context and trade-offs
- **key_facts.md** - Project configuration, credentials, ports, important URLs
- **issues.md** - Work log with ticket IDs, descriptions, and URLs

### Memory-Aware Protocols

**Before proposing architectural changes:**
- Check `docs/project_notes/decisions.md` for existing decisions
- Verify the proposed approach doesn't conflict with past choices
- If it does conflict, acknowledge the existing decision and explain why a change is warranted

**When encountering errors or bugs:**
- Search `docs/project_notes/bugs.md` for similar issues
- Apply known solutions if found
- Document new bugs and solutions when resolved

**When looking up project configuration:**
- Check `docs/project_notes/key_facts.md` for credentials, ports, URLs, service accounts
- Prefer documented facts over assumptions

**When completing work on tickets:**
- Log completed work in `docs/project_notes/issues.md`
- Include ticket ID, date, brief description, and URL

**When user requests memory updates:**
- Update the appropriate memory file (bugs, decisions, key_facts, or issues)
- Follow the established format and style (bullet lists, dates, concise entries)

### Style Guidelines for Memory Files

- **Prefer bullet lists over tables** for simplicity and ease of editing
- **Keep entries concise** (1-3 lines for descriptions)
- **Always include dates** for temporal context
- **Include URLs** for tickets, documentation, monitoring dashboards
- **Manual cleanup** of old entries is expected (not automated)

