"""Manipulador de playlists do YouTube."""

import yt_dlp as youtube_dl
from typing import List, Optional

from ..models.download_result import VideoInfo
from ..utils.logger import logger


class PlaylistHandler:
    """Responsável por manipular playlists do YouTube."""
    
    def __init__(self):
        self.ydl_opts = {
            "quiet": True, 
            "extract_flat": True,
            "no_warnings": True
        }
    
    def is_playlist(self, url: str) -> bool:
        """
        Verifica se uma URL é uma playlist.
        
        Args:
            url: URL para verificar
            
        Returns:
            True se for uma playlist, False caso contrário
        """
        try:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                return info_dict.get("_type") == "playlist"
        except Exception as e:
            logger.warning(f"Não foi possível verificar se é playlist: {e}")
            return False
    
    def get_playlist_entries(self, playlist_url: str) -> List[str]:
        """
        Extrai todas as URLs de vídeos de uma playlist.
        
        Args:
            playlist_url: URL da playlist
            
        Returns:
            Lista de URLs de vídeos individuais
        """
        try:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)
                
                if playlist_info.get("_type") == "playlist":
                    entries = playlist_info.get("entries", [])
                    urls = []
                    
                    for entry in entries:
                        if entry and entry.get("id"):
                            video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                            urls.append(video_url)
                    
                    return urls
                else:
                    # Não é uma playlist, retorna apenas a URL original
                    return [playlist_url]
                    
        except Exception as e:
            logger.error(f"Erro ao extrair playlist: {e}")
            return [playlist_url]
    
    def get_playlist_info(self, playlist_url: str) -> Optional[dict]:
        """
        Obtém informações básicas de uma playlist.
        
        Args:
            playlist_url: URL da playlist
            
        Returns:
            Dicionário com informações da playlist ou None se falhar
        """
        try:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                return ydl.extract_info(playlist_url, download=False)
        except Exception as e:
            logger.error(f"Erro ao obter informações da playlist: {e}")
            return None
    
    def get_playlist_title(self, playlist_url: str) -> str:
        """
        Obtém o título de uma playlist.
        
        Args:
            playlist_url: URL da playlist
            
        Returns:
            Título da playlist ou string padrão se não conseguir obter
        """
        info = self.get_playlist_info(playlist_url)
        return info.get("title", "Playlist sem título") if info else "Playlist desconhecida"
    
    def get_playlist_video_count(self, playlist_url: str) -> int:
        """
        Obtém o número de vídeos em uma playlist.
        
        Args:
            playlist_url: URL da playlist
            
        Returns:
            Número de vídeos na playlist
        """
        entries = self.get_playlist_entries(playlist_url)
        return len(entries)
