import requests
import os
import time
from multiprocessing import Process, Lock, Queue, current_process

os.makedirs("downloads", exist_ok=True)

def download_worker(task_queue, print_lock):
    while True:
        try:
            url, index = task_queue.get_nowait()
        except:
            break

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            file_path = f"downloads/image_{index}.jpg"
            with open(file_path, "wb") as f:
                f.write(response.content)
            with print_lock:
                print(f"{current_process().name} downloaded image_{index}.jpg")
        except Exception as e:
            with print_lock:
                print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    with open("images_urls.txt", "r") as file:
        urls = [line.strip() for line in file.readlines()]

    task_queue = Queue()
    for i, url in enumerate(urls, start=1):
        task_queue.put((url, i))

    print_lock = Lock()

    start = time.perf_counter()

    MAX_PROCESSES = 5
    processes = []

    for i in range(MAX_PROCESSES):
        p = Process(target=download_worker, args=(task_queue, print_lock), name=f"Worker-{i+1}")
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    end = time.perf_counter()
    print(f"\nFinished in {end - start:.2f} seconds using {MAX_PROCESSES} processes.")
