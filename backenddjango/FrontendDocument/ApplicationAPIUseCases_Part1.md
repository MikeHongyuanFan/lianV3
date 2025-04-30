# Application API Use Cases - Part 1

This document outlines the use cases for the Application APIs in the CRM Loan Management System (Part 1).

## 1. List or Create Applications API

### API Details
- **Endpoint**: `/api/applications/`
- **HTTP Methods**: `GET`, `POST`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 1.1 List All Applications
- **Actor**: Authenticated user
- **Description**: User retrieves a paginated list of applications
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System retrieves paginated list of applications
  4. System returns application list
- **Postconditions**: User receives list of applications
- **Request Example**:
  ```
  GET /api/applications/?limit=10&offset=0
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "count": 42,
    "next": "http://example.com/api/applications/?limit=10&offset=10",
    "previous": null,
    "results": [
      {
        "id": 123,
        "reference_number": "A12345",
        "application_type": "residential",
        "purpose": "Home purchase",
        "loan_amount": 500000.00,
        "stage": "formal_approval",
        "stage_display": "Formal Approval",
        "created_at": "2023-04-15T10:30:00Z",
        "broker_name": "John Smith",
        "borrower_count": 2,
        "estimated_settlement_date": "2023-05-30"
      },
      {
        "id": 124,
        "reference_number": "A12346",
        "application_type": "commercial",
        "purpose": "Business expansion",
        "loan_amount": 750000.00,
        "stage": "inquiry",
        "stage_display": "Inquiry",
        "created_at": "2023-04-16T14:45:00Z",
        "broker_name": "Jane Doe",
        "borrower_count": 1,
        "estimated_settlement_date": "2023-06-15"
      },
      // ... more applications
    ]
  }
  ```

#### 1.2 Filter Applications by Status and Stage
- **Actor**: Authenticated user
- **Description**: User retrieves filtered applications
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System validates authentication token
  3. System applies filters to retrieve matching applications
  4. System returns filtered application list
- **Postconditions**: User receives filtered applications
- **Request Example**:
  ```
  GET /api/applications/?stage=formal_approval&date_from=2023-04-01&date_to=2023-04-30&limit=10
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 123,
        "reference_number": "A12345",
        "application_type": "residential",
        "purpose": "Home purchase",
        "loan_amount": 500000.00,
        "stage": "formal_approval",
        "stage_display": "Formal Approval",
        "created_at": "2023-04-15T10:30:00Z",
        "broker_name": "John Smith",
        "borrower_count": 2,
        "estimated_settlement_date": "2023-05-30"
      },
      // ... more applications in formal_approval stage within date range
    ]
  }
  ```

#### 1.3 Search Applications
- **Actor**: Authenticated user
- **Description**: User searches applications by reference number or purpose
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with search parameter
  2. System validates authentication token
  3. System searches applications for matching content
  4. System returns matching applications
- **Postconditions**: User receives applications matching search criteria
- **Request Example**:
  ```
  GET /api/applications/?search=purchase&limit=10
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "count": 8,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 123,
        "reference_number": "A12345",
        "application_type": "residential",
        "purpose": "Home purchase",
        "loan_amount": 500000.00,
        "stage": "formal_approval",
        "stage_display": "Formal Approval",
        "created_at": "2023-04-15T10:30:00Z",
        "broker_name": "John Smith",
        "borrower_count": 2,
        "estimated_settlement_date": "2023-05-30"
      },
      // ... more applications containing "purchase" in purpose
    ]
  }
  ```

### Use Cases for POST Method

#### 1.4 Create New Application
- **Actor**: Authenticated user
- **Description**: User creates a new loan application
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated POST request with application data
  2. System validates authentication token
  3. System validates input data
  4. System creates new application
  5. System returns created application details
- **Postconditions**: New application is created in the system
- **Request Example**:
  ```
  POST /api/applications/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "loan_amount": 500000.00,
    "loan_term": 30,
    "interest_rate": 4.5,
    "purpose": "Home purchase",
    "repayment_frequency": "monthly",
    "application_type": "residential",
    "product_id": "PROD001",
    "estimated_settlement_date": "2023-05-30",
    "stage": "inquiry",
    "broker": 42,
    "bd": 15,
    "branch": 7,
    "security_address": "123 Main St, Anytown",
    "security_type": "residential",
    "security_value": 650000.00
  }
  ```
- **Response Example (201 Created)**:
  ```json
  {
    "id": 125,
    "reference_number": "A12347",
    "loan_amount": 500000.00,
    "loan_term": 30,
    "interest_rate": 4.5,
    "purpose": "Home purchase",
    "repayment_frequency": "monthly",
    "application_type": "residential",
    "product_id": "PROD001",
    "estimated_settlement_date": "2023-05-30",
    "stage": "inquiry",
    "stage_display": "Inquiry",
    "broker": {
      "id": 42,
      "name": "John Smith",
      "company": "ABC Brokers"
    },
    "bd": {
      "id": 15,
      "name": "Jane Wilson"
    },
    "branch": {
      "id": 7,
      "name": "Downtown Branch"
    },
    "security_address": "123 Main St, Anytown",
    "security_type": "residential",
    "security_value": 650000.00,
    "created_at": "2023-04-30T09:15:00Z",
    "created_by": {
      "id": 5,
      "name": "Admin User"
    }
  }
  ```

#### 1.5 Failed Application Creation (Invalid Data)
- **Actor**: Authenticated user
- **Description**: User attempts to create application with invalid data
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated POST request with invalid data
  2. System validates authentication token
  3. System validates input data and finds errors
  4. System returns validation error
- **Postconditions**: No application is created
- **Request Example**:
  ```
  POST /api/applications/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "loan_amount": -500000.00,
    "loan_term": 0,
    "interest_rate": -1.5,
    "purpose": "",
    "repayment_frequency": "invalid",
    "application_type": "unknown",
    "stage": "invalid_stage"
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "loan_amount": ["Ensure this value is greater than 0."],
    "loan_term": ["Ensure this value is greater than 0."],
    "interest_rate": ["Ensure this value is greater than 0."],
    "purpose": ["This field may not be blank."],
    "repayment_frequency": ["\"invalid\" is not a valid choice."],
    "application_type": ["\"unknown\" is not a valid choice."],
    "stage": ["\"invalid_stage\" is not a valid choice."],
    "broker": ["This field is required."],
    "product_id": ["This field is required."]
  }
  ```

## 2. Application Detail Operations API

### API Details
- **Endpoint**: `/api/applications/{id}/`
- **HTTP Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication Required**: Yes

### Use Cases

#### 2.1 Get Application Details
- **Actor**: Authenticated user
- **Description**: User retrieves details of a specific application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated GET request with application ID
  2. System validates authentication token
  3. System verifies user has access to application
  4. System retrieves application details
  5. System returns comprehensive application information
- **Postconditions**: User receives detailed application information
- **Request Example**:
  ```
  GET /api/applications/123/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 123,
    "reference_number": "A12345",
    "loan_amount": 500000.00,
    "loan_term": 30,
    "interest_rate": 4.5,
    "purpose": "Home purchase",
    "repayment_frequency": "monthly",
    "application_type": "residential",
    "product_id": "PROD001",
    "estimated_settlement_date": "2023-05-30",
    "stage": "formal_approval",
    "stage_display": "Formal Approval",
    "broker": {
      "id": 42,
      "name": "John Smith",
      "company": "ABC Brokers"
    },
    "bd": {
      "id": 15,
      "name": "Jane Wilson"
    },
    "branch": {
      "id": 7,
      "name": "Downtown Branch"
    },
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
      }
    ],
    "guarantors": [
      {
        "id": 101,
        "first_name": "Robert",
        "last_name": "Smith",
        "email": "robert@example.com"
      }
    ],
    "security_address": "123 Main St, Anytown",
    "security_type": "residential",
    "security_value": 650000.00,
    "documents": [
      {
        "id": 301,
        "title": "Income Statement",
        "document_type": "financial",
        "uploaded_at": "2023-04-16T11:30:00Z"
      },
      {
        "id": 302,
        "title": "Property Valuation",
        "document_type": "valuation",
        "uploaded_at": "2023-04-18T14:20:00Z"
      }
    ],
    "notes": [
      {
        "id": 401,
        "content": "Client requested expedited processing",
        "created_at": "2023-04-16T09:45:00Z",
        "created_by": {
          "id": 5,
          "name": "Admin User"
        }
      }
    ],
    "fees": [
      {
        "id": 501,
        "fee_type": "application",
        "amount": 500.00,
        "is_paid": true,
        "due_date": "2023-04-20",
        "paid_date": "2023-04-19"
      },
      {
        "id": 502,
        "fee_type": "valuation",
        "amount": 750.00,
        "is_paid": false,
        "due_date": "2023-04-25"
      }
    ],
    "repayments": [
      {
        "id": 601,
        "amount": 2684.11,
        "due_date": "2023-06-30",
        "is_paid": false
      },
      {
        "id": 602,
        "amount": 2684.11,
        "due_date": "2023-07-31",
        "is_paid": false
      }
    ],
    "created_at": "2023-04-15T10:30:00Z",
    "updated_at": "2023-04-18T14:20:00Z",
    "created_by": {
      "id": 5,
      "name": "Admin User"
    },
    "signature": {
      "is_signed": false,
      "signed_by": null,
      "signed_date": null
    }
  }
  ```

#### 2.2 Update Application (Full Update)
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User updates all application information
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to update it
- **Steps**:
  1. User sends authenticated PUT request with application ID and all application fields
  2. System validates authentication token
  3. System verifies user has permission to update application
  4. System validates input data
  5. System updates application
  6. System returns updated application details
- **Postconditions**: Application is updated with new information
- **Request Example**:
  ```
  PUT /api/applications/123/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "loan_amount": 550000.00,
    "loan_term": 25,
    "interest_rate": 4.75,
    "purpose": "Home purchase and renovation",
    "repayment_frequency": "monthly",
    "application_type": "residential",
    "product_id": "PROD001",
    "estimated_settlement_date": "2023-06-15",
    "stage": "formal_approval",
    "broker": 42,
    "bd": 15,
    "branch": 7,
    "security_address": "123 Main St, Anytown",
    "security_type": "residential",
    "security_value": 700000.00
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 123,
    "reference_number": "A12345",
    "loan_amount": 550000.00,
    "loan_term": 25,
    "interest_rate": 4.75,
    "purpose": "Home purchase and renovation",
    "repayment_frequency": "monthly",
    "application_type": "residential",
    "product_id": "PROD001",
    "estimated_settlement_date": "2023-06-15",
    "stage": "formal_approval",
    "stage_display": "Formal Approval",
    "broker": {
      "id": 42,
      "name": "John Smith",
      "company": "ABC Brokers"
    },
    "bd": {
      "id": 15,
      "name": "Jane Wilson"
    },
    "branch": {
      "id": 7,
      "name": "Downtown Branch"
    },
    "security_address": "123 Main St, Anytown",
    "security_type": "residential",
    "security_value": 700000.00,
    // ... other application details
    "updated_at": "2023-04-30T10:15:00Z"
  }
  ```

#### 2.3 Update Application (Partial Update)
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User updates specific application fields
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to update it
- **Steps**:
  1. User sends authenticated PATCH request with application ID and specific fields
  2. System validates authentication token
  3. System verifies user has permission to update application
  4. System validates input data
  5. System updates only the provided fields
  6. System returns updated application details
- **Postconditions**: Specified application fields are updated
- **Request Example**:
  ```
  PATCH /api/applications/123/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "loan_amount": 550000.00,
    "estimated_settlement_date": "2023-06-15"
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 123,
    "reference_number": "A12345",
    "loan_amount": 550000.00,
    "loan_term": 30,
    "interest_rate": 4.5,
    "purpose": "Home purchase",
    "repayment_frequency": "monthly",
    "application_type": "residential",
    "product_id": "PROD001",
    "estimated_settlement_date": "2023-06-15",
    "stage": "formal_approval",
    "stage_display": "Formal Approval",
    // ... other unchanged application details
    "updated_at": "2023-04-30T10:15:00Z"
  }
  ```

#### 2.4 Delete Application
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User deletes an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to delete it
- **Steps**:
  1. User sends authenticated DELETE request with application ID
  2. System validates authentication token
  3. System verifies user has permission to delete application
  4. System deletes application
  5. System returns success confirmation
- **Postconditions**: Application is deleted from the system
- **Request Example**:
  ```
  DELETE /api/applications/123/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (204 No Content)**:
  ```
  (Empty response body)
  ```

#### 2.5 Failed Application Detail Operations (Not Found)
- **Actor**: Authenticated user
- **Description**: User attempts to access a non-existent application
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET/PUT/PATCH/DELETE request with non-existent application ID
  2. System validates authentication token
  3. System attempts to find application and fails
  4. System returns not found error
- **Postconditions**: No application is accessed or modified
- **Request Example**:
  ```
  GET /api/applications/9999/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (404 Not Found)**:
  ```json
  {
    "detail": "Not found."
  }
  ```

#### 2.6 Failed Application Update (Invalid Data)
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User attempts to update application with invalid data
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to update it
- **Steps**:
  1. User sends authenticated PUT/PATCH request with application ID and invalid data
  2. System validates authentication token
  3. System verifies user has permission to update application
  4. System validates input data and finds errors
  5. System returns validation error
- **Postconditions**: Application remains unchanged
- **Request Example**:
  ```
  PATCH /api/applications/123/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "loan_amount": -10000.00,
    "stage": "invalid_stage"
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "loan_amount": ["Ensure this value is greater than 0."],
    "stage": ["\"invalid_stage\" is not a valid choice."]
  }
  ```

## 3. Create Application with Cascade API

### API Details
- **Endpoint**: `/api/applications/create-with-cascade/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes

### Use Cases

#### 3.1 Create Application with Related Entities
- **Actor**: Authenticated user
- **Description**: User creates a new application along with related borrowers, guarantors, and company borrowers
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated POST request with application data and related entities
  2. System validates authentication token
  3. System validates input data
  4. System creates application and all related entities in a transaction
  5. System returns created application with related entities
- **Postconditions**: New application and related entities are created in the system
- **Request Example**:
  ```
  POST /api/applications/create-with-cascade/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "loan_amount": 500000.00,
    "loan_term": 30,
    "interest_rate": 4.5,
    "purpose": "Home purchase",
    "repayment_frequency": "monthly",
    "application_type": "residential",
    "product_id": "PROD001",
    "estimated_settlement_date": "2023-05-30",
    "stage": "inquiry",
    "broker": 42,
    "bd": 15,
    "branch": 7,
    "security_address": "123 Main St, Anytown",
    "security_type": "residential",
    "security_value": 650000.00,
    "borrowers": [
      {
        "first_name": "Michael",
        "last_name": "Johnson",
        "email": "michael@example.com",
        "phone": "+1234567890",
        "residential_address": "456 Oak St, Anytown",
        "date_of_birth": "1980-05-15",
        "employment_type": "full_time",
        "annual_income": 120000.00
      },
      {
        "first_name": "Sarah",
        "last_name": "Johnson",
        "email": "sarah@example.com",
        "phone": "+1234567891",
        "residential_address": "456 Oak St, Anytown",
        "date_of_birth": "1982-08-20",
        "employment_type": "part_time",
        "annual_income": 60000.00
      }
    ],
    "guarantors": [
      {
        "guarantor_type": "individual",
        "first_name": "Robert",
        "last_name": "Smith",
        "email": "robert@example.com",
        "phone": "+1234567892",
        "address": "789 Pine St, Anytown",
        "relationship_to_borrower": "parent"
      }
    ],
    "company_borrowers": [
      {
        "company_name": "Johnson Enterprises",
        "abn": "12345678901",
        "acn": "123456789",
        "business_address": "101 Business Ave, Anytown",
        "contact_name": "Michael Johnson",
        "contact_email": "contact@johnsonenterprises.com",
        "contact_phone": "+1234567893"
      }
    ]
  }
  ```
- **Response Example (201 Created)**:
  ```json
  {
    "id": 125,
    "reference_number": "A12347",
    "loan_amount": 500000.00,
    "loan_term": 30,
    "interest_rate": 4.5,
    "purpose": "Home purchase",
    "repayment_frequency": "monthly",
    "application_type": "residential",
    "product_id": "PROD001",
    "estimated_settlement_date": "2023-05-30",
    "stage": "inquiry",
    "stage_display": "Inquiry",
    "broker": {
      "id": 42,
      "name": "John Smith",
      "company": "ABC Brokers"
    },
    "bd": {
      "id": 15,
      "name": "Jane Wilson"
    },
    "branch": {
      "id": 7,
      "name": "Downtown Branch"
    },
    "borrowers": [
      {
        "id": 203,
        "first_name": "Michael",
        "last_name": "Johnson",
        "email": "michael@example.com",
        "phone": "+1234567890",
        "residential_address": "456 Oak St, Anytown",
        "date_of_birth": "1980-05-15",
        "employment_type": "full_time",
        "annual_income": 120000.00
      },
      {
        "id": 204,
        "first_name": "Sarah",
        "last_name": "Johnson",
        "email": "sarah@example.com",
        "phone": "+1234567891",
        "residential_address": "456 Oak St, Anytown",
        "date_of_birth": "1982-08-20",
        "employment_type": "part_time",
        "annual_income": 60000.00
      }
    ],
    "guarantors": [
      {
        "id": 102,
        "guarantor_type": "individual",
        "first_name": "Robert",
        "last_name": "Smith",
        "email": "robert@example.com",
        "phone": "+1234567892",
        "address": "789 Pine St, Anytown",
        "relationship_to_borrower": "parent"
      }
    ],
    "company_borrowers": [
      {
        "id": 50,
        "company_name": "Johnson Enterprises",
        "abn": "12345678901",
        "acn": "123456789",
        "business_address": "101 Business Ave, Anytown",
        "contact_name": "Michael Johnson",
        "contact_email": "contact@johnsonenterprises.com",
        "contact_phone": "+1234567893"
      }
    ],
    "security_address": "123 Main St, Anytown",
    "security_type": "residential",
    "security_value": 650000.00,
    "created_at": "2023-04-30T09:15:00Z",
    "created_by": {
      "id": 5,
      "name": "Admin User"
    }
  }
  ```

#### 3.2 Failed Cascade Creation (Transaction Rollback)
- **Actor**: Authenticated user
- **Description**: User attempts to create application with related entities but some data is invalid
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated POST request with application data and related entities
  2. System validates authentication token
  3. System validates input data and finds errors in one or more entities
  4. System returns validation error without creating any entities
- **Postconditions**: No application or related entities are created
- **Request Example**:
  ```
  POST /api/applications/create-with-cascade/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "loan_amount": 500000.00,
    "loan_term": 30,
    "interest_rate": 4.5,
    "purpose": "Home purchase",
    "repayment_frequency": "monthly",
    "application_type": "residential",
    "product_id": "PROD001",
    "estimated_settlement_date": "2023-05-30",
    "stage": "inquiry",
    "broker": 42,
    "bd": 15,
    "branch": 7,
    "security_address": "123 Main St, Anytown",
    "security_type": "residential",
    "security_value": 650000.00,
    "borrowers": [
      {
        "first_name": "Michael",
        "last_name": "Johnson",
        "email": "invalid-email",
        "phone": "invalid-phone",
        "date_of_birth": "invalid-date"
      }
    ],
    "guarantors": [
      {
        "guarantor_type": "invalid-type",
        "first_name": "Robert",
        "last_name": "Smith"
      }
    ]
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "borrowers": [
      {
        "email": ["Enter a valid email address."],
        "phone": ["Phone number must be in the format +1234567890."],
        "date_of_birth": ["Date has wrong format. Use YYYY-MM-DD format."]
      }
    ],
    "guarantors": [
      {
        "guarantor_type": ["\"invalid-type\" is not a valid choice."]
      }
    ]
  }
  ```
