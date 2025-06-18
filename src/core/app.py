"""Aplicação principal do YouTube Downloader."""

import os
from typing import List

from ..models.download_result import DownloadType, BatchDownloadResult
from ..services.ffmpeg_manager import FFmpegManager
from ..services.youtube_downloader import YouTubeDownloader
from ..services.playlist_handler import PlaylistHandler
from ..ui.input_handler import InputHandler
from ..ui.menu import MenuDisplay, MenuController
from ..utils.validators import URLValidator
from ..utils.file_utils import FileManager, ReportGenerator
from ..utils.logger import logger
from ..config.settings import paths


class YouTubeDownloaderApp:
    """Aplicação principal do YouTube Downloader."""
    
    def __init__(self):
        # Inicializa componentes
        self.file_manager = FileManager()
        self.ffmpeg_manager = FFmpegManager()
        self.youtube_downloader = YouTubeDownloader(self.ffmpeg_manager)
        self.playlist_handler = PlaylistHandler()
        self.input_handler = InputHandler()
        self.menu_display = MenuDisplay()
        self.menu_controller = MenuController(self.input_handler, self.menu_display)
        self.url_validator = URLValidator()
        self.report_generator = ReportGenerator()
    
    def setup(self) -> bool:
        """
        Configura a aplicação (FFmpeg, diretórios, etc.).
        
        Returns:
            True se a configuração foi bem-sucedida, False caso contrário
        """
        try:
            # Setup do FFmpeg
            if not self.ffmpeg_manager.setup_ffmpeg():
                logger.error("Falha na configuração do FFmpeg")
                return False
            
            # Cria diretório de downloads
            self.file_manager.create_directory_if_not_exists(paths.DOWNLOAD_DIR)
            logger.info("Diretório de downloads criado/verificado")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro durante a configuração: {e}")
            return False
    
    def run(self) -> None:
        """Executa a aplicação principal."""
        try:
            self.menu_display.show_welcome_header()
            
            # Configuração inicial
            if not self.setup():
                logger.error("Falha na configuração inicial. Encerrando.")
                return
            
            # Loop principal
            while True:
                main_choice = self.menu_controller.get_main_menu_choice()
                
                if main_choice == "3":
                    logger.info("Saindo do programa.")
                    break
                
                download_type_choice = self.menu_controller.get_download_type_choice()
                download_type = DownloadType.AUDIO if download_type_choice == "1" else DownloadType.VIDEO
                
                if main_choice == "1":
                    self._handle_single_download(download_type)
                elif main_choice == "2":
                    self._handle_batch_download(download_type)
            
            self.menu_display.show_completion_message()
            
        except KeyboardInterrupt:
            logger.warning("\nDownload interrompido pelo usuário.")
        except Exception as e:
            logger.error(f"\nErro durante o processo: {e}")
            logger.info("Verifique sua conexão e tente novamente.")
    
    def _handle_single_download(self, download_type: DownloadType) -> None:
        """
        Manipula download único.
        
        Args:
            download_type: Tipo de download (áudio ou vídeo)
        """
        url = self.input_handler.get_single_url()
        
        # Verifica se é playlist
        if self.url_validator.is_playlist_url(url) and self.playlist_handler.is_playlist(url):
            playlist_choice = self.menu_controller.get_playlist_choice()
            
            if playlist_choice == "3":
                logger.info("Download cancelado pelo usuário.")
                return
            
            if playlist_choice == "1":
                # Baixar playlist inteira
                self._download_playlist(url, download_type)
            else:
                # Baixar apenas vídeo atual
                result = self.youtube_downloader.download_single(url, download_type)
                self._show_single_download_result(result)
        else:
            # Download único
            result = self.youtube_downloader.download_single(url, download_type)
            self._show_single_download_result(result)
    
    def _handle_batch_download(self, download_type: DownloadType) -> None:
        """
        Manipula download em lote.
        
        Args:
            download_type: Tipo de download (áudio ou vídeo)
        """
        urls = self.input_handler.get_multiple_urls()
        
        if not urls:
            logger.error("Nenhum URL fornecido para download em lote.")
            return
        
        logger.info(f"Modo lote: {len(urls)} URLs para processamento.")
        
        # Expande playlists em vídeos individuais
        all_video_urls = self._expand_playlists(urls)
        
        logger.info(f"Total de {len(all_video_urls)} vídeos para download em lote.")
        
        # Executa downloads em paralelo
        batch_result = self.youtube_downloader.download_batch(all_video_urls, download_type)
        
        # Exibe resultados
        self._show_batch_download_results(batch_result)
    
    def _download_playlist(self, playlist_url: str, download_type: DownloadType) -> None:
        """
        Baixa uma playlist inteira.
        
        Args:
            playlist_url: URL da playlist
            download_type: Tipo de download
        """
        # Obtém informações da playlist
        playlist_title = self.playlist_handler.get_playlist_title(playlist_url)
        video_urls = self.playlist_handler.get_playlist_entries(playlist_url)
        
        self.menu_display.show_playlist_info(playlist_title, len(video_urls))
        
        # Confirma se o usuário quer continuar
        if not self.input_handler.confirm_action(
            f"Deseja baixar {len(video_urls)} vídeos da playlist '{playlist_title}'?"
        ):
            logger.info("Download da playlist cancelado.")
            return
        
        # Executa downloads
        batch_result = self.youtube_downloader.download_batch(video_urls, download_type)
        self._show_batch_download_results(batch_result)
    
    def _expand_playlists(self, urls: List[str]) -> List[str]:
        """
        Expande URLs de playlist em URLs de vídeos individuais.
        
        Args:
            urls: Lista de URLs que podem incluir playlists
            
        Returns:
            Lista de URLs de vídeos individuais
        """
        all_video_urls = []
        
        for url in urls:
            if self.url_validator.is_playlist_url(url) and self.playlist_handler.is_playlist(url):
                logger.info(f"Processando playlist: {url}")
                playlist_videos = self.playlist_handler.get_playlist_entries(url)
                logger.info(f"Adicionados {len(playlist_videos)} vídeos da playlist.")
                all_video_urls.extend(playlist_videos)
            else:
                all_video_urls.append(url)
        
        return all_video_urls
    
    def _show_single_download_result(self, result) -> None:
        """
        Exibe resultado de download único.
        
        Args:
            result: Resultado do download
        """
        if result.is_success:
            logger.success(f"Download concluído: {result.title}")
        elif result.is_skipped:
            logger.warning(f"Arquivo já existe: {result.title}")
        else:
            logger.error(f"Falha no download: {result.error_message}")
    
    def _show_batch_download_results(self, batch_result: BatchDownloadResult) -> None:
        """
        Exibe resultados de download em lote.
        
        Args:
            batch_result: Resultado do download em lote
        """
        self.menu_display.show_batch_download_summary(batch_result)
        
        # Exibe relatório detalhado de falhas
        failed_results = batch_result.get_failed_results()
        if failed_results:
            self.menu_display.show_failed_downloads_report(failed_results)
            self._save_failed_downloads_report(failed_results)
    
    def _save_failed_downloads_report(self, failed_results: List) -> None:
        """
        Salva relatório de downloads com falha em arquivo.
        
        Args:
            failed_results: Lista de resultados que falharam
        """
        report_path = os.path.join(paths.DOWNLOAD_DIR, "failed_downloads.txt")
        
        if self.report_generator.save_failed_downloads_report(failed_results, report_path):
            logger.info(f"Relatório de falhas salvo em: {report_path}")
        else:
            logger.warning("Não foi possível salvar o relatório de falhas.")
