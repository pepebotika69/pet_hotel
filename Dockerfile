FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SECRET_KEY=dummy \
    DEBUG=False \
    ENVIRONMENT=PROD

WORKDIR /opt/apps

RUN apt-get update && apt-get install -y gettext && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-dev | uv pip install --system -r /dev/stdin

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "apps.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--reload"]
