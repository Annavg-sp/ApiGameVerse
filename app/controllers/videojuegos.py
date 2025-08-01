from sqlmodel import Session, select  # Importo Session para gestionar las interacciones con la base de datos
from app.database.models.videojuego import Videojuego  # Importo el modelo de la tabla "Videojuego"
from fastapi import HTTPException  # Para lanzar excepciones de error HTTP cuando algo falla

# Función para obtener todos los videojuegos
def obtener_videojuegos(session: Session):
    # Ejecuta una consulta SELECT para obtener todos los videojuegos y los devuelve
    return session.exec(select(Videojuego)).all()

# Función para obtener un videojuego por su ID
def obtener_videojuego_por_id(videojuego_id: int, session: Session):
    # Busca un videojuego por su ID y lo devuelve
    return session.get(Videojuego, videojuego_id)

# Función para crear un nuevo videojuego (si no existe otro con el mismo nombre)
def crear_videojuego(videojuego: Videojuego, session: Session):
    # Verifico si ya existe un videojuego con el mismo nombre en la base de datos
    existente = session.exec(
        select(Videojuego).where(Videojuego.nombre == videojuego.nombre)
    ).first()

    # Si existe, lanzo un error con código 400
    if existente:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un videojuego con el nombre {videojuego.nombre}"
        )

    # Si no existe, añado el videojuego y lo guardo en la base de datos
    session.add(videojuego)
    session.commit()
    session.refresh(videojuego)  # Refresco el objeto para tener la versión actualizada
    return videojuego  # Devuelvo el videojuego creado

# Función para actualizar un videojuego por su ID
def actualizar_videojuego(videojuego_id: int, datos: Videojuego, session: Session):
    # Busco el videojuego por su ID
    existente = session.get(Videojuego, videojuego_id)
    if existente:
        # Si lo encuentro, actualizo sus atributos
        existente.nombre = datos.nombre
        existente.genero = datos.genero
        existente.plataforma_id = datos.plataforma_id
        session.commit()  # Confirmo los cambios en la base de datos
        session.refresh(existente)  # Refresco el objeto con los datos actualizados
        return {"mensaje": "Videojuego actualizado", "videojuego": existente}
    # Si no se encuentra, devuelvo None
    return None

# Función para eliminar un videojuego por su ID
def borrar_videojuego(videojuego_id: int, session: Session):
    # Busco el videojuego por su ID
    videojuego = session.get(Videojuego, videojuego_id)
    
    if videojuego:
        # Si el videojuego existe, lo elimino de la base de datos
        session.delete(videojuego)
        session.commit()  # Confirmo la eliminación
        # Devuelvo un mensaje con el nombre del videojuego eliminado y el objeto completo
        return {"mensaje": f"Videojuego '{videojuego.nombre}' eliminado con éxito", "videojuego": videojuego}
    
    # Si no se encuentra el videojuego, devuelvo un mensaje de error
    return {"mensaje": "Videojuego no encontrado", "videojuego": None}