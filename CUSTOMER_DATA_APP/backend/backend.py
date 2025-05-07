from datetime import datetime, timedelta
from typing import Union
import io
from io import StringIO
import csv

import reflex as rx
from sqlmodel import String, asc, cast, desc, func, or_, select


def _get_percentage_change(
    value: Union[int, float], prev_value: Union[int, float]
) -> float:
    """Calculate the percentage change between two values."""
    percentage_change = (
        round(((value - prev_value) / prev_value) * 100, 2)
        if prev_value != 0
        else 0.0
        if value == 0
        else float("inf")
    )
    return percentage_change


# def charge_from_csv():
#     """Charge les données depuis un fichier CSV."""
#     myfile = "uploaded_files/data.csv"
#     with rx.session() as session:
#         with open("myfile", newline="") as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 session.add(row)
#             session.commit()
#         return rx.toast.info(
#             "Datos cargados correctamente desde el archivo CSV",
#             position="bottom-right",
#         )

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


class State(rx.State):
    """The app state."""

    incidencias: list[Incidencia] = []
    incidencias_all: list[Incidencia] = []
    # variables para el ordenamiento de la tabla
    sort_value: str = ""
    sort_reverse: bool = False
    search_value: str = ""
    current_incidencia: Incidencia = Incidencia()
    # Values for current and previous month
    current_month_values: MonthValues = MonthValues()
    previous_month_values: MonthValues = MonthValues()
    incidencias_pendientes: list[Incidencia] = []   
    incidencias_bitrix: list[Incidencia] = []
    incidencias_solucionadas: list[Incidencia] = []
    # variables para la actualización de la página 
    last_updated: str = "Jamais"
    uploaded_files: list[str] = []
    # Pagination
    total_items: int
    offset: int = 0
    limit: int = 15

    # les fonctions pour la pagination
    @rx.var(cache=True)
    def page_number(self) -> int:
        """Calculate the current page number."""
        return (self.offset // self.limit) + 1 + (1 if self.offset % self.limit else 0)

    @rx.var(cache=True)
    def total_pages(self) -> int:
        """Calculate the total number of pages."""
        return self.total_items // self.limit + (1 if self.total_items % self.limit else 0)

    @rx.event
    def prev_page(self):
        """Go to the previous page."""
        self.offset = max(self.offset - self.limit, 0)
        self.load_entries()

    @rx.event
    def next_page(self):
        """Go to the next page."""
        if self.offset + self.limit < self.total_items:
            self.offset += self.limit
            self.load_entries()

    def _get_total_items(self, session):
        """Get the total number of items."""
        self.total_items = session.exec(select(func.count(Incidencia.id))).one()


    # Mise à jour automatique toutes les 5 minutes (300000 ms)
    def update_time(self):
        """Update the time."""
        self.load_entries()

    # Carga de datos
    @rx.event
    def load_entries(self) -> list[Incidencia]:
        """Get all incidencias from the database."""
         # get all items for pagination
        with rx.session() as session:
            query = select(Incidencia)
        self.incidencias_all= session.exec(query).all()
        self._get_total_items(session)


        """Get all incidencias from the database and paginate them"""
        with rx.session() as session:
            query = select(Incidencia)
            query = query.offset(self.offset).limit(self.limit)
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

            if self.sort_value:
                sort_column = getattr(Incidencia, self.sort_value)
                order = (
                    desc(func.lower(sort_column))
                    if self.sort_reverse
                    else asc(func.lower(sort_column))
                )
                query = query.order_by(order)
            self.incidencias = session.exec(query).all()
            self.get_current_month_values()
            self.get_previous_month_values()
        #print("Carga de datos completada")
        
    # Calcul des valeurs pour le mois en cours
    def get_current_month_values(self):
        """Calculate current month's values."""
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)

        current_month_incidencias = [
            incidencia_all
            for incidencia_all in self.incidencias_all
            if datetime.strptime(incidencia_all.date, "%Y-%m-%d %H:%M:%S") >= start_of_month
        ]
        num_incidencias = len(current_month_incidencias)
        num_solucionadas = len(
            [incidencia_all for incidencia_all in current_month_incidencias if incidencia_all.status == "Solucionada"]
        )
        num_pendientes = len(
            [incidencia_all for incidencia_all in current_month_incidencias if incidencia_all.status == "Pendiente"]
        )
        num_bitrix = len(
            [incidencia_all for incidencia_all in current_month_incidencias if incidencia_all.status == "Tarea Creada"]
        )
        self.current_month_values = MonthValues(
            num_incidencias=num_incidencias,
            num_solucionadas=num_solucionadas,
            num_pendientes=num_pendientes,
            num_bitrix=num_bitrix,
        )

    # Calcul des valeurs pour le mois précédent
    def get_previous_month_values(self):
        """Calculate previous month's values."""
        now = datetime.now()
        first_day_of_current_month = datetime(now.year, now.month, 1)
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        start_of_last_month = datetime(
            last_day_of_last_month.year, last_day_of_last_month.month, 1
        )

        previous_month_incidencias = [
            incidencia_all 
            for incidencia_all in self.incidencias_all
            if start_of_last_month
            <= datetime.strptime(incidencia_all.date, "%Y-%m-%d %H:%M:%S")
            <= last_day_of_last_month
        ]
        num_incidencias = len(previous_month_incidencias)
        num_solucionadas = len(
            [incidencia_all for incidencia_all in previous_month_incidencias if incidencia_all.status == "Solucionada"]
        )
        num_pendientes = len(
            [incidencia_all for incidencia_all in previous_month_incidencias if incidencia_all.status == "Pendiente"]
        )
        num_bitrix = len(
            [incidencia_all for incidencia_all in previous_month_incidencias if incidencia_all.status == "Tarea Creada"]
        )

        self.previous_month_values = MonthValues(
            num_incidencias=num_incidencias,
            num_solucionadas=num_solucionadas,
            num_pendientes=num_pendientes,
            num_bitrix=num_bitrix,
        )
    
    # Tri des valeurs
    def sort_values(self, sort_value: str):
        """Sort the values."""
        self.sort_value = sort_value
        self.load_entries()

    # Inversion du tri
    def toggle_sort(self):
        """Toggle the sort."""
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    # Filtrage des valeurs
    def filter_values(self, search_value):
        """Filter the values."""
        self.search_value = search_value
        self.load_entries()

    # Récupération de l'incidencia
    def get_incidencia(self, incidencia_all: Incidencia):
        """Get the incidencia."""
        self.current_incidencia = incidencia_all

    # Ajout de l'incidencia à la base de données
    def add_incidencia_to_db(self, form_data: dict):
        """Add the incidencia to the database."""
        with rx.session() as session:
            self.current_incidencia = Incidencia(
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), **form_data
            )
            session.add(self.current_incidencia)
            session.commit()
            session.refresh(self.current_incidencia)
        self.load_entries()
        return rx.toast.info(
            f"Incidencia pour {self.current_incidencia.name} a été ajoutée.", position="bottom-right"
        )

    # Mise à jour de l'incidencia
    def update_incidencia_to_db(self, form_data: dict):
        """Update the incidencia."""
        with rx.session() as session:
            incidencia_all = session.exec(
                select(Incidencia).where(Incidencia.id == self.current_incidencia.id)
            ).first()
            form_data.pop("id", None)
            incidencia_all.set(**form_data)
            session.add(incidencia_all)
            session.commit()
        self.load_entries()
        return rx.toast.info(
            f"Incidencia pour {self.current_incidencia.name} a été modifiée.",
            position="bottom-right",
        )

    # Suppression de l'incidencia
    def delete_incidencia(self, id: int):
        """Delete an incidencia from the database."""
        with rx.session() as session:
            incidencia_all = session.exec(select(Incidencia).where(Incidencia.id == id)).first()
            session.delete(incidencia_all)
            session.commit()
        self.load_entries()
        return rx.toast.info(
            f"Incidencia pour {incidencia_all.name} a été supprimée.", position="bottom-right"
        )

    # Calcul du pourcentage de changement
    @rx.var(cache=True)
    def incidencias_change(self) -> float:
        """Calculate the percentage change for the number of incidencias."""
        return _get_percentage_change(
            self.current_month_values.num_incidencias,
            self.previous_month_values.num_incidencias,
        )

    # Calcul du pourcentage de changement pour les incidencias solucionadas
    @rx.var(cache=True)
    def delivers_change(self) -> float:
        """Calculate the percentage change for the number of incidencias solucionadas."""
        return _get_percentage_change(
            self.current_month_values.num_solucionadas,
            self.previous_month_values.num_solucionadas,
        )
    
    # Calcul du pourcentage de changement pour les incidencias pendientes
    @rx.var(cache=True)
    def incidencias_pendientes_change(self) -> float:
        """Calculate the percentage change for the number of incidencias pendientes."""
        return _get_percentage_change(
            self.current_month_values.num_pendientes,
            self.previous_month_values.num_pendientes,
        ) 
    
    # Calcul du pourcentage de changement pour les incidencias bitrix
    @rx.var(cache=True)
    def incidencias_bitrix_change(self) -> float:
        """Calculate the percentage change for the number of incidencias bitrix."""
        return _get_percentage_change(
            self.current_month_values.num_bitrix,
            self.previous_month_values.num_bitrix,
        )
    
    # Conversion des données en format CSV
    def _convert_to_csv(self):
        """Convert user data to CSV format."""
        fieldnames = list(Incidencia.__fields__)
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for incidencia_all in self.incidencias_all:
            writer.writerow(incidencia_all.dict())
        return output.getvalue()
    
    # Conversion des données en format XML
    def _convert_to_xml(self):
        """Convert user data to XML format."""
        fieldnames = list(Incidencia.__fields__)
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for incidencia_all in self.incidencias_all:
            writer.writerow(incidencia_all.dict())
        return output.getvalue()
    
    # Téléchargement des données en format XML
    def download_xml_data(self):
        """Download the data in XML format."""
        xml_data = self._convert_to_xml()
        filename = datetime.now().strftime("%Y-%m-%d") + "_data.xml"
        return rx.download(
            data=xml_data,
            filename=filename,
        )
    

    # Téléchargement des données en format CSV
    def download_csv_data(self):
        """Download the data in CSV format."""
        csv_data = self._convert_to_csv()
        return rx.download(
            data=csv_data,
            filename="data.csv",
        )
    
    # Importation des données en format CSV
    def upload_csv_data(self, file: rx.UploadFile):
        """Upload the data in CSV format."""
        csv_data = file.read().decode("utf-8")
        reader = csv.DictReader(csv_data.splitlines())
        for row in reader:
            self.add_incidencia_to_db(row)
        self.load_entries()
        return rx.toast.info(
            "Datos cargados correctamente desde el archivo CSV",
            position="bottom-right",
        )
    