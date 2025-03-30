# Django Task Manager

A simple task management application built with Django, containerized with Docker, and set up with CI/CD through GitHub Actions.

## Features

- Create, view, update, and delete tasks
- Task status tracking (Pending, In Progress, Completed)
- Responsive, mobile-friendly UI with Bootstrap
- Containerized with Docker and PostgreSQL
- Full CI/CD pipeline with GitHub Actions

## Development Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- uv (for package management)

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/django-task-manager.git
   cd django-task-manager
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install uv
   uv pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```

4. Run migrations:
   ```
   cd django_project
   python manage.py migrate
   ```

5. Create a superuser for Django Admin:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000

### Using Docker Compose

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/django-task-manager.git
   cd django-task-manager
   ```

2. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```

3. Build and start the containers:
   ```
   docker-compose up -d --build
   ```

4. Create a superuser for Django Admin:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

5. Access the application at http://localhost:8000

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

## Setting up Django Admin

1. Run migrations and create a superuser if you haven't already:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```

2. Log in to the admin panel at http://localhost:8000/admin/ using your superuser credentials.

3. From the admin panel, you can:
   - Add, edit, and delete tasks
   - Manage users and permissions
   - View the system logs

## CI/CD Pipeline

The application uses GitHub Actions for continuous integration and deployment:

1. On every push or pull request to the main branch:
   - Runs all tests
   - Checks code coverage
   
2. On successful push to the main branch:
   - Builds a Docker image
   - Pushes the image to Docker Hub
   - Deploys to the test server

## Environment Variables

The following environment variables should be set:

| Variable | Description | Example |
|----------|-------------|---------|
| DJANGO_SECRET_KEY | Django secret key | random_string |
| DEBUG | Debug mode (True/False) | False |
| ALLOWED_HOSTS | Space-separated list of hosts | localhost 127.0.0.1 |
| POSTGRES_DB | PostgreSQL database name | django_db |
| POSTGRES_USER | PostgreSQL username | postgres |
| POSTGRES_PASSWORD | PostgreSQL password | postgres |
| POSTGRES_HOST | PostgreSQL host | db |
| POSTGRES_PORT | PostgreSQL port | 5432 |

## GitHub Actions Secrets

For the CI/CD pipeline, set these secrets in your GitHub repository:

- `DOCKER_HUB_USERNAME`: Your Docker Hub username
- `DOCKER_HUB_ACCESS_TOKEN`: Your Docker Hub access token
- `TEST_SERVER_HOST`: Your test server hostname/IP
- `TEST_SERVER_USER`: SSH username for the test server
- `TEST_SERVER_SSH_KEY`: SSH private key for the test server 