from justwatch import JustWatch
from typing import Optional, Dict, List
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JustWatchClient:
    def __init__(self, country="us"):
        self.client = JustWatch(country=country)
        logger.info(f"JustWatchClient inicializado con país: {country}")

    def search_movie(self, title: str) -> Optional[Dict]:
        """
        Busca la película y devuelve las plataformas donde está disponible.
        
        Args:
            title (str): Título de la película a buscar
            
        Returns:
            Optional[Dict]: Diccionario con el título y plataformas, o None si hay error
        """
        try:
            logger.info(f"Buscando película: {title}")
            results = self.client.search_for_item(query=title)
            
            if not results:
                logger.warning("No se recibieron resultados de la API")
                return None
                
            if "items" not in results:
                logger.warning("No se encontró la clave 'items' en la respuesta")
                return None
                
            # Filtrar resultados tipo película
            movies = [item for item in results.get("items", []) if item.get("object_type") == "movie"]
            logger.info(f"Películas encontradas: {len(movies)}")
            
            if not movies:
                logger.warning("No se encontraron películas en los resultados")
                return None
            
            # Tomamos la primera coincidencia
            movie = movies[0]
            logger.info(f"Película seleccionada: {movie.get('title')}")
            
            # Extraer plataformas de offers
            platforms: List[str] = []
            offers = movie.get("offers", [])
            logger.info(f"Ofertas encontradas: {len(offers)}")
            
            for offer in offers:
                provider = offer.get("provider_id")
                if provider:
                    try:
                        provider_info = self.client.get_providers([provider])
                        if provider_info and len(provider_info) > 0:
                            platform_name = provider_info[0].get("clear_name", "Unknown")
                            platforms.append(platform_name)
                            logger.info(f"Plataforma encontrada: {platform_name}")
                    except Exception as e:
                        logger.error(f"Error al obtener información del proveedor {provider}: {str(e)}")
                        continue
            
            # Eliminar duplicados
            platforms = list(set(platforms))
            logger.info(f"Plataformas finales: {platforms}")
            
            return {
                "title": movie.get("title", title),
                "platforms": platforms
            }
            
        except Exception as e:
            logger.error(f"Error al buscar la película: {str(e)}")
            return None