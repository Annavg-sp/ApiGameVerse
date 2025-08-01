GameVerse.API
¡Hola! Bienvenido a GameVerse.API 🎮

Este es un proyecto que creé para gestionar videojuegos y plataformas. Aquí puedes añadir, consultar, actualizar y eliminar videojuegos y plataformas de forma muy sencilla. Si eres fan de los videojuegos, ¡este es tu lugar! Además, para tener más control sobre quién puede hacer cambios en los videojuegos, he agregado un sistema de API Keys.

¿Qué puedes hacer con GameVerse.API?
Con esta API puedes:

Ver todos los videojuegos y plataformas.

Añadir nuevos videojuegos o plataformas.

Cambiar la información de un videojuego o plataforma.

Borrar videojuegos y plataformas.

Buscar videojuegos por género.

¿Cómo usarlo?
Si quieres probar GameVerse.API en tu propia máquina, sigue estos pasos:

1. Clona el repositorio:
Primero, necesitas tener el código en tu computadora:
git clone https://github.com/Annavg-sp/ApiGameVerse.git

2. Instala las dependencias:
Asegúrate de tener un entorno virtual activo (si no sabes cómo, pregunta) y luego instala todas las librerías necesarias:
pip install -r requirements.txt
pip install -r dev-requirements.txt

3. Corre la aplicación:
Para ejecutar el proyecto, solo tienes que usar este comando:
fastapi dev app/main.py
Esto arrancará la API y podrás acceder a ella en http://127.0.0.1:8000. Si tienes dudas, puedes probar la API directamente en Swagger UI que te proporciona FastAPI en http://127.0.0.1:8000/docs.

Rutas de la API
Aquí te dejo una pequeña guía para que sepas qué rutas puedes usar:

Videojuegos
Listar todos los videojuegos
GET /videojuegos

Obtener un videojuego por ID
GET /videojuegos/{id}

Crear un videojuego nuevo
POST /videojuegos
Envía un JSON con los detalles del videojuego (nombre, género, plataforma, etc.).

Actualizar un videojuego
PUT /videojuegos/{id}
Modifica cualquier información de un videojuego.

Eliminar un videojuego
DELETE /videojuegos/{id}
Borra un videojuego que ya no te interese.

Filtrar videojuegos por género
GET /videojuegos?genero=Acción
Solo muestra los juegos que son del género que pongas en el parámetro.

Plataformas
Listar todas las plataformas
GET /plataformas

Obtener una plataforma por ID
GET /plataformas/{id}

Crear una nueva plataforma
POST /plataformas
Solo tienes que enviar un JSON con el nombre y fabricante de la plataforma.

Actualizar una plataforma
PUT /plataformas/{id}
Actualiza la información de cualquier plataforma.

Eliminar una plataforma
DELETE /plataformas/{id}
Si ya no usas una plataforma, puedes borrarla.

Autenticación con API Keys
Si quieres hacer cambios en los videojuegos, necesitas una API Key. Para eso, tienes esta ruta:

Crear una nueva API Key
POST /auth/new
Solo tienes que decir qué rol quieres (por ejemplo, admin) y recibirás tu clave para poder autenticarte.

Una vez que tengas tu API Key, puedes incluirla en las solicitudes que necesiten autenticación.

¿Qué tecnologías utilicé?
Este proyecto está hecho con:

FastAPI: Un framework super rápido y fácil para crear APIs.

SQLite: Una base de datos pequeña pero efectiva.

SQLModel: Para interactuar con la base de datos sin complicaciones.

Pydantic: Para asegurarme de que los datos enviados y recibidos sean correctos