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