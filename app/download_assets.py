import os
import requests

def download_file(url, folder):
    local_filename = url.split('/')[-1]
    path = os.path.join(folder, local_filename)
    print(f"Downloading {url} to {path}...")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("Done.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    # Set up assets directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(current_dir, 'assets')
    os.makedirs(assets_dir, exist_ok=True)

    # List of assets to download
    # Using a standard Bootstrap theme compatible with dash-bootstrap-components
    # If the app used a specific theme (e.g., CERULEAN), we would download that.
    # Defaulting to standard bootstrap for now.
    assets = [
        'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
        # Add other assets here if identified
    ]

    print(f"Downloading assets to {assets_dir}...")
    for url in assets:
        download_file(url, assets_dir)
    
    print("All assets download process completed.")
