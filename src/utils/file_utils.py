"""Utilitários para manipulação de arquivos."""

import os
import re
from typing import Tuple, List, Optional
import os


class FileManager:
    """Gerenciador de arquivos e diretórios."""
    
    @staticmethod
    def create_directory_if_not_exists(directory_path: str) -> None:
        """
        Cria um diretório se ele não existir.
        
        Args:
            directory_path: Caminho do diretório a ser criado
        """
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """
        Verifica se um arquivo existe.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            True se o arquivo existir, False caso contrário
        """
        return os.path.exists(file_path)
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Obtém o tamanho de um arquivo em bytes.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Tamanho do arquivo em bytes, 0 se não existir
        """
        try:
            return os.path.getsize(file_path)
        except OSError:
            return 0


class FilenameUtils:
    """Utilitários para manipulação de nomes de arquivos."""
    
    INVALID_CHARS = '<>:"/\\|?*'
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """
        Sanitiza um nome de arquivo removendo caracteres inválidos.
        
        Args:
            filename: Nome do arquivo original
            
        Returns:
            Nome do arquivo sanitizado
        """
        # Remove caracteres inválidos
        for char in cls.INVALID_CHARS:
            filename = filename.replace(char, '')
        
        # Substitui múltiplos espaços por um único espaço
        filename = re.sub(r'\s+', ' ', filename)        
        # Remove espaços no início e fim
        filename = filename.strip()
        
        return filename
    
    @classmethod
    def check_file_exists_with_extensions(
        cls, 
        base_filename: str, 
        extensions: List[str], 
        directory: str = "./downloads"
    ) -> Tuple[bool, Optional[str]]:
        """
        Verifica se existe um arquivo com o nome base e uma das extensões fornecidas.
        
        Args:
            base_filename: Nome base do arquivo (sem extensão)
            extensions: Lista de extensões para verificar
            directory: Diretório onde procurar (padrão: diretório de downloads)
            
        Returns:
            Tupla (existe, nome_do_arquivo) onde existe é booleano e nome_do_arquivo
            é o nome completo do arquivo encontrado ou None        """
        if directory is None:
            directory = "./downloads"
            
        sanitized_filename = cls.sanitize_filename(base_filename)
        
        for ext in extensions:
            full_filename = f"{sanitized_filename}{ext}"
            full_path = os.path.join(directory, full_filename)
            
            if os.path.exists(full_path):
                return True, full_filename
        
        return False, None


class ReportGenerator:
    """Gerador de relatórios."""
    
    @staticmethod
    def save_failed_downloads_report(failed_results: List, output_path: str) -> bool:
        """
        Salva um relatório de downloads com falha.
        
        Args:
            failed_results: Lista de resultados de downloads com falha
            output_path: Caminho onde salvar o relatório
            
        Returns:
            True se o relatório foi salvo com sucesso, False caso contrário
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("RELATÓRIO DE DOWNLOADS COM FALHA\n")
                f.write("=" * 50 + "\n\n")
                
                for i, failure in enumerate(failed_results, 1):
                    f.write(f"[{i}] Tipo: {failure.download_type.value.upper()}\n")
                    f.write(f"URL: {failure.url}\n")
                    f.write(f"Título: {failure.title}\n")
                    f.write(f"Erro: {failure.error_message}\n")
                    f.write("-" * 40 + "\n\n")
            
            return True
            
        except Exception:
            return False
