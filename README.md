# Django Restaurant App

A restaurant management application built with Django, styled with Tailwind CSS, containerized with Docker, and set up with CI/CD through GitHub Actions.

## Features

- Menu management with categories and item details
- Filtering by dietary preferences (vegetarian, vegan, gluten-free)
- Spice level indicators
- Responsive, mobile-friendly UI with Tailwind CSS
- Motion animations with tailwindcss-motion plugin
- Containerized with Docker and PostgreSQL
- Full CI/CD pipeline with GitHub Actions

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js and npm (for Tailwind CSS)
- Docker and Docker Compose

### Local Development

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/django-restaurant.git
   cd django-restaurant
   ```

2. Create a virtual environment and install dependencies:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies for Tailwind CSS:

   ```
   npm install
   ```

4. Build Tailwind CSS:

   ```
   # Either use the npm script
   npm run build

   # Or use the provided shell script
   ./build-tailwind.sh
   ```

5. Create a `.env` file based on `.env.example`:

   ```
   cp .env.example .env
   ```

6. Run migrations:

   ```
   cd django_project
   python manage.py migrate
   ```

7. Seed the database with initial data:

   ```
   python manage.py seed_data
   ```

8. Create a superuser for Django Admin:

   ```
   python manage.py createsuperuser
   ```

9. Run the development server:

   ```
   python manage.py runserver
   ```

10. Access the application at http://127.0.0.1:8000

### Using Docker Compose

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/django-restaurant.git
   cd django-restaurant
   ```

2. Create a `.env` file based on `.env.example`:

   ```
   cp .env.example .env
   ```

3. Build and start the containers:

   ```
   # For production
   docker-compose up -d --build

   # For development with Tailwind CSS hot reloading
   docker-compose -f docker-compose.dev.yml up -d --build
   ```

4. Seed the database with initial data:

   ```
   docker-compose exec web python manage.py seed_data
   ```

5. Create a superuser for Django Admin:

   ```
   docker-compose exec web python manage.py createsuperuser
   ```

6. Access the application at http://localhost:8000

## Working with Tailwind CSS

### Directory Structure

- `django_project/static/src/input.css` - Source CSS file with Tailwind directives
- `django_project/static/css/output.css` - Compiled CSS (don't edit directly)
- `tailwind.config.js` - Tailwind configuration with custom colors and plugins

### Development Workflow

1. Run Tailwind CSS in watch mode for development:

   ```
   npm run dev
   ```

2. The CSS will automatically rebuild when you make changes to the `input.css` file or any template file.

3. If you're using Docker Compose with the development configuration, Tailwind CSS will automatically watch for changes.

### Custom Colors

The project includes custom design colors:

- `brand` - Primary brand colors (based on #e74c3c)
- `secondary` - Secondary colors (based on #34495e)
- `vegetarian`, `vegan`, `gluten-free` - Colors for dietary labels
- `spice-{1-5}` - Colors for spice level indicators

### Motion Animations

The project uses the `tailwindcss-motion` plugin for animations:

```html
<!-- Example usage -->
<div
  class="motion-safe:animate-fade-in motion-safe:animate-once motion-safe:animate-duration-500"
>
  Content with fade-in animation
</div>

<!-- The project includes predefined classes -->
<div class="transition-menu-item">Menu item with animation</div>
<div class="transition-category">Category with animation</div>
```

### Building for Production

Run the following command to build minified CSS for production:

```
npm run build
```

## Testing

Run tests with pytest:

```
cd django_project
python -m pytest
```

For test coverage:

```
python -m coverage run -m pytest
python -m coverage report
```

## Environment Variables

The following environment variables should be set:

| Variable          | Description                   | Example             |
| ----------------- | ----------------------------- | ------------------- |
| DJANGO_SECRET_KEY | Django secret key             | random_string       |
| DEBUG             | Debug mode (True/False)       | False               |
| ALLOWED_HOSTS     | Space-separated list of hosts | localhost 127.0.0.1 |
| POSTGRES_DB       | PostgreSQL database name      | django_db           |
| POSTGRES_USER     | PostgreSQL username           | postgres            |
| POSTGRES_PASSWORD | PostgreSQL password           | postgres            |
| POSTGRES_HOST     | PostgreSQL host               | db                  |
| POSTGRES_PORT     | PostgreSQL port               | 5432                |

## GitHub Actions Secrets

For the CI/CD pipeline, set these secrets in your GitHub repository:

- `DOCKER_HUB_USERNAME`: Your Docker Hub username
- `DOCKER_HUB_ACCESS_TOKEN`: Your Docker Hub access token
- `TEST_SERVER_HOST`: Your test server hostname/IP
- `TEST_SERVER_USER`: SSH username for the test server
- `TEST_SERVER_SSH_KEY`: SSH private key for the test server

Docker container is published into: https://hub.docker.com/r/sinarhen/restaurant-manager

#gh actions comment
