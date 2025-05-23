from datetime import datetime, timedelta
from typing import Union
import io
from io import StringIO
import csv
from ..models.my_model import Incidencia, MonthValues
from ..backend.moteur import _get_percentage_change

import reflex as rx
from sqlmodel import String, asc, cast, desc, func, or_, select


class State(rx.State):
    """The state class."""

    # Variables principales
    incidencias: list[Incidencia] = []
    current_incidencia: Incidencia = Incidencia()

    total_pendientes: int 
    total_solucionadas: int 
    total_bitrix: int 


    # Variables pour le tri et la recherche
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    # Variables pour la pagination
    total_incidencias: int = 0
    offset: int = 0
    limit: int = 10  # Augmenté à 10 pour une meilleure expérience utilisateur

    # Variables pour les statistiques mensuelles
    current_month_values: MonthValues = MonthValues()
    previous_month_values: MonthValues = MonthValues()

    columns: list[str] = ["name","address", "motivo", "usuario", "date", "status", "bitrix"]


    # -- Debut des fonctions responsables de la pagination --
    @rx.var(cache=True)
    def page_number(self) -> int:
        """Calculate the current page number."""
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        """Calculate the total number of pages."""
        return (self.total_incidencias // self.limit) + (
            1 if self.total_incidencias % self.limit else 0
        )

    @rx.var(cache=True)
    def get_current_page(self) -> list[Incidencia]:
        """Get the current page of incidencias."""
        return self.incidencias

    def prev_page(self):
        """Go to the previous page."""
        if self.page_number > 1:
            self.offset -= self.limit
            self.load_entries()

    def next_page(self):
        """Go to the next page."""
        if self.page_number < self.total_pages:
            self.offset += self.limit
            self.load_entries()

    def first_page(self):
        """Go to the first page."""
        self.offset = 0
        self.load_entries()

    def last_page(self):
        """Go to the last page."""
        self.offset = (self.total_pages - 1) * self.limit
        self.load_entries()
    # -- fin des fonctions de pagination --

    # -- Debut des fonctions chargement des données --
    @rx.event
    def load_entries(self) -> list[Incidencia]:
        """Load incidencias from the database with pagination, sorting and filtering."""
        self.affectation()
        with rx.session() as session:
            # Get total count
            self.total_incidencias = session.exec(select(func.count(Incidencia.id))).one()

            # Build query with pagination, sorting and filtering
            query = select(Incidencia)
            
            # Apply search filter
            if self.search_value:
                search_value = f"%{str(self.search_value).lower()}%"
                query = query.where(
                    or_(
                        *[
                            getattr(Incidencia, field).ilike(search_value)
                            for field in Incidencia.get_fields()
                            if field not in ["id"]
                        ]
                    )
                )
            # Apply sorting
            if self.sort_value:
                sort_column = getattr(Incidencia, self.sort_value)
                order = (
                    desc(func.lower(sort_column))
                    if self.sort_reverse
                    else asc(func.lower(sort_column))
                )
                query = query.order_by(order)

            # Apply pagination
            query = query.offset(self.offset).limit(self.limit)
            
            # Execute query
            self.incidencias = session.exec(query).all()
        
            # Update monthly statistics
            self.get_current_month_values()
            self.get_previous_month_values()
    # -- fin des fonctions chargement des données --


    # -- Debut des fonctions responsables des statistiques mensuelles --
    def get_current_month_values(self):
        """Calculate current month's statistics."""
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)

        current_month_incidencias = [
            incidencia
            for incidencia in self.incidencias
            if datetime.strptime(incidencia.date, "%Y-%m-%d %H:%M:%S") >= start_of_month
        ]

        self.current_month_values = MonthValues(
            num_incidencias=len(current_month_incidencias),
            num_solucionadas=len([i for i in current_month_incidencias if i.status == "Solucionada"]),
            num_pendientes=len([i for i in current_month_incidencias if i.status == "Pendiente"]),
            num_bitrix=len([i for i in current_month_incidencias if i.status == "Tarea Creada"])
        )

    def get_previous_month_values(self):
        """Calculate previous month's statistics."""
        now = datetime.now()
        first_day_of_current_month = datetime(now.year, now.month, 1)
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        start_of_last_month = datetime(last_day_of_last_month.year, last_day_of_last_month.month, 1)

        previous_month_incidencias = [
            incidencia
            for incidencia in self.incidencias
            if start_of_last_month <= datetime.strptime(incidencia.date, "%Y-%m-%d %H:%M:%S") <= last_day_of_last_month
        ]

        self.previous_month_values = MonthValues(
            num_incidencias=len(previous_month_incidencias),
            num_solucionadas=len([i for i in previous_month_incidencias if i.status == "Solucionada"]),
            num_pendientes=len([i for i in previous_month_incidencias if i.status == "Pendiente"]),
            num_bitrix=len([i for i in previous_month_incidencias if i.status == "Tarea Creada"])
        )
    # -- fin des fonctions responsables des statistiques mensuelles --

    # -- Debut des fonctions responsables de la recherche, tri et pagination --
    @rx.event
    def set_sort_value(self, value: str):
        """Set the sort value."""
        self.sort_value = value
        self.load_entries()

    @rx.event
    def set_filter_value(self, value: str):
        """Set the search value."""
        self.search_value = value
        self.load_entries()

    def toggle_sort(self):
        """Toggle sort direction."""
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    def get_incidencia(self, incidencia: Incidencia):
        """Set the current incidencia."""
        self.current_incidencia = incidencia
    

    def add_incidencia_to_db(self, form_data: dict):
        """Add a new incidencia to the database."""
        with rx.session() as session:
            self.current_incidencia = Incidencia(
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), **form_data
            )
            session.add(self.current_incidencia)
            session.commit()
            session.refresh(self.current_incidencia)
        self.load_entries()
        return rx.toast.info(
            f"Incidencia pour {self.current_incidencia.name} a été ajoutée.",
            position="bottom-right"
        )

    def update_incidencia_to_db(self, form_data: dict):
        """Update an existing incidencia in the database."""
        with rx.session() as session:
            incidencia = session.exec(
                select(Incidencia).where(Incidencia.id == self.current_incidencia.id)
            ).first()
            form_data.pop("id", None)
            incidencia.set(**form_data)
            session.add(incidencia)
            session.commit()
        self.load_entries()
        return rx.toast.info(
            f"Incidencia pour {self.current_incidencia.name} a été modifiée.",
            position="bottom-right"
        )

    def delete_incidencia(self, id: int):
        """Delete an incidencia from the database."""
        with rx.session() as session:
            incidencia = session.exec(select(Incidencia).where(Incidencia.id == id)).first()
            session.delete(incidencia)
            session.commit()
        self.load_entries()
        return rx.toast.info(
            f"Incidencia pour {incidencia.name} a été supprimée.",
            position="bottom-right"
        )
    # -- fin des fonctions responsables de la recherche, tri et pagination --
    def download_csv_data(self):
        """Download incidencias data as CSV."""
        filename = f"atc_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=Incidencia.__fields__)
        writer.writeheader()
        for incidencia in self.incidencias:
            writer.writerow(incidencia.dict())
        return rx.download(
            data=output.getvalue(),
            filename=filename
        )
    # -- fin des fonctions responsables de la recherche, tri et pagination --

    # -- Debut des fonctions responsables des statistiques --

    @rx.var(cache=True)
    def incidencias_change(self) -> float:
        """Calculate the percentage change for total incidencias."""
        return _get_percentage_change(
            self.current_month_values.num_incidencias,
            self.previous_month_values.num_incidencias,
        )

    @rx.var(cache=True)
    def incidencias_pendientes_change(self) -> float:
        """Calculate the percentage change for pending incidencias."""
        return _get_percentage_change(
            self.current_month_values.num_pendientes,
            self.previous_month_values.num_pendientes,
        )

    @rx.var(cache=True)
    def delivers_change(self) -> float:
        """Calculate the percentage change for solved incidencias."""
        return _get_percentage_change(
            self.current_month_values.num_solucionadas,
            self.previous_month_values.num_solucionadas,
        )

    @rx.var(cache=True)
    def incidencias_bitrix_change(self) -> float:
        """Calculate the percentage change for bitrix incidencias."""
        return _get_percentage_change(
            self.current_month_values.num_bitrix,
            self.previous_month_values.num_bitrix,
        )


    def get_total_pendientes(self) -> int:
        """Get the total number of pending incidencias."""
        with rx.session() as session:
            query = select(func.count()).select_from(Incidencia).where(Incidencia.status == "Pendiente")
            return session.exec(query).first()

   
    def get_total_solucionadas(self) -> int:
        """Get the total number of solved incidencias."""
        with rx.session() as session:
            query = select(func.count()).select_from(Incidencia).where(Incidencia.status == "Solucionada")
            return session.exec(query).first()
     
   
    def get_total_bitrix(self) -> int:
        """Get the total number of bitrix incidencias."""
        with rx.session() as session:           
            query = select(func.count()).select_from(Incidencia).where(Incidencia.status == "Tarea Creada")
            return session.exec(query).first()
    

    def affectation(self):
        self.total_pendientes = self.get_total_pendientes()
        self.total_solucionadas = self.get_total_solucionadas()
        self.total_bitrix = self.get_total_bitrix()

    # -- fin des fonctions responsables des statistiques --


    @rx.event
    def update_time(self):
        """Update the state every 5 minutes."""
        self.load_entries()
        return rx.toast.info(
            "Données actualisées",
            position="bottom-right"
        )

    # Nouvelles méthodes pour la page de services
    @rx.event
    def filter_by_status(self, status: str):
        """Filter incidencias by status."""
        if status == "Tous":
            self.search_value = ""
        else:
            self.search_value = status
        self.load_entries()

    @rx.event
    def filter_by_user(self, user: str):
        """Filter incidencias by user."""
        if user == "Tous":
            self.search_value = ""
        else:
            self.search_value = user
        self.load_entries()

    @rx.event
    def filter_by_date(self, period: str):
        """Filter incidencias by date period."""
        from datetime import datetime, timedelta
        
        if period == "Toutes":
            self.search_value = ""
        elif period == "Aujourd'hui":
            today = datetime.now().strftime("%Y-%m-%d")
            self.search_value = today
        elif period == "Cette semaine":
            # Get current week start
            today = datetime.now()
            start_week = today - timedelta(days=today.weekday())
            self.search_value = start_week.strftime("%Y-%m-%d")
        elif period == "Ce mois":
            # Get current month start
            today = datetime.now()
            start_month = datetime(today.year, today.month, 1)
            self.search_value = start_month.strftime("%Y-%m-%d")
        elif period == "Cette année":
            # Get current year start
            today = datetime.now()
            start_year = datetime(today.year, 1, 1)
            self.search_value = start_year.strftime("%Y-%m-%d")
        
        self.load_entries()

    @rx.event
    def reset_filters(self):
        """Reset all filters."""
        self.search_value = ""
        self.sort_value = ""
        self.sort_reverse = False
        self.offset = 0
        self.load_entries()
        return rx.toast.info("Filtres réinitialisés", position="bottom-right")
