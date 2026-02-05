import reflex as rx
from . import styles
from services.factory import get_service
from models.goal import Goal

class State(rx.State):
    """The app state."""
    current_page: str = "home"
    user_id: str = ""
    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""
    error_message: str = ""
    is_loading: bool = False
    show_registration: bool = False
    # ... existing state ...
    goals: list[Goal] = []
    is_add_modal_open: bool = False

    def toggle_add_modal(self):
        self.is_add_modal_open = not self.is_add_modal_open

    def add_goal(self, form_data: dict):
        if not self.user_id:
            return
            
        title = form_data.get("title")
        description = form_data.get("description")
        deadline = form_data.get("deadline")
        
        if not title:
            return
            
        try:
            service = get_service()
            from models.goal import GoalCreate
            from uuid import UUID
            from datetime import datetime
            
            # Simple date parsing
            deadline_date = None
            if deadline:
                try:
                    deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
                except ValueError:
                    pass

            goal_create = GoalCreate(
                title=title,
                description=description,
                deadline=deadline_date,
                user_id=UUID(self.user_id)
            )
            
            service.create_goal(goal_create)
            
            # Refresh and close
            self.load_goals()
            self.is_add_modal_open = False
            
        except Exception as e:
            self.error_message = f"Failed to add goal: {str(e)}"

    def load_goals(self):
        """Fetch goals for the current user."""
        if not self.user_id:
            return
        
        self.is_loading = True
        try:
            service = get_service()
            # Convert UUID string to UUID object if necessary, or ensure service handles it
            from uuid import UUID
            self.goals = service.get_goals(UUID(self.user_id))
        except Exception as e:
            self.error_message = f"Failed to load goals: {str(e)}"
        finally:
            self.is_loading = False

    @rx.var
    def is_authenticated(self) -> bool:
        return self.user_id != ""

    def toggle_registration(self):
        """Toggle between login and registration forms."""
        self.show_registration = not self.show_registration
        self.error_message = ""
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""

    def login(self):
        """Log in with Supabase."""
        self.is_loading = True
        self.error_message = ""
        try:
            service = get_service()
            response = service.sign_in(self.email, self.password)
            if response.user:
                self.user_id = response.user.id
                self.email = ""
                self.password = ""
            else:
                self.error_message = "Invalid credentials"
        except Exception as e:
            self.error_message = str(e)
        finally:
            self.is_loading = False

    def signup(self):
        """Sign up with Supabase with metadata."""
        if not self.first_name or not self.last_name:
            self.error_message = "First name and Last name are required"
            return

        self.is_loading = True
        self.error_message = ""
        try:
            service = get_service()
            metadata = {
                "first_name": self.first_name,
                "last_name": self.last_name
            }
            response = service.sign_up(self.email, self.password, metadata=metadata)
            if response.user:
                # Signup successful
                self.user_id = response.user.id
                self.email = ""
                self.password = ""
                self.first_name = ""
                self.last_name = ""
            else:
                self.error_message = "Could not sign up"
        except Exception as e:
            self.error_message = str(e)
        finally:
            self.is_loading = False

    def logout(self):
        """Log out and reset state."""
        try:
            service = get_service()
            service.sign_out()
        except:
            pass
        self.user_id = ""
        self.current_page = "home"
        self.email = ""
        self.password = ""

    def set_current_page(self, page: str):
        self.current_page = page
        if page == "goals":
            self.load_goals()

def nav_item(text: str, icon: str, page: str) -> rx.Component:
    """A single navigation item in the sidebar."""
    return rx.hstack(
        rx.icon(icon, size=20),
        rx.text(text, font_weight="500"),
        on_click=lambda: State.set_current_page(page),
        style=rx.cond(
            State.current_page == page,
            styles.active_nav_item_style,
            styles.nav_item_style
        ),
        spacing="3",
        width="100%",
    )

def sidebar() -> rx.Component:
    """The sidebar component."""
    return rx.box(
        rx.vstack(
            rx.heading("Goals", size="7", color=styles.accent_color, margin_bottom="1em"),
            nav_item("Home", "home", "home"),
            nav_item("Goals", "target", "goals"),
            nav_item("Milestones", "list-check", "milestones"),
            rx.spacer(),
            # Logout Button
            rx.hstack(
                rx.icon("log-out", size=20),
                rx.text("Logout", font_weight="500"),
                on_click=State.logout,
                style=styles.nav_item_style,
                spacing="3",
                width="100%",
                cursor="pointer",
            ),
            nav_item("Settings", "settings", "settings"),
            spacing="4",
            height="100%",
            align="start",
        ),
        style=styles.sidebar_style,
    )

def layout(content: rx.Component) -> rx.Component:
    """The main layout wrapper."""
    return rx.box(
        sidebar(),
        rx.box(
            content,
            style=styles.content_style,
        ),
        background_color=styles.bg_dark,
    )

def auth_form() -> rx.Component:
    """A simple authentication form."""
    return rx.vstack(
        rx.heading("Welcome back", size="8", margin_bottom="0.5em"),
        rx.text("Enter your credentials to continue.", color=styles.text_dim, margin_bottom="1.5em"),
        
        # Error message
        rx.cond(
            State.error_message != "",
            rx.callout(
                State.error_message,
                icon="info",
                color_scheme="red",
                role="alert",
                width="100%",
                margin_bottom="1em",
            ),
        ),

        rx.input(
            placeholder="Email", 
            type="email", 
            width="100%",
            on_change=State.set_email,
            value=State.email,
        ),
        rx.input(
            placeholder="Password", 
            type="password", 
            width="100%",
            on_change=State.set_password,
            value=State.password,
        ),
        rx.button(
            "Log In", 
            on_click=State.login, 
            loading=State.is_loading,
            width="100%",
            color_scheme="violet",
            cursor="pointer",
        ),
        rx.hstack(
            rx.text("Don't have an account?", size="2"),
            rx.text(
                "Sign up", 
                size="2", 
                cursor="pointer", 
                color=styles.accent_color,
                on_click=State.toggle_registration,
                font_weight="bold",
            ),
            spacing="1",
        ),
        spacing="4",
        style={**styles.glass_style, "padding": "3em", "width": "400px"},
        align="center",
    )

def registration_form() -> rx.Component:
    """The registration form for new users."""
    return rx.vstack(
        rx.heading("Create an account", size="8", margin_bottom="0.5em"),
        rx.text("Join us to start tracking your goals.", color=styles.text_dim, margin_bottom="1.5em"),
        
        # Error message
        rx.cond(
            State.error_message != "",
            rx.callout(
                State.error_message,
                icon="info",
                color_scheme="red",
                role="alert",
                width="100%",
                margin_bottom="1em",
            ),
        ),

        rx.hstack(
            rx.input(
                placeholder="First Name", 
                width="100%",
                on_change=State.set_first_name,
                value=State.first_name,
            ),
            rx.input(
                placeholder="Last Name", 
                width="100%",
                on_change=State.set_last_name,
                value=State.last_name,
            ),
            width="100%",
            spacing="2",
        ),
        rx.input(
            placeholder="Email", 
            type="email", 
            width="100%",
            on_change=State.set_email,
            value=State.email,
        ),
        rx.input(
            placeholder="Password", 
            type="password", 
            width="100%",
            on_change=State.set_password,
            value=State.password,
        ),
        rx.button(
            "Register", 
            on_click=State.signup, 
            loading=State.is_loading,
            width="100%",
            color_scheme="violet",
            cursor="pointer",
        ),
        rx.hstack(
            rx.text("Already have an account?", size="2"),
            rx.text(
                "Log in", 
                size="2", 
                cursor="pointer", 
                color=styles.accent_color,
                on_click=State.toggle_registration,
                font_weight="bold",
            ),
            spacing="1",
        ),
        spacing="4",
        style={**styles.glass_style, "padding": "3em", "width": "400px"},
        align="center",
    )

def welcome_page() -> rx.Component:
    """The landing/welcome page."""
    return rx.center(
        rx.vstack(
            rx.heading("Master Your Ambitions", size="9", weight="bold"),
            rx.text(
                "The most elegant way to track your life goals and milestones.", 
                color=styles.text_dim, 
                size="5",
                text_align="center",
            ),
            rx.divider(border_color=styles.glass_border, width="200px", margin_y="2em"),
            rx.cond(
                State.show_registration,
                registration_form(),
                auth_form(),
            ),
            spacing="6",
            align="center",
        ),
        width="100%",
        height="100vh",
        background_color=styles.bg_dark,
    )

def index() -> rx.Component:
    """The main page entry point."""
    from .components.goals_views import goals_page
    return rx.box(
        rx.cond(
            State.is_authenticated,
            layout(
                rx.vstack(
                    rx.heading("Dashboard", size="9"),
                    rx.text("Build your future, one goal at a time.", color=styles.text_dim),
                    rx.divider(border_color=styles.glass_border, margin_y="2em"),
                    
                    rx.cond(
                        State.current_page == "home",
                        rx.text("Summary Dashboard Content (Coming Soon)"),
                        rx.cond(
                            State.current_page == "goals",
                            goals_page(),
                            rx.text(f"Currently viewing: {State.current_page}"),
                        )
                    ),
                    align="start",
                    spacing="4",
                )
            ),
            welcome_page(),
        ),
        width="100%",
    )

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        accent_color="violet",
    ),
)
app.add_page(index)
