import reflex as rx
from sqlmodel import select
from ..backend.backend import Incidencia

def verify_db():
    """Verify the database structure."""
    with rx.session() as session:
        try:
            result = session.exec(select(Incidencia)).all()
            print(f"Base de données vérifiée : {len(result)} incidences trouvées")
            
            if result:
                print("\nPremière incidence :")
                inc = result[0]
                print(f"Nom : {inc.name}")
                print(f"Téléphone : {inc.phone}")
                print(f"Adresse : {inc.address}")
                print(f"Motif : {inc.motivo}")
                print(f"Utilisateur : {inc.usuario}")
                print(f"Date : {inc.date}")
                print(f"Statut : {inc.status}")
                print(f"Bitrix : {inc.bitrix}")
                
        except Exception as e:
            print(f"Erreur lors de la vérification : {e}")

if __name__ == "__main__":
    verify_db()