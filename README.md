![Logo](Title/logo.png)

# Kissa - Simple YouTube Music Downloader

A simple CLI application for Linux that downloads songs, albums, and playlists from YouTube Music using system-installed `yt-dlp` and `ffmpeg`.

The application automatically:

* Downloads the best available audio quality
* Converts audio to MP3, FLAC, M4A, OPUS, or WAV
* Embeds metadata (artist, album, track title, etc.)
* Embeds album artwork
* Creates a clean music library structure

## Features

* No Python dependencies required
* Uses system-installed `yt-dlp` and `ffmpeg`
* Automatic artist/album folder structure
* Album artwork embedding

## Requirements

### Debian / Ubuntu

```bash
sudo apt install yt-dlp ffmpeg
```

### Arch Linux

```bash
sudo pacman -S yt-dlp ffmpeg
```

### Fedora

```bash
sudo dnf install yt-dlp ffmpeg
```

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/musicdl.git
cd Kissa
```

Make the script executable:

```bash
chmod +x kissa.py
```

## Usage

### Download a single track

```bash
./kissa.py "https://music.youtube.com/watch?v=VIDEO_ID"
```

### Download an album

```bash
./kissa.py "https://music.youtube.com/playlist?list=ALBUM_ID"
```

### Download a playlist

```bash
./kissa.py "https://music.youtube.com/playlist?list=PLAYLIST_ID"
```

### Save to a custom directory

```bash
./kissa.py URL -o ~/Music
```

### Download as FLAC

```bash
./kissa.py URL --format flac
```

### Use browser cookies

Firefox:

```bash
./kissa.py URL --browser-cookies firefox
```

Chrome:

```bash
./kissa.py URL --browser-cookies chrome
```

Chromium:

```bash
./kissa.py URL --browser-cookies chromium
```

## Output Structure

MusicDL automatically organizes downloads into a music library structure:

```text
Music/
└── Artist/
    └── Album (Year)/
        ├── cover.jpg
        ├── 01 - Track Name.mp3
        ├── 02 - Track Name.mp3
        └── ...
```

## Supported Audio Formats

* mp3
* flac
* m4a
* opus
* wav

Example:

```bash
./kissa.py URL --format flac
```

## Example

```bash
./kissa.py \
"https://music.youtube.com/playlist?list=OLAK5uy_xxxxx" \
--format mp3 \
-o ~/Music \
--browser-cookies firefox
```
