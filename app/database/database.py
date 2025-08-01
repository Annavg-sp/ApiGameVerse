from sqlmodel import create_engine, Session  # Para crear el motor de base de datos y abrir sesiones

# Aquí defino la ruta de mi base de datos SQLite
DB_URL = "sqlite:///app/database/gameverse.db"  # Está dentro de la carpeta del proyecto

# Creo el motor que se va a encargar de conectar con SQLite
# echo=True me sirve para ver las consultas SQL que se hacen en consola (muy útil para depurar)
engine = create_engine(DB_URL, echo=True)

# Esta función devuelve una sesión de base de datos para usar dentro de las rutas o controladores
def get_session():
    with Session(engine) as session:
        yield session  # Se usa con Depends para inyectarla automáticamente donde se necesite
