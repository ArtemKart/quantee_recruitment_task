import time
from urllib.parse import quote

import httpx

from app import ROOT_DIR

url = "http://localhost:80/api/v1/upload"
# url = "http://localhost:8000/upload"
filename = "UPLOAD_TEST.zip"
filepath = ROOT_DIR / filename
headers = {"filename": quote(filename)}
start = time.time()


with open(filepath, "rb") as f:
    r = httpx.post(url=url, data=f, headers=headers, timeout=100000 * 60)

end = time.time()

print(f"Затраченное время: {end - start} секунд")
print(r.json())
