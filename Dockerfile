# syntax=docker/dockerfile:1

# Build static assets with Node
FROM node:20 AS assets
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY assets ./assets
COPY tailwind.config.js ./
RUN npx @tailwindcss/cli --input assets/tailwind/input.css --config assets/tailwind/tailwind.config.js --output dist/site.css

# Final application image
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=conduit.settings.prod \
    SECRET_KEY=please-set-a-secret-key
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
COPY --from=assets /app/dist ./dist
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir . \
    && python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "conduit.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
