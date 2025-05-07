import reflex as rx


def _badge(icon: str, text: str, color_scheme: str):
    return rx.badge(
        rx.icon(icon, size=16),
        text,
        color_scheme=color_scheme,
        radius="full",
        variant="soft",
        size="3",
    )


def status_badge(status: str):
    badge_mapping = {
        "Solucionada": ("check", "Solucionada", "green"),
        "Pendiente": ("loader", "Pendiente", "yellow"),
        "Tarea Creada": ("wrench", "Tarea Creada", "orange"),
    }
    return _badge(*badge_mapping.get(status, ("loader", "Pending", "yellow")))
