import reflex as rx

class Incidencia(rx.Model, table=True):
    """The incidencia model."""

    name: str
    phone: str
    address: str
    motivo: str
    usuario: str
    date: str
    status: str
    bitrix: str


class MonthValues(rx.Base):
    """Values for a month."""

    num_incidencias: int = 0
    num_solucionadas: int = 0
    num_pendientes: int = 0
    num_bitrix: int = 0

class Operador(rx.Model, table=True):
    """The operador model."""
    nombre: str
    telefono: str
    email: str
    status: str