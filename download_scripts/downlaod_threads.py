import requests
import os
import time
from threading import Thread

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
        print(f"\n Failed to download {url}: {e}")

threads = []
start = time.perf_counter()

for i, url in enumerate(urls, start=1):
    thread = Thread(target = download_image, args = (url, i))
    thread.start()
    threads.append(thread)

for i, thrd in enumerate(threads, start=1):
    thrd.join()
    print(f"thread {i} finished...exiting")

end = time.perf_counter()
print(f"\n Finished in {end - start:.2f} seconds.")
