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
                "-i",
                "pipe:0",
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
    }

    #subtitles {
        text-align: center;
        border: round white;
        width: auto;
    }


    """

    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.streamer = Streamer(url, self.update_frame)
        self.frame_widget = Static(" " * 20 + "Loading..." + " " * 20, id="frame")
        self.perf_widget = Static("", id="perf")
        self.subtitles_widget = Label("subtitles go here...", id="subtitles")
        self.last_updated = time.time()
        self.progress = ProgressBar(
            total=Streamer.get_duration(url), show_eta=False, show_percentage=True
        )

    def on_mount(self):
        self.log("App mounted")
        self.subtitles_data = Streamer.get_subtitles(self.url)

    def get_current_subtitle(self, frame_count):
        current_time_ms = (frame_count / 30) * 1000
        for start, end, text in self.subtitles_data:
            if start <= current_time_ms <= end:
                return text
        return ""

    def update_frame(self, frame_str, perf=None, frame_count=0):
        text = Text.from_ansi(frame_str)
        self.call_from_thread(self.frame_widget.update, text)

        self.progress.progress = frame_count

        self.perf_widget.update(
            f"dt: {time.time() - self.last_updated:.3f}s | {perf} | {1 / (time.time() - self.last_updated):.3f} fps"
        )

        self.subtitles_widget.update(f"{self.get_current_subtitle(frame_count)}")

        self.last_updated = time.time()

    def compose(self) -> ComposeResult:
        with Vertical(id="v1"):
            with Vertical(id="video-container"):
                yield Static(
                    f"Streaming video from YouTube ID: {self.url}", id="header"
                )
                yield self.frame_widget
                with Center(id="subtitles-container"):
                    yield self.subtitles_widget
                yield self.progress
                yield self.perf_widget

            yield Footer()


if __name__ == "__main__":
    app = ChafaYTApp("dQw4w9WgXcQ")
    app.run()
