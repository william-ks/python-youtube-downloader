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

# Caminho para o executável do ffmpeg
ffmpeg_dir = "./tools/ffmpeg/bin"
ffmpeg_path = os.path.join(ffmpeg_dir, "ffmpeg.exe")

# URL para baixar a última versão do ffmpeg
ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"


def download_ffmpeg():
    if os.path.exists(ffmpeg_path):
        print(f"{SUCCESS}ffmpeg já existe, pulando download.")
        return

    if not os.path.exists(ffmpeg_dir):
        print(f"{INFO}Criando o diretório do ffmpeg...")
        os.makedirs(ffmpeg_dir)


    zip_path = os.path.join(ffmpeg_dir, "ffmpeg.zip")

    # Baixa o arquivo zip do ffmpeg
    print(f"{INFO}Baixando a última versão do ffmpeg...")
    response = requests.get(ffmpeg_url)
    with open(zip_path, "wb") as file:
        file.write(response.content)

    # Extrai o executável do ffmpeg
    print(f"{INFO}Extraindo o ffmpeg...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file in zip_ref.namelist():
            if "bin/ffmpeg.exe" in file:
                zip_ref.extract(file, ffmpeg_dir)
                os.rename(os.path.join(ffmpeg_dir, file), ffmpeg_path)

    # Remove o arquivo zip
    os.remove(zip_path)
    print(f"{SUCCESS}ffmpeg atualizado com sucesso!")


# Configuração do yt-dlp
ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "ffmpeg_location": ffmpeg_path,
    "outtmpl": "./download/%(title)s.%(ext)s",
}


def download_audio(youtube_url):
    ydl_opts_single = ydl_opts.copy()
    ydl_opts_single.update({"noplaylist": True})
    with youtube_dl.YoutubeDL(ydl_opts_single) as ydl:
        ydl.download([youtube_url])
    print(f"{SUCCESS}Download concluído!")


def is_playlist(youtube_url):
    ydl_opts = {"quiet": True, "extract_flat": True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        return info_dict.get("_type") == "playlist"


def download_playlist(youtube_url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    print(f"{SUCCESS}Downloads concluídos!")


if __name__ == "__main__":
    # Baixa e atualiza o ffmpeg se necessário
    download_ffmpeg()

    # Cria a pasta de download se não existir
    if not os.path.exists("./download"):
        print(f"{INFO}Criando a pasta de download...")
        os.makedirs("./download")

    # Solicita o link do vídeo do YouTube
    youtube_url = input(f"{INFO}Digite o link do vídeo do YouTube: {RESET}")

    # Verifica se a URL contém a palavra "list"
    if re.search(r"[?&]list=", youtube_url):
        print(f"{INFO}A URL é uma playlist. Escolha uma opção:")
        print(f"{INFO}1 - Baixar todos os vídeos da playlist")
        print(f"{INFO}2 - Baixar apenas o vídeo atual")
        print(f"{INFO}3 - Cancelar (encerra o programa)")
        choice = input(f"{INFO}Digite o número da opção desejada: {RESET}").strip()
        
        if choice == "1":
            if is_playlist(youtube_url):
                print("playlist verificada com sucesso") 
                download_playlist(youtube_url)
            else:
                print("Playlist inválida, baixando apenas o vídeo do link.")
                download_audio(youtube_url)
        elif choice == "2":
            download_audio(youtube_url)
        elif choice == "3":
            print("Download cancelado.")
            exit()
        else:
            print(f"{ERROR}Opção inválida. Encerrando o programa.")
            exit()
    else:
        download_audio(youtube_url)
