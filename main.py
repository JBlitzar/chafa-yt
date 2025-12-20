import os
import tempfile
import re
import subprocess
import threading
import time
from textual.app import App, ComposeResult
from textual.widgets import Tree, Static, Button
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from textual.widgets import Footer
from rich.text import Text


# file = "/tmp/frame.png"
# url = input("Enter the URL: ")  # https://www.youtube.com/watch?v=dQw4w9WgXcQ
# if url == "":
#     url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# url = re.match(r"(.+youtube\.com\/watch\?v=)?([a-zA-Z0-9]{11}).*", url).group(2)


class Streamer:
    def __init__(self, url, callback):
        self.url = url
        self.callback = callback
        self.thread = threading.Thread(target=self.stream)
        self.thread.daemon = True
        self.thread.start()

    def stream(self):
        ytdl_process = subprocess.Popen(
            [
                "yt-dlp",
                "-f",
                "bestvideo[height<=240][fps<=30]",
                "-o",
                "-",
                self.url,
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

                # print("\033[H", end="", flush=True)

                chafa = subprocess.run(
                    [
                        "chafa",
                        "--format",
                        "symbols",
                        "--symbols",
                        "block",
                        "--colors",
                        "256",
                        "-s",
                        "80x24",
                        "-",
                    ],
                    input=complete_frame,
                    stdout=subprocess.PIPE,
                )
                out = chafa.stdout.decode("utf-8")

                self.callback(out)

                # time.sleep(1 / 20)


class ChafaYTApp(App):
    CSS = """
    Screen {
        background: $surface;
    }


    """

    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.streamer = Streamer(url, self.update_frame)
        self.frame_widget = Static("", id="frame")

    def on_mount(self):
        self.log("App mounted")

    def update_frame(self, frame_str):
        text = Text.from_ansi(frame_str)
        self.call_from_thread(self.frame_widget.update, text)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static(f"Streaming video from YouTube ID: {self.url}", id="header")
            yield self.frame_widget
            yield Footer()


if __name__ == "__main__":
    app = ChafaYTApp("dQw4w9WgXcQ")
    app.run()
