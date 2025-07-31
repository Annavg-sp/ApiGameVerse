from sqlmodel import Session, select
from app.database.models.plataforma import Plataforma

# Lista todas las plataformas
def obtener_plataformas(session: Session):
    return session.exec(select(Plataforma)).all()

# Busca una plataforma por ID
def obtener_plataforma_por_id(plataforma_id: int, session: Session):
    return session.get(Plataforma, plataforma_id)

# Crea una nueva plataforma
def crear_plataforma(plataforma: Plataforma, session: Session):
    session.add(plataforma)
    session.commit()
    session.refresh(plataforma)
    return plataforma

# Actualiza una plataforma
def actualizar_plataforma(plataforma_id: int, datos: Plataforma, session: Session):
    plataforma = session.get(Plataforma, plataforma_id)
    if plataforma:
        plataforma.nombre = datos.nombre
        plataforma.fabricante = datos.fabricante
        session.commit()
        session.refresh(plataforma)
        return plataforma
    return None

# Elimina una plataforma
def borrar_plataforma(plataforma_id: int, session: Session):
    plataforma = session.get(Plataforma, plataforma_id)
    if plataforma:
        session.delete(plataforma)
        session.commit()
        return True
    return False
