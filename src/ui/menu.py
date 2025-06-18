"""Menus da interface de usuário."""

from typing import List

from ..models.download_result import BatchDownloadResult, DownloadResult
from ..utils.logger import logger
from ..config.settings import paths


class MenuDisplay:
    """Responsável por exibir menus e relatórios."""
    
    def show_welcome_header(self) -> None:
        """Exibe o cabeçalho de boas-vindas."""
        logger.header("YouTube Downloader v3.0", 50)
        logger.info("Baixe vídeos e áudios do YouTube!")
        print()
    
    def show_main_menu(self) -> None:
        """Exibe o menu principal."""
        lines = [
            "          Modo de Download:            ",
            "                                      ",
            "  1 - Download Único                  ",
            "  2 - Download em Lote (Paralelo)     ",
            "  3 - Sair                            "
        ]
        logger.box(lines, 40)
    
    def show_download_type_menu(self) -> None:
        """Exibe o menu de tipo de download."""
        lines = [
            "     Escolha o tipo de download:      ",
            "                                      ",
            "  1 - Baixar como ÁUDIO (MP3)         ",
            "  2 - Baixar como VÍDEO (MP4)         "
        ]
        logger.box(lines, 40)
    
    def show_playlist_menu(self) -> None:
        """Exibe o menu de opções para playlist."""
        logger.warning("╔═══════════════════════════════════════╗")
        logger.warning("║      URL de Playlist Detectada        ║")
        logger.warning("╠═══════════════════════════════════════╣")
        logger.warning("║  1 - Baixar TODA a playlist           ║")
        logger.warning("║  2 - Baixar APENAS o vídeo atual      ║")
        logger.warning("║  3 - Cancelar                         ║")
        logger.warning("╚═══════════════════════════════════════╝")
    
    def show_completion_message(self) -> None:
        """Exibe mensagem de conclusão."""
        lines = [
            "             Download Finalizado!                 ",
            f"    Verifique a pasta '{paths.DOWNLOAD_DIR}' para ver seus arquivos    "
        ]
        logger.box(lines, 50)
    
    def show_batch_download_summary(self, result: BatchDownloadResult) -> None:
        """
        Exibe resumo de downloads em lote.
        
        Args:
            result: Resultado do download em lote
        """
        logger.info("\n" + "=" * 50)
        logger.info("RESUMO DOS DOWNLOADS")
        logger.info("=" * 50)
        
        logger.info(f"Total de downloads: {result.total_downloads}")
        logger.success(f"Bem-sucedidos: {result.successful}")
        logger.error(f"Falharam: {result.failed}")
        logger.warning(f"Pulados: {result.skipped}")
        
        success_rate = result.success_rate * 100
        logger.info(f"Taxa de sucesso: {success_rate:.1f}%")
        
        if result.failed > 0:
            logger.warning("\nVídeos que falharam:")
            for i, failed_result in enumerate(result.get_failed_results(), 1):
                logger.error(f"  {i}. {failed_result.title or failed_result.url}")
                logger.error(f"     Erro: {failed_result.error_message}")
    
    def show_failed_downloads_report(self, failed_results: List[DownloadResult]) -> None:
        """
        Exibe relatório detalhado de downloads com falha.
        
        Args:
            failed_results: Lista de resultados que falharam
        """
        if not failed_results:
            return
        
        logger.warning("\n╔══════════════════════════════════════════════════╗")
        logger.warning("║              RELATÓRIO DE FALHAS                 ║")
        logger.warning("╚══════════════════════════════════════════════════╝")
        
        logger.error(f"\nTotal de vídeos com falha: {len(failed_results)}")
        logger.separator("─", 80)
        
        for i, failure in enumerate(failed_results, 1):
            logger.error(f"\n[{i}] Tipo: {failure.download_type.value.upper()}")
            logger.error(f"URL: {failure.url}")
            logger.error(f"Título: {failure.title or 'Não disponível'}")
            logger.error(f"Motivo: {failure.error_message}")
            logger.separator("─", 40)
    
    def show_progress_info(self, current: int, total: int, title: str = "") -> None:
        """
        Exibe informações de progresso.
        
        Args:
            current: Número atual
            total: Total de itens
            title: Título opcional
        """
        progress = (current / total) * 100 if total > 0 else 0
        logger.info(f"Progresso: {current}/{total} ({progress:.1f}%)")
        
        if title:
            logger.info(f"Processando: {title}")
    
    def show_playlist_info(self, title: str, video_count: int) -> None:
        """
        Exibe informações sobre uma playlist.
        
        Args:
            title: Título da playlist
            video_count: Número de vídeos
        """
        logger.info(f"Playlist: {title}")
        logger.info(f"Vídeos encontrados: {video_count}")


class MenuController:
    """Controlador dos menus."""
    
    def __init__(self, input_handler, menu_display: MenuDisplay):
        self.input_handler = input_handler
        self.menu_display = menu_display
    
    def get_main_menu_choice(self) -> str:
        """
        Exibe o menu principal e obtém a escolha do usuário.
        
        Returns:
            Escolha do usuário
        """
        self.menu_display.show_main_menu()
        return self.input_handler.get_choice(
            "Digite sua escolha (1, 2 ou 3): ",
            ["1", "2", "3"]
        )
    
    def get_download_type_choice(self) -> str:
        """
        Exibe o menu de tipo de download e obtém a escolha.
        
        Returns:
            Escolha do usuário ("1" para áudio, "2" para vídeo)
        """
        self.menu_display.show_download_type_menu()
        return self.input_handler.get_choice(
            "Digite sua escolha (1 ou 2): ",
            ["1", "2"]
        )
    
    def get_playlist_choice(self) -> str:
        """
        Exibe o menu de playlist e obtém a escolha.
        
        Returns:
            Escolha do usuário
        """
        self.menu_display.show_playlist_menu()
        return self.input_handler.get_choice(
            "Digite sua escolha (1, 2 ou 3): ",
            ["1", "2", "3"]
        )
