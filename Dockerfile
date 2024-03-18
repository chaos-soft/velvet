FROM python:3.12-slim-bookworm

COPY requirements.txt .

RUN apt-get update; \
    apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        git \
        pkg-config \
        wkhtmltopdf; \
    \
    pip install --no-cache-dir --upgrade pip; \
    pip install --no-cache-dir --upgrade -r requirements.txt; \
    \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
        build-essential \
        git \
        pkg-config; \
    rm -rf /var/lib/apt/lists/*; \
    rm requirements.txt
