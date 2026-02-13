import os
import subprocess
import sys
import venv

WORKSPACE_DIR = "zephyr-hydrogreen-workspace"
MANIFEST_URL = "https://github.com/hydrogreenpollub/zephyr-manifest.git"
MANIFEST_DEST = "zephyr-manifest"

def run(cmd, cwd=None):
    subprocess.check_call(cmd, shell=True, cwd=cwd)

if os.path.exists(WORKSPACE_DIR):
    sys.exit(f"Error: Directory {WORKSPACE_DIR} already exists.")

os.makedirs(WORKSPACE_DIR)
os.chdir(WORKSPACE_DIR)

print(f"\n=== Setting up workspace in {os.getcwd()} ===")
venv.create(".venv", with_pip=True)

if sys.platform == "win32":
    pip = os.path.join(".venv", "Scripts", "pip")
    west = os.path.join(".venv", "Scripts", "west")
else:
    pip = os.path.join(".venv", "bin", "pip")
    west = os.path.join(".venv", "bin", "west")

run(f"{pip} install west ninja")
run(f"git clone {MANIFEST_URL} {MANIFEST_DEST}")
run(f"{west} init -l {MANIFEST_DEST}")
run(f"{west} update")

if os.path.exists("zephyr"):
    run(f"{west} zephyr-export")
    run(f"{pip} install -r zephyr/scripts/requirements.txt")

print("\n=== Setup Complete ===")