import requests
from typing import Optional, Dict, List
import logging
import os
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

class TMDBClient:
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        if not self.api_key:
            raise ValueError("TMDB_API_KEY no está configurada en las variables de entorno")
        
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
        self.profile_base_url = "https://image.tmdb.org/t/p/w185"  # Tamaño más pequeño para fotos de perfil
        self.language = "es-ES"
        self.region = "ES"  # Región para las plataformas de streaming
        
    def search_movie(self, title: str) -> Optional[Dict]:
        """
        Busca una película en TMDB y devuelve su información básica.
        
        Args:
            title (str): Título de la película a buscar
            
        Returns:
            Optional[Dict]: Diccionario con la información de la película o None si hay error
        """
        try:
            logger.info(f"Buscando película: {title}")
            
            # Endpoint de búsqueda
            search_url = f"{self.base_url}/search/movie"
            params = {
                "api_key": self.api_key,
                "query": title,
                "language": self.language,
                "region": self.region
            }
            
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                logger.warning("No se encontraron resultados")
                return None
            
            # Tomamos la primera coincidencia
            movie = results[0]
            movie_id = movie.get("id")
            
            # Obtener detalles adicionales de la película
            details_url = f"{self.base_url}/movie/{movie_id}"
            details_params = {
                "api_key": self.api_key,
                "language": self.language,
                "region": self.region,
                "append_to_response": "watch/providers,translations,credits"
            }
            
            details_response = requests.get(details_url, params=details_params)
            details_response.raise_for_status()
            
            details = details_response.json()
            watch_providers = details.get("watch/providers", {}).get("results", {})
            
            # Obtener plataformas de streaming disponibles
            platforms = []
            if self.region in watch_providers:
                flatrate = watch_providers[self.region].get("flatrate", [])
                platforms = [provider.get("provider_name") for provider in flatrate]
            
            # Obtener traducción al español si está disponible
            translations = details.get("translations", {}).get("translations", [])
            spanish_translation = next(
                (t for t in translations if t.get("iso_639_1") == "es"),
                None
            )
            
            overview = None
            if spanish_translation:
                overview = spanish_translation.get("data", {}).get("overview")
            
            # Obtener los actores principales (cast)
            cast = details.get("credits", {}).get("cast", [])
            # Tomamos los primeros 5 actores
            main_cast = []
            for actor in cast[:5]:
                main_cast.append({
                    "name": actor.get("name"),
                    "character": actor.get("character"),
                    "profile_path": f"{self.profile_base_url}{actor.get('profile_path')}" if actor.get("profile_path") else None
                })
            
            return {
                "title": movie.get("title"),
                "original_title": movie.get("original_title"),
                "overview": overview or movie.get("overview"),
                "release_date": movie.get("release_date"),
                "poster_path": f"{self.image_base_url}{movie.get('poster_path')}" if movie.get("poster_path") else None,
                "platforms": platforms,
                "cast": main_cast
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en la petición a TMDB: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return None 