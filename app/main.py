from fastapi import FastAPI
from app.api import routes

app = FastAPI(
    title="Movie Availability API",
    description="Consulta en qué plataformas de streaming están disponibles las películas.",
    version="0.1.0"
)

# Incluir las rutas desde app/api/routes.py
app.include_router(routes.router)