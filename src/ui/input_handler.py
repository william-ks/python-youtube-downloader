"""Manipulador de entrada do usuário."""

from typing import List

from ..utils.validators import URLValidator, InputValidator
from ..utils.logger import logger


class InputHandler:
    """Responsável por coletar e validar entradas do usuário."""
    
    def __init__(self):
        self.url_validator = URLValidator()
        self.input_validator = InputValidator()
    
    def get_single_url(self) -> str:
        """
        Coleta uma única URL do usuário com validação.
        
        Returns:
            URL válida do YouTube
        """
        while True:
            url = input(f"Digite o link do YouTube: ").strip()
            
            if self.input_validator.is_empty_string(url):
                logger.error("URL não pode estar vazia. Tente novamente.")
                continue
            
            if self.url_validator.is_valid_youtube_url(url):
                return url
            else:
                logger.error("URL inválida. Digite uma URL válida do YouTube.")
    
    def get_multiple_urls(self) -> List[str]:
        """
        Coleta múltiplas URLs do usuário.
        
        Returns:
            Lista de URLs válidas do YouTube
        """
        logger.info("Digite os links do YouTube, um por linha.")
        logger.info("Pressione Enter duas vezes para finalizar.")
        
        urls = []
        empty_line_count = 0
        
        while True:
            line = input(f"Link {len(urls) + 1} (ou Enter para concluir): ").strip()
            
            if self.input_validator.is_empty_string(line):
                empty_line_count += 1
                
                if empty_line_count >= 2 or urls:
                    break
                elif not urls:
                    logger.error("Digite pelo menos um URL válido.")
                    empty_line_count = 0
                    continue
            else:
                empty_line_count = 0
                
                if self.url_validator.is_valid_youtube_url(line):
                    urls.append(line)
                else:
                    logger.error("URL inválida. Digite uma URL válida do YouTube.")
        
        return urls
    
    def get_choice(self, prompt: str, valid_choices: List[str]) -> str:
        """
        Coleta uma escolha do usuário de uma lista de opções válidas.
        
        Args:
            prompt: Mensagem para exibir ao usuário
            valid_choices: Lista de opções válidas
            
        Returns:
            Escolha válida do usuário
        """
        while True:
            choice = input(prompt).strip()
            
            if self.input_validator.is_valid_choice(choice, valid_choices):
                return choice
            
            valid_options = ", ".join(valid_choices)
            logger.error(f"Opção inválida. Escolha uma das opções: {valid_options}")
    
    def confirm_action(self, message: str) -> bool:
        """
        Pede confirmação do usuário para uma ação.
        
        Args:
            message: Mensagem de confirmação
            
        Returns:
            True se o usuário confirmar, False caso contrário
        """
        response = self.get_choice(
            f"{message} (s/n): ",
            ["s", "n", "S", "N", "sim", "não", "yes", "no"]
        )
        
        return response.lower() in ["s", "sim", "yes"]
