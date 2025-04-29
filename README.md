# CRM Loan Management System - Docker Setup

This repository contains both the frontend and backend components of the CRM Loan Management System, configured to run with Docker.

## Project Structure

- **Backend**: Django + Django REST Framework (in `/backenddjango`)
- **Frontend**: Vue 3 + Pinia (in `/frontendvue/frontend`)

## Running the Application with Docker

1. Make sure you have Docker and Docker Compose installed on your system.

2. Clone this repository:
   ```
   git clone <repository-url>
   cd lianV3-501a294797023b7f3fa802ddb963f1a4b1577785
   ```

3. Start the application using Docker Compose:
   ```
   docker-compose up
   ```

4. The application will be available at:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - Admin interface: http://localhost:8000/admin/
   - API documentation: http://localhost:8000/swagger/

## Testing the Application

### Backend Testing

1. Create a superuser to access the admin interface:
   ```
   docker-compose exec backend python manage.py createsuperuser
   ```

2. Access the admin interface at http://localhost:8000/admin/ and log in with the superuser credentials.

### Frontend Testing

1. Register a new user at http://localhost:3000/register

2. Log in with the registered user at http://localhost:3000/login

3. Explore the dashboard and profile management features.

## Services

The Docker Compose setup includes the following services:

- **backend**: Django application
- **frontend**: Vue.js application
- **db**: PostgreSQL database
- **redis**: Redis for caching and Celery
- **celery**: Celery worker for background tasks

## Environment Variables

### Backend Environment Variables

- `DEBUG`: Set to 1 for development
- `DATABASE_URL`: PostgreSQL connection string
- `CELERY_BROKER_URL`: Redis connection for Celery
- `REDIS_URL`: Redis connection for Channels

### Frontend Environment Variables

- `VITE_API_URL`: URL of the backend API

## Volumes

- `postgres_data`: Persistent storage for PostgreSQL
- `backend_static`: Static files for the backend
- `backend_media`: Media files uploaded to the backend

## Next Steps

After testing Phase 1 (Authentication), you can proceed with implementing Phase 2 (Core Application Management) according to the implementation strategy.
