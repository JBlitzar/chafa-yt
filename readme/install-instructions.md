# Installation instructions

_A fork in the road appears_

1. I can read and am okay with installing a few dependencies (recommended)

   1. Go [here](real-installation-instructions.md)!

2. I want a script to do things for me (experimental)

```bash
curl -sSL https://raw.githubusercontent.com/JBlitzar/chafa-yt/main/bootstrap.py | python3
```

<details>
  <summary>Why does it have to be this way?</summary>

If I could make a really easy binary in Github releases or a `pipx` command, I would. Unfortunately, this project has a lot of _non-python external dependencies_. This makes packaging/bundling non-trivial. Binaries wouldn't be cross-platform. And installation instructions already exist for each of these. Anyways, the bootstrap script is my best try to streamline this. Every system is different.

</details>
