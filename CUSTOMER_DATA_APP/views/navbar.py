import reflex as rx
from ..backend.backend import State

def nav_menu():
    """Create the navigation menu with old-school icons and hover animation."""
    return rx.hstack(
        rx.link(
            rx.hstack(
                rx.icon("layout-dashboard", size=20),
                rx.text("Dashboard"),
                align="center",
                spacing="2",
                transition="all 0.2s",
                _hover={"transform": "scale(1.1)"},
            ),
            href="/",
            color=rx.cond(rx.color_mode == "dark", "white", "black"),
            text_decoration="none",
        ),
        rx.link(
            rx.hstack(
                rx.icon("wrench", size=20),
                rx.text("Servicio"),
                align="center",
                spacing="2",
                transition="all 0.2s",
                _hover={"transform": "scale(1.1)"},
            ),
            href="/servicio",
            color=rx.cond(rx.color_mode == "dark", "white", "black"),
            text_decoration="none",
        ),
        rx.link(
            rx.hstack(
                rx.icon("database", size=20),
                rx.text("Datos"),
                align="center",
                spacing="2",
                transition="all 0.2s",
                _hover={"transform": "scale(1.1)"},
            ),
            href="/datos",
            color=rx.cond(rx.color_mode == "dark", "white", "black"),
            text_decoration="none",
        ),
        rx.link(
            rx.hstack(
                rx.icon("help-circle", size=20),
                rx.text("Ayuda"),
                align="center",
                spacing="2",
                transition="all 0.2s",
                _hover={"transform": "scale(1.1)"},
            ),
            href="/ayuda",
            color=rx.cond(rx.color_mode == "dark", "white", "black"),
            text_decoration="none",
        ),
        spacing="6",
        padding="1em",
        justify="center",
        width="100%",
    )

def navbar():
    return rx.flex(
        rx.hstack(
            rx.icon(tag="radio-tower", size=28, color="red"),
            rx.text("CONEXXIA", size="6", background_color="none", color="red"),
            rx.text("Atención al cliente", size="2", background_color="none", color=rx.cond(rx.color_mode == "dark", "white", "black"),),
            align="center",
            padding="0.65rem",
            color="white",
        ),
        nav_menu(),
        rx.spacer(),
        rx.hstack(
            #rx.image(src="radio-tower.png", width="100px", height="100px"),
            rx.color_mode.button(),
            align="center",
            spacing="3",
        ),
        spacing="2",
        flex_direction=["column", "column", "row"],
        align="center",
        width="100%",
        top="0px",
        padding_top="2em",
    )

def footer():
    return rx.flex(
        rx.text("© 2025 CONEXXIA - Atención al cliente",
                font_size="0.8em",
                ),
                rx.link(
                    "ANJA-HARIVONY - 222 304 981",
                    mailto="jefe.incidencias@conexxiaeg.com",
                    color="white",
                    font_size="0.8em",
                    font_style="italic",
                    text_decoration="underline",
                ),
        align="center",
        direction="column",
        spacing="2",
        width="100%",
        padding_bottom="1em",
        justify="center",
    )
