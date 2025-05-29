# API de Disponibilidad de Películas

API que permite consultar en qué plataformas de streaming están disponibles las películas, junto con información detallada y el reparto principal.

## Características

- Búsqueda de películas
- Información detallada en español
- Plataformas de streaming disponibles
- Reparto principal con fotos
- Póster de la película

## Despliegue en Render.com

1. Crea una cuenta en [Render.com](https://render.com)

2. Crea un nuevo repositorio en GitHub y sube tu código:
```bash
git init
git add .
git commit -m "Primer commit"
git branch -M main
git remote add origin <URL_DE_TU_REPOSITORIO>
git push -u origin main
```

3. En Render.com:
   - Haz clic en "New +"
   - Selecciona "Web Service"
   - Conecta tu repositorio de GitHub
   - Configura el servicio:
     - Name: movie-api (o el nombre que prefieras)
     - Environment: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - En la sección "Environment Variables":
     - Añade `TMDB_API_KEY` con tu API key de TMDB

4. Haz clic en "Create Web Service"

## Variables de Entorno

- `TMDB_API_KEY`: Tu API key de TMDB (obtenida de https://www.themoviedb.org/settings/api)

## Uso de la API

### Endpoints

- `GET /availability?title=<título>`: Busca una película y devuelve su información

### Ejemplo de respuesta a la siguiente url

https://movie-api-xfxx.onrender.com/availability?title=Inception

```json
{
    "title": "Inception",
    "original_title": "Inception",
    "platforms": ["Netflix", "HBO Max"],
    "overview": "Dom Cobb es un ladrón hábil...",
    "poster": "https://image.tmdb.org/t/p/w500/...",
    "release_date": "2010-07-16",
    "cast": [
        {
            "name": "Leonardo DiCaprio",
            "character": "Dom Cobb",
            "profile_path": "https://image.tmdb.org/t/p/w185/..."
        }
    ]
}
```

## Desarrollo Local

1. Clona el repositorio
2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Crea un archivo `.env` con tu API key:
```
TMDB_API_KEY=tu_api_key_aqui
```

5. Inicia el servidor:
```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`
