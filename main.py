import os
import tempfile
import re
import subprocess
import threading
import time
from textual.app import App, ComposeResult
from textual.widgets import Tree, Static, Button, Label
from textual.containers import Horizontal, Vertical, Center
from textual.binding import Binding
from textual.widgets import Footer, ProgressBar
from rich.text import Text
import asyncio
import fire


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
        self.start_time = None
        self.frame_count = 0
        self.target_fps = 30
        self.skipped_frames = 0
        self.thread.start()

    @staticmethod
    def get_title(url):
        result = subprocess.run(
            [
                "yt-dlp",
                "--get-title",
                url,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        title = result.stdout.decode("utf-8").strip()
        return title

    @staticmethod
    def get_subtitles(url):
        result = subprocess.run(
            [
                "yt-dlp",
                "--write-subs",
                "--write-auto-subs",
                "--sub-langs",
                "en",
                "--sub-format",
                "srt",
                "--skip-download",
                "-o",
                "/tmp/subs",
                url,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            with open("/tmp/subs.en.srt", "r") as f:
                a = f.read()
                parts = a.split("\n\n")

                out = []
                for part in parts:
                    sections = part.split("\n")
                    sections = [s for s in sections if s.strip() != ""]
                    # sections[0] = index
                    # sections[1] = timecode
                    # sections[2] = text
                    if len(sections) < 3:
                        continue
                    start = sections[1].split(" --> ")[0]
                    h, m, s, ms = re.match(r"(\d+):(\d+):(\d+),(\d+)", start).groups()
                    start_time = (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(ms)

                    end = sections[1].split(" --> ")[1]
                    h, m, s, ms = re.match(r"(\d+):(\d+):(\d+),(\d+)", end).groups()
                    end_time = (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(ms)

                    text = " ".join(sections[2:])

                    out.append((start_time, end_time, text))
                # print(out)
                return out

        except FileNotFoundError:
            return ""

    @staticmethod
    def get_duration(url):
        result = subprocess.run(
            [
                "yt-dlp",
                "--get-duration",
                url,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        duration_str = result.stdout.decode("utf-8").strip()

        m, s = map(int, duration_str.split(":"))
        return (m * 60 + s) * 30

    def stream(self):
        ytdl_process = subprocess.Popen(
            [
                "yt-dlp",
                "-f",
                "worstvideo",
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
                "-re",
                "-i",
                "pipe:0",
                "-f",
                "image2pipe",
                "-vcodec",
                "png",
                "-r",
                "30",
                "pipe:1",
            ],
            stdin=ytdl_process.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        PNG_HEADER = b"\x89PNG\r\n\x1a\n"
        EOF = b"IEND\xae\x42\x60\x82"

        frame_data = bytearray()
        self.start_time = None
        while True:
            chunk = ffmpeg_process.stdout.read(4096)
            if self.start_time is None:
                self.start_time = time.time()
            if not chunk:
                break

            frame_data += chunk

            if EOF in frame_data:
                end_idx = frame_data.find(EOF) + len(EOF)
                complete_frame = bytes(frame_data[:end_idx])
                frame_data = frame_data[end_idx:]

                self.frame_count += 1

                elapsed = time.time() - self.start_time
                expected_frame = int(elapsed * self.target_fps)

                if self.frame_count < expected_frame - 2:
                    self.skipped_frames += 1
                    continue

                start = time.time()
                chafa = subprocess.run(
                    [
                        "chafa",
                        "--format",
                        "symbols",
                        # "--symbols",
                        # "block",
                        # "-c",
                        # "240",
                        # "--symbols",
                        # "0..fffff-block-border-stipple-dot-geometric",
                        # "--dither",
                        # "bayer",
                        # "--fill",
                        # "braille",
                        "-s",
                        "80x24",
                        "-w",
                        "1",
                    ],
                    input=complete_frame,
                    stdout=subprocess.PIPE,
                )
                out = chafa.stdout.decode("utf-8")

                end = time.time()

                perf = f"chafa dt: {end - start:.3f}s | skipped: {self.skipped_frames}/{self.frame_count} frames ({round(self.skipped_frames / self.frame_count * 100)}%)"

                self.callback(out, perf, self.frame_count)

                # time.sleep(1 / 20)


class ChafaYTApp(App):
    CSS = """
    Screen {
        background: $surface;
        align: center middle;
    }

    ProgressBar {
        color: white;
        width: 100%;
        text-align: center;
    }
    ProgressBar > Bar {
        width: 100%;
    }
    Bar > .bar--bar {
        color: red;
        background: red 30%;
    }
    #frame{
        height: auto;
        width: auto;
        text-align: center;
    }
    #v1{
        align: center middle;
    }
    #h1{
        align: center middle;
    }
    #video-container {
        width: auto;
        align: center middle;
    }
    #header, #perf {
        width: 100%;
    }

    #subtitles-container {
        width: 100%;
        align: center middle;
        height: 3;
    }

    #subtitles {
        text-align: center;
        border: round white;
        width: auto;
    }

    #header{
        border: tall white;
        text-align: center;
    }


    """

    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.streamer = Streamer(url, self.update_frame)
        self.frame_widget = Static(" " * 20 + "Loading..." + " " * 20, id="frame")
        self.perf_widget = Static("", id="perf")
        self.subtitles_widget = Label("Loading...", id="subtitles")
        self.last_updated = time.time()
        self.progress = ProgressBar(
            total=Streamer.get_duration(url), show_eta=False, show_percentage=True
        )

        self.timestamp = Static("", id="timestamp")

        self.title = ""

    async def get_and_set_subtitles(self):
        subtitles = Streamer.get_subtitles(self.url)
        self.subtitles_data = subtitles
        self.subtitles_widget.update("Subtitles loaded.")

    async def get_and_set_title(self):
        title = Streamer.get_title(self.url)
        self.title = title
        header = self.query_one("#header", Static)
        header.update(f"{title}")

    def on_mount(self):
        self.log("App mounted")
        self.subtitles_data = []
        asyncio.create_task(self.get_and_set_subtitles())
        asyncio.create_task(self.get_and_set_title())

        self.frame_widget.loading = True

    def get_current_subtitle(self, frame_count):
        current_time_ms = (frame_count / 30) * 1000
        for start, end, text in self.subtitles_data:
            if start <= current_time_ms <= end:
                return text
        return ""

    def _format_time(self, t):
        m = str(int(t // 60)).zfill(2)
        s = str(int(t % 60)).zfill(2)

        return f"{m}:{s}"

    def update_frame(self, frame_str, perf=None, frame_count=0):
        self.frame_widget.loading = False
        text = Text.from_ansi(frame_str)
        self.call_from_thread(self.frame_widget.update, text)

        self.progress.progress = frame_count

        self.perf_widget.update(
            f"dt: {time.time() - self.last_updated:.3f}s | {perf} | {1 / (time.time() - self.last_updated):.3f} fps"
        )

        self.subtitles_widget.update(f"{self.get_current_subtitle(frame_count)}")
        if self.get_current_subtitle(frame_count) == "":
            self.subtitles_widget.visible = False
        else:
            self.subtitles_widget.visible = True

        self.timestamp.update(
            f"{self._format_time(frame_count / 30)} / {self._format_time(self.progress.total / 30)} s"
        )
        self.last_updated = time.time()

    def compose(self) -> ComposeResult:
        with Vertical(id="v1"):
            with Vertical(id="video-container"):
                yield Static(f"{self.title}", id="header")
                yield Static("")
                yield self.frame_widget
                with Center(id="subtitles-container"):
                    yield self.subtitles_widget
                yield Static("")
                yield self.timestamp
                yield self.progress

                yield self.perf_widget

            # yield Footer()


def main(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
    """Play a YouTube video in the terminal using yt-dlp, ffmpeg, chafa, and textual!

    Args:
        url: The URL of the YouTube video to play
    """
    app = ChafaYTApp(url)
    app.run()


if __name__ == "__main__":
    fire.Fire(main)
