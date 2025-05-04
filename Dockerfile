# ---- FRONTEND BUILD ----
FROM node:18 AS frontend

WORKDIR /app

COPY sweepy-ui/ ./

RUN npm install
RUN npm run build

# ---- BACKEND BUILD ----
FROM python:3.11-slim-bookworm AS backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential curl

# Install Poetry
ENV POETRY_VERSION=1.8.2
ENV PATH="/root/.local/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/bin/poetry


RUN poetry --version

WORKDIR /app

# Install Python dependencies
COPY pyproject.toml  .
COPY poetry.lock .
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy backend code
COPY sweepy/ ./sweepy

# Copy built frontend
COPY --from=frontend /app/dist ./sweepy/static

# Expose port (FastAPI default is 8000)
EXPOSE 8000

# Run with gunicorn + uvicorn workers
CMD ["poetry", "run", "uvicorn", "sweepy.api:app", "--host", "0.0.0.0", "--port", "8000"]