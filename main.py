#!/usr/bin/env python3
"""
YouTube Downloader v3.0
Aplicação para download de vídeos e áudios do YouTube.

Autor: Will
Data: 2025
"""

from colorama import init

# Inicializa colorama para cores no terminal
init(autoreset=True)

# Importa a aplicação principal
from src.core.app import YouTubeDownloaderApp


def main():
    """Função principal da aplicação."""
    app = YouTubeDownloaderApp()
    app.run()


if __name__ == "__main__":
    main()
