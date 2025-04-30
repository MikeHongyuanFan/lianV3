# User API Use Cases

This document outlines the use cases for the User APIs in the CRM Loan Management System.

## 1. Get User Profile API

### API Details
- **Endpoint**: `/api/users/profile/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases

#### 1.1 Retrieve User Profile
- **Actor**: Authenticated user
- **Description**: User retrieves their own profile information
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System retrieves user profile data
  4. System returns profile information
- **Postconditions**: User receives their profile data
- **Request Example**:
  ```
  GET /api/users/profile/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 42,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "role": "broker",
    "phone": "+1234567890"
  }
  ```

#### 1.2 Failed Profile Retrieval (Unauthenticated)
- **Actor**: Unauthenticated user
- **Description**: User attempts to retrieve profile without authentication
- **Preconditions**: None
- **Steps**:
  1. User sends GET request without authentication token
  2. System checks for authentication and finds none
  3. System returns authentication error
- **Postconditions**: User does not receive profile data
- **Request Example**:
  ```
  GET /api/users/profile/
  ```
- **Response Example (401 Unauthorized)**:
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```

## 2. Update User Profile API

### API Details
- **Endpoint**: `/api/users/profile/update/`
- **HTTP Methods**: `PUT`, `PATCH`
- **Authentication Required**: Yes

### Use Cases

#### 2.1 Update User Profile (Full Update)
- **Actor**: Authenticated user
- **Description**: User updates all their profile information
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated PUT request with all profile fields
  2. System validates authentication token
  3. System validates input data
  4. System updates user profile
  5. System returns updated profile information
- **Postconditions**: User profile is updated with new information
- **Request Example**:
  ```
  PUT /api/users/profile/update/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1987654321"
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 42,
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "broker",
    "phone": "+1987654321"
  }
  ```

#### 2.2 Update User Profile (Partial Update)
- **Actor**: Authenticated user
- **Description**: User updates only specific profile fields
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated PATCH request with specific profile fields
  2. System validates authentication token
  3. System validates input data
  4. System updates only the provided fields
  5. System returns updated profile information
- **Postconditions**: Specified user profile fields are updated
- **Request Example**:
  ```
  PATCH /api/users/profile/update/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "phone": "+1987654321"
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 42,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "role": "broker",
    "phone": "+1987654321"
  }
  ```

#### 2.3 Failed Profile Update (Invalid Data)
- **Actor**: Authenticated user
- **Description**: User attempts to update profile with invalid data
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated PUT/PATCH request with invalid data
  2. System validates authentication token
  3. System validates input data and finds errors
  4. System returns validation error
- **Postconditions**: User profile remains unchanged
- **Request Example**:
  ```
  PATCH /api/users/profile/update/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "email": "invalid-email",
    "phone": "invalid-phone"
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "email": ["Enter a valid email address."],
    "phone": ["Phone number must be in the format +1234567890."]
  }
  ```

## 3. List All Users API

### API Details
- **Endpoint**: `/api/users/users/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes
- **Authorization Required**: Admin role

### Use Cases

#### 3.1 List All Users (Admin)
- **Actor**: Admin user
- **Description**: Admin retrieves a list of all users in the system
- **Preconditions**: User is authenticated with valid JWT token and has admin role
- **Steps**:
  1. Admin sends authenticated GET request
  2. System validates authentication token and admin role
  3. System retrieves paginated list of users
  4. System returns user list
- **Postconditions**: Admin receives list of users
- **Request Example**:
  ```
  GET /api/users/users/?limit=10&offset=0
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "count": 42,
    "next": "http://example.com/api/users/users/?limit=10&offset=10",
    "previous": null,
    "results": [
      {
        "id": 1,
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin",
        "phone": "+1111111111"
      },
      {
        "id": 2,
        "email": "broker1@example.com",
        "first_name": "Broker",
        "last_name": "One",
        "role": "broker",
        "phone": "+1222222222"
      },
      // ... more users
    ]
  }
  ```

#### 3.2 List Users with Search and Filter (Admin)
- **Actor**: Admin user
- **Description**: Admin searches and filters users
- **Preconditions**: User is authenticated with valid JWT token and has admin role
- **Steps**:
  1. Admin sends authenticated GET request with search/filter parameters
  2. System validates authentication token and admin role
  3. System applies search and filter criteria
  4. System returns filtered user list
- **Postconditions**: Admin receives filtered list of users
- **Request Example**:
  ```
  GET /api/users/users/?search=john&role=broker&limit=10
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 5,
        "email": "john.smith@example.com",
        "first_name": "John",
        "last_name": "Smith",
        "role": "broker",
        "phone": "+1555555555"
      },
      {
        "id": 8,
        "email": "johnny.broker@example.com",
        "first_name": "Johnny",
        "last_name": "Broker",
        "role": "broker",
        "phone": "+1666666666"
      },
      {
        "id": 12,
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "broker",
        "phone": "+1777777777"
      }
    ]
  }
  ```

#### 3.3 Failed User List Retrieval (Non-Admin)
- **Actor**: Non-admin user
- **Description**: Non-admin user attempts to retrieve list of all users
- **Preconditions**: User is authenticated with valid JWT token but does not have admin role
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System checks user role and finds insufficient permissions
  4. System returns permission error
- **Postconditions**: User does not receive user list
- **Request Example**:
  ```
  GET /api/users/users/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (403 Forbidden)**:
  ```json
  {
    "detail": "You do not have permission to perform this action."
  }
  ```

## 4. User Detail Operations API

### API Details
- **Endpoint**: `/api/users/users/{id}/`
- **HTTP Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication Required**: Yes
- **Authorization Required**: Admin role (for all operations), or self (for GET only)

### Use Cases

#### 4.1 Get User Details (Admin)
- **Actor**: Admin user
- **Description**: Admin retrieves details of a specific user
- **Preconditions**: User is authenticated with valid JWT token and has admin role
- **Steps**:
  1. Admin sends authenticated GET request with user ID
  2. System validates authentication token and admin role
  3. System retrieves user details
  4. System returns user information
- **Postconditions**: Admin receives user details
- **Request Example**:
  ```
  GET /api/users/users/42/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 42,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "role": "broker",
    "phone": "+1234567890"
  }
  ```

#### 4.2 Get Own User Details (Self)
- **Actor**: Any authenticated user
- **Description**: User retrieves their own details
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with their own ID
  2. System validates authentication token and confirms user is requesting their own details
  3. System retrieves user details
  4. System returns user information
- **Postconditions**: User receives their details
- **Request Example**:
  ```
  GET /api/users/users/42/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 42,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "role": "broker",
    "phone": "+1234567890"
  }
  ```

#### 4.3 Update User (Admin)
- **Actor**: Admin user
- **Description**: Admin updates a user's information
- **Preconditions**: User is authenticated with valid JWT token and has admin role
- **Steps**:
  1. Admin sends authenticated PUT/PATCH request with user ID and updated data
  2. System validates authentication token and admin role
  3. System validates input data
  4. System updates user information
  5. System returns updated user details
- **Postconditions**: User information is updated
- **Request Example**:
  ```
  PATCH /api/users/users/42/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "first_name": "Jonathan",
    "role": "client"
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 42,
    "email": "user@example.com",
    "first_name": "Jonathan",
    "last_name": "Smith",
    "role": "client",
    "phone": "+1234567890"
  }
  ```

#### 4.4 Delete User (Admin)
- **Actor**: Admin user
- **Description**: Admin deletes a user from the system
- **Preconditions**: User is authenticated with valid JWT token and has admin role
- **Steps**:
  1. Admin sends authenticated DELETE request with user ID
  2. System validates authentication token and admin role
  3. System deletes user
  4. System returns success confirmation
- **Postconditions**: User is deleted from the system
- **Request Example**:
  ```
  DELETE /api/users/users/42/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (204 No Content)**:
  ```
  (Empty response body)
  ```

#### 4.5 Failed User Detail Operations (Non-Admin)
- **Actor**: Non-admin user
- **Description**: Non-admin user attempts to update or delete another user
- **Preconditions**: User is authenticated with valid JWT token but does not have admin role
- **Steps**:
  1. User sends authenticated PUT/PATCH/DELETE request for another user's ID
  2. System validates authentication token
  3. System checks user role and finds insufficient permissions
  4. System returns permission error
- **Postconditions**: Target user remains unchanged
- **Request Example**:
  ```
  PATCH /api/users/users/43/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "first_name": "Changed"
  }
  ```
- **Response Example (403 Forbidden)**:
  ```json
  {
    "detail": "You do not have permission to perform this action."
  }
  ```

#### 4.6 Failed User Detail Retrieval (User Not Found)
- **Actor**: Admin user
- **Description**: Admin attempts to retrieve details for a non-existent user
- **Preconditions**: User is authenticated with valid JWT token and has admin role
- **Steps**:
  1. Admin sends authenticated GET request with non-existent user ID
  2. System validates authentication token and admin role
  3. System attempts to find user and fails
  4. System returns not found error
- **Postconditions**: No user details are returned
- **Request Example**:
  ```
  GET /api/users/users/9999/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (404 Not Found)**:
  ```json
  {
    "detail": "Not found."
  }
  ```

## 5. Get Current User Information API

### API Details
- **Endpoint**: `/api/users/users/me/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases

#### 5.1 Get Current User Information
- **Actor**: Authenticated user
- **Description**: User retrieves their own information
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System retrieves current user's information
  4. System returns user details
- **Postconditions**: User receives their information
- **Request Example**:
  ```
  GET /api/users/users/me/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 42,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "role": "broker",
    "phone": "+1234567890"
  }
  ```

#### 5.2 Failed Current User Information Retrieval (Unauthenticated)
- **Actor**: Unauthenticated user
- **Description**: User attempts to retrieve current user information without authentication
- **Preconditions**: None
- **Steps**:
  1. User sends GET request without authentication token
  2. System checks for authentication and finds none
  3. System returns authentication error
- **Postconditions**: No user information is returned
- **Request Example**:
  ```
  GET /api/users/users/me/
  ```
- **Response Example (401 Unauthorized)**:
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```
