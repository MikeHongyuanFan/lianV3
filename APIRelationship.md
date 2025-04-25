# API Relationship Documentation

This document outlines the API relationships between the frontend Vue application and the backend Django application in the CRM Loan Management System.

## Authentication Flow

### Backend Endpoints
- `/api/users/token/` - Login endpoint that returns JWT tokens
- `/api/users/token/refresh/` - Refresh token endpoint
- `/api/users/register/` - User registration endpoint

### Frontend Implementation
- Authentication is managed through the Pinia auth store (`src/store/auth.js`)
- JWT tokens are stored in localStorage and attached to API requests via Axios interceptors
- Token refresh is handled automatically when a 401 response is received

### Connection Points
- Frontend login form submits to `/api/users/token/` via `authService.login()`
- Token refresh is handled by `api.interceptors.response` in `src/services/api.js`
- User registration form submits to `/api/users/register/` via `authService.register()`

## Application Management

### Backend Endpoints
- `/api/applications/` - List and create applications
- `/api/applications/{id}/` - Retrieve, update, delete applications
- `/api/applications/{id}/update_stage/` - Update application stage
- `/api/applications/{id}/add_borrowers/` - Add borrowers to application
- `/api/applications/{id}/remove_borrowers/` - Remove borrowers from application
- `/api/applications/{id}/notes/` - Get and add notes
- `/api/applications/{id}/documents/` - Get and upload documents
- `/api/applications/{id}/process_signature/` - Process signature data
- `/api/applications/{id}/fees/` - Get and add fees
- `/api/applications/{id}/repayments/` - Get and add repayments
- `/api/applications/{id}/record_payment/` - Record payment for repayment
- `/api/applications/{id}/ledger/` - Get ledger entries

### Frontend Implementation
- Application data is managed through the Pinia application store (`src/store/application.js`)
- API calls are abstracted through `src/services/applicationService.js`
- Multi-step form for application creation with validation

### Connection Points
- Application listing page fetches from `/api/applications/` via `applicationService.getApplications()`
- Application detail page fetches from `/api/applications/{id}/` via `applicationService.getApplication()`
- Application creation form submits to `/api/applications/` via `applicationService.createApplication()`
- Application stage updates via `applicationService.updateApplicationStage()`
- Notes, documents, fees, and repayments are managed through their respective API endpoints

## Borrower Management

### Backend Endpoints
- `/api/borrowers/` - List and create borrowers
- `/api/borrowers/{id}/` - Retrieve, update, delete borrowers
- `/api/borrowers/{id}/assets/` - Get and add assets
- `/api/borrowers/{id}/liabilities/` - Get and add liabilities

### Frontend Implementation
- Borrower data is included in the application form and managed through the application store
- Dedicated borrower components for form inputs and validation

### Connection Points
- Borrowers are created as part of the application creation process
- Borrower details are fetched when viewing application details

## Broker Management

### Backend Endpoints
- `/api/brokers/` - List and create brokers
- `/api/brokers/{id}/` - Retrieve, update, delete brokers
- `/api/brokers/bdms/` - List and create BDMs
- `/api/brokers/branches/` - List and create branches

### Frontend Implementation
- Broker selection in application form
- Broker-specific views for broker users

### Connection Points
- Broker data is fetched for dropdowns in the application form
- Broker-specific applications are filtered in the broker dashboard

## Document Management

### Backend Endpoints
- `/api/documents/` - List and create documents
- `/api/documents/{id}/` - Retrieve, update, delete documents
- `/api/applications/{id}/documents/` - Get and upload documents for an application

### Frontend Implementation
- Document upload component in application form
- Document listing and download in application detail view

### Connection Points
- Documents are uploaded via `applicationService.uploadDocuments()`
- Documents are fetched via `applicationService.getDocuments()`

## Notification System

### Backend Implementation
- WebSocket consumer in `users/consumers.py` handles real-time notifications
- Notification model in `users/models.py` stores notifications
- Notification service in `users/services.py` creates and sends notifications

### Frontend Implementation
- WebSocket connection managed in `src/services/websocket.js`
- Notification components display notifications
- Notification preferences managed in settings

### Connection Points
- WebSocket connection established on authentication
- Real-time notifications received via WebSocket
- Notification preferences updated via API

## Reports

### Backend Endpoints
- `/api/reports/repayment-compliance/` - Repayment compliance report
- `/api/reports/application-volume/` - Application volume report
- `/api/reports/application-status/` - Application status report

### Frontend Implementation
- Report views with filters and charts
- Report data fetched from API endpoints

### Connection Points
- Report data is fetched when viewing report pages
- Filters are applied via query parameters

## API Security

### Authentication
- JWT token-based authentication
- Token refresh mechanism
- Role-based access control

### Authorization
- Permission classes in Django views restrict access based on user roles
- Frontend router guards prevent unauthorized access to routes

## Data Validation

### Backend Validation
- Django serializers validate incoming data
- Custom validators for specific fields (e.g., ABN/ACN validation)
- JSON schema validation for complex structures

### Frontend Validation
- Form validation with schema-bound field types
- Multi-step form validation with step tracking
- Client-side validation before submission

## Conclusion

The API relationships between the frontend and backend are well-structured and follow RESTful principles. The frontend services abstract API calls, making it easier to maintain and update the codebase. The WebSocket implementation provides real-time notifications, enhancing the user experience.

All API endpoints are properly connected and functioning as expected, with appropriate error handling and validation on both sides. The role-based access control ensures that users can only access the data and functionality they are authorized to use.