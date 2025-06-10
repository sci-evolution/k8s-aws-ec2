# syntax=docker/dockerfile:1

# Base Image
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY ./requirements.txt ./

# Development Image
FROM base AS development
WORKDIR /app
EXPOSE 8000
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]

# Production Image
FROM base AS production
WORKDIR /app
EXPOSE 8000
RUN adduser --disabled-password --gecos '' django \
    && chown -R django:django /app
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
COPY . .
USER django
CMD ["gunicorn", "todo.wsgi:application", "--bind", "0.0.0.0:8000"]