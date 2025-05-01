# Guarantor API Use Cases

This document outlines the use cases for the Guarantor APIs in the CRM Loan Management System.

## 1. List or Create Guarantors API

### API Details
- **Endpoint**: `/api/borrowers/guarantors/`
- **HTTP Methods**: `GET`, `POST`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 1.1 List All Guarantors
- **Actor**: Authenticated user (Admin, Broker, Client)
- **Description**: User retrieves a paginated list of guarantors
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System filters guarantors based on user role:
     - Admin: All guarantors
     - Broker: Only guarantors created by the broker
     - Client: Only guarantors associated with their borrower profile
  4. System returns paginated list of guarantors
- **Response**: List of guarantors with their details
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 1.2 Filter Guarantors
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User filters guarantors by various criteria
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System applies filters and returns matching guarantors
- **Query Parameters**:
  - `search`: Search across first_name, last_name, email, phone, company_name, address
  - `guarantor_type`: Filter by guarantor type (individual/company)
  - `borrower`: Filter by borrower ID
  - `application`: Filter by application ID
- **Response**: Filtered list of guarantors
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 1.3 Search Guarantors
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User searches for guarantors by name, email, or company name
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with search parameter
  2. System searches across first_name, last_name, email, company_name fields
  3. System returns matching guarantors
- **Query Parameters**:
  - `search`: Search term
- **Response**: List of matching guarantors
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

### Use Cases for POST Method

#### 1.4 Create New Individual Guarantor
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User creates a new individual guarantor
- **Preconditions**: User is authenticated with valid JWT token and has appropriate permissions
- **Steps**:
  1. User sends authenticated POST request with guarantor data
  2. System validates the data
  3. System creates new guarantor and associates it with the creator
  4. System returns the created guarantor details
- **Request Body**:
  ```json
  {
    "guarantor_type": "individual",
    "first_name": "Jane",
    "last_name": "Smith",
    "date_of_birth": "1985-05-15",
    "email": "jane.smith@example.com",
    "phone": "0423456789",
    "address": "456 Guarantor St, Sydney NSW 2000",
    "borrower": 1,
    "application": 1
  }
  ```
- **Response**: Created guarantor details
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden

#### 1.5 Create New Company Guarantor
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User creates a new company guarantor
- **Preconditions**: User is authenticated with valid JWT token and has appropriate permissions
- **Steps**:
  1. User sends authenticated POST request with company guarantor data
  2. System validates the data
  3. System creates new company guarantor and associates it with the creator
  4. System returns the created company guarantor details
- **Request Body**:
  ```json
  {
    "guarantor_type": "company",
    "company_name": "XYZ Pty Ltd",
    "company_abn": "98765432109",
    "company_acn": "987654321",
    "email": "contact@xyzcompany.com",
    "phone": "0298765432",
    "address": "789 Company St, Sydney NSW 2000",
    "borrower": 1,
    "application": 1
  }
  ```
- **Response**: Created company guarantor details
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden

## 2. Guarantor Detail Operations API

### API Details
- **Endpoint**: `/api/borrowers/guarantors/{id}/`
- **HTTP Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 2.1 Retrieve Guarantor Details
- **Actor**: Authenticated user (Admin, Broker, Client)
- **Description**: User retrieves detailed information about a specific guarantor
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested guarantor
- **Steps**:
  1. User sends authenticated GET request with guarantor ID
  2. System validates user has access to the guarantor
  3. System returns detailed guarantor information
- **Response**: Detailed guarantor information including all fields
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PUT Method

#### 2.2 Update Guarantor (Full Update)
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User updates all information for a guarantor
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the guarantor
- **Steps**:
  1. User sends authenticated PUT request with complete guarantor data
  2. System validates the data
  3. System updates the guarantor
  4. System returns the updated guarantor details
- **Request Body**: Complete guarantor data (all fields required)
- **Response**: Updated guarantor details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PATCH Method

#### 2.3 Update Guarantor (Partial Update)
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User updates specific information for a guarantor
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the guarantor
- **Steps**:
  1. User sends authenticated PATCH request with partial guarantor data
  2. System validates the data
  3. System updates only the provided fields
  4. System returns the updated guarantor details
- **Request Body**: Partial guarantor data (only fields to update)
  ```json
  {
    "phone": "0487654321",
    "address": "123 New Address St, Brisbane QLD 4000"
  }
  ```
- **Response**: Updated guarantor details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for DELETE Method

#### 2.4 Delete Guarantor
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User deletes a guarantor
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the guarantor
- **Steps**:
  1. User sends authenticated DELETE request with guarantor ID
  2. System validates user has permission to delete
  3. System deletes the guarantor
- **Response**: No content
- **Status Codes**:
  - 204: No Content (success)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 3. Guaranteed Applications API

### API Details
- **Endpoint**: `/api/borrowers/guarantors/{id}/guaranteed_applications/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 3.1 List Applications Guaranteed by a Guarantor
- **Actor**: Authenticated user (Admin, Broker, Client)
- **Description**: User retrieves all applications that a specific guarantor is guaranteeing
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested guarantor
- **Steps**:
  1. User sends authenticated GET request with guarantor ID
  2. System retrieves all applications associated with the guarantor through the ManyToMany relationship
  3. System returns the list of applications
- **Response**: List of applications with summary information
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found
