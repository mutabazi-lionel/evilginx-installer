import urllib.request
import os
import json
import zipfile
from typing import  Optional
def downloading_evil_gnix (working_directory):
    """Fetches the latest release of Evil_ginx from GitHub and downloads it."""
    api_url="https://api.github.com/repos/kgretzky/evilginx2/releases/latest"
    try:
        print("[⏳] Fetching latest Evil_ginx release info...")
        with urllib.request.urlopen(api_url) as response:
            data= json.load(response)
            assets = data.get("assets", [])
            tarball_url = None
            for asset in assets:
                if asset["name"].endsWith("linux-64bit.zip"):
                    tarball_url = asset["browser_download_url"]
                    break
            if not tarball_url:
                print("[✘] Could not find suitable download for Evil_ginx.")
                return None
            file_name = tarball_url.split("/")[-1]
            destination_path = os.path.join(working_directory, file_name)
            if os.path.exists(destination_path):
                print(f"[✔] Archive already downloaded at {destination_path}")
                return destination_path
            print(f"[↓] Downloading from {tarball_url} ...")
            urllib.request.urlretrieve(tarball_url, destination_path)
            print(f"[✔] Download completed: ...")
            return destination_path
    except Exception as e:
        print(f"[✘] Failed to fetch or download Evil_ginx : {e}")
        return  None

def unzip_evil_ginx(zip_path: str, extract_to: str) -> Optional[str]:
    """Unzips the Evil_ginx archive into the working directory securely."""
    print(f"[📦] Extracting {zip_path} to {extract_to}...")
    if not zip_path.endswith(".zip") or not os.path.isfile(zip_path):
        print("[✘] Invalid archive path.")
        return None

    try:
        # Validate the zip file content paths (ZIP Slip protection)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                member_path = os.path.abspath(os.path.join(extract_to, member))
                if not member_path.startswith(os.path.abspath(extract_to)):
                    print(f"[✘] Unsafe path inside archive: {member}")
                    return None
            zip_ref.extractall(path=extract_to)
        print("[✔] Extraction completed.")
        return extract_to
    except zipfile.BadZipFile:
        print("[✘] Invalid ZIP archive.")
    except Exception as e:
        print(f"[✘] Extraction error: {e}")
    return None


