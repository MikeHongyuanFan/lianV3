# Application API Use Cases - Part 2

This document outlines the use cases for the Application APIs in the CRM Loan Management System (Part 2).

## 4. Validate Application Schema API

### API Details
- **Endpoint**: `/api/applications/validate-schema/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes

### Use Cases

#### 4.1 Validate Valid Application Schema
- **Actor**: Authenticated user
- **Description**: User validates application data against schema rules
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated POST request with application data to validate
  2. System validates authentication token
  3. System validates application data against schema rules
  4. System returns validation success
- **Postconditions**: User receives validation confirmation
- **Request Example**:
  ```
  POST /api/applications/validate-schema/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "application_type": "residential",
    "purpose": "Home purchase",
    "loan_amount": 500000.00,
    "loan_term": 30,
    "repayment_frequency": "monthly"
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "valid": true
  }
  ```

#### 4.2 Validate Invalid Application Schema
- **Actor**: Authenticated user
- **Description**: User validates invalid application data against schema rules
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated POST request with invalid application data
  2. System validates authentication token
  3. System validates application data against schema rules and finds errors
  4. System returns validation errors
- **Postconditions**: User receives validation errors
- **Request Example**:
  ```
  POST /api/applications/validate-schema/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "application_type": "invalid_type",
    "purpose": "",
    "loan_amount": -5000.00,
    "loan_term": 0,
    "repayment_frequency": "invalid_frequency"
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "valid": false,
    "error": "Invalid application schema: application_type must be one of [residential, commercial, personal], loan_amount must be positive, loan_term must be positive, repayment_frequency must be one of [weekly, fortnightly, monthly]"
  }
  ```

## 5. Update Application Stage API

### API Details
- **Endpoint**: `/api/applications/{id}/stage/`
- **HTTP Method**: `PUT`
- **Authentication Required**: Yes

### Use Cases

#### 5.1 Update Application Stage
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User updates the stage of an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to update it
  - New stage follows valid workflow progression
- **Steps**:
  1. User sends authenticated PUT request with application ID and new stage
  2. System validates authentication token
  3. System verifies user has permission to update application
  4. System validates stage transition is allowed
  5. System updates application stage
  6. System returns updated application stage information
- **Postconditions**: 
  - Application stage is updated
  - Notifications are sent to relevant users
- **Request Example**:
  ```
  PUT /api/applications/123/stage/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "stage": "valuation"
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 123,
    "reference_number": "A12345",
    "stage": "valuation",
    "status": "Application stage updated successfully"
  }
  ```

#### 5.2 Failed Stage Update (Invalid Stage)
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User attempts to update application to an invalid stage
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to update it
- **Steps**:
  1. User sends authenticated PUT request with application ID and invalid stage
  2. System validates authentication token
  3. System verifies user has permission to update application
  4. System validates stage and finds it's invalid
  5. System returns validation error
- **Postconditions**: Application stage remains unchanged
- **Request Example**:
  ```
  PUT /api/applications/123/stage/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "stage": "invalid_stage"
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "stage": ["\"invalid_stage\" is not a valid choice."]
  }
  ```

#### 5.3 Failed Stage Update (Invalid Workflow)
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User attempts to update application stage with invalid workflow progression
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to update it
  - New stage violates workflow progression rules
- **Steps**:
  1. User sends authenticated PUT request with application ID and stage that violates workflow
  2. System validates authentication token
  3. System verifies user has permission to update application
  4. System validates stage transition and finds it violates workflow rules
  5. System returns workflow error
- **Postconditions**: Application stage remains unchanged
- **Request Example**:
  ```
  PUT /api/applications/123/stage/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "stage": "settlement"
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "error": "Invalid stage transition. Cannot move from 'inquiry' directly to 'settlement'."
  }
  ```

## 6. Update Application Borrowers API

### API Details
- **Endpoint**: `/api/applications/{id}/borrowers/`
- **HTTP Method**: `PUT`
- **Authentication Required**: Yes

### Use Cases

#### 6.1 Update Application Borrowers
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User updates the borrowers associated with an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to update it
  - All borrower IDs exist in the system
- **Steps**:
  1. User sends authenticated PUT request with application ID and borrower IDs
  2. System validates authentication token
  3. System verifies user has permission to update application
  4. System validates all borrower IDs exist
  5. System updates application borrowers
  6. System returns updated borrower information
- **Postconditions**: Application is associated with new set of borrowers
- **Request Example**:
  ```
  PUT /api/applications/123/borrowers/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "borrowers": [201, 202, 205]
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 123,
    "reference_number": "A12345",
    "borrowers": [
      {
        "id": 201,
        "first_name": "Michael",
        "last_name": "Johnson",
        "email": "michael@example.com"
      },
      {
        "id": 202,
        "first_name": "Sarah",
        "last_name": "Johnson",
        "email": "sarah@example.com"
      },
      {
        "id": 205,
        "first_name": "David",
        "last_name": "Wilson",
        "email": "david@example.com"
      }
    ]
  }
  ```

#### 6.2 Failed Borrower Update (Invalid Borrower IDs)
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User attempts to update application with non-existent borrower IDs
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to update it
  - Some borrower IDs don't exist in the system
- **Steps**:
  1. User sends authenticated PUT request with application ID and some invalid borrower IDs
  2. System validates authentication token
  3. System verifies user has permission to update application
  4. System validates borrower IDs and finds some don't exist
  5. System returns validation error
- **Postconditions**: Application borrowers remain unchanged
- **Request Example**:
  ```
  PUT /api/applications/123/borrowers/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "borrowers": [201, 999, 1000]
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "error": "Borrowers with IDs [999, 1000] not found"
  }
  ```

## 7. Sign Application API

### API Details
- **Endpoint**: `/api/applications/{id}/signature/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes

### Use Cases

#### 7.1 Sign Application
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User signs an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to sign it
  - Application is in a stage that allows signing
- **Steps**:
  1. User sends authenticated POST request with application ID and signature data
  2. System validates authentication token
  3. System verifies user has permission to sign application
  4. System validates signature data
  5. System stores signature information
  6. System returns updated application with signature information
- **Postconditions**: Application is marked as signed
- **Request Example**:
  ```
  POST /api/applications/123/signature/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "signature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "name": "Michael Johnson",
    "signature_date": "2023-04-30"
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 123,
    "reference_number": "A12345",
    "signature": {
      "is_signed": true,
      "signed_by": "Michael Johnson",
      "signed_date": "2023-04-30",
      "signature_image_url": "/media/signatures/application_123_signature.png"
    },
    // ... other application details
  }
  ```

#### 7.2 Failed Signature (Invalid Signature Data)
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User attempts to sign application with invalid signature data
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to sign it
- **Steps**:
  1. User sends authenticated POST request with application ID and invalid signature data
  2. System validates authentication token
  3. System verifies user has permission to sign application
  4. System validates signature data and finds it's invalid
  5. System returns validation error
- **Postconditions**: Application remains unsigned
- **Request Example**:
  ```
  POST /api/applications/123/signature/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "signature": "invalid-data",
    "name": ""
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "signature": ["Invalid signature format. Must be a valid Base64 encoded image."],
    "name": ["This field may not be blank."]
  }
  ```

## 8. Get Application Guarantors API

### API Details
- **Endpoint**: `/api/applications/{id}/guarantors/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases

#### 8.1 Get Application Guarantors
- **Actor**: Authenticated user
- **Description**: User retrieves guarantors associated with an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated GET request with application ID
  2. System validates authentication token
  3. System verifies user has access to application
  4. System retrieves guarantors associated with application
  5. System returns guarantor list
- **Postconditions**: User receives list of application guarantors
- **Request Example**:
  ```
  GET /api/applications/123/guarantors/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  [
    {
      "id": 101,
      "first_name": "Robert",
      "last_name": "Smith",
      "email": "robert@example.com",
      "phone_number": "+1234567892",
      "guarantor_type": "individual",
      "relationship_to_borrower": "parent",
      "address": "789 Pine St, Anytown",
      "date_of_birth": "1955-03-10"
    },
    {
      "id": 102,
      "first_name": "Jennifer",
      "last_name": "Brown",
      "email": "jennifer@example.com",
      "phone_number": "+1234567893",
      "guarantor_type": "individual",
      "relationship_to_borrower": "sibling",
      "address": "456 Elm St, Anytown",
      "date_of_birth": "1978-07-22"
    }
  ]
  ```

#### 8.2 Get Application Guarantors (No Guarantors)
- **Actor**: Authenticated user
- **Description**: User retrieves guarantors for an application that has none
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
  - Application has no guarantors
- **Steps**:
  1. User sends authenticated GET request with application ID
  2. System validates authentication token
  3. System verifies user has access to application
  4. System finds no guarantors associated with application
  5. System returns empty list
- **Postconditions**: User receives empty guarantor list
- **Request Example**:
  ```
  GET /api/applications/124/guarantors/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  []
  ```

## 9. Get Application Notes API

### API Details
- **Endpoint**: `/api/applications/{id}/notes/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases

#### 9.1 Get Application Notes
- **Actor**: Authenticated user
- **Description**: User retrieves notes associated with an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated GET request with application ID
  2. System validates authentication token
  3. System verifies user has access to application
  4. System retrieves paginated notes associated with application
  5. System returns note list
- **Postconditions**: User receives list of application notes
- **Request Example**:
  ```
  GET /api/applications/123/notes/?limit=10&offset=0
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
        "id": 401,
        "content": "Client requested expedited processing",
        "created_at": "2023-04-16T09:45:00Z",
        "created_by": {
          "id": 5,
          "name": "Admin User"
        }
      },
      {
        "id": 402,
        "content": "Valuation scheduled for April 25",
        "created_at": "2023-04-18T14:30:00Z",
        "created_by": {
          "id": 15,
          "name": "Jane Wilson"
        }
      },
      {
        "id": 403,
        "content": "Client provided additional income documentation",
        "created_at": "2023-04-20T11:15:00Z",
        "created_by": {
          "id": 42,
          "name": "John Smith"
        }
      }
    ]
  }
  ```

#### 9.2 Search Application Notes
- **Actor**: Authenticated user
- **Description**: User searches notes associated with an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated GET request with application ID and search parameter
  2. System validates authentication token
  3. System verifies user has access to application
  4. System searches notes for matching content
  5. System returns matching notes
- **Postconditions**: User receives notes matching search criteria
- **Request Example**:
  ```
  GET /api/applications/123/notes/?search=valuation&limit=10
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 402,
        "content": "Valuation scheduled for April 25",
        "created_at": "2023-04-18T14:30:00Z",
        "created_by": {
          "id": 15,
          "name": "Jane Wilson"
        }
      }
    ]
  }
  ```

## 10. Add Application Note API

### API Details
- **Endpoint**: `/api/applications/{id}/add-note/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes

### Use Cases

#### 10.1 Add Note to Application
- **Actor**: Authenticated user
- **Description**: User adds a note to an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated POST request with application ID and note content
  2. System validates authentication token
  3. System verifies user has access to application
  4. System validates note content
  5. System creates new note associated with application
  6. System returns created note
- **Postconditions**: New note is added to application
- **Request Example**:
  ```
  POST /api/applications/123/add-note/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "content": "Client called to discuss interest rate options"
  }
  ```
- **Response Example (201 Created)**:
  ```json
  {
    "id": 404,
    "content": "Client called to discuss interest rate options",
    "created_at": "2023-04-30T15:20:00Z",
    "created_by": {
      "id": 5,
      "name": "Admin User"
    }
  }
  ```

#### 10.2 Failed Note Addition (Empty Content)
- **Actor**: Authenticated user
- **Description**: User attempts to add an empty note to an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated POST request with application ID and empty note content
  2. System validates authentication token
  3. System verifies user has access to application
  4. System validates note content and finds it's empty
  5. System returns validation error
- **Postconditions**: No note is added to application
- **Request Example**:
  ```
  POST /api/applications/123/add-note/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "content": ""
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "content": ["This field may not be blank."]
  }
  ```
