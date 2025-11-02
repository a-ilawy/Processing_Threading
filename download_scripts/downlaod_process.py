from multiprocessing import Process
import requests
import os
import time

os.makedirs("downloads", exist_ok=True)

def download_image(url, index):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        file_path = f"downloads/image_{index}.jpg"
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Process {index} downloaded image_{index}.jpg")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    with open("images_urls.txt", "r") as file:
        urls = [line.strip() for line in file.readlines()]

    start = time.perf_counter()
    processes = []

    for i, url in enumerate(urls, start=1):
        p = Process(target=download_image, args=(url, i))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    end = time.perf_counter()
    print(f"\nFinished in {end - start:.2f} seconds using {len(processes)} processes.")
