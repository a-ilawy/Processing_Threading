import requests
import os
import time
from threading import Thread, Lock
from queue import Queue
import threading


os.makedirs("downloads", exist_ok=True)


with open("images_urls.txt", "r") as file:
    urls = [line.strip() for line in file.readlines()]

task_queue = Queue()
for i, url in enumerate(urls, start=1):
    task_queue.put((url, i))

print_lock = Lock() # lock consol

def download_worker():
    downloaded_count = 0
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
            downloaded_count += 1
            with print_lock:
                print(f"Thread {threading.current_thread().name} downloaded image_{index}.jpg")
        except Exception as e:
            with print_lock:
                print(f"\nError downloading {url}: {e}")
        finally:
            task_queue.task_done()

    with print_lock:
        print(f"Thread {threading.current_thread().name} finished, downloaded {downloaded_count} images.")

start = time.perf_counter()

MAX_THREADS = 5
threads = []


for i in range(MAX_THREADS):
    t = Thread(target=download_worker, name=f"Worker-{i+1}")
    t.start()
    threads.append(t)


for t in threads:
    t.join()

end = time.perf_counter()
print(f"\nFinished in {end - start:.2f} seconds using {MAX_THREADS} threads.")



# import requests
# import os
# import time
# from concurrent.futures import ThreadPoolExecutor, as_completed

# os.makedirs("downloads", exist_ok=True)

# with open("images_urls.txt", "r") as file:
#     urls = [line.strip() for line in file.readlines()]

# def download_image(url, index):
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         file_path = f"downloads/image_{index}.jpg"
#         with open(file_path, "wb") as f:
#             f.write(response.content)
#         print(f"Downloaded image_{index}.jpg")
#     except Exception as e:
#         print(f"\n Failed to download {url}: {e}")

# start = time.perf_counter()


# MAX_THREADS = 5

# with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:

#     futures = [executor.submit(download_image, url, i) for i, url in enumerate(urls, start=1)]
    

#     for future in as_completed(futures):
#         future.result() 

# end = time.perf_counter()
# print(f"\n Finished in {end - start:.2f} seconds using {MAX_THREADS} threads.")
