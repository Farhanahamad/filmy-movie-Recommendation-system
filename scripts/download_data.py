import os
import requests
import zipfile
import urllib3
from io import BytesIO

def download_and_extract():
    url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    dest_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
    
    print(f"Downloading dataset from {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = None
    # 1. Try with default SSL verification
    try:
        response = requests.get(url, headers=headers, timeout=30)
    except requests.exceptions.SSLError:
        print("GroupLens SSL certificate expired/invalid. Retrying with verify=False...")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, headers=headers, verify=False, timeout=30)
    except Exception as e:
        print(f"HTTPS connection error: {e}. Trying HTTP fallback...")
        http_url = url.replace("https://", "http://")
        try:
            response = requests.get(http_url, headers=headers, timeout=30)
        except Exception as e2:
            print(f"HTTP fallback also failed: {e2}")
            # Try verify=False on HTTPS as last resort
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(url, headers=headers, verify=False, timeout=30)

    if response and response.status_code == 200:
        print("Download complete. Extracting zip archive...")
        os.makedirs(dest_dir, exist_ok=True)
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(dest_dir)
        print(f"Extraction complete. Data stored in '{dest_dir}' directory.")
    else:
        status = response.status_code if response else "No Response"
        raise RuntimeError(f"Failed to download dataset from GroupLens (Status: {status}).")

if __name__ == "__main__":
    download_and_extract()
