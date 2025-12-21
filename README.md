# chafa-yt

Play Youtube videos in the terminal with Chafa!

<img src="readme/demo.png">

## Quickstart

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

## Installation for development

- Git clone and `uv sync`. Then `uv run main.py` as usual.
