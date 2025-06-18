import os
import re
import requests
import zipfile
import yt_dlp as youtube_dl
import concurrent.futures
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
MAX_PARALLEL_DOWNLOADS = 5  # Número máximo de downloads simultâneos

# Global list to track failed downloads
failed_downloads = []

# Global list to track already existing files
already_existing = []


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
        "ignoreerrors": True,  # Continue on errors
        "extract_flat": False,  # Extract detailed info
    }


def get_video_download_options():
    """
    Returns yt-dlp options for video download (MP4).
    """
    return {
        "format": "best[ext=mp4]/best",
        "ffmpeg_location": FFMPEG_PATH,
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "ignoreerrors": True,  # Continue on errors
        "extract_flat": False,  # Extract detailed info
    }


def check_video_availability(url):
    """
    Checks if a video is available before attempting download.
    
    Args:
        url (str): YouTube URL to check
    
    Returns:
        tuple: (is_available, video_info)
    """
    try:
        ydl_opts = {"quiet": True, "no_warnings": True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return True, info_dict
    except Exception as e:
        error_msg = str(e).lower()
        if any(keyword in error_msg for keyword in ['unavailable', 'removed', 'private', 'blocked']):
            return False, str(e)
        return False, str(e)


def download_with_error_handling(ydl, url_list, download_type):
    """
    Downloads videos/audio with proper error handling.
    
    Args:
        ydl: YoutubeDL instance
        url_list: List of URLs to download
        download_type: "audio" or "video"
    
    Returns:
        tuple: (successful_count, failed_count)
    """
    global failed_downloads
    successful = 0
    failed = 0
    
    for url in url_list:
        try:
            print(f"{INFO}Verificando disponibilidade: {url}")
            is_available, info = check_video_availability(url)
            
            if not is_available:
                print(f"{ERROR}Vídeo indisponível: {url}")
                print(f"{ERROR}Motivo: {info}")
                failed_downloads.append({
                    'url': url,
                    'reason': info,
                    'type': download_type
                })
                failed += 1
                continue
            
            print(f"{INFO}Baixando: {info.get('title', 'Título desconhecido')}")
            ydl.download([url])
            successful += 1
            print(f"{SUCCESS}Download concluído!")
            
        except Exception as e:
            error_msg = str(e)
            print(f"{ERROR}Erro ao baixar {url}: {error_msg}")
            
            failed_downloads.append({
                'url': url,
                'reason': error_msg,
                'type': download_type
            })
            failed += 1
            
            # Continue with next video instead of stopping
            continue
    
    return successful, failed


def download_url_worker(url, download_type):
    """
    Worker function for parallel downloads.
    
    Args:
        url (str): YouTube URL to download
        download_type (str): "audio" or "video"
    
    Returns:
        dict: Result information about the download
    """
    global already_existing
    
    result = {
        'url': url,
        'success': False,
        'title': '',
        'error': None,
        'skipped': False
    }
    
    try:
        # Check video availability first
        is_available, info = check_video_availability(url)
        
        if not is_available:
            result['error'] = info
            return result
        
        # Get title for logging
        result['title'] = info.get('title', 'Título desconhecido')
        
        # Check if file already exists
        file_exists, existing_filename = check_file_exists(info, download_type)
        
        if file_exists:
            print(f"{WARNING}Arquivo já existe: {result['title']} ({existing_filename})")
            result['skipped'] = True
            result['success'] = True  # Mark as success since we're skipping intentionally
            
            already_existing.append({
                'title': result['title'],
                'url': url,
                'existing_file': existing_filename
            })
            
            return result
        
        print(f"{INFO}Baixando: {result['title']}")
        
        # Setup options based on download type
        if download_type == "audio":
            options = get_audio_download_options()
        else:
            options = get_video_download_options()
        
        options.update({"noplaylist": True})
        
        # Perform the actual download
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])
            result['success'] = True
        
    except Exception as e:
        result['error'] = str(e)
    
    return result


def download_batch_parallel(url_list, download_type):
    """
    Downloads multiple videos/audios in parallel.
    
    Args:
        url_list (list): List of YouTube URLs to download
        download_type (str): "audio" or "video"
    
    Returns:
        tuple: (successful_count, failed_count)
    """
    global failed_downloads
    successful = 0
    failed = 0
    
    print(f"{INFO}Iniciando downloads em paralelo de {len(url_list)} itens...")
    print(f"{INFO}Máximo de {MAX_PARALLEL_DOWNLOADS} downloads simultâneos.")
    
    # Create a thread pool executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PARALLEL_DOWNLOADS) as executor:
        # Submit all download tasks
        future_to_url = {
            executor.submit(download_url_worker, url, download_type): url 
            for url in url_list
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                
                if result['success']:
                    successful += 1
                    print(f"{SUCCESS}Download concluído: {result['title']}")
                else:
                    failed += 1
                    error_msg = result['error']
                    print(f"{ERROR}Falha ao baixar {url}: {error_msg}")
                    
                    failed_downloads.append({
                        'url': url,
                        'reason': error_msg,
                        'type': download_type
                    })
            
            except Exception as e:
                failed += 1
                error_msg = str(e)
                print(f"{ERROR}Erro no processamento de {url}: {error_msg}")
                
                failed_downloads.append({
                    'url': url,
                    'reason': error_msg,
                    'type': download_type
                })
    
    print(f"{INFO}Downloads em paralelo finalizados. Sucesso: {successful}, Falhas: {failed}")
    return successful, failed


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
            successful, failed = download_with_error_handling(ydl, [youtube_url], "audio")
            if successful > 0:
                print(f"{SUCCESS}Download de áudio concluído!")
            else:
                print(f"{ERROR}Falha no download do áudio.")
        
    except Exception as e:
        print(f"{ERROR}Erro ao baixar áudio: {e}")
        failed_downloads.append({
            'url': youtube_url,
            'reason': str(e),
            'type': 'audio'
        })
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
            successful, failed = download_with_error_handling(ydl, [youtube_url], "video")
            if successful > 0:
                print(f"{SUCCESS}Download de vídeo concluído!")
            else:
                print(f"{ERROR}Falha no download do vídeo.")
        
    except Exception as e:
        print(f"{ERROR}Erro ao baixar vídeo: {e}")
        failed_downloads.append({
            'url': youtube_url,
            'reason': str(e),
            'type': 'video'
        })
        raise


def get_playlist_entries(youtube_url):
    """
    Gets all video URLs from a playlist.
    
    Args:
        youtube_url (str): YouTube playlist URL
    
    Returns:
        list: List of individual video URLs
    """
    try:
        ydl_opts = {"quiet": True, "extract_flat": True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(youtube_url, download=False)
            if playlist_info.get("_type") == "playlist":
                entries = playlist_info.get("entries", [])
                urls = []
                for entry in entries:
                    if entry and entry.get("id"):
                        video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                        urls.append(video_url)
                return urls
            else:
                return [youtube_url]
    except Exception as e:
        print(f"{ERROR}Erro ao extrair playlist: {e}")
        return [youtube_url]


def download_playlist_audio(youtube_url):
    """
    Downloads all audio files from a YouTube playlist.
    
    Args:
        youtube_url (str): YouTube playlist URL to download
    """
    print(f"{INFO}Iniciando download de playlist (áudio)...")
    
    # Get individual video URLs from playlist
    video_urls = get_playlist_entries(youtube_url)
    print(f"{INFO}Encontrados {len(video_urls)} vídeos na playlist.")
    
    try:
        # Use parallel downloads for playlist
        successful, failed = download_batch_parallel(video_urls, "audio")
        print(f"{SUCCESS}Downloads de playlist (áudio) concluídos!")
        print(f"{INFO}Sucessos: {successful}, Falhas: {failed}")
        
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
    
    # Get individual video URLs from playlist
    video_urls = get_playlist_entries(youtube_url)
    print(f"{INFO}Encontrados {len(video_urls)} vídeos na playlist.")
    
    try:
        # Use parallel downloads for playlist
        successful, failed = download_batch_parallel(video_urls, "video")
        print(f"{SUCCESS}Downloads de playlist (vídeo) concluídos!")
        print(f"{INFO}Sucessos: {successful}, Falhas: {failed}")
        
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


def get_batch_urls_input():
    """
    Gets multiple YouTube URLs from user input.
    
    Returns:
        list: List of valid YouTube URLs
    """
    print(f"{INFO}Digite os links do YouTube, um por linha.")
    print(f"{INFO}Pressione Enter duas vezes para finalizar.")
    
    urls = []
    
    while True:
        line = input(f"{INFO}Link {len(urls) + 1} (ou Enter para concluir): {RESET}").strip()
        
        if not line and not urls:
            print(f"{ERROR}Digite pelo menos um URL válido.")
            continue
            
        if not line and urls:
            break
            
        # Basic YouTube URL validation
        youtube_patterns = [
            r'youtube\.com/watch',
            r'youtube\.com/playlist',
            r'youtu\.be/',
            r'youtube\.com/embed'
        ]
        
        if any(re.search(pattern, line) for pattern in youtube_patterns):
            urls.append(line)
        else:
            print(f"{ERROR}URL inválida. Digite uma URL válida do YouTube.")
    
    return urls


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


def show_failed_downloads_report():
    """
    Shows a report of all failed downloads.
    """
    global failed_downloads
    
    if not failed_downloads:
        return
    
    print(f"\n{WARNING}╔══════════════════════════════════════════════════╗")
    print(f"{WARNING}║              RELATÓRIO DE FALHAS                 ║")
    print(f"{WARNING}╚══════════════════════════════════════════════════╝{RESET}")
    
    print(f"\n{ERROR}Total de vídeos com falha: {len(failed_downloads)}")
    print(f"{ERROR}{'─' * 80}")
    
    for i, failure in enumerate(failed_downloads, 1):
        print(f"\n{ERROR}[{i}] Tipo: {failure['type'].upper()}")
        print(f"{ERROR}URL: {failure['url']}")
        print(f"{ERROR}Motivo: {failure['reason']}")
        print(f"{ERROR}{'─' * 40}")
    
    # Save failed URLs to a file for later reference
    try:
        failed_urls_file = os.path.join(DOWNLOAD_DIR, "failed_downloads.txt")
        with open(failed_urls_file, "w", encoding="utf-8") as f:
            f.write("RELATÓRIO DE DOWNLOADS COM FALHA\n")
            f.write("=" * 50 + "\n\n")
            for i, failure in enumerate(failed_downloads, 1):
                f.write(f"[{i}] Tipo: {failure['type'].upper()}\n")
                f.write(f"URL: {failure['url']}\n")
                f.write(f"Motivo: {failure['reason']}\n")
                f.write("-" * 40 + "\n\n")
        
        print(f"\n{INFO}Relatório salvo em: {failed_urls_file}")
        
    except Exception as e:
        print(f"{WARNING}Não foi possível salvar o relatório: {e}")


def sanitize_filename(filename):
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters for file names
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    
    # Replace multiple spaces with single space
    filename = re.sub(r'\s+', ' ', filename)
    
    # Remove leading/trailing spaces
    filename = filename.strip()
    
    return filename


def check_file_exists(video_info, download_type):
    """
    Check if a file with the same title already exists in the downloads folder.
    
    Args:
        video_info (dict): Video information from yt-dlp
        download_type (str): "audio" or "video"
        
    Returns:
        tuple: (exists, filename) - exists is boolean, filename is the existing file name
    """
    if not video_info or not video_info.get('title'):
        return False, None
    
    title = sanitize_filename(video_info['title'])
    
    # Define extensions to check based on download type
    if download_type == "audio":
        extensions = ['.mp3', '.m4a', '.webm', '.opus']
    else:  # video
        extensions = ['.mp4', '.mkv', '.webm', '.avi']
    
    # Check if any file exists with the same title and compatible extension
    for ext in extensions:
        potential_filename = f"{title}{ext}"
        full_path = os.path.join(DOWNLOAD_DIR, potential_filename)
        
        if os.path.exists(full_path):
            return True, potential_filename
    
    return False, None


def download_url_worker(url, download_type):
    """
    Worker function for parallel downloads.
    
    Args:
        url (str): YouTube URL to download
        download_type (str): "audio" or "video"
    
    Returns:
        dict: Result information about the download
    """
    result = {
        'url': url,
        'success': False,
        'title': '',
        'error': None
    }
    
    try:
        # Check video availability first
        is_available, info = check_video_availability(url)
        
        if not is_available:
            result['error'] = info
            return result
        
        # Get title for logging
        result['title'] = info.get('title', 'Título desconhecido')
        print(f"{INFO}Baixando: {result['title']}")
        
        # Setup options based on download type
        if download_type == "audio":
            options = get_audio_download_options()
        else:
            options = get_video_download_options()
        
        options.update({"noplaylist": True})
        
        # Check if file already exists
        file_exists, existing_file = check_file_exists(info, download_type)
        
        if file_exists:
            result['success'] = True
            print(f"{WARNING}Arquivo já existe, pulando download: {existing_file}")
            already_existing.append({
                'url': url,
                'file': existing_file,
                'type': download_type
            })
            return result
        
        # Perform the actual download
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])
            result['success'] = True
        
    except Exception as e:
        result['error'] = str(e)
    
    return result


def download_batch_parallel(url_list, download_type):
    """
    Downloads multiple videos/audios in parallel.
    
    Args:
        url_list (list): List of YouTube URLs to download
        download_type (str): "audio" or "video"
    
    Returns:
        tuple: (successful_count, failed_count)
    """
    global failed_downloads
    successful = 0
    failed = 0
    
    print(f"{INFO}Iniciando downloads em paralelo de {len(url_list)} itens...")
    print(f"{INFO}Máximo de {MAX_PARALLEL_DOWNLOADS} downloads simultâneos.")
    
    # Create a thread pool executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PARALLEL_DOWNLOADS) as executor:
        # Submit all download tasks
        future_to_url = {
            executor.submit(download_url_worker, url, download_type): url 
            for url in url_list
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                
                if result['success']:
                    successful += 1
                    print(f"{SUCCESS}Download concluído: {result['title']}")
                else:
                    failed += 1
                    error_msg = result['error']
                    print(f"{ERROR}Falha ao baixar {url}: {error_msg}")
                    
                    failed_downloads.append({
                        'url': url,
                        'reason': error_msg,
                        'type': download_type
                    })
            
            except Exception as e:
                failed += 1
                error_msg = str(e)
                print(f"{ERROR}Erro no processamento de {url}: {error_msg}")
                
                failed_downloads.append({
                    'url': url,
                    'reason': error_msg,
                    'type': download_type
                })
    
    print(f"{INFO}Downloads em paralelo finalizados. Sucesso: {successful}, Falhas: {failed}")
    return successful, failed


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
            successful, failed = download_with_error_handling(ydl, [youtube_url], "audio")
            if successful > 0:
                print(f"{SUCCESS}Download de áudio concluído!")
            else:
                print(f"{ERROR}Falha no download do áudio.")
        
    except Exception as e:
        print(f"{ERROR}Erro ao baixar áudio: {e}")
        failed_downloads.append({
            'url': youtube_url,
            'reason': str(e),
            'type': 'audio'
        })
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
            successful, failed = download_with_error_handling(ydl, [youtube_url], "video")
            if successful > 0:
                print(f"{SUCCESS}Download de vídeo concluído!")
            else:
                print(f"{ERROR}Falha no download do vídeo.")
        
    except Exception as e:
        print(f"{ERROR}Erro ao baixar vídeo: {e}")
        failed_downloads.append({
            'url': youtube_url,
            'reason': str(e),
            'type': 'video'
        })
        raise


def get_playlist_entries(youtube_url):
    """
    Gets all video URLs from a playlist.
    
    Args:
        youtube_url (str): YouTube playlist URL
    
    Returns:
        list: List of individual video URLs
    """
    try:
        ydl_opts = {"quiet": True, "extract_flat": True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(youtube_url, download=False)
            if playlist_info.get("_type") == "playlist":
                entries = playlist_info.get("entries", [])
                urls = []
                for entry in entries:
                    if entry and entry.get("id"):
                        video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                        urls.append(video_url)
                return urls
            else:
                return [youtube_url]
    except Exception as e:
        print(f"{ERROR}Erro ao extrair playlist: {e}")
        return [youtube_url]


def download_playlist_audio(youtube_url):
    """
    Downloads all audio files from a YouTube playlist.
    
    Args:
        youtube_url (str): YouTube playlist URL to download
    """
    print(f"{INFO}Iniciando download de playlist (áudio)...")
    
    # Get individual video URLs from playlist
    video_urls = get_playlist_entries(youtube_url)
    print(f"{INFO}Encontrados {len(video_urls)} vídeos na playlist.")
    
    try:
        # Use parallel downloads for playlist
        successful, failed = download_batch_parallel(video_urls, "audio")
        print(f"{SUCCESS}Downloads de playlist (áudio) concluídos!")
        print(f"{INFO}Sucessos: {successful}, Falhas: {failed}")
        
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
    
    # Get individual video URLs from playlist
    video_urls = get_playlist_entries(youtube_url)
    print(f"{INFO}Encontrados {len(video_urls)} vídeos na playlist.")
    
    try:
        # Use parallel downloads for playlist
        successful, failed = download_batch_parallel(video_urls, "video")
        print(f"{SUCCESS}Downloads de playlist (vídeo) concluídos!")
        print(f"{INFO}Sucessos: {successful}, Falhas: {failed}")
        
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


def get_batch_urls_input():
    """
    Gets multiple YouTube URLs from user input.
    
    Returns:
        list: List of valid YouTube URLs
    """
    print(f"{INFO}Digite os links do YouTube, um por linha.")
    print(f"{INFO}Pressione Enter duas vezes para finalizar.")
    
    urls = []
    
    while True:
        line = input(f"{INFO}Link {len(urls) + 1} (ou Enter para concluir): {RESET}").strip()
        
        if not line and not urls:
            print(f"{ERROR}Digite pelo menos um URL válido.")
            continue
            
        if not line and urls:
            break
            
        # Basic YouTube URL validation
        youtube_patterns = [
            r'youtube\.com/watch',
            r'youtube\.com/playlist',
            r'youtu\.be/',
            r'youtube\.com/embed'
        ]
        
        if any(re.search(pattern, line) for pattern in youtube_patterns):
            urls.append(line)
        else:
            print(f"{ERROR}URL inválida. Digite uma URL válida do YouTube.")
    
    return urls


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


def show_failed_downloads_report():
    """
    Shows a report of all failed downloads.
    """
    global failed_downloads
    
    if not failed_downloads:
        return
    
    print(f"\n{WARNING}╔══════════════════════════════════════════════════╗")
    print(f"{WARNING}║              RELATÓRIO DE FALHAS                 ║")
    print(f"{WARNING}╚══════════════════════════════════════════════════╝{RESET}")
    
    print(f"\n{ERROR}Total de vídeos com falha: {len(failed_downloads)}")
    print(f"{ERROR}{'─' * 80}")
    
    for i, failure in enumerate(failed_downloads, 1):
        print(f"\n{ERROR}[{i}] Tipo: {failure['type'].upper()}")
        print(f"{ERROR}URL: {failure['url']}")
        print(f"{ERROR}Motivo: {failure['reason']}")
        print(f"{ERROR}{'─' * 40}")
    
    # Save failed URLs to a file for later reference
    try:
        failed_urls_file = os.path.join(DOWNLOAD_DIR, "failed_downloads.txt")
        with open(failed_urls_file, "w", encoding="utf-8") as f:
            f.write("RELATÓRIO DE DOWNLOADS COM FALHA\n")
            f.write("=" * 50 + "\n\n")
            for i, failure in enumerate(failed_downloads, 1):
                f.write(f"[{i}] Tipo: {failure['type'].upper()}\n")
                f.write(f"URL: {failure['url']}\n")
                f.write(f"Motivo: {failure['reason']}\n")
                f.write("-" * 40 + "\n\n")
        
        print(f"\n{INFO}Relatório salvo em: {failed_urls_file}")
        
    except Exception as e:
        print(f"{WARNING}Não foi possível salvar o relatório: {e}")


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


def handle_batch_download(download_type):
    """
    Handles downloading multiple videos/audios in batch.
    
    Args:
        download_type (str): "1" for audio, "2" for video
    """
    urls = get_batch_urls_input()
    
    if not urls:
        print(f"{ERROR}Nenhum URL fornecido para download em lote.")
        return
    
    print(f"{INFO}Modo lote: {len(urls)} URLs para processamento.")
    
    # Filter out playlist URLs and gather individual video URLs
    all_video_urls = []
    
    for url in urls:
        if re.search(r"[?&]list=", url) and is_playlist_url(url):
            print(f"{INFO}Processando playlist: {url}")
            playlist_videos = get_playlist_entries(url)
            print(f"{INFO}Adicionados {len(playlist_videos)} vídeos da playlist.")
            all_video_urls.extend(playlist_videos)
        else:
            all_video_urls.append(url)
    
    print(f"{INFO}Total de {len(all_video_urls)} vídeos para download em lote.")
    
    # Process with parallel downloads
    download_type_str = "audio" if download_type == "1" else "video"
    download_batch_parallel(all_video_urls, download_type_str)


def show_main_menu():
    """
    Shows the main menu for selecting download mode.
    
    Returns:
        str: User's choice (1, 2, or 3)
    """
    print(f"\n{SUCCESS}╔═══════════════════════════════════════╗")
    print(f"{SUCCESS}║         Modo de Download:             ║")
    print(f"{SUCCESS}╠═══════════════════════════════════════╣")
    print(f"{SUCCESS}║  1 - Download Único                   ║")
    print(f"{SUCCESS}║  2 - Download em Lote (Paralelo)      ║")
    print(f"{SUCCESS}║  3 - Sair                             ║")
    print(f"{SUCCESS}╚═══════════════════════════════════════╝{RESET}")
    
    while True:
        choice = input(f"{INFO}Digite sua escolha (1, 2 ou 3): {RESET}").strip()
        if choice in ["1", "2", "3"]:
            return choice
        print(f"{ERROR}Opção inválida. Digite 1, 2 ou 3.")


def main():
    """
    Main function that orchestrates the download process.
    """
    print(f"{SUCCESS}╔══════════════════════════════════════════════════╗")
    print(f"{SUCCESS}║          YouTube Downloader v3.0                 ║")
    print(f"{SUCCESS}║     Baixe vídeos e áudios do YouTube!            ║")
    print(f"{SUCCESS}╚══════════════════════════════════════════════════╝{RESET}\n")
    
    try:
        # Setup
        setup_ffmpeg()
        create_download_directory()
        
        while True:
            # Show main menu
            main_choice = show_main_menu()
            
            if main_choice == "3":
                print(f"{INFO}Saindo do programa.")
                break
            
            # Get download type (audio or video)
            download_type = show_download_type_menu()
            
            if main_choice == "1":
                # Single download mode
                youtube_url = get_user_url_input()
                
                # Check if URL contains playlist parameter
                if re.search(r"[?&]list=", youtube_url):
                    # Handle playlist URL
                    playlist_choice = show_playlist_menu()
                    
                    if playlist_choice == "3":
                        print(f"{INFO}Download cancelado pelo usuário.")
                        continue
                    
                    if playlist_choice == "1":
                        # Download entire playlist
                        if is_playlist_url(youtube_url):
                            handle_playlist_download(youtube_url, download_type)
                        else:
                            print(f"{WARNING}Playlist inválida. Baixando apenas o vídeo atual.")
                            handle_single_download(youtube_url, download_type)
                    else:
                        # Download only current video
                        handle_single_download(youtube_url, download_type)
                else:
                    # Handle single video URL
                    handle_single_download(youtube_url, download_type)
                    
            elif main_choice == "2":
                # Batch download mode
                handle_batch_download(download_type)
        
        print(f"\n{SUCCESS}╔══════════════════════════════════════════════════╗")
        print(f"{SUCCESS}║             Download Finalizado!                 ║")
        print(f"{SUCCESS}║    Verifique a pasta '{DOWNLOAD_DIR}' para ver seus arquivos    ║")
        print(f"{SUCCESS}╚══════════════════════════════════════════════════╝{RESET}")
        
        # Show failed downloads report if there are any failures
        show_failed_downloads_report()
        
    except KeyboardInterrupt:
        print(f"\n{WARNING}Download interrompido pelo usuário.")
        show_failed_downloads_report()
    except Exception as e:
        print(f"\n{ERROR}Erro durante o processo: {e}")
        print(f"{INFO}Verifique sua conexão e tente novamente.")
        show_failed_downloads_report()


if __name__ == "__main__":
    main()
