# chafa-yt

![](https://hackatime-badge.hackclub.com/U099JENAUGP/chafa-yt)

A YouTube TUI! Featuring a sophisticated UI, real-time video playback, subtitles, and a progress indicator.

<img src="readme/demo.png">

Advantages:

- No ads
- Looks cool
- Real streaming, not just predownloading
- In the terminal
- Blazingly fast 30fps at the innovative 80x24 resolution
- Full 24-bit color
- Open-source
- Is cool

## Install

[look here!](readme/install-instructions.md)

## How this works

> _Sometimes in life, the best solution is to use pre-existing libraries_ - Sun Tzu, the Art of Software Development

Pipes `yt-dlp` to `ffmpeg` to `chafa` to `textual` to your eyeballs!

Read all about it in `main.py`. TUI code is in `ChafaYTApp`, streaming code is in `Streamer`.

Have a feature request? An implementation idea? Issues / PRs are open. If you like this project, please do leave a star, it would mean a lot to me.

## Installation for development

- Git clone and `uv sync`. Then `uv run main.py` as usual.
