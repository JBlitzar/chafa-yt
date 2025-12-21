# chafa-yt

Play Youtube videos in the terminal with Chafa!

## Quickstart

> [!IMPORTANT]
> Do not skip installing the dependencies! 'twill not work without them. Chafa especially is not something a whole lot of people have installed on their system.

- Install dependencies: [`uv`](https://docs.astral.sh/uv/getting-started/installation/), [`ffmpeg`](https://www.ffmpeg.org/download.html), and [`chafa`](https://hpjansson.org/chafa/download/)
  - On mac, `brew install ffmpeg chafa; curl -LsSf https://astral.sh/uv/install.sh | sh`
- Run it!!

  ```bash
    uv run https://raw.githubusercontent.com/JBlitzar/chafa-yt/refs/heads/main/main.py
  ```

  > [!TIP]
  > Append a youtube URL of your choice to play a different video or append --help to view more information.

## Installation for development

- Git clone and `uv sync`. Then `uv run main.py` as usual.
