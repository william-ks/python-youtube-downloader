"""Serviço principal de download do YouTube."""

import concurrent.futures
import yt_dlp as youtube_dl
from typing import List, Optional, Tuple

from ..models.download_result import (
    DownloadResult, 
    DownloadStatus, 
    DownloadType, 
    BatchDownloadResult,
    VideoInfo
)
from ..config.settings import paths, settings
from ..utils.logger import logger
from ..utils.file_utils import FilenameUtils
from ..services.ffmpeg_manager import FFmpegManager


class YouTubeDownloader:
    """Serviço principal para downloads do YouTube."""
    
    def __init__(self, ffmpeg_manager: FFmpegManager):
        self.ffmpeg_manager = ffmpeg_manager
        self.filename_utils = FilenameUtils()
    
    def check_video_availability(self, url: str) -> Tuple[bool, Optional[VideoInfo]]:
        """
        Verifica se um vídeo está disponível para download.
        
        Args:
            url: URL do vídeo
            
        Returns:
            Tupla (disponível, informações_do_vídeo)
        """
        try:
            ydl_opts = {"quiet": True, "no_warnings": True}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                
                video_info = VideoInfo(
                    title=info_dict.get('title', 'Título desconhecido'),
                    url=url,
                    duration=info_dict.get('duration'),
                    thumbnail=info_dict.get('thumbnail')
                )
                
                return True, video_info
                
        except Exception as e:
            logger.error(f"Vídeo indisponível: {url} - {str(e)}")
            return False, None
    
    def _get_download_options(self, download_type: DownloadType) -> dict:
        """
        Obtém as opções de download baseadas no tipo.
        
        Args:
            download_type: Tipo de download (AUDIO ou VIDEO)
            
        Returns:
            Dicionário com opções do yt-dlp
        """
        base_options = {
            "ffmpeg_location": self.ffmpeg_manager.get_ffmpeg_path(),
            "outtmpl": f"{paths.DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "ignoreerrors": True,
            "extract_flat": False,
            "noplaylist": True
        }
        
        if download_type == DownloadType.AUDIO:
            base_options.update({
                "format": settings.DEFAULT_AUDIO_FORMAT,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": settings.DEFAULT_AUDIO_QUALITY,
                }]
            })
        else:  # VIDEO
            base_options.update({
                "format": settings.DEFAULT_VIDEO_FORMAT
            })
        
        return base_options
    
    def _check_existing_file(self, video_info: VideoInfo, download_type: DownloadType) -> Tuple[bool, Optional[str]]:
        """
        Verifica se já existe um arquivo com o mesmo título.
        
        Args:
            video_info: Informações do vídeo
            download_type: Tipo de download
            
        Returns:
            Tupla (existe, nome_do_arquivo)
        """
        if download_type == DownloadType.AUDIO:
            extensions = ['.mp3', '.m4a', '.webm', '.opus']
        else:
            extensions = ['.mp4', '.mkv', '.webm', '.avi']
        
        return self.filename_utils.check_file_exists_with_extensions(
            video_info.title, 
            extensions
        )
    
    def download_single(self, url: str, download_type: DownloadType) -> DownloadResult:
        """
        Baixa um único vídeo/áudio.
        
        Args:
            url: URL do vídeo
            download_type: Tipo de download
            
        Returns:
            Resultado do download
        """
        result = DownloadResult(
            url=url,
            status=DownloadStatus.PENDING,
            download_type=download_type
        )
        
        try:
            # Verifica disponibilidade
            is_available, video_info = self.check_video_availability(url)
            
            if not is_available:
                result.status = DownloadStatus.FAILED
                result.error_message = "Vídeo indisponível"
                return result
            
            result.title = video_info.title
            
            # Verifica se arquivo já existe
            file_exists, existing_file = self._check_existing_file(video_info, download_type)
            
            if file_exists:
                logger.warning(f"Arquivo já existe: {existing_file}")
                result.status = DownloadStatus.SKIPPED
                result.existing_file = existing_file
                return result
            
            # Realiza o download
            logger.info(f"Baixando: {video_info.title}")
            
            options = self._get_download_options(download_type)
            
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([url])
            
            result.status = DownloadStatus.SUCCESS
            logger.success(f"Download concluído: {video_info.title}")
            
        except Exception as e:
            result.status = DownloadStatus.FAILED
            result.error_message = str(e)
            logger.error(f"Erro no download: {str(e)}")
        
        return result
    
    def download_batch(self, urls: List[str], download_type: DownloadType) -> BatchDownloadResult:
        """
        Baixa múltiplos vídeos/áudios em paralelo.
        
        Args:
            urls: Lista de URLs
            download_type: Tipo de download
            
        Returns:
            Resultado do download em lote
        """
        logger.info(f"Iniciando downloads em paralelo de {len(urls)} itens...")
        logger.info(f"Máximo de {settings.MAX_PARALLEL_DOWNLOADS} downloads simultâneos.")
        
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=settings.MAX_PARALLEL_DOWNLOADS) as executor:
            # Submete todas as tarefas
            future_to_url = {
                executor.submit(self.download_single, url, download_type): url 
                for url in urls
            }
            
            # Processa resultados conforme completam
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result.is_success:
                        logger.success(f"Download concluído: {result.title}")
                    elif result.is_skipped:
                        logger.warning(f"Download pulado: {result.title}")
                    else:
                        logger.error(f"Download falhou: {result.url}")
                        
                except Exception as e:
                    url = future_to_url[future]
                    error_result = DownloadResult(
                        url=url,
                        status=DownloadStatus.FAILED,
                        download_type=download_type,
                        error_message=str(e)
                    )
                    results.append(error_result)
                    logger.error(f"Erro no processamento de {url}: {str(e)}")
        
        # Calcula estatísticas
        successful = sum(1 for r in results if r.is_success)
        failed = sum(1 for r in results if r.is_failed)
        skipped = sum(1 for r in results if r.is_skipped)
        
        batch_result = BatchDownloadResult(
            total_downloads=len(results),
            successful=successful,
            failed=failed,
            skipped=skipped,
            download_results=results
        )
        
        logger.info(f"Downloads finalizados. Sucesso: {successful}, Falhas: {failed}, Pulados: {skipped}")
        
        return batch_result
