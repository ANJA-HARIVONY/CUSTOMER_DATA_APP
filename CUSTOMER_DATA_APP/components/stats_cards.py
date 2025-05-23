import reflex as rx
from reflex.components.radix.themes.base import (
    LiteralAccentColor,
)

from ..backend.backend import State




def _arrow_badge(arrow_icon: str, percentage_change: float, arrow_color: str):
    """Create an arrow badge with percentage change."""
    return rx.badge(
        rx.icon(
            tag=arrow_icon,
            color=rx.color(arrow_color, 9),
        ),
        rx.text(
            f"{percentage_change}%",
            size="2",
            color=rx.color(arrow_color, 9),
            weight="medium",
        ),
        color_scheme=arrow_color,
        radius="large",
        align_items="center",
    )


def stats_card(
    stat_name: str,
    value: int,
    prev_value: int,
    percentage_change: float,
    total_value: int,
    icon: str,
    icon_color: LiteralAccentColor,
    extra_char: str = "",
) -> rx.Component:
    """Create a statistics card component."""
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.icon(
                            tag=icon,
                            size=22,
                            color=rx.color(icon_color, 11),
                        ),
                        rx.text(
                            stat_name,
                            size="4",
                            weight="medium",
                            color=rx.color("gray", 11),
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.cond(
                        value > prev_value,
                        _arrow_badge("trending-up", percentage_change, "grass"),
                        _arrow_badge("trending-down", percentage_change, "tomato"),
                    ),
                    justify="between",
                    width="100%",
                ),
                rx.hstack(
                    rx.heading(
                        f"{total_value}",
                        size="7",
                        weight="bold",
                    ),
                    rx.text(
                        f"desde {extra_char}{prev_value}",
                        size="3",
                        color=rx.color("gray", 10),
                    ),
                    rx.text(
                       f"Parcial: {extra_char}{value}",
                        size="3",
                        color=rx.color("gray", 10),
                    ),

                    spacing="2",
                    align_items="end",
                ),
                align_items="start",
                justify="between",
                width="100%",
            ),
            align_items="start",
            width="100%",
            justify="between",
        ),
        size="3",
        width="100%",
        max_width="22rem",
        transition="all 0.2s",
        _hover={"transform": "scale(1.1)"},
    )


def stats_cards_group() -> rx.Component:
    """Create a group of statistics cards."""
    return rx.flex(
        stats_card(
            "Total Incidencias",
            value=State.current_month_values.num_incidencias,
            prev_value=State.previous_month_values.num_incidencias,
            percentage_change=State.incidencias_change,
            icon="users",
            icon_color="blue",
            total_value=State.total_incidencias,
        ),
        stats_card(
            "Total Pendientes",
            value=State.current_month_values.num_pendientes,
            prev_value=State.previous_month_values.num_pendientes,
            percentage_change=State.incidencias_pendientes_change,
            icon="circle-alert",
            icon_color="orange",
            total_value=State.total_pendientes,
        ),
        stats_card(
            "Total Solucionadas",
            value=State.current_month_values.num_solucionadas,
            prev_value=State.previous_month_values.num_solucionadas,
            percentage_change=State.delivers_change,
            icon="circle-check-big",
            icon_color="green",
            total_value=State.total_solucionadas,
        ),
        stats_card(
            "Total Bitrix",
            value=State.current_month_values.num_bitrix,
            prev_value=State.previous_month_values.num_bitrix,
            percentage_change=State.incidencias_bitrix_change,
            icon="wrench",
            icon_color="orange",
            total_value=State.total_bitrix,
        ),
        spacing="5",
        width="100%",
        wrap="wrap",
        display=["none", "none", "flex"],
    )
