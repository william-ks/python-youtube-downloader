"""Logger personalizado para o YouTube Downloader."""

from typing import Any
from colorama import Fore


class Logger:
    """Logger personalizado com cores."""
    
    # Cores definidas diretamente
    SUCCESS = Fore.GREEN
    ERROR = Fore.LIGHTRED_EX
    INFO = Fore.CYAN
    WARNING = Fore.YELLOW
    RESET = Fore.RESET
    
    @classmethod
    def success(cls, message: str) -> None:
        """Imprime mensagem de sucesso."""
        print(f"{cls.SUCCESS}{message}{cls.RESET}")
    
    @classmethod
    def error(cls, message: str) -> None:
        """Imprime mensagem de erro."""
        print(f"{cls.ERROR}{message}{cls.RESET}")
    
    @classmethod
    def info(cls, message: str) -> None:
        """Imprime mensagem informativa."""
        print(f"{cls.INFO}{message}{cls.RESET}")
    
    @classmethod
    def warning(cls, message: str) -> None:
        """Imprime mensagem de aviso."""
        print(f"{cls.WARNING}{message}{cls.RESET}")
    
    @classmethod
    def plain(cls, message: str) -> None:
        """Imprime mensagem sem cor."""
        print(message)
    
    @classmethod
    def separator(cls, char: str = "─", length: int = 40) -> None:
        """Imprime uma linha separadora."""
        print(f"{cls.INFO}{char * length}{cls.RESET}")
    
    @classmethod
    def header(cls, title: str, width: int = 50) -> None:
        """Imprime um cabeçalho formatado."""
        border = "═" * width
        padding = " " * ((width - len(title) - 2) // 2)
        
        print(f"{cls.SUCCESS}╔{border}╗")
        print(f"{cls.SUCCESS}║{padding}{title}{padding}║")
        print(f"{cls.SUCCESS}╚{border}╝{cls.RESET}")
    
    @classmethod
    def box(cls, lines: list[str], width: int = 40) -> None:
        """Imprime texto em uma caixa formatada."""
        border_top = "╔" + "═" * width + "╗"
        border_bottom = "╚" + "═" * width + "╝"
        
        print(f"{cls.INFO}{border_top}")
        
        for line in lines:
            padding = " " * (width - len(line))
            print(f"{cls.INFO}║ {line}{padding}║")
        
        print(f"{cls.INFO}{border_bottom}{cls.RESET}")


# Instância global do logger
logger = Logger()
