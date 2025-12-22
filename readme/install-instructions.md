## Installation

## Demo video

![](https://hc-cdn.hel1.your-objectstorage.com/s/v3/1da403915c4342d8_demo.webp)

## Instructions

This project uses standard multimedia tools that your package manager already knows how to install:

**Mac:**

```bash
brew install ffmpeg chafa yt-dlp
uv run https://raw.githubusercontent.com/JBlitzar/chafa-yt/main/main.py
```

**Linux:**

```bash
sudo apt install ffmpeg chafa yt-dlp  # or pacman -S, or dnf install
uv run https://raw.githubusercontent.com/JBlitzar/chafa-yt/main/main.py
```

**Why not a single executable?**
Because ffmpeg, chafa, and yt-dlp are system tools, not Python libraries. Your package manager already handles them better than any bundled executable could. This is intentional design.

<details>
<summary>Want automation anyway?</summary>

Try the experimental bootstrap script

```bash
curl -sSL https://raw.githubusercontent.com/JBlitzar/chafa-yt/main/bootstrap.py | python3
```

</details>
