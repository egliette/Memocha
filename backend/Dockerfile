FROM python:3.10-slim as base

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/0.4.17/install.sh /uv-installer.sh 

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.cargo/bin/:$PATH"

COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

COPY . .