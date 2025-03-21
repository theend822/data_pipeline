import requests

def download_data(url, output_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Data downloaded to {output_path}")
    else:
        raise Exception(f"Failed to download data: {response.status_code}")

if __name__ == "__main__":
    # for standalone testing only
    url = "..."
    output_path = "..." 
    download_data(url, output_path)