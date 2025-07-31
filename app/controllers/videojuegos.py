from sqlmodel import Session, select
from app.database.models.videojuego import Videojuego
from fastapi import HTTPException

# Lista todos los videojuegos
def obtener_videojuegos(session: Session):
    return session.exec(select(Videojuego)).all()

# Obtiene un videojuego por su ID
def obtener_videojuego_por_id(videojuego_id: int, session: Session):
    return session.get(Videojuego, videojuego_id)

# Crea un nuevo videojuego si no existe otro con el mismo nombre
def crear_videojuego(videojuego: Videojuego, session: Session):
    existente = session.exec(
        select(Videojuego).where(Videojuego.nombre == videojuego.nombre)
    ).first()
    if existente:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un videojuego con el nombre {videojuego.nombre}"
        )

    session.add(videojuego)
    session.commit()
    session.refresh(videojuego)
    return videojuego  # ← devuelves solo el objeto


# Actualiza un videojuego por su ID
def actualizar_videojuego(videojuego_id: int, datos: Videojuego, session: Session):
    existente = session.get(Videojuego, videojuego_id)
    if existente:
        existente.nombre = datos.nombre
        existente.genero = datos.genero
        existente.plataforma_id = datos.plataforma_id
        session.commit()
        session.refresh(existente)
        return {"mensaje": "Videojuego actualizado", "videojuego": existente}
    return None

# Elimina un videojuego por su ID
def borrar_videojuego(videojuego_id: int, session: Session):
    videojuego = session.get(Videojuego, videojuego_id)
    if videojuego:
        session.delete(videojuego)
        session.commit()
        return True
    return False
