# Builder stage
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache pip wheel --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


# App stage
FROM python:3.11-slim as app

WORKDIR /app

COPY --from=builder /app /app

COPY app app
COPY run.py run.py
COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh

COPY --from=builder /usr/src/app/wheels /wheels
RUN --mount=type=cache,target=/root/.cache pip install /wheels/*

HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

RUN chmod 700 entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
