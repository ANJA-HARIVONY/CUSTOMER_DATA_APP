import reflex as rx

from ..backend.backend import Incidencia, State
from ..components.form_field import form_field
from ..components.status_badges import status_badge



def show_incidencia(user: Incidencia):
    """Show a customer in a table row."""
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.phone),
        rx.table.cell(user.address),
        rx.table.cell(user.motivo),
        rx.table.cell(user.usuario),
        rx.table.cell(user.date),
        rx.table.cell(
            rx.match(
                user.status,
                ("Solucionada", status_badge("Solucionada")),
                ("Pendiente", status_badge("Pendiente")),
                ("Tarea Creada", status_badge("Tarea Creada")),
                #status_badge("Pending"),
            )
        ),
        rx.table.cell(user.bitrix),
        rx.table.cell(
            rx.hstack(
                update_incidencia_dialog(user),
                delete_incidencia_dialog(user),
            )
        ),
        style={"_hover": {"bg": rx.color("gray", 3)}},
        align="center",
    )


def add_customer_button() -> rx.Component:
    """Add a new customer to the database."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Agregar nuevo incidencia", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="users", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Agregar nueva incidencia",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Rellene el formulario con la información de la incidencia",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(

                    rx.flex(
                        # Name
                        form_field(
                            "Nombre",
                            "Nombre del cliente",
                            "text",
                            "name",
                            "user",
                        ),
                        # Phone
                        form_field("Teléfono", "Teléfono del cliente", "tel", "phone", "phone"),
                        # Address
                        form_field("Dirección", "Dirección del cliente", "text", "address", "home"),
                        # Motivo
                        form_field(
                            "Motivo", "Motivo de la incidencia", "text", "motivo", "pen"
                        ),
                        # Usuario
                        rx.hstack(
                            rx.icon("user-round-pen", size=16, stroke_width=1.5),
                            rx.text("Usuario"),
                            align="center",
                            spacing="2",
                        ),
                        rx.select(
                            ["Esther", "Juanita", "Restituta", "Estelina", "Anja", "Crecensia"],
                            name="usuario",
                            direction="row",
                            as_child=True,
                            required=True,
                            placeholder="Selecciona un usuario",
                        ),
                        # Status
                        rx.vstack(
                            rx.hstack(
                                rx.icon("list-todo", size=16, stroke_width=1.5),
                                rx.text("Status"),
                                align="center",
                                spacing="2",
                            ),
                            rx.radio(
                                ["Solucionada", "Pendiente", "Tarea Creada"],
                                name="status",
                                direction="row",
                                as_child=True,
                                required=True,
                            ),
                        ),
                        # Bitrix
                        form_field(
                            "Bitrix", "¿Es una incidencia de Bitrix?", "number", "bitrix", "wrench"
                        ),

                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancelar",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Agregar incidencia"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.add_incidencia_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def update_incidencia_dialog(user):
    """Update a customer in the database."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("square-pen", size=22),
                color_scheme="blue",
                size="2",
                variant="solid",
                on_click=lambda: State.get_incidencia(user),
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="square-pen", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Editar incidencia",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Edite la información de la incidencia",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Name
                        form_field(
                            "Name",
                            "Nombre del cliente",
                            "text",
                            "name",
                            "user",
                            user.name,
                        ),
                        # Phone
                        form_field(
                            "Phone",
                            "Teléfono del cliente",
                            "tel",
                            "phone",
                            "phone",
                            user.phone,
                        ),
                        # Address
                        form_field(
                            "Address",
                            "Dirección del cliente",
                            "text",
                            "address",
                            "home",
                            user.address,
                        ),
                        # Motivo
                        form_field(
                            "Motivo", "Motivo de la visita", "text", "motivo", "pen",
                            user.motivo,
                        ),
                        # Usuario
                        rx.hstack(
                            rx.icon("user-round-pen", size=16, stroke_width=1.5),
                            rx.text("Usuario"),
                            align="center",
                            spacing="2",
                        ),
                        rx.select(
                            ["Esther", "Juanita", "Restituta", "Estelina", "Anja", "Crecensia"],
                            name="usuario",
                            direction="row",
                            as_child=True,
                            required=True,
                            default_value=user.usuario,
                        ),
                        # Status
                        rx.vstack(
                            rx.hstack(
                                rx.icon("truck", size=16, stroke_width=1.5),
                                rx.text("Status"),
                                align="center",
                                spacing="2",
                            ),
                            rx.radio(
                                ["Solucionada", "Pendiente", "Tarea Creada"],
                                default_value=user.status,
                                name="status",
                                direction="row",
                                as_child=True,
                                required=True,
                            ),
                        ),
                        # Bitrix
                        form_field(
                            "Bitrix", "Tarea#  ", "number", "bitrix", "wrench",
                            user.bitrix,
                        ),  
                        
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Actualizar incidencia"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.update_incidencia_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )

def delete_incidencia_dialog(user):
    """Delete a customer from the database."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(rx.icon("trash-2", size=22), color_scheme="red", size="2", variant="solid"),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(rx.icon("trash-2", size=34), color_scheme="red", radius="full", padding="0.65rem"),
                rx.vstack(rx.dialog.title("Eliminar incidencia", weight="bold", margin="0"), rx.dialog.description("¿Está seguro de que desea eliminar la incidencia de " + user.name + "?"), spacing="1", height="100%", align_items="start"),
            ),
            rx.dialog.close(
                rx.hstack(
                    rx.button("Cancelar", variant="soft", color_scheme="gray"),
                    rx.button("Eliminar", variant="solid", color_scheme="red", on_click=lambda: State.delete_incidencia(user.id)),
                    spacing="3",
                    mt="4",
                    justify="end",
                )
            ),
        ),
    )


def _header_cell(text: str, icon: str):
    """Show a header cell in the table."""
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )

def main_table():
    """Show the main table."""
    return rx.fragment(
        rx.flex(
            add_customer_button(),
            rx.spacer(),
            rx.cond(
                State.sort_reverse,
                rx.icon(
                    "arrow-down-z-a",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=State.toggle_sort,
                ),
                rx.icon(
                    "arrow-down-a-z",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=State.toggle_sort,
                ),
            ),
            rx.select(
                ["name", "phone", "address", "motivo", "usuario", "date", "status"],
                placeholder="Ordenar por: Nombre",
                size="3",
                on_change=State.set_sort_value,
            ),
            rx.input(
                rx.input.slot(rx.icon("search")),
                placeholder="Buscar...",
                size="3",
                max_width="225px",
                width="100%",
                variant="surface",
                on_change=State.set_filter_value,
            ),
            justify="end",
            align="center",
            spacing="3",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Nombre", "user"),
                    _header_cell("Teléfono", "phone"),
                    _header_cell("Dirección", "home"),
                    _header_cell("Motivo", "pen"),
                    _header_cell("Usuario", "user-round-pen"),
                    _header_cell("Fecha", "calendar"),
                    _header_cell("Status", "list-todo"),
                    _header_cell("Bitrix", "wrench"),
                    _header_cell("Acciones", "cog"),    
                ),
            ),
            rx.table.body(rx.foreach(State.get_current_page, show_incidencia)),
            variant="surface",
            size="3",
            width="100%",
            on_mount=State.load_entries,
        ),
        rx.spacer(),
        _pagination_view(),
    )

def _pagination_view() -> rx.Component:
    """Create the pagination view."""
    return rx.hstack(
        rx.text(
            "Página ",
            rx.code(State.page_number),
            f" de {State.total_pages}",
            justify="end",
        ),
        rx.hstack(
            rx.icon_button(
                rx.icon("chevrons-left", size=18),
                on_click=State.first_page,
                opacity=rx.cond(State.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(State.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-left", size=18),
                on_click=State.prev_page,
                opacity=rx.cond(State.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(State.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-right", size=18),
                on_click=State.next_page,
                opacity=rx.cond(State.page_number == State.total_pages, 0.6, 1),
                color_scheme=rx.cond(State.page_number == State.total_pages, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevrons-right", size=18),
                on_click=State.last_page,
                opacity=rx.cond(State.page_number == State.total_pages, 0.6, 1),
                color_scheme=rx.cond(State.page_number == State.total_pages, "gray", "accent"),
                variant="soft",
            ),
            align="center",
            spacing="2",
            justify="end",
        ),
        spacing="5",
        margin_top="1em",
        align="center",
        width="100%",
        justify="end",
    )
