FROM node:18-slim as node-builder

# Set work directory
WORKDIR /app

# Copy package.json and config files
COPY package.json tailwind.config.js postcss.config.js /app/

# Copy static files AND templates for Tailwind to scan
COPY django_project/static/ /app/django_project/static/
COPY django_project/templates/ /app/django_project/templates/

# Install dependencies and build Tailwind CSS
RUN npm install && \
    npx tailwindcss -i ./django_project/static/css/tailwind.css -o ./django_project/static/css/output.css --minify

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

# Create static/css directory if it doesn't exist
RUN mkdir -p /app/static/css/

# Copy the compiled CSS from the node-builder stage
COPY --from=node-builder /app/django_project/static/css/output.css /app/static/css/output.css

# Collect static files
RUN python manage.py collectstatic --noinput

# Double-check that the CSS file in staticfiles is the correct one
RUN cp /app/static/css/output.css /app/staticfiles/css/output.css

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"] 