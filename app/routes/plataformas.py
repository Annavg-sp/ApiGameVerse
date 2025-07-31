from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_session
from app.database.models.plataforma import Plataforma, PlataformaCreate, PlataformaResponse
from app.controllers.plataformas import (
    obtener_plataformas,
    obtener_plataforma_por_id,
    crear_plataforma,
    actualizar_plataforma,
    borrar_plataforma
)

router = APIRouter()

# Listar todas las plataformas disponibles
@router.get("/", response_model=list[PlataformaResponse])
async def listar_plataformas(session: Session = Depends(get_session)):
    return obtener_plataformas(session)

# Obtener detalles de una plataforma específica por ID
@router.get("/{id}", response_model=PlataformaResponse)
async def obtener_plataforma_ruta(id: int, session: Session = Depends(get_session)):
    plataforma = obtener_plataforma_por_id(id, session)
    if not plataforma:
        raise HTTPException(status_code=404, detail="Plataforma no encontrada")
    return plataforma

# Crear una nueva plataforma en la base de datos
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_plataforma_ruta(datos: PlataformaCreate, session: Session = Depends(get_session)):
    plataforma = Plataforma(**datos.dict())
    creada = crear_plataforma(plataforma, session)
    return {
        "mensaje": f"¡Plataforma '{creada.nombre}' creada exitosamente!",
        "plataforma": creada
    }

# Actualizar los datos de una plataforma por ID
@router.put("/{id}", response_model=PlataformaResponse)
async def actualizar_plataforma_ruta(id: int, datos: PlataformaCreate, session: Session = Depends(get_session)):
    actualizada = actualizar_plataforma(id, Plataforma(**datos.dict()), session)
    if not actualizada:
        raise HTTPException(status_code=404, detail="No se pudo actualizar la plataforma")
    return actualizada

# Eliminar una plataforma por ID
@router.delete("/{id}")
async def eliminar_plataforma_ruta(id: int, session: Session = Depends(get_session)):
    eliminada = borrar_plataforma(id, session)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Plataforma no encontrada para eliminar")
    return {"mensaje": "Plataforma eliminada con éxito"}
