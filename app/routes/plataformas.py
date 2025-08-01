# Importo FastAPI y herramientas necesarias para manejar rutas y errores
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  # Para trabajar con la base de datos
from app.database.database import get_session  # Función que me da la sesión activa de la DB

# Importo los modelos de plataforma (entrada, salida y base)
from app.database.models.plataforma import Plataforma, PlataformaCreate, PlataformaResponse

# Importo las funciones que controlan la lógica (controladores)
from app.controllers.plataformas import (
    obtener_plataformas,
    obtener_plataforma_por_id,
    crear_plataforma,
    actualizar_plataforma,
    borrar_plataforma
)

# Creo el router para las rutas relacionadas con plataformas
router = APIRouter()

# Ruta para listar todas las plataformas
@router.get("/", response_model=list[PlataformaResponse])  # devuelvo una lista con el esquema de respuesta
async def listar_plataformas(session: Session = Depends(get_session)):
    return obtener_plataformas(session)

# Ruta para obtener una plataforma por su ID
@router.get("/{id}", response_model=PlataformaResponse)
async def obtener_plataforma_ruta(id: int, session: Session = Depends(get_session)):
    plataforma = obtener_plataforma_por_id(id, session)
    if not plataforma:
        # Si no se encuentra, devuelvo error 404
        raise HTTPException(status_code=404, detail="Plataforma no encontrada")
    return plataforma

# Ruta para crear una nueva plataforma
@router.post("/", status_code=status.HTTP_201_CREATED)  # Devuelve 201 si se crea correctamente
async def crear_plataforma_ruta(datos: PlataformaCreate, session: Session = Depends(get_session)):
    # Creo una instancia de Plataforma a partir del modelo de entrada
    plataforma = Plataforma(**datos.dict())
    creada = crear_plataforma(plataforma, session)
    return {
        "mensaje": f"¡Plataforma '{creada.nombre}' creada exitosamente!",
        "plataforma": creada
    }

# Ruta para actualizar una plataforma por ID
@router.put("/{id}", response_model=PlataformaResponse)
async def actualizar_plataforma_ruta(id: int, datos: PlataformaCreate, session: Session = Depends(get_session)):
    actualizada = actualizar_plataforma(id, Plataforma(**datos.dict()), session)
    if not actualizada:
        raise HTTPException(status_code=404, detail="No se pudo actualizar la plataforma")
    return actualizada

# Ruta para eliminar una plataforma por ID
@router.delete("/{id}")
async def eliminar_plataforma_ruta(id: int, session: Session = Depends(get_session)):
    eliminada = borrar_plataforma(id, session)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Plataforma no encontrada para eliminar")
    return {"mensaje": "Plataforma eliminada con éxito"}
