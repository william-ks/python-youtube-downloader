"""Gerenciador do FFmpeg."""

import os
import requests
import zipfile
from typing import Optional

from ..config.settings import paths, urls, settings
from ..utils.logger import logger
from ..utils.file_utils import FileManager


class FFmpegManager:
    """Gerenciador responsável pelo setup do FFmpeg."""
    
    def __init__(self):
        self.ffmpeg_dir = paths.FFMPEG_DIR
        self.ffmpeg_path = paths.FFMPEG_PATH
        self.download_url = urls.FFMPEG_DOWNLOAD_URL
        self.file_manager = FileManager()
    
    def is_ffmpeg_available(self) -> bool:
        """
        Verifica se o FFmpeg está disponível.
        
        Returns:
            True se o FFmpeg estiver disponível, False caso contrário
        """
        return self.file_manager.file_exists(self.ffmpeg_path)
    
    def setup_ffmpeg(self) -> bool:
        """
        Faz o setup do FFmpeg se necessário.
        
        Returns:
            True se o setup foi bem-sucedido, False caso contrário
        """
        if self.is_ffmpeg_available():
            logger.success("FFmpeg já existe, pulando download.")
            return True
        
        logger.info("Configurando FFmpeg...")
        
        try:
            self._create_ffmpeg_directory()
            zip_path = self._download_ffmpeg()
            self._extract_ffmpeg(zip_path)
            self._cleanup_zip_file(zip_path)
            
            logger.success("FFmpeg configurado com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao configurar FFmpeg: {e}")
            return False
    
    def _create_ffmpeg_directory(self) -> None:
        """Cria o diretório do FFmpeg se não existir."""
        logger.info("Criando diretório do FFmpeg...")
        self.file_manager.create_directory_if_not_exists(self.ffmpeg_dir)
    
    def _download_ffmpeg(self) -> str:
        """
        Baixa o arquivo ZIP do FFmpeg.
        
        Returns:
            Caminho para o arquivo ZIP baixado
            
        Raises:
            Exception: Se o download falhar
        """
        zip_path = os.path.join(self.ffmpeg_dir, "ffmpeg.zip")
        
        logger.info("Baixando a última versão do FFmpeg...")
        
        response = requests.get(
            self.download_url, 
            timeout=settings.REQUEST_TIMEOUT
        )
        response.raise_for_status()
        
        with open(zip_path, "wb") as file:
            file.write(response.content)
        
        return zip_path
    
    def _extract_ffmpeg(self, zip_path: str) -> None:
        """
        Extrai o executável do FFmpeg do arquivo ZIP.
        
        Args:
            zip_path: Caminho para o arquivo ZIP
            
        Raises:
            Exception: Se a extração falhar
        """
        logger.info("Extraindo FFmpeg...")
        
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for file in zip_ref.namelist():
                if "bin/ffmpeg.exe" in file:
                    zip_ref.extract(file, self.ffmpeg_dir)
                    extracted_path = os.path.join(self.ffmpeg_dir, file)
                    os.rename(extracted_path, self.ffmpeg_path)
                    break
            else:
                raise Exception("FFmpeg executável não encontrado no arquivo ZIP")
    
    def _cleanup_zip_file(self, zip_path: str) -> None:
        """
        Remove o arquivo ZIP após a extração.
        
        Args:
            zip_path: Caminho para o arquivo ZIP
        """
        try:
            os.remove(zip_path)
        except OSError:
            logger.warning("Não foi possível remover o arquivo ZIP temporário")
    
    def get_ffmpeg_path(self) -> Optional[str]:
        """
        Retorna o caminho do FFmpeg se estiver disponível.
        
        Returns:
            Caminho do FFmpeg ou None se não estiver disponível
        """
        return self.ffmpeg_path if self.is_ffmpeg_available() else None
