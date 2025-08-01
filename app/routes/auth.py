from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import secrets
import bcrypt
from typing import Optional
from sqlmodel import Session, select
from app.database.database import get_session
from app.database.models.apikey import API_Keys

security = HTTPBearer()
router = APIRouter(prefix="/auth", tags=["API Keys"])
roles = ["admin", "user", "test"]

class APIRequest(BaseModel):
    role: str

class APIResponse(APIRequest):
    api_key: str

# Generar y guardar una nueva API Key
async def generate_new_key(role: str, session: Session) -> str:
    raw_key = "S-API-" + secrets.token_urlsafe(32)
    salt = bcrypt.gensalt()
    hashed_key = bcrypt.hashpw(raw_key.encode(), salt).decode()

    nueva_clave = API_Keys(api_key=hashed_key, role=role)
    session.add(nueva_clave)
    session.commit()

    return raw_key

# Validar una API Key contra la base de datos
async def validate_api_key(raw_key: str, session: Session) -> Optional[str]:
    result = session.exec(select(API_Keys)).all()
    for item in result:
        if bcrypt.checkpw(raw_key.encode(), item.api_key.encode()):
            return item.role
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="API Key inválida")

# Extraer y validar la API Key desde el header Authorization
async def get_api_key_from_headers(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> Optional[str]:
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Falta el header Authorization")
    role = await validate_api_key(credentials.credentials, session)
    return role

# Crear una nueva API Key
@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=APIResponse)
async def create_new_key(request: APIRequest, session: Session = Depends(get_session)):
    if request.role not in roles:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Rol no válido")
    raw_key = await generate_new_key(request.role, session)
    return APIResponse(role=request.role, api_key=raw_key)

# Ver tu rol actual
@router.get("/me")
async def read_role(role: str = Depends(get_api_key_from_headers)):
    return { "message": f"Tu rol es '{role}'." }
