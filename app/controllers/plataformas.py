from sqlmodel import Session, select  # Importo las herramientas necesarias para interactuar con la base de datos
from app.database.models.plataforma import Plataforma  # Importo el modelo de la tabla "Plataforma"

# Función para listar todas las plataformas
def obtener_plataformas(session: Session):
    # Utilizo una consulta SELECT para obtener todas las plataformas de la tabla
    return session.exec(select(Plataforma)).all()

# Función para obtener una plataforma por su ID
def obtener_plataforma_por_id(plataforma_id: int, session: Session):
    # Busco la plataforma utilizando el método 'get' que busca por el ID
    return session.get(Plataforma, plataforma_id)

# Función para crear una nueva plataforma
def crear_plataforma(plataforma: Plataforma, session: Session):
    # Añado la nueva plataforma a la sesión
    session.add(plataforma)
    # Confirmo los cambios en la base de datos
    session.commit()
    # Refresco el objeto para obtener los cambios de la base de datos (como el ID autoincrementado)
    session.refresh(plataforma)
    return plataforma

# Función para actualizar una plataforma existente
def actualizar_plataforma(plataforma_id: int, datos: Plataforma, session: Session):
    # Busco la plataforma por su ID
    plataforma = session.get(Plataforma, plataforma_id)
    if plataforma:
        # Si la plataforma existe, actualizo sus datos
        plataforma.nombre = datos.nombre
        plataforma.fabricante = datos.fabricante
        session.commit()  # Guardamos los cambios
        session.refresh(plataforma)  # Refrescamos para tener la versión más actualizada
        return plataforma
    # Si no se encuentra la plataforma, devuelvo None
    return None

# Función para borrar una plataforma
def borrar_plataforma(plataforma_id: int, session: Session):
    # Busco la plataforma por su ID
    plataforma = session.get(Plataforma, plataforma_id)
    if plataforma:
        # Si la plataforma existe, la elimino de la base de datos
        session.delete(plataforma)
        session.commit()  # Confirmo la eliminación
        return True
    # Si no se encuentra la plataforma, devuelvo False
    return False
