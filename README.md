# 🚀 Goals Dashboard

Un dashboard premium para la gestión de objetivos personales, construido con **Reflex** (Python) y **Supabase**.

## 🛠️ Tech Stack
- **Frontend/Backend**: [Reflex](https://reflex.dev/)
- **Base de Datos & Auth**: [Supabase](https://supabase.com/)
- **Estilo**: Glassmorphism / Dark Mode Premium
- **Infraestructura de Agente**: Inspirada en Prowler (TDD + Skills)

## 🏁 Estado del Desarrollo
- **Fase 1-3**: Completadas (Entorno, Modelado de Datos, Servicio de Base de Datos).
- **Fase 4**: Completada (Interfaz UI Premium, Layout con Sidebar, Lógica de Navegación).
- **Fase 5**: En progreso (Autenticación real con Supabase).

## 🧪 Calidad e Integridad (TDD)
Este proyecto sigue una metodología estrictamente dirigida por pruebas (**Test-Driven Development**):

- **Tests de Servicio**: Validación de la lógica de negocio y conexión (Mocks).
- **Tests de UI**: Verificación de estados de navegación y renderizado de componentes.

Para ejecutar las pruebas:
```bash
./venv/bin/pytest                     # Todos los tests
./venv/bin/pytest tests/test_ui.py    # Solo tests de interfaz
```

## 🎨 Sistema de Diseño
- **Estilo**: Premium Dark Mode con efectos de **Glassmorphism** (`backdrop-filter: blur(15px)`).
- **Color de Acento**: Violeta Eléctrico (`#8A2BE2`).
- **Componentes**: Sidebar persistente, estados de navegación reactivos.

## 📐 Arquitectura de Datos

### 1. Esquema SQL (Supabase)
El corazón de la aplicación reside en dos tablas principales ubicadas en el esquema público de Supabase:

- **`goals`**: Almacena el objetivo principal.
  - `id`: Identificador único (UUID).
  - `user_id`: Enlace al usuario de Supabase Auth (Seguridad RLS activa).
  - `title`, `description`, `deadline`: Información del objetivo.
  - `status`: Estado actual (`pending`, `in_progress`, etc.).
  - `progress`: Valor de 0 a 100 calculado.
- **`milestones`**: Pasos intermedios para completar un objetivo.
  - Relación 1:N con `goals` (un objetivo tiene muchos hitos).

### 2. Modelos Pydantic (Python)
Ubicados en `models/goal.py`, estos modelos sirven como "puente" entre la base de datos y la interfaz:
- **Validación**: Aseguran que los datos tengan el formato correcto antes de guardarlos.
- **Tipado**: Permiten que Reflex entienda la estructura del objeto para renderizar la UI.

## 🚀 Configuración del Proyecto

### Requisitos
- Python 3.11+
- [Reflex CLI](https://reflex.dev/docs/getting-started/installation/)

### Instalación
1. Clonar el repositorio.
2. Crear y activar el entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Ejecución
```bash
reflex run
```

---
*Este proyecto utiliza un sistema de Agente Inteligente configurado en `AGENTS.md`.*
