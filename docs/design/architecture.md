# Project Architecture: Goals Dashboard

This document describes the high-level architecture of the Goals Dashboard, a project aimed at centralizing goal tracking and task management using Reflex and Supabase.

## System Overview (C4 Container Diagram)

The following diagram illustrates the major components of the system and their interactions.

```mermaid
graph TB
    User([👤 User<br/>Web Browser])

    subgraph "Goals Dashboard Ecosystem"
        direction TB

        subgraph "Reflex Web Application (Python)"
            UI[🌐 UI / Pages<br/>Reflex Components]
            State[⚙️ State Management<br/>Reflex State/Events]
            Service[🔌 Service Layer<br/>Supabase Service]
        end

        subgraph "Backend & Storage (Supabase)"
            Auth[🔐 Supabase Auth<br/>Authentication]
            DB[(💾 PostgreSQL<br/>Core Data & Search)]
        end

        subgraph "Project Intelligence"
            Skills[🧠 Agent Skills<br/>.agent/skills/*]
            Rules[📜 Agent Rules<br/>AGENTS.md]
        end
    end

    %% Interactions
    User -->|Interacts with| UI
    UI -->|Triggers events| State
    State -->|Calls| Service
    
    Service -->|Authenticates| Auth
    Service -->|Queries/Writes| DB
    
    %% Agent loop awareness
    Skills -.->|Guides| UI
    Rules -.->|Orchestrates| State

    %% Styling
    classDef frontend fill:#FFE66D,stroke:#F08C00,color:#000
    classDef logic fill:#4ECDC4,stroke:#0B7285,color:#fff
    classDef Storage fill:#A8DADC,stroke:#1864AB,color:#000
    classDef agent fill:#E6E6FA,stroke:#5F3DC4,color:#000

    class UI frontend
    class State,Service logic
    class Auth,DB Storage
    class Skills,Rules agent
```

## Component Breakdown

### 1. Reflex Web Application
A unified Python framework for building full-stack web apps.
- **UI / Pages**: Declarative Python components that compile to React.
- **State Management**: Handles user sessions, global variables, and event logic.
- **Service Layer**: Abstraction for interacting with external APIs and databases.

### 2. Supabase
Backend-as-a-Service providing the database and authentication infrastructure.
- **PostgreSQL**: Stores goals, milestones, and user preferences. Supports vector search for future AI integrations.
- **Auth**: Secure user login and session management.

### 3. Agent Intelligence
A custom layer of metadata and instructions that guides the AI assistant (Antigravity) during development.
- **Skills**: Specialized knowledge bases (e.g., `mastering-git-cli`, `reflex-ui`).
- **AGENTS.md**: Orchestrates skill invocation and enforces project-specific "golden rules".
