import reflex as rx

def services_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Servicios", size="2", margin_bottom="1em"),
        width="100%",
        padding="1em",
    )