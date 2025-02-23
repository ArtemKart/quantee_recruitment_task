import time

import httpx

from app import ROOT_DIR

# from urllib.parse import quote


# url = "http://localhost:80/api/v1/upload"
url = "http://localhost:8000/files"
filename = "alembic.ini"
filepath = ROOT_DIR / filename
headers = {
    # "filename": quote(filename),
    # "path_to_save": "alembic_files",
    # "file_size": "10000",
}
start = time.time()


with open(filepath, "rb") as f:
    r = httpx.get(url=url, headers=headers, timeout=100000 * 60)

end = time.time()

print(f"Затраченное время: {end - start} секунд")
print(r.json())
