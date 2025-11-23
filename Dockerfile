FROM python:3.14-slim-trixie

COPY requirements.txt .

RUN apt-get update; \
    apt-get install -y --no-install-recommends \
        file \
        imagemagick \
        postgresql-contrib; \
    \
    pip install --no-cache-dir --upgrade pip; \
    pip install --no-cache-dir --upgrade -r requirements.txt; \
    \
    rm -rf /var/lib/apt/lists/*; \
    rm requirements.txt
