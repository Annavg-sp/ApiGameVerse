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
from app.routes.auth import get_api_key_from_headers  # Importamos la función para obtener y validar la API Key

# Crear el router para las rutas de videojuegos
router = APIRouter(tags=["Videojuegos"])

# Listar videojuegos con filtro opcional por género (acceso libre)
@router.get("/", response_model=list[VideojuegoResponse])
async def listar_videojuegos(
    genero: str = None,
    session: Session = Depends(get_session)
):
    videojuegos = obtener_videojuegos(session)
    if genero:
        videojuegos = [v for v in videojuegos if v.genero.lower() == genero.lower()]
    return videojuegos

# Obtener detalles de un videojuego por ID (acceso libre)
@router.get("/{id}", response_model=VideojuegoResponse)
async def obtener_videojuego_ruta(
    id: int,
    session: Session = Depends(get_session)
):
    videojuego = obtener_videojuego_por_id(id, session)
    if not videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return videojuego

# Crear un nuevo videojuego (solo admin, requiere autenticación Bearer)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=VideojuegoResponse)
async def crear_videojuego_ruta(
    datos: VideojuegoCreate,
    session: Session = Depends(get_session),
    role: str = Depends(get_api_key_from_headers)  # Verificación de la API Key
):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden crear videojuegos")

    videojuego = Videojuego(**datos.dict())
    creado = crear_videojuego(videojuego, session)
    return creado  # Asegúrate de devolver el objeto correctamente

# Actualizar un videojuego por ID (solo admin, requiere autenticación Bearer)
@router.put("/{id}", response_model=VideojuegoResponse)
async def actualizar_videojuego_ruta(
    id: int,
    datos: VideojuegoCreate,
    session: Session = Depends(get_session),
    role: str = Depends(get_api_key_from_headers)  # Verificación de la API Key
):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden actualizar videojuegos")

    actualizado = actualizar_videojuego(id, Videojuego(**datos.dict()), session)
    if not actualizado:
        raise HTTPException(status_code=404, detail="No se pudo actualizar el videojuego")
    return actualizado

# Eliminar un videojuego por ID (solo admin, requiere autenticación Bearer)
@router.delete("/{id}")
async def eliminar_videojuego_ruta(
    id: int,
    session: Session = Depends(get_session),
    role: str = Depends(get_api_key_from_headers)  # Verificación de la API Key
):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden eliminar videojuegos")

    eliminado = borrar_videojuego(id, session)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado para eliminar")
    return {"mensaje": "Videojuego eliminado con éxito"}
