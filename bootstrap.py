import sys
import shutil
import os

required = ["ffmpeg", "chafa", "yt-dlp", "uv"]

install_links = {
    "ffmpeg": "https://ffmpeg.org/download.html",
    "chafa": "https://hpjansson.org/chafa/download/",
    "yt-dlp": "https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#installation",
    "uv": "https://docs.astral.sh/uv/getting-started/installation/",
}
missing = [cmd for cmd in required if not shutil.which(cmd)]
if missing == []:
    print("You're all set!")
    print(
        "Now run: \nuv run https://raw.githubusercontent.com/JBlitzar/chafa-yt/refs/heads/main/main.py"
    )
    print(
        "Append a youtube URL of your choice to play a different video or append --help to view more information."
    )
    exit(0)

is_windows = sys.platform.startswith("win")
is_mac = sys.platform.startswith("darwin")
is_arch = os.path.exists("/etc/arch-release")
is_linux = (
    sys.platform.startswith("linux") and not is_arch and shutil.which("apt") is not None
)


def prompt_install(pkg):
    cmd = None
    if pkg == "uv":
        if is_windows:
            cmd = """powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" """
        elif is_mac or is_linux or is_arch:
            cmd = """curl -LsSf https://astral.sh/uv/install.sh | sh"""
    else:
        if is_mac:
            cmd = f"brew install {pkg}"
        elif is_linux:
            cmd = f"sudo apt install {pkg}"
        elif is_arch:
            cmd = f"sudo pacman -S {pkg}"
        elif is_windows:
            cmd = f"scoop install {pkg}"

    if cmd is None:
        print(
            f"uhh I don't know how to install {pkg} on your system. Please install it manually. See: {install_links.get(pkg, 'No link available (should never happen)')}"
        )
        exit(1)
    response = input(f"Do you want to install {pkg}?\nWill run: `{cmd}`\n (y/n): ")
    if response.lower() == "y":
        result = os.system(cmd)
        if result != 0:
            print(
                f"uhh failed to install {pkg}. Please install it manually. See: {install_links.get(pkg, 'No link available (should never happen)')}"
            )
            exit(1)

    else:
        print(
            f"Please install {pkg} manually. See: {install_links.get(pkg, 'No link available (should never happen)')}"
        )
        exit(1)


print(f"Missing dependencies: {', '.join(missing)}")
print()
for m in missing:
    prompt_install(m)

print("Verifying install...")
still_missing = [cmd for cmd in required if not shutil.which(cmd)]
for m in still_missing:
    print(
        f"uhh you're still missing {m}, or at least it's not in your PATH. Please install it manually. See: {install_links.get(m, 'No link available (should never happen)')}. If you're absolutely sure it's installed, make sure it's in your PATH too (do you need to reload the shell)"
    )
    exit(1)

print("All dependencies installed! Now run:")
print(
    "uv run https://raw.githubusercontent.com/JBlitzar/chafa-yt/refs/heads/main/main.py"
)
print(
    "Append a youtube URL of your choice to play a different video or append --help to view more information."
)
