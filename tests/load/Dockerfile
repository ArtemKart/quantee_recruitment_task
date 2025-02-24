FROM python:3.12-slim

WORKDIR /app

COPY client.py /app
RUN pip install requests

CMD ["python", "client.py"]
