import reflex as rx
from .. import styles
from models.goal import Goal
from ..goals_dashboard import State

def goal_card(goal: Goal) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(goal.title, size="5", color="white"),
                rx.spacer(),
                rx.badge(goal.status, color_scheme="violet"),
                width="100%",
                align="center",
            ),
            rx.text(goal.description, color=styles.text_dim, size="3"),
            rx.progress(value=goal.progress, width="100%", color_scheme="violet"),
            rx.hstack(
                rx.text(f"Progress: {goal.progress}%", size="2", color=styles.text_dim),
                rx.spacer(),
                rx.cond(
                    goal.deadline,
                    rx.text(f"Due: {goal.deadline}", size="2", color=styles.text_dim),
                    rx.fragment()
                ),
                width="100%",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="1.5em",
        border_radius="12px",
        background="rgba(255, 255, 255, 0.03)",
        border=f"1px solid {styles.glass_border}",
        width="100%",
    )

def add_goal_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus"),
                "Add Goal",
                color_scheme="violet",
                variant="solid"
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Create New Goal"),
            rx.dialog.description("Set a new target for yourself."),
            rx.form(
                rx.vstack(
                    rx.text("Title", size="2", mb="1", color=styles.text_dim),
                    rx.input(placeholder="e.g. Learn Python", name="title", required=True),
                    rx.text("Description", size="2", mb="1", color=styles.text_dim),
                    rx.text_area(placeholder="Details...", name="description"),
                    rx.text("Deadline", size="2", mb="1", color=styles.text_dim),
                    rx.input(type="date", name="deadline"),
                    rx.flex(
                        rx.dialog.close(
                            rx.button("Cancel", color_scheme="gray", variant="soft")
                        ),
                        rx.button("Save Goal", type="submit", color_scheme="violet"),
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    spacing="3",
                ),
                on_submit=State.add_goal,
            ),
            max_width="450px",
        ),
        open=State.is_add_modal_open,
        on_open_change=State.toggle_add_modal,
    )

def goals_page() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("My Goals", size="8"),
            rx.spacer(),
            add_goal_dialog(),
            width="100%",
            align="center",
        ),
        rx.text("Track and manage your ambitions.", color=styles.text_dim),
        rx.divider(border_color=styles.glass_border, margin_y="1em"),
        
        rx.cond(
            State.is_loading,
            rx.spinner(color="violet", size="3"),
            rx.vstack(
                rx.foreach(
                    State.goals,
                    goal_card
                ),
                width="100%",
                spacing="4",
            )
        ),
        width="100%",
        spacing="4",
    )
