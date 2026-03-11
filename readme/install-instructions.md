## Installation

## To the shipwrights

Don't reject this because it's a markdown, I've discussed this before with the team and they've determined that this is the best way forward for this project.

https://hackclub.slack.com/archives/C099P9FQQ91/p1769214202506129

## Demo video

![](https://user-cdn.hackclub-assets.com/019cdad2-dec4-7683-8606-addad6dd31d1/demo.webp)

## Instructions

This project uses standard multimedia tools that your package manager already knows how to install:

> [!TIP]
> You may also need to install `uv` if you haven't already: https://docs.astral.sh/uv/getting-started/installation/

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

## Usage

> [!TIP]
> Use a more modern terminal emulator like Ghostty for better colors (but it should work on the default terminal, too)

```bash
# Default
uv run https://raw.githubusercontent.com/JBlitzar/chafa-yt/main/main.py


# Custom video (use quotes!)
uv run https://raw.githubusercontent.com/JBlitzar/chafa-yt/main/main.py "https://youtube.com/watch?v=..."

# See all options
uv run https://raw.githubusercontent.com/JBlitzar/chafa-yt/main/main.py --help
# (Press 'q' to exit help)

# Exit the player
Press Ctrl+Q
```
