from sqlmodel import Session
from app.database.database import engine
from app.database.models.plataforma import Plataforma
from app.database.models.videojuego import Videojuego

def seed_data():
    with Session(engine) as session:
        # Eliminar datos existentes para evitar duplicados
        session.query(Videojuego).delete()
        session.query(Plataforma).delete()
        session.commit()

        # Crear plataformas
        ps2 = Plataforma(nombre="PlayStation 2", fabricante="Sony")
        xbox360 = Plataforma(nombre="Xbox 360", fabricante="Microsoft")
        switch = Plataforma(nombre="Nintendo Switch", fabricante="Nintendo")
        pc = Plataforma(nombre="PC", fabricante="Variado")
        dreamcast = Plataforma(nombre="Dreamcast", fabricante="Sega")

        session.add_all([ps2, xbox360, switch, pc, dreamcast])
        session.commit()

        # Crear videojuegos (usando los IDs generados al hacer commit)
        juegos = [
            Videojuego(nombre="Final Fantasy X", genero="RPG", lanzamiento=2001, plataforma_id=ps2.id),
            Videojuego(nombre="Halo 3", genero="FPS", lanzamiento=2007, plataforma_id=xbox360.id),
            Videojuego(nombre="Zelda: Breath of the Wild", genero="Aventura", lanzamiento=2017, plataforma_id=switch.id),
            Videojuego(nombre="The Witcher 3", genero="RPG", lanzamiento=2015, plataforma_id=pc.id),
            Videojuego(nombre="Sonic Adventure", genero="Plataformas", lanzamiento=1998, plataforma_id=dreamcast.id)
        ]

        session.add_all(juegos)
        for juego in juegos:
            print(f"🎮 Añadido: {juego.nombre} ({juego.genero}, {juego.lanzamiento})")
        session.commit()
        print(" Base de datos inicializada con 5 plataformas y 5 videojuegos.")

if __name__ == "__main__":
    seed_data()