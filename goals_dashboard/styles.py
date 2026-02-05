import reflex as rx

# Color Palette - Premium Dark Mode
bg_dark = "#0D0D0D"
sidebar_bg = "rgba(20, 20, 20, 0.8)"
accent_color = "#8A2BE2"  # Electric Violet
glass_bg = "rgba(255, 255, 255, 0.05)"
glass_border = "rgba(255, 255, 255, 0.1)"
text_main = "#F5F5F5"
text_dim = "#A0A0A0"

# Glassmorphism Style
glass_style = {
    "backdrop_filter": "blur(12px)",
    "background_color": glass_bg,
    "border": f"1px solid {glass_border}",
    "border_radius": "16px",
}

sidebar_style = {
    "width": "280px",
    "height": "100vh",
    "position": "fixed",
    "left": "0",
    "top": "0",
    "background_color": sidebar_bg,
    "backdrop_filter": "blur(15px)",
    "border_right": f"1px solid {glass_border}",
    "padding": "2em",
}

content_style = {
    "margin_left": "280px",
    "min_height": "100vh",
    "background_color": bg_dark,
    "color": text_main,
    "padding": "2em",
}

nav_item_style = {
    "padding": "10px 15px",
    "border_radius": "10px",
    "cursor": "pointer",
    "color": text_dim,
    "_hover": {
        "background_color": "rgba(138, 43, 226, 0.1)",
        "color": text_main,
    }
}

active_nav_item_style = {
    **nav_item_style,
    "color": text_main,
    "background_color": "rgba(138, 43, 226, 0.2)",
    "border": f"1px solid {accent_color}",
}
