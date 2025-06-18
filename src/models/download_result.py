"""Modelos de dados para resultados de download."""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class DownloadType(Enum):
    """Tipos de download disponíveis."""
    AUDIO = "audio"
    VIDEO = "video"


class DownloadStatus(Enum):
    """Status possíveis de um download."""
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    PENDING = "pending"


@dataclass
class VideoInfo:
    """Informações de um vídeo."""
    title: str
    url: str
    duration: Optional[int] = None
    thumbnail: Optional[str] = None


@dataclass
class DownloadResult:
    """Resultado de um download."""
    url: str
    status: DownloadStatus
    download_type: DownloadType
    title: str = ""
    error_message: Optional[str] = None
    existing_file: Optional[str] = None
    
    @property
    def is_success(self) -> bool:
        """Verifica se o download foi bem-sucedido."""
        return self.status == DownloadStatus.SUCCESS
    
    @property
    def is_failed(self) -> bool:
        """Verifica se o download falhou."""
        return self.status == DownloadStatus.FAILED
    
    @property
    def is_skipped(self) -> bool:
        """Verifica se o download foi pulado."""
        return self.status == DownloadStatus.SKIPPED


@dataclass
class BatchDownloadResult:
    """Resultado de downloads em lote."""
    total_downloads: int
    successful: int
    failed: int
    skipped: int
    download_results: list[DownloadResult]
    
    @property
    def success_rate(self) -> float:
        """Taxa de sucesso dos downloads."""
        if self.total_downloads == 0:
            return 0.0
        return (self.successful + self.skipped) / self.total_downloads
    
    def get_failed_results(self) -> list[DownloadResult]:
        """Retorna apenas os resultados que falharam."""
        return [result for result in self.download_results if result.is_failed]
    
    def get_successful_results(self) -> list[DownloadResult]:
        """Retorna apenas os resultados bem-sucedidos."""
        return [result for result in self.download_results if result.is_success]
