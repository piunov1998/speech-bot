FROM python:3.11-slim-buster

RUN apt update && apt install -y ffmpeg

COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY . /app
WORKDIR /app/src

CMD ["python", "run.py"]
