import reflex as rx

from .components.stats_cards import stats_cards_group
from .views.navbar import navbar, footer
from .views.table import main_table
from .backend.backend import State, Incidencia
from .pages.ayuda_page import ayuda_page
from .pages.services_page import services_page
from .pages.data_page import datos_page

@rx.page(route="/", title="Atención al cliente", description="Aplicación para la atención al cliente.")
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

@rx.page(route="/servicio", title="Servicio", description="Servicio de la aplicación.")
def servicio() -> rx.Component:
    return rx.vstack(
        navbar(),
        services_page(),
        footer(),
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em"],
    )

@rx.page(route="/datos", title="Datos", description="Datos de la aplicación.")
def datos() -> rx.Component:
    return rx.vstack(
        navbar(),
        datos_page(),
        footer(),
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em"],
    )


@rx.page(route="/ayuda", title="Ayuda", description="Ayuda de la aplicación.")
def ayuda() -> rx.Component:
    return rx.vstack(
        navbar(),
        ayuda_page(),
        footer(),
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em"],
    )

app = rx.App(
    theme=rx.theme(
        appearance="dark", has_background=True, radius="large", accent_color="grass"
    ),
)


