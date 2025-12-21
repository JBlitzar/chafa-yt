## Quickstart

> [!IMPORTANT]
> Do not skip installing the dependencies! 'twill not work without them. Chafa especially is not something a whole lot of people have installed on their system.

- Install dependencies: [`uv`](https://docs.astral.sh/uv/getting-started/installation/), [`ffmpeg`](https://www.ffmpeg.org/download.html), [`yt-dlp`](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#installation) and [`chafa`](https://hpjansson.org/chafa/download/)
  - **Mac**

```bash
# install homebrew if not already
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install ffmpeg chafa yt-dlp; curl -LsSf https://astral.sh/uv/install.sh | sh
```

- **Linux (untested, please report issues)**:

```bash
sudo apt install ffmpeg chafa yt-dlp && curl -LsSf https://astral.sh/uv/install.sh | sh

# For Arch
sudo pacman -S ffmpeg chafa yt-dlp && curl -LsSf https://astral.sh/uv/install.sh | sh

```

- **Windows (untested, please report issues)**:
  - _in powershell_

```powershell
scoop install ffmpeg chafa yt-dlp && irm https://astral.sh/uv/install.ps1 | iex

```

- Run it!!

```bash
uv run https://raw.githubusercontent.com/JBlitzar/chafa-yt/refs/heads/main/main.py
```

> [!TIP]
> Append a youtube URL of your choice to play a different video or append --help to view more information.
