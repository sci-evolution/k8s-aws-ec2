# syntax=docker/dockerfile:1

# Base image
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./

# Development stage
FROM base AS development
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=webapp.settings
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production stage
FROM base AS production
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
# Create non-root user
RUN adduser --disabled-password --gecos '' django
USER django
EXPOSE 8000
CMD ["gunicorn", "webapp.wsgi:application", "--bind", "0.0.0.0:8000"]