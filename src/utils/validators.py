"""Validadores para URLs e entradas do usuário."""

import re
from typing import List


class URLValidator:
    """Validador de URLs do YouTube."""
    
    YOUTUBE_PATTERNS = [
        r'youtube\.com/watch',
        r'youtube\.com/playlist',
        r'youtu\.be/',
        r'youtube\.com/embed'
    ]
    
    @classmethod
    def is_valid_youtube_url(cls, url: str) -> bool:
        """
        Valida se a URL é uma URL válida do YouTube.
        
        Args:
            url: URL para validar
            
        Returns:
            True se a URL for válida, False caso contrário
        """
        if not url or not isinstance(url, str):
            return False
            
        url = url.strip()
        return any(re.search(pattern, url) for pattern in cls.YOUTUBE_PATTERNS)
    
    @classmethod
    def is_playlist_url(cls, url: str) -> bool:
        """
        Verifica se a URL contém parâmetros de playlist.
        
        Args:
            url: URL para verificar
            
        Returns:
            True se contém parâmetro de playlist, False caso contrário
        """
        return bool(re.search(r"[?&]list=", url))
    
    @classmethod
    def validate_url_list(cls, urls: List[str]) -> List[str]:
        """
        Valida uma lista de URLs e retorna apenas as válidas.
        
        Args:
            urls: Lista de URLs para validar
            
        Returns:
            Lista de URLs válidas
        """
        return [url for url in urls if cls.is_valid_youtube_url(url)]


class InputValidator:
    """Validador para entradas do usuário."""
    
    @staticmethod
    def is_valid_choice(choice: str, valid_choices: List[str]) -> bool:
        """
        Valida se a escolha do usuário está entre as opções válidas.
        
        Args:
            choice: Escolha do usuário
            valid_choices: Lista de escolhas válidas
            
        Returns:
            True se a escolha for válida, False caso contrário
        """
        return choice.strip() in valid_choices
    
    @staticmethod
    def is_empty_string(value: str) -> bool:
        """
        Verifica se a string está vazia ou contém apenas espaços.
        
        Args:
            value: String para verificar
            
        Returns:
            True se estiver vazia, False caso contrário
        """
        return not value or not value.strip()
