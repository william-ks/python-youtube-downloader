"""Configurações e constantes do aplicativo."""

import os
from dataclasses import dataclass
from colorama import Fore


@dataclass
class Colors:
    """Cores para output do terminal."""
    SUCCESS = Fore.GREEN
    ERROR = Fore.LIGHTRED_EX
    INFO = Fore.CYAN
    WARNING = Fore.YELLOW
    RESET = Fore.RESET


@dataclass
class Paths:
    """Configurações de caminhos."""
    FFMPEG_DIR = "./tools/ffmpeg/bin"
    FFMPEG_PATH = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
    DOWNLOAD_DIR = "./downloads"


@dataclass
class URLs:
    """URLs de download."""
    FFMPEG_DOWNLOAD_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"


@dataclass
class Settings:
    """Configurações gerais da aplicação."""
    MAX_PARALLEL_DOWNLOADS = 5
    DEFAULT_AUDIO_QUALITY = "192"
    DEFAULT_VIDEO_FORMAT = "best[ext=mp4]/best"
    DEFAULT_AUDIO_FORMAT = "bestaudio/best"
    REQUEST_TIMEOUT = 30


# Instâncias globais das configurações
colors = Colors()
paths = Paths()
urls = URLs()
settings = Settings()
