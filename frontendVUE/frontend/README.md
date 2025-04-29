# CRM Loan Management System - Frontend

This is the frontend application for the CRM Loan Management System built with Vue 3, Pinia, and Vue Router.

## Project Structure

```
frontend/
├── src/
│   ├── assets/       # Static assets
│   ├── components/   # Reusable Vue components
│   ├── router/       # Vue Router configuration
│   ├── services/     # API services
│   ├── store/        # Pinia stores
│   ├── views/        # Page components
│   ├── App.vue       # Root component
│   └── main.js       # Entry point
├── .env              # Environment variables
└── package.json      # NPM dependencies
```

## Phase 1 Implementation: Project Setup and Authentication

This phase includes:

1. Project scaffolding with Vue 3 and Vite
2. Authentication implementation (login, register, profile management)
3. Base components for UI consistency
4. API service setup with Axios
5. State management with Pinia

### Components Implemented

- **Base Components**:
  - BaseButton: Reusable button component with variants and loading state
  - BaseInput: Form input component with validation support
  - AlertMessage: Alert component for displaying messages

- **Views**:
  - LoginView: User login page
  - RegisterView: User registration page
  - DashboardView: Main dashboard (placeholder for now)
  - ProfileView: User profile management
  - NotFoundView: 404 page

### Services Implemented

- **API Service**: Base Axios configuration with interceptors for authentication
- **Auth Service**: Authentication operations (login, register, token refresh)

### Stores Implemented

- **Auth Store**: Authentication state management with Pinia

## API Integration

The frontend integrates with the following API endpoints:

- `/api/users/auth/login/`: User login
- `/api/users/auth/register/`: User registration
- `/api/users/auth/refresh/`: Token refresh
- `/api/users/profile/`: Get user profile
- `/api/users/profile/update/`: Update user profile

## Getting Started

### Running with Docker

1. Navigate to the frontend directory:
   ```
   cd frontendvue/frontend
   ```

2. Build and run the Docker container:
   ```
   docker-compose up
   ```

3. Access the application at http://localhost:3000

### Running Locally

1. Navigate to the frontend directory:
   ```
   cd frontendvue/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run dev
   ```

4. Access the application at http://localhost:3000

## Next Steps

- Implement application management views
- Create borrower and guarantor management
- Implement document management
- Add notification system
