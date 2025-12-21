# chafa-yt

A YouTube TUI! Featuring a sophisticated UI, real-time video playback, subtitles, and a progress indicator.

<img src="readme/demo.png">

Advantages:

- No ads
- Looks cool
- In the terminal
- Blazingly fast 30fps at the innovative 80x24 resolution
- Full 24-bit color
- Support open source
- Is cool

## Quickstart


https://github.com/user-attachments/assets/824d5e60-3cc8-42c2-ac1d-2638da33850b


> [!IMPORTANT]
> Do not skip installing the dependencies! 'twill not work without them. Chafa especially is not something a whole lot of people have installed on their system.

- Install dependencies: [`uv`](https://docs.astral.sh/uv/getting-started/installation/), [`ffmpeg`](https://www.ffmpeg.org/download.html), [`yt-dlp`](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#installation) and [`chafa`](https://hpjansson.org/chafa/download/)
  - On mac, assuming brew is installed, you can run: `brew install ffmpeg chafa yt-dlp; curl -LsSf https://astral.sh/uv/install.sh | sh`
- Run it!!

```bash
uv run https://raw.githubusercontent.com/JBlitzar/chafa-yt/refs/heads/main/main.py
```

> [!TIP]
> Append a youtube URL of your choice to play a different video or append --help to view more information.

## How this works

> _Sometimes in life, the best solution is to use pre-existing libraries_ - Sun Tzu, the Art of Software Development

Pipes `yt-dlp` to `ffmpeg` to `chafa` to `textual` to your eyeballs!

Read all about it in `main.py`. TUI code is in `ChafaYTApp`, streaming code is in `Streamer`.

Have a feature request? An implementation idea? Issues / PRs are open. If you like this project, please do leave a star, it would mean a lot to me.

## Installation for development

- Git clone and `uv sync`. Then `uv run main.py` as usual.
