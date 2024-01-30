from messager import Messager
from pytube import YouTube, Playlist
from colorama import init, Fore as style
import os

init(autoreset=True)


class Youtube_manager():
    def __init__(self):
        self.messager = Messager()
        self.yt = YouTube

    def set_playlist(self, id):
        list = Playlist(f'https://www.youtube.com/playlist?list={id}')
        return list.video_urls

    def download(self, type, link, directory):
        if type == 2:
            self.download_music(link, directory)
        else:
            self.download_video(link, directory)
        self.messager.blue_line()

    def download_music(self, url, directory):
        try:
            video = self.yt(url)
            stream = video.streams.filter(
                only_audio=True, file_extension='mp4').first()

            print(f"{style.BLUE}Baixando áudio de {video.title}...")

            if stream:
                out_file = stream.download(output_path=str(directory))
                base_name, ext = os.path.splitext(out_file)
                new_file = base_name + '.mp3'
                os.rename(out_file, new_file)
                print(f"{style.GREEN}Download de {
                      video.title} concluído com sucesso!")
            else:
                print(f"{style.RED}ERRO ao baixar {video.title}")
                self.messager.red_line()

        except Exception as e:
            print(f"{style.RED}Erro ao baixar o vídeo {url}: {e}")
            self.messager.red_line()

    def download_video(self, url, directory):
        try:
            video = self.yt(url)
            stream = video.streams.filter(res='720p', file_extension='mp4').first()

            print(f"{style.BLUE}Baixando vídeo: {video.title}...")

            if stream:
                out_file = stream.download(output_path=str(directory))
                print(f"{style.GREEN}Download de {
                      video.title} concluído com sucesso!")
            else:
                print(f"{style.RED}ERRO ao baixar {video.title}")
                self.messager.red_line()

        except Exception as e:
            print(f"{style.RED}Erro ao baixar o vídeo {url}: {e}")
            self.messager.red_line()
