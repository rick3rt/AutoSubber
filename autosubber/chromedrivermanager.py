import urllib.request
import platform
import zipfile
import os


BINARY_FOLDER = "./bin"
DOWNLOAD_FOLDER = "./tmp"
DEFAULT_VERSION = "114.0.5735.90"

# outdated, replace with urls here:
# https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json


class ChromeDriverManager:
    def __init__(self, version=DEFAULT_VERSION):
        self.version = version
        self.executable = None

        os.makedirs(BINARY_FOLDER, exist_ok=True)
        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    @staticmethod
    def getPlatformCode():
        os = platform.system()
        if os == "Windows":
            platform_code = "win32"
            exe_postfix = ".exe"
        elif os == "Linux":
            platform_code = "linux64"
            exe_postfix = ""
        elif os == "Darwin":
            platform_code = "mac64"
            exe_postfix = ""
        else:
            raise Exception("Unsupported OS")
        return platform_code, exe_postfix

    def getExecutable(self):
        platform_code, exe_postfix = self.getPlatformCode()
        self.executable = os.path.join(
            BINARY_FOLDER, self.version, "chromedriver" + exe_postfix
        )
        if not os.path.exists(self.executable):
            self.downloadExecutable()

        return os.path.abspath(self.executable)

    def downloadExecutable(self):

        platform_code, exe_postfix = self.getPlatformCode()
        filename_remote = f"chromedriver_{platform_code}.zip"
        download_path = os.path.join(DOWNLOAD_FOLDER, filename_remote)

        url = f"https://chromedriver.storage.googleapis.com/{self.version}/{filename_remote}"
        print(f"[CDM] Downloading {url} to {download_path}")
        urllib.request.urlretrieve(url, download_path)

        print(f"[CDM] Extracting zip")
        with zipfile.ZipFile(download_path, "r") as zip_ref:
            zip_ref.extractall(DOWNLOAD_FOLDER)

        print(f"[CDM] Moving to {BINARY_FOLDER}")
        os.makedirs(os.path.join(BINARY_FOLDER, self.version), exist_ok=True)
        os.rename(
            os.path.join(DOWNLOAD_FOLDER, "chromedriver" + exe_postfix),
            os.path.join(BINARY_FOLDER, self.version, "chromedriver" + exe_postfix),
        )

        # remove all files in tmp folder
        for file in os.listdir(DOWNLOAD_FOLDER):
            os.remove(os.path.join(DOWNLOAD_FOLDER, file))

        print(f"[CDM] Download Finished!")


if __name__ == "__main__":

    cdm = ChromeDriverManager(DEFAULT_VERSION)
    exe = cdm.getExecutable()
    print(exe)
