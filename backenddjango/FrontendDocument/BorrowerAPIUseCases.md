# Borrower API Use Cases

This document outlines the use cases for the Borrower APIs in the CRM Loan Management System.

## 1. List or Create Borrowers API

### API Details
- **Endpoint**: `/api/borrowers/`
- **HTTP Methods**: `GET`, `POST`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 1.1 List All Borrowers
- **Actor**: Authenticated user (Admin, Broker, Client)
- **Description**: User retrieves a paginated list of borrowers
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System filters borrowers based on user role:
     - Admin: All borrowers
     - Broker: Only borrowers created by the broker
     - Client: Only their own borrower profile
  4. System returns paginated list of borrowers with minimal information
- **Response**: List of borrowers with fields: id, first_name, last_name, email, phone, created_at, application_count
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 1.2 Filter Borrowers
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User filters borrowers by various criteria
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System applies filters and returns matching borrowers
- **Query Parameters**:
  - `search`: Search across first_name, last_name, email, phone, residential_address
  - `residency_status`: Filter by residency status
  - `marital_status`: Filter by marital status
  - `has_applications`: Filter borrowers with/without applications
- **Response**: Filtered list of borrowers
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 1.3 Search Borrowers
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User searches for borrowers by name, email, or phone
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with search parameter
  2. System searches across first_name, last_name, email, phone fields
  3. System returns matching borrowers
- **Query Parameters**:
  - `search`: Search term
- **Response**: List of matching borrowers
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

### Use Cases for POST Method

#### 1.4 Create New Borrower
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User creates a new borrower
- **Preconditions**: User is authenticated with valid JWT token and has appropriate permissions
- **Steps**:
  1. User sends authenticated POST request with borrower data
  2. System validates the data
  3. System creates new borrower and associates it with the creator
  4. System returns the created borrower details
- **Request Body**:
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1980-01-01",
    "email": "john.doe@example.com",
    "phone": "0412345678",
    "residential_address": "123 Main St, Sydney NSW 2000",
    "mailing_address": "123 Main St, Sydney NSW 2000",
    "tax_id": "12345678",
    "marital_status": "married",
    "residency_status": "citizen",
    "employment_type": "full_time",
    "employer_name": "ABC Company",
    "employer_address": "456 Business Ave, Sydney NSW 2000",
    "job_title": "Manager",
    "employment_duration": 36,
    "annual_income": 120000.00,
    "other_income": 10000.00,
    "monthly_expenses": 3000.00,
    "bank_name": "Commonwealth Bank",
    "bank_account_name": "John Doe",
    "bank_account_number": "12345678",
    "bank_bsb": "062-000",
    "referral_source": "Website",
    "tags": "priority,new",
    "notes_text": "Potential high-value client"
  }
  ```
- **Response**: Created borrower details
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden

#### 1.5 Create Company Borrower
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User creates a new company borrower
- **Preconditions**: User is authenticated with valid JWT token and has appropriate permissions
- **Steps**:
  1. User sends authenticated POST request with company borrower data
  2. System validates the data
  3. System creates new company borrower and associates it with the creator
  4. System returns the created company borrower details
- **Request Body**:
  ```json
  {
    "is_company": true,
    "company_name": "ABC Pty Ltd",
    "company_abn": "12345678901",
    "company_acn": "123456789",
    "company_address": "456 Business Ave, Sydney NSW 2000",
    "email": "contact@abccompany.com",
    "phone": "0298765432",
    "bank_name": "Commonwealth Bank",
    "bank_account_name": "ABC Pty Ltd",
    "bank_account_number": "87654321",
    "bank_bsb": "062-000",
    "referral_source": "Partner Referral",
    "tags": "company,priority",
    "notes_text": "Large company with multiple loan requirements"
  }
  ```
- **Response**: Created company borrower details
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden

## 2. Borrower Detail Operations API

### API Details
- **Endpoint**: `/api/borrowers/{id}/`
- **HTTP Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 2.1 Retrieve Borrower Details
- **Actor**: Authenticated user (Admin, Broker, Client)
- **Description**: User retrieves detailed information about a specific borrower
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested borrower
- **Steps**:
  1. User sends authenticated GET request with borrower ID
  2. System validates user has access to the borrower
  3. System returns detailed borrower information
- **Response**: Detailed borrower information including all fields
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PUT Method

#### 2.2 Update Borrower (Full Update)
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User updates all information for a borrower
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the borrower
- **Steps**:
  1. User sends authenticated PUT request with complete borrower data
  2. System validates the data
  3. System updates the borrower
  4. System returns the updated borrower details
- **Request Body**: Complete borrower data (all fields required)
- **Response**: Updated borrower details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PATCH Method

#### 2.3 Update Borrower (Partial Update)
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User updates specific information for a borrower
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the borrower
- **Steps**:
  1. User sends authenticated PATCH request with partial borrower data
  2. System validates the data
  3. System updates only the provided fields
  4. System returns the updated borrower details
- **Request Body**: Partial borrower data (only fields to update)
  ```json
  {
    "phone": "0487654321",
    "residential_address": "789 New St, Melbourne VIC 3000",
    "annual_income": 130000.00
  }
  ```
- **Response**: Updated borrower details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for DELETE Method

#### 2.4 Delete Borrower
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User deletes a borrower
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the borrower
- **Steps**:
  1. User sends authenticated DELETE request with borrower ID
  2. System validates user has permission to delete
  3. System deletes the borrower
- **Response**: No content
- **Status Codes**:
  - 204: No Content (success)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 3. List Company Borrowers API

### API Details
- **Endpoint**: `/api/borrowers/company/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 3.1 List Company Borrowers
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User retrieves a list of company borrowers
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System filters borrowers where is_company=True
  3. System returns list of company borrowers
- **Response**: List of company borrowers
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

## 4. Borrower Financial Summary API

### API Details
- **Endpoint**: `/api/borrowers/{id}/financial-summary/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 4.1 Retrieve Borrower Financial Summary
- **Actor**: Authenticated user (Admin, Broker, Client)
- **Description**: User retrieves financial summary for a specific borrower
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested borrower
- **Steps**:
  1. User sends authenticated GET request with borrower ID
  2. System calculates financial summary including:
     - Total assets
     - Total liabilities
     - Net worth
     - Monthly income
     - Monthly expenses
     - Disposable income
     - Asset breakdown
     - Liability breakdown
  3. System returns the financial summary
- **Response**: 
  ```json
  {
    "total_assets": 1250000.00,
    "total_liabilities": 450000.00,
    "net_worth": 800000.00,
    "monthly_income": 10000.00,
    "monthly_expenses": 5000.00,
    "disposable_income": 5000.00,
    "asset_breakdown": [
      {
        "type": "Property",
        "value": 1000000.00,
        "description": "Primary residence"
      },
      {
        "type": "Vehicle",
        "value": 50000.00,
        "description": "2022 Toyota Land Cruiser"
      },
      {
        "type": "Savings",
        "value": 200000.00,
        "description": "Term deposit"
      }
    ],
    "liability_breakdown": [
      {
        "type": "Mortgage",
        "amount": 400000.00,
        "monthly_payment": 2500.00,
        "description": "Home loan"
      },
      {
        "type": "Car Loan",
        "amount": 50000.00,
        "monthly_payment": 800.00,
        "description": "Vehicle finance"
      }
    ]
  }
  ```
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 5. Borrower Applications API

### API Details
- **Endpoint**: `/api/borrowers/{id}/applications/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 5.1 List Borrower Applications
- **Actor**: Authenticated user (Admin, Broker, Client)
- **Description**: User retrieves all applications for a specific borrower
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested borrower
- **Steps**:
  1. User sends authenticated GET request with borrower ID
  2. System retrieves all applications associated with the borrower
  3. System returns the list of applications
- **Response**: List of applications with summary information
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 6. Borrower Guarantors API

### API Details
- **Endpoint**: `/api/borrowers/{id}/guarantors/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 6.1 List Borrower Guarantors
- **Actor**: Authenticated user (Admin, Broker, Client)
- **Description**: User retrieves all guarantors for a specific borrower
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested borrower
- **Steps**:
  1. User sends authenticated GET request with borrower ID
  2. System retrieves all guarantors associated with the borrower
  3. System returns the list of guarantors
- **Response**: List of guarantors with their details
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 7. Guarantor Management API

### API Details
- **Endpoint**: `/api/borrowers/guarantors/`
- **HTTP Methods**: `GET`, `POST`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 7.1 List All Guarantors
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User retrieves a list of all guarantors
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System filters guarantors based on user role:
     - Admin: All guarantors
     - Broker: Only guarantors created by the broker
     - Client: Only guarantors associated with their borrower profile
  3. System returns list of guarantors
- **Response**: List of guarantors
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 7.2 Filter Guarantors
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

### Use Cases for POST Method

#### 7.3 Create New Guarantor
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User creates a new guarantor
- **Preconditions**: User is authenticated with valid JWT token and has appropriate permissions
- **Steps**:
  1. User sends authenticated POST request with guarantor data
  2. System validates the data
  3. System creates new guarantor and associates it with the creator
  4. System returns the created guarantor details
- **Request Body for Individual Guarantor**:
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
- **Request Body for Company Guarantor**:
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
- **Response**: Created guarantor details
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden

## 8. Guarantor Detail Operations API

### API Details
- **Endpoint**: `/api/borrowers/guarantors/{id}/`
- **HTTP Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 8.1 Retrieve Guarantor Details
- **Actor**: Authenticated user (Admin, Broker, Client)
- **Description**: User retrieves detailed information about a specific guarantor
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested guarantor
- **Steps**:
  1. User sends authenticated GET request with guarantor ID
  2. System validates user has access to the guarantor
  3. System returns detailed guarantor information
- **Response**: Detailed guarantor information
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PUT/PATCH Methods

#### 8.2 Update Guarantor
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User updates information for a guarantor
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the guarantor
- **Steps**:
  1. User sends authenticated PUT/PATCH request with guarantor data
  2. System validates the data
  3. System updates the guarantor
  4. System returns the updated guarantor details
- **Request Body**: Complete or partial guarantor data
- **Response**: Updated guarantor details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for DELETE Method

#### 8.3 Delete Guarantor
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
