import reflex as rx
from . import styles

class State(rx.State):
    """The app state."""
    current_page: str = "home"
    user_id: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return self.user_id != ""

    def login(self, user_id: str):
        self.user_id = user_id

    def logout(self):
        self.user_id = ""
        self.current_page = "home"

    def set_current_page(self, page: str):
        self.current_page = page

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
        rx.input(placeholder="Email", type="email", width="100%"),
        rx.input(placeholder="Password", type="password", width="100%"),
        rx.button(
            "Log In", 
            on_click=lambda: State.login("user-temp-id"), 
            width="100%",
            color_scheme="violet",
            cursor="pointer",
        ),
        rx.text("Don't have an account? Sign up", size="2", cursor="pointer", color=styles.accent_color),
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
            auth_form(),
            spacing="6",
            align="center",
        ),
        width="100%",
        height="100vh",
        background_color=styles.bg_dark,
    )

def index() -> rx.Component:
    """The main page entry point."""
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
                        rx.text(f"Currently viewing: {State.current_page}"),
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
