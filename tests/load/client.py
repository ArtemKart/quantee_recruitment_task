import os
import time
from random import randint, uniform
from urllib.parse import quote

import requests

FILE_SIZE = 4 * 1024 * 1024 * 1024
CHUNK_SIZE = 10 * 1024 * 1024


def generate_file() -> str:
    random_value = randint(1000, 9999)
    file_name = f"test_file_nr_{random_value}.txt"
    print(f"Generating file {file_name}")
    with open(file_name, "wb") as f:
        for _ in range(FILE_SIZE // CHUNK_SIZE):
            f.write(os.urandom(CHUNK_SIZE))
        remaining_bytes = FILE_SIZE % CHUNK_SIZE
        if remaining_bytes:
            f.write(os.urandom(remaining_bytes))
    print("File generated")
    return file_name


def upload_file(filename) -> None:
    url = "http://nginx/api/v1/upload"
    headers = {
        "filename": quote(filename),
        "filesize": "10000",
        "pathtosave": "dummy_path",
    }
    with open(filename, "rb") as f:
        response = requests.post(url, data=f, headers=headers)
    print(f"Uploaded: {response.status_code}")


if __name__ == "__main__":
    time.sleep(uniform(1, 2))
    file = generate_file()

    upload_file(file)
