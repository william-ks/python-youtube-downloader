import os
import re
import requests
import zipfile
import yt_dlp as youtube_dl
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Define message colors
SUCCESS = Fore.GREEN
ERROR = Fore.LIGHTRED_EX
INFO = Fore.CYAN
WARNING = Fore.YELLOW
RESET = Fore.RESET

# Paths and URLs
FFMPEG_DIR = "./tools/ffmpeg/bin"
FFMPEG_PATH = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
FFMPEG_DOWNLOAD_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
DOWNLOAD_DIR = "./downloads"


def setup_ffmpeg():
    """
    Downloads and sets up ffmpeg if it doesn't exist.
    """
    if os.path.exists(FFMPEG_PATH):
        print(f"{SUCCESS}ffmpeg já existe, pulando download.")
        return

    if not os.path.exists(FFMPEG_DIR):
        print(f"{INFO}Criando o diretório do ffmpeg...")
        os.makedirs(FFMPEG_DIR, exist_ok=True)

    zip_path = os.path.join(FFMPEG_DIR, "ffmpeg.zip")

    try:
        # Download ffmpeg zip file
        print(f"{INFO}Baixando a última versão do ffmpeg...")
        response = requests.get(FFMPEG_DOWNLOAD_URL, timeout=30)
        response.raise_for_status()
        
        with open(zip_path, "wb") as file:
            file.write(response.content)

        # Extract ffmpeg executable
        print(f"{INFO}Extraindo o ffmpeg...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for file in zip_ref.namelist():
                if "bin/ffmpeg.exe" in file:
                    zip_ref.extract(file, FFMPEG_DIR)
                    os.rename(os.path.join(FFMPEG_DIR, file), FFMPEG_PATH)
                    break

        # Clean up zip file
        os.remove(zip_path)
        print(f"{SUCCESS}ffmpeg configurado com sucesso!")
        
    except Exception as e:
        print(f"{ERROR}Erro ao configurar ffmpeg: {e}")
        raise


def create_download_directory():
    """
    Creates the download directory if it doesn't exist.
    """
    if not os.path.exists(DOWNLOAD_DIR):
        print(f"{INFO}Criando a pasta de downloads...")
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def get_audio_download_options():
    """
    Returns yt-dlp options for audio download (MP3).
    """
    return {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "ffmpeg_location": FFMPEG_PATH,
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
    }


def get_video_download_options():
    """
    Returns yt-dlp options for video download (MP4).
    """
    return {
        "format": "best[ext=mp4]/best",
        "ffmpeg_location": FFMPEG_PATH,
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
    }


def download_single_audio(youtube_url):
    """
    Downloads a single audio file from YouTube URL.
    
    Args:
        youtube_url (str): YouTube URL to download
    """
    print(f"{INFO}Iniciando download de áudio...")
    
    audio_options = get_audio_download_options()
    audio_options.update({"noplaylist": True})
    
    try:
        with youtube_dl.YoutubeDL(audio_options) as ydl:
            ydl.download([youtube_url])
        print(f"{SUCCESS}Download de áudio concluído!")
        
    except Exception as e:
        print(f"{ERROR}Erro ao baixar áudio: {e}")
        raise


def download_single_video(youtube_url):
    """
    Downloads a single video file from YouTube URL.
    
    Args:
        youtube_url (str): YouTube URL to download
    """
    print(f"{INFO}Iniciando download de vídeo...")
    
    video_options = get_video_download_options()
    video_options.update({"noplaylist": True})
    
    try:
        with youtube_dl.YoutubeDL(video_options) as ydl:
            ydl.download([youtube_url])
        print(f"{SUCCESS}Download de vídeo concluído!")
        
    except Exception as e:
        print(f"{ERROR}Erro ao baixar vídeo: {e}")
        raise


def download_playlist_audio(youtube_url):
    """
    Downloads all audio files from a YouTube playlist.
    
    Args:
        youtube_url (str): YouTube playlist URL to download
    """
    print(f"{INFO}Iniciando download de playlist (áudio)...")
    
    audio_options = get_audio_download_options()
    
    try:
        with youtube_dl.YoutubeDL(audio_options) as ydl:
            ydl.download([youtube_url])
        print(f"{SUCCESS}Downloads de playlist (áudio) concluídos!")
        
    except Exception as e:
        print(f"{ERROR}Erro ao baixar playlist de áudio: {e}")
        raise


def download_playlist_video(youtube_url):
    """
    Downloads all video files from a YouTube playlist.
    
    Args:
        youtube_url (str): YouTube playlist URL to download
    """
    print(f"{INFO}Iniciando download de playlist (vídeo)...")
    
    video_options = get_video_download_options()
    
    try:
        with youtube_dl.YoutubeDL(video_options) as ydl:
            ydl.download([youtube_url])
        print(f"{SUCCESS}Downloads de playlist (vídeo) concluídos!")
        
    except Exception as e:
        print(f"{ERROR}Erro ao baixar playlist de vídeo: {e}")
        raise


def is_playlist_url(youtube_url):
    """
    Checks if the YouTube URL is a playlist.
    
    Args:
        youtube_url (str): YouTube URL to check
    
    Returns:
        bool: True if URL is a playlist, False otherwise
    """
    try:
        ydl_opts = {"quiet": True, "extract_flat": True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            return info_dict.get("_type") == "playlist"
    except Exception as e:
        print(f"{WARNING}Não foi possível verificar se é playlist: {e}")
        return False


def get_user_url_input():
    """
    Gets YouTube URL from user input with validation.
    
    Returns:
        str: Valid YouTube URL
    """
    while True:
        url = input(f"{INFO}Digite o link do YouTube: {RESET}").strip()
        
        if not url:
            print(f"{ERROR}URL não pode estar vazia. Tente novamente.")
            continue
            
        # Basic YouTube URL validation
        youtube_patterns = [
            r'youtube\.com/watch',
            r'youtube\.com/playlist',
            r'youtu\.be/',
            r'youtube\.com/embed'
        ]
        
        if any(re.search(pattern, url) for pattern in youtube_patterns):
            return url
        else:
            print(f"{ERROR}URL inválida. Digite uma URL válida do YouTube.")


def show_download_type_menu():
    """
    Shows the download type selection menu.
    
    Returns:
        str: User's choice (1 or 2)
    """
    print(f"\n{INFO}╔═══════════════════════════════════════╗")
    print(f"{INFO}║     Escolha o tipo de download:       ║")
    print(f"{INFO}╠═══════════════════════════════════════╣")
    print(f"{INFO}║  1 - Baixar como ÁUDIO (MP3)          ║")
    print(f"{INFO}║  2 - Baixar como VÍDEO (MP4)          ║")
    print(f"{INFO}╚═══════════════════════════════════════╝{RESET}")
    
    while True:
        choice = input(f"{INFO}Digite sua escolha (1 ou 2): {RESET}").strip()
        if choice in ["1", "2"]:
            return choice
        print(f"{ERROR}Opção inválida. Digite 1 ou 2.")


def show_playlist_menu():
    """
    Shows the playlist handling menu.
    
    Returns:
        str: User's choice (1, 2, or 3)
    """
    print(f"\n{WARNING}╔═══════════════════════════════════════╗")
    print(f"{WARNING}║      URL de Playlist Detectada        ║")
    print(f"{WARNING}╠═══════════════════════════════════════╣")
    print(f"{WARNING}║  1 - Baixar TODA a playlist           ║")
    print(f"{WARNING}║  2 - Baixar APENAS o vídeo atual      ║")
    print(f"{WARNING}║  3 - Cancelar                         ║")
    print(f"{WARNING}╚═══════════════════════════════════════╝{RESET}")
    
    while True:
        choice = input(f"{INFO}Digite sua escolha (1, 2 ou 3): {RESET}").strip()
        if choice in ["1", "2", "3"]:
            return choice
        print(f"{ERROR}Opção inválida. Digite 1, 2 ou 3.")


def handle_single_download(youtube_url, download_type):
    """
    Handles downloading a single video/audio.
    
    Args:
        youtube_url (str): YouTube URL to download
        download_type (str): "1" for audio, "2" for video
    """
    if download_type == "1":
        download_single_audio(youtube_url)
    else:
        download_single_video(youtube_url)


def handle_playlist_download(youtube_url, download_type):
    """
    Handles downloading a playlist.
    
    Args:
        youtube_url (str): YouTube playlist URL to download
        download_type (str): "1" for audio, "2" for video
    """
    if download_type == "1":
        download_playlist_audio(youtube_url)
    else:
        download_playlist_video(youtube_url)


def main():
    """
    Main function that orchestrates the download process.
    """
    print(f"{SUCCESS}╔══════════════════════════════════════════════════╗")
    print(f"{SUCCESS}║          YouTube Downloader v2.0                 ║")
    print(f"{SUCCESS}║     Baixe vídeos e áudios do YouTube!            ║")
    print(f"{SUCCESS}╚══════════════════════════════════════════════════╝{RESET}\n")
    
    try:
        # Setup
        setup_ffmpeg()
        create_download_directory()
        
        # Get URL from user
        youtube_url = get_user_url_input()
        
        # Check if URL contains playlist parameter
        if re.search(r"[?&]list=", youtube_url):
            # Handle playlist URL
            playlist_choice = show_playlist_menu()
            
            if playlist_choice == "3":
                print(f"{INFO}Download cancelado pelo usuário.")
                return
            
            if playlist_choice == "1":
                # Download entire playlist
                if is_playlist_url(youtube_url):
                    download_type = show_download_type_menu()
                    handle_playlist_download(youtube_url, download_type)
                else:
                    print(f"{WARNING}Playlist inválida. Baixando apenas o vídeo atual.")
                    download_type = show_download_type_menu()
                    handle_single_download(youtube_url, download_type)
            else:
                # Download only current video
                download_type = show_download_type_menu()
                handle_single_download(youtube_url, download_type)
        else:
            # Handle single video URL
            download_type = show_download_type_menu()
            handle_single_download(youtube_url, download_type)
            
        print(f"\n{SUCCESS}╔══════════════════════════════════════════════════╗")
        print(f"{SUCCESS}║             Download Finalizado!                 ║")
        print(f"{SUCCESS}║    Verifique a pasta '{DOWNLOAD_DIR}' para ver seus arquivos    ║")
        print(f"{SUCCESS}╚══════════════════════════════════════════════════╝{RESET}")
        
    except KeyboardInterrupt:
        print(f"\n{WARNING}Download interrompido pelo usuário.")
    except Exception as e:
        print(f"\n{ERROR}Erro durante o processo: {e}")
        print(f"{INFO}Verifique sua conexão e tente novamente.")


if __name__ == "__main__":
    main()
