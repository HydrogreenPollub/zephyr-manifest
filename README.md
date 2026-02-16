# Hydrogreen Zephyr manifest
This repository serves as the T3 topology manifest for the hydrogreen zephyr workspace. It automates the setup of the entire development environment, including the zephyr RTOS kernel, modules, and all application repositories.

## Prerequisites (Windows only)
If you are on windows, ensure you have chocolatey and the required system tools installed before proceeding.

### Install chocolatey
Run powershell as administrator and execute the following command:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('[https://community.chocolatey.org/install.ps1](https://community.chocolatey.org/install.ps1)'))
```

### Install system libraries
Once chocolatey is installed, run these commands in the same administrator powershell window to install python and build dependencies:

```powershell
# Install specific python version
choco install python --version=3.13.11 --allow-downgrade -y

# Install build tools
choco upgrade cmake ninja gperf git dtc-msys2 wget 7zip putty openocd gh protoc -y
```

## Quick start (bootstrap)
To initialize the full workspace, navigate to your projects folder and run the bootstrap script. This handles cloning, west initialization, virtual environment creation, and dependency installation automatically.

### Windows (powershell)
```powershell
irm [https://raw.githubusercontent.com/HydrogreenPollub/zephyr-manifest/refs/heads/main/bootstrap.py](https://raw.githubusercontent.com/HydrogreenPollub/zephyr-manifest/refs/heads/main/bootstrap.py) | python
```

### Linux / macOS (bash)
```bash
curl -fsSL [https://raw.githubusercontent.com/HydrogreenPollub/zephyr-manifest/refs/heads/main/bootstrap.py](https://raw.githubusercontent.com/HydrogreenPollub/zephyr-manifest/refs/heads/main/bootstrap.py) | python3
```

## Workspace structure
After bootstrapping, your `zephyr-hydrogreen-workspace` directory will be organized as follows:

```text
zephyr-hydrogreen-workspace/
├── .venv/                          # Python virtual environment
├── .west/                          # West configuration
├── modules/                        # Zephyr modules (HALs, drivers)
├── zephyr/                         # Zephyr RTOS kernel
├── zephyr-can-converter-unit/      # (CCA) Can converter app
├── zephyr-fuel-cell-control-unit/  # (FCCU) Fuel cell control app
├── zephyr-lighting-control-unit/   # (LCU) Lighting control app
├── zephyr-steering-wheel-unit/     # (SWU) Steering wheel app
└── zephyr-manifest/                # Manifest repository
```

## IDE configuration (clion)
If you are using CLion, follow these steps to finalize the setup:

1. **Configure toolchain:**
   * Go to **Settings** > **Build, Execution, Deployment** > **Toolchains**.
   * Ensure the "System" toolchain is selected (or configure MinGW if needed).

2. **J-Link setup:**
   * Go to **Settings** > **Build, Execution, Deployment** > **Debugger** > **Embedded Development**.
   * Verify that the path to the **J-Link Debug Server** executable is correct.

3. **Run/debug configuration:**
   * When creating a configuration, select **Embedded GDB Server**.
   * If the target executable is missing, manually select `zephyr_final` from the build directory.

