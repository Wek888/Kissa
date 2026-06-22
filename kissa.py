#!/usr/bin/env python3

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    missing = []

    for prog in ("yt-dlp", "ffmpeg"):
        if shutil.which(prog) is None:
            missing.append(prog)

    if missing:
        print(
            f"Отсутствуют зависимости: {', '.join(missing)}",
            file=sys.stderr
        )
        sys.exit(1)

def sanitize(text):
    if not text:
        return "Unknown"

    text = str(text)

    text = re.sub(r'[<>:"/\\|?*]', "_", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def get_info(url):
    cmd = [
        "yt-dlp",
        "--dump-single-json",
        "--flat-playlist",
        url
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    return json.loads(result.stdout)

def detect_album_info(info):
    artist = (
        info.get("album_artist")
        or info.get("artist")
        or info.get("uploader")
        or "Unknown Artist"
    )

    album = (
        info.get("album")
        or info.get("title")
        or "Unknown Album"
    )

    year = (
        str(info.get("release_year"))
        if info.get("release_year")
        else None
    )

    if not year:
        release_date = info.get("release_date")

        if release_date and len(release_date) >= 4:
            year = release_date[:4]

    if not year:
        year = "0000"

    return (
        sanitize(artist),
        sanitize(album),
        year
    )

def download(url, root_dir, audio_format):
    info = get_info(url)

    artist, album, year = detect_album_info(info)

    album_dir = root_dir / artist / f"{album} ({year})"
    album_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nКаталог: {album_dir}\n")

    output_template = str(
        album_dir /
        "%(track_number,playlist_index|1)02d - %(title)s.%(ext)s"
    )

    cmd = [
        "yt-dlp",

        "-f",
        "bestaudio/best",

        "--extract-audio",

        "--audio-format",
        audio_format,

        "--audio-quality",
        "0",

        "--embed-thumbnail",

        "--embed-metadata",

        "--add-metadata",

        "--write-thumbnail",

        "--convert-thumbnails",
        "jpg",

        "--no-overwrites",

        "-o",
        output_template,

        url,
    ]

    result = subprocess.run(cmd)

    if result.returncode != 0:
        sys.exit(result.returncode)

    print("\nГотово.")
    print(f"Файлы сохранены в: {album_dir}")

def main():
    parser = argparse.ArgumentParser(
        description="Kissa - Simple YouTube Music Downloader"
    )

    parser.add_argument(
        "url",
        help="Ссылка на трек, альбом или плейлист YouTube Music"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="Music",
        help="Корневой каталог"
    )

    parser.add_argument(
        "--format",
        default="mp3",
        choices=[
            "mp3",
            "m4a",
            "opus",
            "flac",
            "wav"
        ],
        help="Формат аудио"
    )

    args = parser.parse_args()

    check_dependencies()

    root_dir = Path(args.output).expanduser()

    download(
        args.url,
        root_dir,
        args.format
    )


if __name__ == "__main__":
    main()