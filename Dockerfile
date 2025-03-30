FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

# Set work directory
WORKDIR /app

# Install dependencies
RUN pip install uv
COPY requirements.txt /app/
RUN uv pip install --system -r requirements.txt

# Copy project
COPY django_project/ /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"] 