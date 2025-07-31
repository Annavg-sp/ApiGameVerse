from sqlmodel import create_engine, Session  # Para crear el motor y gestionar sesiones

DB_URL = "sqlite:///app/database/gameverse.db"  # Ruta de la base de datos SQLite

engine = create_engine(DB_URL, echo=True)  # Motor con log de operaciones SQL (echo=True)

# Función que genera una sesión para usar en las rutas
def get_session():
    with Session(engine) as session:
        yield session  # Se usa con Depends para inyección automática
