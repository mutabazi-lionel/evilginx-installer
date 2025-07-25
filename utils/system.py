"""
utils/system.py
System-related utilities for the Evil_ginx Installer.
This module contains helper functions for:
- Ensuring the script is run as root
- Detecting the Linux distribution from /etc/os-release
"""
import os
import sys
import subprocess
import shutil
from  utils.evilginx import downloading_evil_gnix

def check_root():
    """
    Check if the script is being run as root.
    Exit the program if not.
    """
    if  os.geteuid() == 0 :
        print("[✔] Running script as root.")
        return True
    print("[✘] Please run this script as root.")
    return False

def detect_distro():
    """
    Detect the Linux distribution by reading /etc/os-release.cl
    Returns:
        string: The distribution ID (e.g., 'ubuntu', 'debian', 'arch', etc.)
    """
    distro = "unknown"
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith("ID="):
                    distro = line.strip().split("=")[1].strip('"')
                    break
    except FileNotFoundError:
        print("[✘] Unable to detect Linux distribution (missing /etc/os-release).")
        sys.exit(1)
    print(f"[✔] Detected Linux distro: {distro}")
    return distro


def is_installed (program) :
    """" Check if a program is installed and available in PATH. """
    return shutil.which(program) is not  None
def dep_installation (distro):
    """Installation of dependencies based on the distro if they are not installed """
    required = ["wget", "unzip"]
    missing = [pkg for pkg in required if not is_installed(pkg)]
    if not missing:
        print("[✔] Dependencies checked")
        return
    print(f"[!] Installing missing : {', '.join(missing)}.")
    if distro in ["ubuntu", "debian"]:
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "install ", "-y"] +missing,  check=True)
        print(f"[✔] The {', '.join(missing)} is now installed ... ")
    elif distro in ["fedora", "rhel", "centos"]:
        subprocess.run(["dnf", "install", "-y"] +missing, check=True)
        print(f"[✔] The {', '.join(missing)} is now installed ... ")
    elif distro in ["arch", "manjaro"] :
        subprocess.run(["pacman", "-Sy", "--noconfirm"] +missing, check=True)
        print(f"[✔] The {', '.join(missing)} is now installed ... ")
    else:
        print(f"[✘] Unsupported distro: {distro}")
        sys.exit(1)
    print("[✔] All dependencies are installed.")

def working_directory():
    """Creates and handles the Evil_ginx working directory and starts the download."""
    working_dir = os.path.abspath("/opt/evil_ginx")
    os.makedirs(working_dir, exist_ok=True)
    print(f"[✔] Working directory set to: {working_dir}")
    if not downloading_evil_gnix(working_dir):
        print("[✘] Download failed. Exiting.")
        sys.exit(1)
    return working_dir

