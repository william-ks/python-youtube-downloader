# About the Program

This Python script is designed to download videos and audio (music) directly from YouTube links.

The project is still under development, which may cause some bugs. Please see the Troubleshooting section for common issues and the Contributing section to report new ones.

## Features

- Download single YouTube videos.
- Download entire YouTube playlists.
- Convert downloaded videos to audio (e.g., MP3).
- Cross-platform compatibility (Windows, macOS, Linux - requires Python and FFmpeg).
- Ease of use (interactive command-line interface).

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

First, you need **Python 3.7+**, which can be downloaded from [python.org](https://www.python.org/).
After installing Python, install the necessary libraries from the `requirements.txt` file using the command:

```bash
pip install -r requirements.txt
```

## How to Use:

When you run the script using `python main.py`, it will guide you through the download process interactively.

### Downloading a Single Video or Song:
1.  Start the program:
    ```bash
    python main.py
    ```
2.  The script will display a welcome message and ensure `ffmpeg` (for audio conversion) is available, downloading it if necessary.
3.  Paste the YouTube URL for the video or song when prompted and press Enter.
    ![Program Interface](image-1.png)
    *(Note: The image above shows the initial URL prompt. The script will subsequently ask you to choose the download format (Audio/Video) and handle playlist options as described below.)*
4.  You will then be asked to choose the download format:
    *   **Audio (MP3):** Select this to download and convert the content to an MP3 audio file.
    *   **Video (MP4):** Select this to download the content as an MP4 video file.
5.  The download will begin, and the file will be saved in the `downloads` folder.

### Downloading a Playlist:
1.  Start the program as described above.
2.  Paste the YouTube playlist URL when prompted. The playlist **must be public** for the script to access its contents.
3.  The script will detect that the URL is a playlist and ask for your preference:
    *   **Download ENTIRE playlist:** Choose this to download all videos/songs in the playlist.
    *   **Download ONLY the current video:** If the playlist URL also points to a specific video within the playlist, choose this to download only that single video.
    *   **Cancel:** Stop the download process.
4.  If you choose to download (either the entire playlist or a single video from it), you will then be prompted to select the format (Audio MP3 or Video MP4), similar to a single item download.
5.  The files will be downloaded to the `downloads` folder.

## Troubleshooting

Here are solutions to common issues you might encounter:

### 1. FFmpeg Download Issues
-   **Context:** The script attempts to download `ffmpeg` automatically on its first run, which is necessary for audio conversion. The script looks for `ffmpeg.exe` (on Windows) or `ffmpeg` (on macOS/Linux) within a `./tools/ffmpeg/bin` directory relative to the script.
-   **Solution:**
    *   Ensure you have a stable internet connection when running the script for the first time.
    *   Try running the script again; the download might have failed due to a temporary glitch.
    *   If the automatic download continues to fail, you can download `ffmpeg` manually from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html). After downloading, you can either:
        *   Place the `ffmpeg.exe` (or `ffmpeg` binary) directly into a folder structure like `./tools/ffmpeg/bin/` relative to the script.
        *   Or, add the `bin` directory of your manual `ffmpeg` installation to your system's PATH environment variable.

### 2. Playlist Download Issues
-   **Privacy:** Playlists **must be public**. Private or unlisted playlists cannot be accessed by the script.
-   **Individual Video Failures:** Sometimes, a playlist download might fail or hang due to issues with a specific video within that playlist (e.g., it's deleted, private, or region-restricted). Try downloading other videos from the playlist or a single video from the playlist to see if the issue is isolated.

### 3. General Download Failures
-   **Internet Connection:** A stable internet connection is crucial. Check your connection if downloads fail repeatedly.
-   **Restricted Content:** Some YouTube videos are region-restricted, private, or have other settings that prevent downloading through third-party scripts. These may not be downloadable.
-   **Try Again:** Sometimes, download issues are temporary. It's often worth trying the download again after a few moments.

### 4. Outdated Libraries
-   **Problem:** Old versions of downloaded libraries (especially `yt-dlp`) can cause unexpected errors as YouTube frequently updates its platform.
-   **Solution:** Keep your libraries updated by running the following command in your terminal, in the script's directory:
    ```bash
    pip install --upgrade -r requirements.txt
    ```

### 5. Reporting Bugs
-   If you encounter a persistent issue that isn't covered here, please consider opening an issue on the project's GitHub issues page: [https://github.com/william-ks/python-youtube-downloader/issues](https://github.com/william-ks/python-youtube-downloader/issues).
-   When reporting, please provide as much detail as possible, including:
    *   The exact YouTube link (URL) you were trying to download.
    *   The error message(s) you received.
    *   The steps you took before the error occurred.
    *   Your operating system.

## Contributing

We welcome contributions to improve this project! Here's how you can help:

### Reporting Bugs
-   **Check Existing Issues:** Before submitting a new bug report, please check the [GitHub Issues](https://github.com/william-ks/python-youtube-downloader/issues) to see if someone has already reported it.
-   **Provide Details:** If the bug hasn't_been reported, open a new issue. Please include:
    *   Clear steps to reproduce the bug.
    *   Any error messages you received.
    *   Your operating system (e.g., Windows 10, Ubuntu 20.04).
    *   Your Python version (e.g., Python 3.9.5).
    *   The YouTube link(s) that caused the problem.

### Suggesting Enhancements
-   **Clear Description:** If you have an idea for a new feature or an improvement to an existing one, please open an issue on [GitHub Issues](https://github.com/william-ks/python-youtube-downloader/issues).
-   Provide a clear and detailed explanation of the enhancement, why it would be beneficial, and if possible, suggest how it might be implemented.

### Pull Requests
We are happy to review pull requests (PRs) for bug fixes and features. Please follow this basic workflow:
1.  **Fork the Repository:** Create your own copy of the project at [https://github.com/william-ks/python-youtube-downloader](https://github.com/william-ks/python-youtube-downloader).
2.  **Create a Branch:** Make a new branch in your fork for your changes. Use a descriptive name:
    ```bash
    git checkout -b feature/YourAmazingFeatureName
    # or for bug fixes:
    git checkout -b fix/IssueDescriptionOrNumber
    ```
3.  **Make Your Changes:** Implement your feature or bug fix.
4.  **Commit Your Changes:** Write clear and concise commit messages:
    ```bash
    git commit -m "Add: Implement YourAmazingFeatureName"
    # or for fixes:
    git commit -m "Fix: Resolve bug #123 by doing X"
    ```
5.  **Push to Your Branch:**
    ```bash
    git push origin feature/YourAmazingFeatureName
    ```
6.  **Open a Pull Request:** Go to the original repository on GitHub and open a new Pull Request from your forked branch.
    *   Reference any relevant issues in your PR description (e.g., "Closes #123").

### Coding Standards
-   **PEP 8:** Please try to follow [PEP 8 guidelines](https://www.python.org/dev/peps/pep-0008/) for Python code.
-   **Commit Messages:** Write meaningful commit messages that explain the "what" and "why" of your changes.
-   **Keep it Simple:** Aim for clear and readable code.

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.