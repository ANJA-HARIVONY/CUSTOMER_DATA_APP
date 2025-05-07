import reflex as rx

from .components.stats_cards import stats_cards_group
from .views.navbar import navbar, footer
from .views.table import main_table
from .backend.backend import State

def index() -> rx.Component:
    return rx.vstack(
        navbar(),               
        stats_cards_group(),
        rx.box(
            main_table(),
            width="100%",
        ),
        # Mise à jour automatique toutes les 5 minutes (300000 ms)
        rx.moment(interval=300000, on_change=State.update_time, display="none"),
        footer(),
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em"],
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark", has_background=True, radius="large", accent_color="grass"
    ),
)

app.add_page(
    index,
    title="Atención al cliente",
    description="Aplicación para la atención al cliente.",
)
