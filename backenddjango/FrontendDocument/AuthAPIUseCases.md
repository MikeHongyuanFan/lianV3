# Authentication API Use Cases

This document outlines the use cases for the authentication APIs in the CRM Loan Management System.

## 1. User Login API

### API Details
- **Endpoint**: `/api/users/auth/login/`
- **HTTP Method**: `POST`
- **Authentication Required**: No

### Use Cases

#### 1.1 Standard User Login
- **Actor**: Any user (admin, broker, bd, client)
- **Description**: User logs in with valid credentials to access the system
- **Preconditions**: User has a registered account
- **Steps**:
  1. User enters email and password
  2. System validates credentials
  3. System generates JWT access and refresh tokens
  4. System returns tokens and user information
- **Postconditions**: User is authenticated and can access protected resources
- **Request Example**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword123"
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user_id": 42,
    "email": "user@example.com",
    "role": "broker",
    "name": "John Smith"
  }
  ```

#### 1.2 Failed Login (Invalid Credentials)
- **Actor**: Any user
- **Description**: User attempts to log in with invalid credentials
- **Preconditions**: None
- **Steps**:
  1. User enters incorrect email and/or password
  2. System validates credentials and finds they don't match
  3. System returns authentication error
- **Postconditions**: User remains unauthenticated
- **Request Example**:
  ```json
  {
    "email": "user@example.com",
    "password": "wrongpassword"
  }
  ```
- **Response Example (401 Unauthorized)**:
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

#### 1.3 Failed Login (Missing Fields)
- **Actor**: Any user
- **Description**: User attempts to log in without providing all required fields
- **Preconditions**: None
- **Steps**:
  1. User submits login form with missing email or password
  2. System validates request and finds missing fields
  3. System returns validation error
- **Postconditions**: User remains unauthenticated
- **Request Example**:
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "password": ["This field is required."]
  }
  ```

## 2. User Registration API

### API Details
- **Endpoint**: `/api/users/auth/register/`
- **HTTP Method**: `POST`
- **Authentication Required**: No

### Use Cases

#### 2.1 Standard User Registration
- **Actor**: New user
- **Description**: New user registers an account in the system
- **Preconditions**: Email is not already registered
- **Steps**:
  1. User provides registration details (email, password, first_name, last_name, role)
  2. System validates input data
  3. System creates new user account
  4. System generates JWT access and refresh tokens
  5. System returns tokens and user information
- **Postconditions**: User is registered, authenticated, and can access protected resources
- **Request Example**:
  ```json
  {
    "email": "newuser@example.com",
    "password": "securepassword123",
    "first_name": "Jane",
    "last_name": "Doe",
    "role": "client"
  }
  ```
- **Response Example (201 Created)**:
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user_id": 43,
    "email": "newuser@example.com",
    "role": "client",
    "name": "Jane Doe"
  }
  ```

#### 2.2 Failed Registration (Email Already Exists)
- **Actor**: New user
- **Description**: User attempts to register with an email that's already in use
- **Preconditions**: Email is already registered
- **Steps**:
  1. User provides registration details with an existing email
  2. System validates input and finds email already exists
  3. System returns validation error
- **Postconditions**: No new user is created
- **Request Example**:
  ```json
  {
    "email": "existing@example.com",
    "password": "securepassword123",
    "first_name": "Jane",
    "last_name": "Doe",
    "role": "client"
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "email": ["user with this email address already exists."]
  }
  ```

#### 2.3 Failed Registration (Invalid Role)
- **Actor**: New user
- **Description**: User attempts to register with an invalid role
- **Preconditions**: None
- **Steps**:
  1. User provides registration details with invalid role
  2. System validates input and finds role is invalid
  3. System returns validation error
- **Postconditions**: No new user is created
- **Request Example**:
  ```json
  {
    "email": "newuser@example.com",
    "password": "securepassword123",
    "first_name": "Jane",
    "last_name": "Doe",
    "role": "invalid_role"
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "role": ["\"invalid_role\" is not a valid choice."]
  }
  ```

## 3. Token Refresh API

### API Details
- **Endpoint**: `/api/users/auth/refresh/`
- **HTTP Method**: `POST`
- **Authentication Required**: No (but requires valid refresh token)

### Use Cases

#### 3.1 Standard Token Refresh
- **Actor**: Authenticated user with expired access token
- **Description**: User refreshes their access token using a valid refresh token
- **Preconditions**: User has a valid refresh token
- **Steps**:
  1. User provides refresh token
  2. System validates refresh token
  3. System generates new access token
  4. System returns new access token
- **Postconditions**: User has a new valid access token
- **Request Example**:
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

#### 3.2 Failed Token Refresh (Invalid Refresh Token)
- **Actor**: User with invalid refresh token
- **Description**: User attempts to refresh access token with invalid refresh token
- **Preconditions**: None
- **Steps**:
  1. User provides invalid refresh token
  2. System validates refresh token and finds it's invalid
  3. System returns authentication error
- **Postconditions**: User remains with expired access token
- **Request Example**:
  ```json
  {
    "refresh": "invalid_token"
  }
  ```
- **Response Example (401 Unauthorized)**:
  ```json
  {
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
  }
  ```

#### 3.3 Failed Token Refresh (Missing Refresh Token)
- **Actor**: User
- **Description**: User attempts to refresh access token without providing refresh token
- **Preconditions**: None
- **Steps**:
  1. User submits refresh request without refresh token
  2. System validates request and finds missing token
  3. System returns validation error
- **Postconditions**: User remains with expired access token
- **Request Example**:
  ```json
  {}
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "refresh": ["This field is required."]
  }
  ```