from fastapi import APIRouter, Query
from app.services.availability import get_movie_availability

router = APIRouter()

@router.get("/availability")
async def availability(title: str = Query(..., description="Título de la película")):
    """
    Devuelve en qué plataformas de streaming está disponible una película.
    """
    result = await get_movie_availability(title)
    return result