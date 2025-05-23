import reflex as rx
from ..backend.backend import State, Incidencia
from ..components.status_badges import status_badge
from datetime import datetime

def filter_panel():
    """Create the filter panel for incidencias."""
    return rx.card(
        rx.vstack(
            rx.heading("🔍 Filtres et Recherche", size="4", margin_bottom="1em"),
            
            # Search bar
            rx.vstack(
                rx.text("Recherche générale", size="3", weight="bold"),
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    placeholder="Rechercher par nom, téléphone, adresse...",
                    size="3",
                    width="100%",
                    variant="surface",
                    on_change=State.set_filter_value,
                ),
                spacing="2",
                width="100%",
            ),
            
            # Filters row
            rx.hstack(
                # Status filter
                rx.vstack(
                    rx.text("Status", size="3", weight="bold"),
                    rx.select(
                        ["Tous", "Solucionada", "Pendiente", "Tarea Creada"],
                        placeholder="Filtrer par status",
                        size="3",
                        on_change=State.filter_by_status,
                    ),
                    spacing="2",
                    flex="1",
                ),
                
                # User filter
                rx.vstack(
                    rx.text("Usuario", size="3", weight="bold"),
                    rx.select(
                        ["Tous", "Esther", "Juanita", "Restituta", "Estelina", "Anja", "Crecensia"],
                        placeholder="Filtrer par usuario",
                        size="3",
                        on_change=State.filter_by_user,
                    ),
                    spacing="2",
                    flex="1",
                ),
                
                # Date filter
                rx.vstack(
                    rx.text("Période", size="3", weight="bold"),
                    rx.select(
                        ["Toutes", "Aujourd'hui", "Cette semaine", "Ce mois", "Cette année"],
                        placeholder="Filtrer par date",
                        size="3",
                        on_change=State.filter_by_date,
                    ),
                    spacing="2",
                    flex="1",
                ),
                
                spacing="4",
                width="100%",
            ),
            
            # Action buttons
            rx.hstack(
                rx.button(
                    rx.icon("refresh-cw", size=16),
                    "Réinitialiser",
                    variant="outline",
                    color_scheme="gray",
                    on_click=State.reset_filters,
                    transition="all 0.2s",
                    _hover={"transform": "scale(1.05)"},
                ),
                rx.button(
                    rx.icon("download", size=16),
                    "Exporter",
                    variant="solid",
                    color_scheme="blue",
                    on_click=State.download_csv_data,
                    transition="all 0.2s",
                    _hover={"transform": "scale(1.05)"},
                ),
                spacing="3",
                justify="end",
                width="100%",
            ),
            
            spacing="4",
            width="100%",
        ),
        width="100%",
        padding="1.5em",
        margin_bottom="1em",
    )

def statistics_cards():
    """Create statistics cards for filtered data."""
    return rx.hstack(
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.icon("users", size=20, color=rx.color("blue", 9)),
                    rx.text("Total", size="3", weight="bold"),
                    spacing="2",
                ),
                rx.text(
                    State.total_incidencias,
                    size="6",
                    weight="bold",
                    color=rx.color("blue", 9),
                ),
                spacing="2",
                align_items="center",
            ),
            background_color=rx.color("blue", 2),
            padding="1.5em",
            border_radius="lg",
            transition="all 0.2s",
            _hover={"transform": "scale(1.05)"},
        ),
        
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.icon("circle-alert", size=20, color=rx.color("orange", 9)),
                    rx.text("Pendientes", size="3", weight="bold"),
                    spacing="2",
                ),
                rx.text(
                    State.total_pendientes,
                    size="6",
                    weight="bold",
                    color=rx.color("orange", 9),
                ),
                spacing="2",
                align_items="center",
            ),
            background_color=rx.color("orange", 2),
            padding="1.5em",
            border_radius="lg",
            transition="all 0.2s",
            _hover={"transform": "scale(1.05)"},
        ),
        
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.icon("circle-check-big", size=20, color=rx.color("green", 9)),
                    rx.text("Solucionadas", size="3", weight="bold"),
                    spacing="2",
                ),
                rx.text(
                    State.total_solucionadas,
                    size="6",
                    weight="bold",
                    color=rx.color("green", 9),
                ),
                spacing="2",
                align_items="center",
            ),
            background_color=rx.color("green", 2),
            padding="1.5em",
            border_radius="lg",
            transition="all 0.2s",
            _hover={"transform": "scale(1.05)"},
        ),
        
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.icon("wrench", size=20, color=rx.color("purple", 9)),
                    rx.text("Bitrix", size="3", weight="bold"),
                    spacing="2",
                ),
                rx.text(
                    State.total_bitrix,
                    size="6",
                    weight="bold",
                    color=rx.color("purple", 9),
                ),
                spacing="2",
                align_items="center",
            ),
            background_color=rx.color("purple", 2),
            padding="1.5em",
            border_radius="lg",
            transition="all 0.2s",
            _hover={"transform": "scale(1.05)"},
        ),
        
        spacing="4",
        width="100%",
        wrap="wrap",
        justify="center",
    )

def show_incidencia_service(incidencia: Incidencia):
    """Show an incidencia in the service view."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(incidencia.name, size="4", weight="bold"),
                    rx.text(f"📞 {incidencia.phone}", size="3"),
                    rx.text(f"📍 {incidencia.address}", size="3"),
                    align_items="start",
                    spacing="1",
                    flex="1",
                ),
                rx.vstack(
                    rx.match(
                        incidencia.status,
                        ("Solucionada", status_badge("Solucionada")),
                        ("Pendiente", status_badge("Pendiente")),
                        ("Tarea Creada", status_badge("Tarea Creada")),
                    ),
                    rx.text(f"👤 {incidencia.usuario}", size="3"),
                    align_items="end",
                    spacing="2",
                ),
                justify="between",
                width="100%",
            ),
            
            rx.text(f"💬 {incidencia.motivo}", size="3", color=rx.color("gray", 10)),
            rx.text(f"📅 {incidencia.date}", size="2", color=rx.color("gray", 8)),
            
            spacing="3",
            align_items="start",
            width="100%",
        ),
        padding="1em",
        border_radius="lg",
        border=f"1px solid {rx.color('gray', 6)}",
        transition="all 0.2s",
        _hover={"transform": "scale(1.02)", "box_shadow": "lg"},
        width="100%",
    )

def services_table():
    """Create the services table view."""
    return rx.vstack(
        rx.hstack(
            rx.heading("📊 Résultats", size="4"),
            rx.spacer(),
            rx.text(
                f"Affichage de {State.page_number} / {State.total_pages} pages",
                size="3",
                color=rx.color("gray", 10),
            ),
            width="100%",
            align="center",
        ),
        
        # Grid view for incidencias
        rx.box(
            rx.foreach(
                State.get_current_page,
                show_incidencia_service,
            ),
            width="100%",
            max_height="600px",
            overflow_y="auto",
            padding="1em",
            border_radius="lg",
            border=f"1px solid {rx.color('gray', 6)}",
        ),
        
        # Pagination
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
            rx.text(
                f"Page {State.page_number} de {State.total_pages}",
                size="3",
                padding_x="1em",
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
            spacing="2",
            justify="center",
            width="100%",
        ),
        
        spacing="4",
        width="100%",
    )

def services_page():
    """Create the services page with advanced filtering and data processing."""
    return rx.vstack(
        rx.heading("🔧 Services - Traitement des Incidencias", size="6", margin_bottom="1em", text_align="center"),
        
        # Filter panel
        filter_panel(),
        
        # Statistics cards
        statistics_cards(),
        
        # Services table
        services_table(),
        
        spacing="6",
        width="100%",
        max_width="1400px",
        padding="2em",
        margin="0 auto",
        on_mount=State.load_entries,
    )