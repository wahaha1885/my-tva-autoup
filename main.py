import requests
from bs4 import BeautifulSoup
import os

# Constants
GITHUB_RELEASE_URL = "https://github.com/lizongying/my-tv/releases/latest"
VERSION_FILE = "version.txt"
APK_FILENAME = "my-tv.apk"

def get_latest_version():
    """Fetches the latest version from the GitHub release page."""
    try:
        response = requests.get(GITHUB_RELEASE_URL)
        response.raise_for_status()  # Raise an exception if the request failed
        soup = BeautifulSoup(response.content, 'html.parser')
        version_tag = soup.find('a', {'href': lambda x: x and x.startswith('/lizongying/my-tv/releases/tag/')})
        if version_tag:
            version = version_tag['href'].split('/')[-1]
            if version.startswith("v"):
                version = version[1:]
            return version
        return None
    except Exception as e:
        print(f"Error fetching the latest version: {e}")
        return None

def read_local_version():
    """Reads the locally stored version from the version.txt file."""
    try:
        with open(VERSION_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading the local version: {e}")
        return None

def download_and_install(version):
    """Downloads the APK file and installs it."""
    apk_url = f"https://github.com/lizongying/my-tv/releases/download/v{version}/my-tv-v{version}.apk"
    try:
        response = requests.get(apk_url, stream=True)
        response.raise_for_status()  # Raise an exception if the request failed
        with open(APK_FILENAME, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # Install the downloaded APK
        install_apk(APK_FILENAME)

        # Remove the downloaded APK file
        os.remove(APK_FILENAME)
    except Exception as e:
        print(f"Error downloading or installing the APK: {e}")

def install_apk(file_path):
    """Installs the APK file."""
    try:
        os.system(f"pm install -r {file_path}")
    except Exception as e:
        print(f"Error installing the APK: {e}")

def update_local_version(new_version):
    """Writes the new version to the version.txt file."""
    try:
        with open(VERSION_FILE, "w") as file:
            file.write(new_version)
    except Exception as e:
        print(f"Error updating the local version: {e}")

if __name__ == "__main__":
    latest_version = get_latest_version()
    if latest_version:
        local_version = read_local_version()

        if latest_version != local_version:
            print(f"New version available: {latest_version}")
            download_and_install(latest_version)
            update_local_version(latest_version)
            print(f"Updated to version: {latest_version}")
        else:
            print(f"You are already running the latest version: {latest_version}")
    else:
        print("Error: Could not fetch the latest version from GitHub.")
