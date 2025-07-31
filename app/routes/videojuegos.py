from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_session
from app.database.models.videojuego import Videojuego, VideojuegoCreate, VideojuegoResponse
from app.controllers.videojuegos import (
    obtener_videojuegos,
    obtener_videojuego_por_id,
    crear_videojuego,
    actualizar_videojuego,
    borrar_videojuego
)

router = APIRouter()

# 🎮 Listar videojuegos con filtro opcional por género
@router.get("/", response_model=list[VideojuegoResponse])
async def listar_videojuegos(genero: str = None, session: Session = Depends(get_session)):
    videojuegos = obtener_videojuegos(session)

    if genero:
        videojuegos = [v for v in videojuegos if v.genero.lower() == genero.lower()]

    return videojuegos

# Obtener detalles de un videojuego por ID
@router.get("/{id}", response_model=VideojuegoResponse)
async def obtener_videojuego_ruta(id: int, session: Session = Depends(get_session)):
    videojuego = obtener_videojuego_por_id(id, session)
    if not videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return videojuego

# Crear un nuevo videojuego
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_videojuego_ruta(datos: VideojuegoCreate, session: Session = Depends(get_session)):
    videojuego = Videojuego(**datos.dict())
    creado = crear_videojuego(videojuego, session)
    return {
        "mensaje": f"🎮 ¡Videojuego '{creado.nombre}' creado exitosamente!",
        "videojuego": creado
    }

# Actualizar un videojuego por ID
@router.put("/{id}", response_model=VideojuegoResponse)
async def actualizar_videojuego_ruta(id: int, datos: VideojuegoCreate, session: Session = Depends(get_session)):
    actualizado = actualizar_videojuego(id, Videojuego(**datos.dict()), session)
    if not actualizado:
        raise HTTPException(status_code=404, detail="No se pudo actualizar el videojuego")
    return actualizado

# Eliminar un videojuego por ID
@router.delete("/{id}")
async def eliminar_videojuego_ruta(id: int, session: Session = Depends(get_session)):
    eliminado = borrar_videojuego(id, session)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado para eliminar")
    return {"mensaje": "Videojuego eliminado con éxito"}
