FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV UV_LINK_MODE=copy

WORKDIR /app

ADD . /app

RUN uv sync

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]