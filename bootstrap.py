import os
import subprocess
import sys
import venv

WORKSPACE_DIR = "zephyr-hydrogreen-workspace"
MANIFEST_URL = "https://github.com/hydrogreenpollub/zephyr-manifest.git"
MANIFEST_DEST = "zephyr-manifest"

def run(cmd, cwd=None):
    print(f"--> Executing: {cmd}")
    subprocess.check_call(cmd, shell=True, cwd=cwd)

if not os.path.exists(WORKSPACE_DIR):
    os.makedirs(WORKSPACE_DIR)

os.chdir(WORKSPACE_DIR)

if not os.path.exists(".venv"):
    venv.create(".venv", with_pip=True)

if sys.platform == "win32":
    pip_exe = os.path.join(".venv", "Scripts", "pip")
    west_exe = os.path.join(".venv", "Scripts", "west")
else:
    pip_exe = os.path.join(".venv", "bin", "pip")
    west_exe = os.path.join(".venv", "bin", "west")

run(f"{pip_exe} install -U west ninja")

if not os.path.exists(MANIFEST_DEST):
    run(f"git clone {MANIFEST_URL} {MANIFEST_DEST}")
else:
    run("git pull", cwd=MANIFEST_DEST)

if not os.path.exists(".west"):
    run(f"{west_exe} init -l {MANIFEST_DEST}")

run(f"{west_exe} update")

if os.path.exists("zephyr"):
    run(f"{west_exe} zephyr-export")
    req_file = os.path.join("zephyr", "scripts", "requirements.txt")
    if os.path.exists(req_file):
        run(f"{pip_exe} install -r {req_file}")

print("\n=== Setup Complete ===")