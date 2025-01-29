# About the Program
This Python script is designed to download music and videos directly from a YouTube link.

The project is still under development, which may cause some bugs.

## Downloading with Git:

```bash
git clone https://github.com/william-ks/python-youtube-downloader.git
```

```bash
cd python-youtube-downloader
```

## Downloading without Git:

Click the green `Code` button and then click `Download ZIP`.

![Download ZIP](image.png)

After the download is complete, unzip the ZIP file and open the terminal inside the folder.

## Configuration
First, we need **Python 3.7+**, which can be downloaded from [here](https://www.python.org/). After installing Python, we need to install the libraries from the _requirements.txt_ file using the command:

```bash
pip install -r requirements.txt
```

## Useful Information:
- The first time you run the script, it will download `ffmpeg`, which we will use to convert videos to music.

## How to Use:

### Downloading a Single Song:
To download a single song, start the program with the command:

```bash
python main.py
```

You will see something similar to the image below:

![Program Interface](image-1.png)

Simply paste the song link and press `ENTER`.

### Downloading a Playlist:

The steps to download a playlist are basically the same. The only difference is that the playlist needs to be public. The script will recognize that it is a playlist and ask if you want to download all the songs.