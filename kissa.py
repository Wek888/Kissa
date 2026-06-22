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