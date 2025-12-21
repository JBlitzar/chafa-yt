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

_To the Shipwrights: Is there a Github release? No. Is there a single `pipx` command? No. It's a python CLI tool with external dependencies (not just pip packages). This is the easiest installation method I could come up with. It's arguably less ergonomic to make a `pyinstaller` binary. If you have ideas, please do let me know!_
