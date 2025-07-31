from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel

# Tabla para plataformas en la BD
class Plataforma(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    fabricante: str

# Modelo para creación de plataformas
class PlataformaCreate(BaseModel):
    nombre: str
    fabricante: str

# Modelo para respuestas
class PlataformaResponse(BaseModel):
    id: int
    nombre: str
    fabricante: str

    class Config:
        orm_mode = True