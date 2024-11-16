import os
import platform
import zipfile
from typing import Optional

import requests

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chromedriver_dir = os.path.join(root_dir, "chromedriver")
platform_system_name = platform.system().lower()

def set_chromedriver_permissions(chromedriver_path):
    os.chmod(chromedriver_path, 0o755)
    print(f"Разрешение на chromedriver установлено по пути: {chromedriver_path}")

def get_chromedriver_path() -> Optional[str]:
    """
    Get the path to the chromedriver executable.

    Returns:
    str: The path to the chromedriver executable.
    None: If the chromedriver is not found.
    """
    if platform_system_name == "win32":
        platform_name = "win32"
    elif platform_system_name == "win64":
        platform_name = "win64"
    elif platform_system_name == "linux":
        platform_name = "linux64"
    elif platform_system_name == "darwin":
        platform_name = "mac64"
    else:
        raise ValueError(f"Unsupported platform: {platform_system_name}")

    executable_name = (
        "chromedriver.exe"
        if platform_name == "win32" or platform_name == "win64"
        else "chromedriver"
    )
    chromedriver_path = os.path.join(
        root_dir, "chromedriver", f"chromedriver-{platform_name}", executable_name
    )

    if os.path.exists(chromedriver_path):
            set_chromedriver_permissions(chromedriver_path)
            return chromedriver_path

    return None



def download_chromedriver():
    api_endpoint = "https://googlechromelabs.github.io/chrome-for-testing"
    release_specific = "LATEST_RELEASE_STABLE"

    try:
        response = requests.get(f"{api_endpoint}/{release_specific}")
        response.raise_for_status()
        latest_release = response.text.strip()
        print(f"Latest ChromeDriver release: {latest_release}")

        base_url = f"https://storage.googleapis.com/chrome-for-testing-public/{latest_release}"
        download_urls = {
            "linux": f"{base_url}/linux64/chromedriver-linux64.zip",
            "darwin": f"{base_url}/mac64/chromedriver-mac64.zip",
            "win32": f"{base_url}/win32/chromedriver-win32.zip",
            "win64": f"{base_url}/win64/chromedriver-win64.zip"
        }

        download_url = download_urls.get(platform_system_name)
        if not download_url:
            raise ValueError(f"Unsupported platform: {platform_system_name}")

        print(f"Downloading ChromeDriver from {download_url}")
        response = requests.get(download_url)

        response.raise_for_status()

        content_disposition = response.headers.get('Content-Disposition')
        filename = content_disposition.split('filename=')[1] if content_disposition else f"chromedriver_{platform_system_name}.zip"

        os.makedirs(chromedriver_dir, exist_ok=True)

        with open(filename, 'wb') as f:
            f.write(response.content)

        print(f"Chromedriver downloaded successfully: {filename}")

        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(chromedriver_dir)

        os.remove(filename)
        if chromedriver_dir:
            set_chromedriver_permissions(chromedriver_dir)

        return chromedriver_dir
    except requests.RequestException as e:
        print(f"Error fetching latest ChromeDriver release: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    driver_path = download_chromedriver()
    if driver_path:
        print("Chromedriver extracted successfully")
    else:
        print("Failed to download and extract chromedriver")
