import shlex
import subprocess
import sys
import venv
from pathlib import Path

DEFAULT_NAME = "zephyr-hydrogreen-workspace"
MANIFEST_URL = "https://github.com/hydrogreenpollub/zephyr-manifest.git"
MANIFEST_DEST = "zephyr-manifest"


def run(cmd, cwd):
    args = [str(arg) for arg in cmd]
    print(f"[bootstrap.py] Running: {subprocess.list2cmdline(args)}", flush=True)
    subprocess.run(args, check=True, cwd=cwd)


def main():
    name = input(f"[bootstrap.py] Enter workspace name [{DEFAULT_NAME}]: ").strip()

    workspace = Path(name or DEFAULT_NAME).expanduser().resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    print("\n[bootstrap.py] [1/5] Preparing Python environment", flush=True)
    venv_dir = workspace / ".venv"
    if not venv_dir.exists():
        venv.create(venv_dir, with_pip=True)

    python = venv_dir / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    pip = [python, "-m", "pip"]
    west = [python, "-m", "west"]

    run([*pip, "install", "-U", "west", "ninja"], workspace)

    print("\n[bootstrap.py] [2/5] Updating manifest repository", flush=True)
    manifest = workspace / MANIFEST_DEST
    if not manifest.exists():
        run(["git", "clone", MANIFEST_URL, MANIFEST_DEST], workspace)
    else:
        run(["git", "pull"], manifest)

    print("\n[bootstrap.py] [3/5] Updating workspace repositories", flush=True)
    if not (workspace / ".west").exists():
        run([*west, "init", "-l", MANIFEST_DEST], workspace)

    run([*west, "update"], workspace)

    print("\n[bootstrap.py] [4/5] Installing Zephyr dependencies and exporting CMake package", flush=True)
    run([*pip, "install", "-r", workspace / "zephyr/scripts/requirements.txt"], workspace)
    run([*west, "zephyr-export"], workspace)

    print("\n[bootstrap.py] [5/5] Installing ARM and ESP32-S3 toolchains", flush=True)
    run([*west, "sdk", "install", "-t", "arm-zephyr-eabi"], workspace)
    run([*west, "sdk", "install", "-t", "xtensa-espressif_esp32s3_zephyr-elf"], workspace)

    print("\n[bootstrap.py] Setup complete.")
    print(f"[bootstrap.py] Workspace: {workspace}")
    print("[bootstrap.py] Activate the environment in your terminal:")

    if sys.platform == "win32":
        activation = str(venv_dir / "Scripts/Activate.ps1").replace("'", "''")
        print(f"  & '{activation}'")
    else:
        print(f"  source {shlex.quote(str(venv_dir / 'bin/activate'))}")


if __name__ == "__main__":
    main()
