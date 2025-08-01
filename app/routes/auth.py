from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import secrets
import bcrypt
from typing import Optional
from sqlmodel import Session, select
from app.database.database import get_session
from app.database.models.apikey import API_Keys

# Configuramos el esquema de seguridad tipo Bearer para usar en endpoints protegidos
security = HTTPBearer()

# Defino el router para autenticación y manejo de API Keys
router = APIRouter(prefix="/auth", tags=["API Keys"])

# Lista de roles válidos
roles = ["admin", "user", "test"]

# Esquema de entrada para crear una API Key
class APIRequest(BaseModel):
    role: str

# Esquema de respuesta al crear una API Key
class APIResponse(APIRequest):
    api_key: str

# Función que genera una nueva API Key, la encripta con bcrypt y la guarda
async def generate_new_key(role: str, session: Session) -> str:
    try:
        raw_key = "S-API-" + secrets.token_urlsafe(32)
        salt = bcrypt.gensalt()
        hashed_key = bcrypt.hashpw(raw_key.encode(), salt).decode()

        nueva_clave = API_Keys(api_key=hashed_key, role=role)
        session.add(nueva_clave)
        session.commit()

        return raw_key  # Devuelvo la clave sin encriptar al cliente (solo se muestra una vez)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al generar la API Key.")

# Función que compara una clave enviada por el cliente con las claves guardadas
async def validate_api_key(raw_key: str, session: Session) -> Optional[str]:
    item = session.exec(select(API_Keys).where(API_Keys.api_key == raw_key)).first()
    if item and bcrypt.checkpw(raw_key.encode(), item.api_key.encode()):
        return item.role  # Devuelvo el rol si la clave es válida
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="API Key inválida")

# Esta función se usa como dependencia: extrae y valida la API Key del header Authorization
async def get_api_key_from_headers(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> Optional[str]:
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Falta el header Authorization")
    role = await validate_api_key(credentials.credentials, session)
    return role  # Devuelvo el rol para usarlo en rutas protegidas

# Endpoint para generar una nueva API Key (solo pasa si el rol es válido)
@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=APIResponse)
async def create_new_key(request: APIRequest, session: Session = Depends(get_session)):
    if request.role not in roles:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Rol no válido")

    # Generar la nueva clave API
    raw_key = await generate_new_key(request.role, session)

    # Devuelves el 'role' y la 'api_key' como se requiere en APIResponse
    return APIResponse(role=request.role, api_key=raw_key)
