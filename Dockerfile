FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

ENV UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml /app/

RUN uv sync

COPY . /app

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []
