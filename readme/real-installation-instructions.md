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

<!-- ## Please read if you are a shipwright

Previous feedback:

> _Hi! Cool project! But for a Python project, it needs to be packaged so others can easily run it. Please provide a compiled executable in a GitHub Release or publish it to PyPI/pipx, then resubmit._

It's less easy to make a fully packaged Github binary or single `pipx` command to run this, since it's a CLI tool _with non-python external dependencies_. I've tried to make these installation instructions as easy as possible: On mac under ideal conditions, it's just two commands. If you have ideas, please do let me know!

Bundling chafa, ffmpeg, and yt-dlp in a pyinstaller build would mean having to manually create tons of unique builds with platform-specific binaries bundled for each. I wouldn't really be able to test this reliably since I have a finite amount of computers available to me, so it's better to just find the installation instructions. For mac, I put a brew command and the uv universal install command. Every distro / os is different-- that's what package managers are for.

thank you 😭 -->
