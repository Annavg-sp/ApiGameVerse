from sqlmodel import SQLModel, Field  # SQLModel para definir la estructura de la tabla

# Modelo que representa la tabla de claves API en la base de datos
class API_Keys(SQLModel, table=True):  # table=True indica que esta clase es una tabla en la base de datos
    id: int | None = Field(default=None, primary_key=True)  # ID autoincremental y clave primaria
    api_key: str  # Clave API, se almacena en texto plano (aunque se encriptará en el proceso)
    role: str  # Rol asociado a la clave API (admin, user, etc.)
