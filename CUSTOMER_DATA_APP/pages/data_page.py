import reflex as rx

def datos_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Datos de Incidencias", size="2", margin_bottom="1em"),
        width="100%",
        padding="1em",
    )