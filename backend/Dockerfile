FROM python:3.10-slim as base

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

# Use a different virtual environment directory to avoid
# creating it inside the mounted project directory
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

# Ensure uv uses dependencies from the created virtual environment
ENV PATH="${UV_PROJECT_ENVIRONMENT}/bin:$PATH"

COPY . .