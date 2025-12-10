# Dockerfile
FROM python:3.12-slim

# okoljske spremenljivke
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# sistemske odvisnosti za Pillow (slike)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    fonts-dejavu-core \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# kopiraj in namesti python odvisnosti
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# kopiraj aplikacijo
COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]
