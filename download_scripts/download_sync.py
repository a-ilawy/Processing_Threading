import requests
import os
import time

os.makedirs("downloads", exist_ok=True)


with open("images_urls.txt", "r") as file:
    urls = [line.strip() for line in file.readlines()]

def download_image(url, index):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        file_path = f"downloads/image_{index}.jpg"
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded image_{index}.jpg")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

start = time.perf_counter()

for i, url in enumerate(urls, start=1):
    download_image(url, i)

end = time.perf_counter()
print(f"\n Finished in {end - start:.2f} seconds.")
