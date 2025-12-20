import os
import tempfile
import re
import subprocess
import threading
import time


file = "/tmp/frame.png"
url = input("Enter the URL: ")  # https://www.youtube.com/watch?v=dQw4w9WgXcQ
if url == "":
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

url = re.match(r"(.+youtube\.com\/watch\?v=)?([a-zA-Z0-9]{11}).*", url).group(2)


def download_and_extract_frames():
    ytdl_process = subprocess.Popen(
        [
            "yt-dlp",
            "-f",
            "bestvideo[height<=240][fps<=30]",
            "-o",
            "-",
            url,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    ffmpeg_process = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            "pipe:0",
            "-vf",
            "fps=30",
            "-f",
            "image2pipe",
            "-vcodec",
            "png",
            "pipe:1",
        ],
        stdin=ytdl_process.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    PNG_HEADER = b"\x89PNG\r\n\x1a\n"
    EOF = b"IEND\xae\x42\x60\x82"

    frame_data = bytearray()
    while True:
        chunk = ffmpeg_process.stdout.read(4096)
        if not chunk:
            break

        frame_data += chunk

        if EOF in frame_data:
            end_idx = frame_data.find(EOF) + len(EOF)
            complete_frame = bytes(frame_data[:end_idx])
            frame_data = frame_data[end_idx:]

            print("\033[H", end="", flush=True)

            subprocess.run(["chafa", "-"], input=complete_frame)

            # time.sleep(1 / 20)


download_and_extract_frames()
