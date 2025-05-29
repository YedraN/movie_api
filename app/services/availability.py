from app.utils.tmdb_client import TMDBClient
import logging

logger = logging.getLogger(__name__)
tmdb_client = TMDBClient()

async def get_movie_availability(title: str) -> dict:
    try:
        logger.info(f"Buscando disponibilidad para: {title}")
        data = tmdb_client.search_movie(title)
        
        if data:
            logger.info(f"Resultados encontrados para {title}: {data}")
            return {
                "title": data["title"],
                "original_title": data["original_title"],
                "platforms": data["platforms"],
                "overview": data["overview"],
                "poster": data["poster_path"],
                "release_date": data["release_date"],
                "cast": data["cast"]
            }
        else:
            logger.warning(f"No se encontraron resultados para {title}")
            return {
                "title": title,
                "platforms": [],
                "message": "No se encontró la película o no está disponible en plataformas conocidas."
            }
    except Exception as e:
        logger.error(f"Error al buscar disponibilidad para {title}: {str(e)}")
        return {
            "title": title,
            "platforms": [],
            "message": f"Error al buscar la película: {str(e)}"
        }