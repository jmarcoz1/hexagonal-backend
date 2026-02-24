FROM python:{{ cookiecutter.python_version }}-slim AS base

ARG INSTALL_DEV=false

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:0.9.8 /uv /uvx /bin/

RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml uv.lock README.md ./

RUN if [ "$INSTALL_DEV" = "true" ] ; then \
        uv pip install . --group dev ; \
    else \
    uv pip install . ; \
    fi

# ===============================
FROM docker.io/python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY . .
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
RUN mkdir -p /app/static /app/media
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["/entrypoint.sh"]

CMD ["opentelemetry-instrument", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "6", "config.wsgi:application"]
