import reflex as rx


def navbar():
    return rx.flex(
        rx.badge(
            rx.icon(tag="radio-tower", size=28),
            rx.heading("CONEXXIA - Atención al cliente", size="6"),
            color_scheme="green",
            radius="large",
            align="center",
            variant="surface",
            padding="0.65rem",
        ),
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
        rx.text("© 2025 CONEXXIA - Atención al cliente - ",
                font_size="0.8em",
                ),
                rx.link(
                    "ANJA-HARIVONY",
                    href="https://www.linkedin.com/in/anja-harivony/",
                    color="white",
                    font_size="0.8em",
                    font_style="italic",
                    text_decoration="underline",
                ),
        align="center",
        width="100%",
        padding_bottom="1em",
        justify="center",
    )
