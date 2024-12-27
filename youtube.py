from messager import Messager
from yt_dlp import YoutubeDL
from colorama import init, Fore as style
import os

init(autoreset=True)

class Youtube_manager():
    def __init__(self):
        self.messager = Messager()

    def set_playlist(self, id):
        playlist_url = f'https://www.youtube.com/playlist?list={id}'
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            return [entry['url'] for entry in info['entries']]

    def download(self, type, link, directory):
        if type == 2:
            self.download_music(link, directory)
        else:
            self.download_video(link, directory)
        self.messager.blue_line()

    def download_music(self, url, directory):
        try:
            options = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(directory, '%(title)s.%(ext)s'),
                'ffmpeg_location': r'C:\Users\willk\Desktop\ffmpeg\bin',  # Caminho do FFmpeg
                'quiet': False
            }

            print(f"{style.BLUE}Baixando áudio...")
            with YoutubeDL(options) as ydl:
                ydl.download([url])

            print(f"{style.GREEN}Download concluído com sucesso!")
        except Exception as e:
            print(f"{style.RED}Erro ao baixar o áudio: {e}")
            self.messager.red_line()

    def download_video(self, url, directory):
        try:
            options = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(directory, '%(title)s.%(ext)s'),
                'ffmpeg_location': r'C:\Users\willk\Desktop\ffmpeg\bin',  # Caminho do FFmpeg
                'quiet': False
            }

            print(f"{style.BLUE}Baixando vídeo...")
            with YoutubeDL(options) as ydl:
                ydl.download([url])

            print(f"{style.GREEN}Download concluído com sucesso!")
        except Exception as e:
            print(f"{style.RED}Erro ao baixar o vídeo: {e}")
            self.messager.red_line()
