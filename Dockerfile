FROM node:18-slim as node-builder

# Set work directory
WORKDIR /app

# Copy package.json and config files
COPY package.json tailwind.config.js postcss.config.js /app/

# Copy static files
COPY django_project/static/src/ /app/django_project/static/src/

# Install dependencies and build Tailwind CSS
RUN npm install && \
    npx tailwindcss -i ./django_project/static/src/input.css -o ./output.css --minify

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

# Create static/css directory
RUN mkdir -p /app/static/css/

# Copy the compiled CSS from the node-builder stage
COPY --from=node-builder /app/output.css /app/static/css/output.css

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"] 