from messager import Messager
from youtube import Youtube_manager
from colorama import init, Fore as s
from directory import Directory
import re

init(autoreset=True)


messager = Messager()
yt = Youtube_manager()
directory_manager = Directory()


def get_url():
    global url
    msg = 'do seu video' if download_type == 1 else 'da sua musica'
    print(f"{s.BLUE}Insira a URL {msg}:")
    url = str(input(f"{s.BLUE} -> {s.WHITE}"))

    if url.strip() == '':
        messager.red_line()
        print(f"{s.RED}URL inválida.")
        messager.red_line()

        get_url()
    else:
        if not is_a_url(url):
            messager.red_line()
            print(f"{s.RED}URL inválida.")
            messager.red_line()
            get_url()

    messager.blue_line()


def is_a_url(url):
    regex = (r'(https?://)?(www\.)?'
             r'(youtube|youtu|youtube-nocookie)\.(com|be)/')
    result = bool(re.match(regex, url))
    return result


def verify_list(url):
    regex = re.compile(r'list=([^&]+)')

    if 'list' in url:
        match = regex.search(url)
        playlist_id = match.group(1)

        if 'playlist' in url:
            return {
                "type": "playlist",
                "id": playlist_id
            }
        else:
            return {
                "type": "list",
                "id": playlist_id
            }
    else:
        return None


def get_download_type():
    global download_type
    print(f"{s.BLUE}Escolha uma opção de download: \n1 - Video\n2 - Musica")
    download_type = input(f"{s.BLUE} -> {s.WHITE}")

    try:
        download_type = int(download_type)
    except Exception as e:
        print(f"{s.RED}\nOpção inválida! Escolha novamente.")
        messager.red_line()
        get_download_type()

    if download_type != 1 and download_type != 2:
        print(f"{s.RED}\nOpção inválida! Escolha novamente.")
        messager.red_line()
        get_download_type()
    else:
        messager.blue_line()


def all_music_quest(object):
    if object['type'] == 'list':
        print(
            f"{s.BLUE}Você deseja baixar todos os videos da playlist ? [S/n]")
        anwser = input(f"{s.BLUE} -> {s.WHITE}")

        if anwser.strip().lower() == 's':
            playlist = yt.set_playlist(object['id'])
            return playlist
        else:
            print(f'{s.BLUE}Escolhendo a opção padrão (Sim)')
            messager.blue_line()
            return [url]
    else:
        playlist = yt.set_playlist(object['id'])
        return playlist


def main():
    global directory
    global playlist
    global itens_to_download
    print(f"{s.YELLOW}\n╰(*°▽°*)╯ Bem vindo ╰(*°▽°*)╯")
    messager.blue_line()
    get_download_type()
    get_url()
    directory = directory_manager.create_directory(
        'Video' if download_type == 1 else 'Musica')

    is_playlist = verify_list(url)
    if is_playlist:
        itens_to_download = all_music_quest(is_playlist)
        print(f"{s.BLUE}Baixando {'Videos' if download_type == 1 else 'Musicas'}")
        messager.blue_line()
    else:
        itens_to_download = [url]
        print(f"{s.BLUE}baixando {'Video' if download_type == 1 else 'Musica'}")
        messager.blue_line()

    for url_stream in itens_to_download:
        yt.download(download_type, url_stream, directory)


if __name__ == "__main__":
    main()
# https://www.youtube.com/watch?v=fitLjLcxmJs&list=PLbSR09XJIO4Fb53XWjBnCF3sI94fGkw09&index=1
