# Application API Use Cases - Part 3

This document outlines the use cases for the Application APIs in the CRM Loan Management System (Part 3).

## 11. Get Application Documents API

### API Details
- **Endpoint**: `/api/applications/{id}/documents/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases

#### 11.1 Get Application Documents
- **Actor**: Authenticated user
- **Description**: User retrieves documents associated with an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated GET request with application ID
  2. System validates authentication token
  3. System verifies user has access to application
  4. System retrieves paginated documents associated with application
  5. System returns document list
- **Postconditions**: User receives list of application documents
- **Request Example**:
  ```
  GET /api/applications/123/documents/?limit=10&offset=0
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
        "id": 301,
        "title": "Income Statement",
        "file": "/media/documents/income_statement.pdf",
        "document_type": "financial",
        "uploaded_at": "2023-04-16T11:30:00Z",
        "uploaded_by": {
          "id": 42,
          "name": "John Smith"
        }
      },
      {
        "id": 302,
        "title": "Property Valuation",
        "file": "/media/documents/property_valuation.pdf",
        "document_type": "valuation",
        "uploaded_at": "2023-04-18T14:20:00Z",
        "uploaded_by": {
          "id": 15,
          "name": "Jane Wilson"
        }
      },
      {
        "id": 303,
        "title": "Loan Agreement",
        "file": "/media/documents/loan_agreement.pdf",
        "document_type": "contract",
        "uploaded_at": "2023-04-20T09:45:00Z",
        "uploaded_by": {
          "id": 5,
          "name": "Admin User"
        }
      }
    ]
  }
  ```

#### 11.2 Filter Documents by Type
- **Actor**: Authenticated user
- **Description**: User filters documents by document type
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated GET request with application ID and document type filter
  2. System validates authentication token
  3. System verifies user has access to application
  4. System retrieves documents matching the filter
  5. System returns filtered document list
- **Postconditions**: User receives filtered list of documents
- **Request Example**:
  ```
  GET /api/applications/123/documents/?document_type=financial&limit=10
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
        "id": 301,
        "title": "Income Statement",
        "file": "/media/documents/income_statement.pdf",
        "document_type": "financial",
        "uploaded_at": "2023-04-16T11:30:00Z",
        "uploaded_by": {
          "id": 42,
          "name": "John Smith"
        }
      }
    ]
  }
  ```

## 12. Upload Application Document API

### API Details
- **Endpoint**: `/api/applications/{id}/upload_document/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes
- **Note**: The endpoint uses an underscore (`upload_document`) rather than a hyphen (`upload-document`) in the actual implementation.

### Use Cases

#### 12.1 Upload Document to Application
- **Actor**: Authenticated user
- **Description**: User uploads a document to an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated POST request with application ID, document title, type, and file
  2. System validates authentication token
  3. System verifies user has access to application
  4. System validates document data and file
  5. System saves document and associates it with application
  6. System returns created document details
- **Postconditions**: New document is added to application
- **Request Example**:
  ```
  POST /api/applications/123/upload_document/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: multipart/form-data

  title: Bank Statement
  document_type: financial
  file: [binary file data]
  ```
- **Response Example (201 Created)**:
  ```json
  {
    "id": 304,
    "title": "Bank Statement",
    "file": "/media/documents/bank_statement.pdf",
    "document_type": "financial",
    "uploaded_at": "2023-04-30T16:45:00Z",
    "uploaded_by": {
      "id": 5,
      "name": "Admin User"
    }
  }
  ```

#### 12.2 Failed Document Upload (Invalid File)
- **Actor**: Authenticated user
- **Description**: User attempts to upload an invalid document
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated POST request with application ID and invalid file
  2. System validates authentication token
  3. System verifies user has access to application
  4. System validates document data and finds file is invalid
  5. System returns validation error
- **Postconditions**: No document is added to application
- **Request Example**:
  ```
  POST /api/applications/123/upload_document/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: multipart/form-data

  title: Bank Statement
  document_type: financial
  file: [invalid file data]
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "file": ["The submitted file is empty.", "Upload a valid document. The file you uploaded was either not a document or a corrupted document."]
  }
  ```

#### 12.3 Failed Document Upload (Missing Required Fields)
- **Actor**: Authenticated user
- **Description**: User attempts to upload a document without required fields
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated POST request with application ID but missing required fields
  2. System validates authentication token
  3. System verifies user has access to application
  4. System validates document data and finds missing required fields
  5. System returns validation error
- **Postconditions**: No document is added to application
- **Request Example**:
  ```
  POST /api/applications/123/upload_document/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: multipart/form-data

  title: Bank Statement
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "document_type": ["This field is required."],
    "file": ["No file was submitted."]
  }
  ```

## 13. Get Application Fees API

### API Details
- **Endpoint**: `/api/applications/{id}/fees/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases

#### 13.1 Get Application Fees
- **Actor**: Authenticated user
- **Description**: User retrieves fees associated with an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated GET request with application ID
  2. System validates authentication token
  3. System verifies user has access to application
  4. System retrieves paginated fees associated with application
  5. System returns fee list
- **Postconditions**: User receives list of application fees
- **Request Example**:
  ```
  GET /api/applications/123/fees/?limit=10&offset=0
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
        "due_date": "2023-04-25",
        "paid_date": null
      },
      {
        "id": 503,
        "fee_type": "legal",
        "amount": 1200.00,
        "is_paid": false,
        "due_date": "2023-05-10",
        "paid_date": null
      }
    ]
  }
  ```

#### 13.2 Filter Fees by Payment Status
- **Actor**: Authenticated user
- **Description**: User filters fees by payment status
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated GET request with application ID and payment status filter
  2. System validates authentication token
  3. System verifies user has access to application
  4. System retrieves fees matching the filter
  5. System returns filtered fee list
- **Postconditions**: User receives filtered list of fees
- **Request Example**:
  ```
  GET /api/applications/123/fees/?is_paid=false&limit=10
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 502,
        "fee_type": "valuation",
        "amount": 750.00,
        "is_paid": false,
        "due_date": "2023-04-25",
        "paid_date": null
      },
      {
        "id": 503,
        "fee_type": "legal",
        "amount": 1200.00,
        "is_paid": false,
        "due_date": "2023-05-10",
        "paid_date": null
      }
    ]
  }
  ```

## 14. Add Application Fee API

### API Details
- **Endpoint**: `/api/applications/{id}/add_fee/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes
- **Note**: The endpoint uses an underscore (`add_fee`) rather than a hyphen (`add-fee`) in the actual implementation.

### Use Cases

#### 14.1 Add Fee to Application
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User adds a fee to an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to add fees
- **Steps**:
  1. User sends authenticated POST request with application ID and fee details
  2. System validates authentication token
  3. System verifies user has permission to add fees
  4. System validates fee data
  5. System creates new fee associated with application
  6. System returns created fee details
- **Postconditions**: New fee is added to application
- **Request Example**:
  ```
  POST /api/applications/123/add_fee/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "fee_type": "broker",
    "amount": 2500.00,
    "due_date": "2023-05-15"
  }
  ```
- **Response Example (201 Created)**:
  ```json
  {
    "id": 504,
    "fee_type": "broker",
    "amount": 2500.00,
    "is_paid": false,
    "due_date": "2023-05-15",
    "paid_date": null
  }
  ```

#### 14.2 Failed Fee Addition (Invalid Data)
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User attempts to add a fee with invalid data
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to add fees
- **Steps**:
  1. User sends authenticated POST request with application ID and invalid fee data
  2. System validates authentication token
  3. System verifies user has permission to add fees
  4. System validates fee data and finds errors
  5. System returns validation error
- **Postconditions**: No fee is added to application
- **Request Example**:
  ```
  POST /api/applications/123/add_fee/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "fee_type": "invalid_type",
    "amount": -500.00,
    "due_date": "invalid-date"
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "fee_type": ["\"invalid_type\" is not a valid choice."],
    "amount": ["Ensure this value is greater than 0."],
    "due_date": ["Date has wrong format. Use YYYY-MM-DD format."]
  }
  ```

## 15. Get Application Repayments API

### API Details
- **Endpoint**: `/api/applications/{id}/repayments/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases

#### 15.1 Get Application Repayments
- **Actor**: Authenticated user
- **Description**: User retrieves repayments associated with an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated GET request with application ID
  2. System validates authentication token
  3. System verifies user has access to application
  4. System retrieves paginated repayments associated with application
  5. System returns repayment list
- **Postconditions**: User receives list of application repayments
- **Request Example**:
  ```
  GET /api/applications/123/repayments/?limit=10&offset=0
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
        "id": 601,
        "amount": 2684.11,
        "due_date": "2023-06-30",
        "is_paid": false,
        "paid_date": null,
        "payment_method": null
      },
      {
        "id": 602,
        "amount": 2684.11,
        "due_date": "2023-07-31",
        "is_paid": false,
        "paid_date": null,
        "payment_method": null
      },
      {
        "id": 603,
        "amount": 2684.11,
        "due_date": "2023-08-31",
        "is_paid": false,
        "paid_date": null,
        "payment_method": null
      }
    ]
  }
  ```

#### 15.2 Filter Repayments by Payment Status and Date Range
- **Actor**: Authenticated user
- **Description**: User filters repayments by payment status and date range
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated GET request with application ID, payment status, and date range filters
  2. System validates authentication token
  3. System verifies user has access to application
  4. System retrieves repayments matching the filters
  5. System returns filtered repayment list
- **Postconditions**: User receives filtered list of repayments
- **Request Example**:
  ```
  GET /api/applications/123/repayments/?is_paid=false&date_from=2023-06-01&date_to=2023-07-31&limit=10
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 601,
        "amount": 2684.11,
        "due_date": "2023-06-30",
        "is_paid": false,
        "paid_date": null,
        "payment_method": null
      },
      {
        "id": 602,
        "amount": 2684.11,
        "due_date": "2023-07-31",
        "is_paid": false,
        "paid_date": null,
        "payment_method": null
      }
    ]
  }
  ```

## 16. Add Application Repayment API

### API Details
- **Endpoint**: `/api/applications/{id}/add_repayment/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes
- **Note**: The endpoint uses an underscore (`add_repayment`) rather than a hyphen (`add-repayment`) in the actual implementation.

### Use Cases

#### 16.1 Add Repayment to Application
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User adds a repayment to an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to add repayments
- **Steps**:
  1. User sends authenticated POST request with application ID and repayment details
  2. System validates authentication token
  3. System verifies user has permission to add repayments
  4. System validates repayment data
  5. System creates new repayment associated with application
  6. System returns created repayment details
- **Postconditions**: New repayment is added to application
- **Request Example**:
  ```
  POST /api/applications/123/add_repayment/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "amount": 2684.11,
    "due_date": "2023-09-30"
  }
  ```
- **Response Example (201 Created)**:
  ```json
  {
    "id": 604,
    "amount": 2684.11,
    "due_date": "2023-09-30",
    "is_paid": false,
    "paid_date": null,
    "payment_method": null
  }
  ```

#### 16.2 Failed Repayment Addition (Invalid Data)
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User attempts to add a repayment with invalid data
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to add repayments
- **Steps**:
  1. User sends authenticated POST request with application ID and invalid repayment data
  2. System validates authentication token
  3. System verifies user has permission to add repayments
  4. System validates repayment data and finds errors
  5. System returns validation error
- **Postconditions**: No repayment is added to application
- **Request Example**:
  ```
  POST /api/applications/123/add_repayment/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "amount": -500.00,
    "due_date": "invalid-date"
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "amount": ["Ensure this value is greater than 0."],
    "due_date": ["Date has wrong format. Use YYYY-MM-DD format."]
  }
  ```

## 17. Record Payment API

### API Details
- **Endpoint**: `/api/applications/{id}/record_payment/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes
- **Note**: The endpoint uses an underscore (`record_payment`) rather than a hyphen (`record-payment`) in the actual implementation.

### Use Cases

#### 17.1 Record Payment for Repayment
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User records a payment for a repayment
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to record payments
  - Repayment exists and is not already paid
- **Steps**:
  1. User sends authenticated POST request with application ID, repayment ID, and payment details
  2. System validates authentication token
  3. System verifies user has permission to record payments
  4. System validates payment data
  5. System updates repayment as paid
  6. System returns updated repayment details
- **Postconditions**: Repayment is marked as paid
- **Request Example**:
  ```
  POST /api/applications/123/record_payment/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "repayment_id": 601,
    "payment_amount": 2684.11,
    "payment_date": "2023-06-28",
    "payment_method": "bank_transfer"
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "id": 601,
    "amount": 2684.11,
    "due_date": "2023-06-30",
    "is_paid": true,
    "paid_date": "2023-06-28",
    "payment_method": "bank_transfer"
  }
  ```

#### 17.2 Failed Payment Recording (Invalid Repayment)
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User attempts to record payment for non-existent repayment
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to record payments
- **Steps**:
  1. User sends authenticated POST request with application ID and non-existent repayment ID
  2. System validates authentication token
  3. System verifies user has permission to record payments
  4. System attempts to find repayment and fails
  5. System returns not found error
- **Postconditions**: No payment is recorded
- **Request Example**:
  ```
  POST /api/applications/123/record_payment/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "repayment_id": 9999,
    "payment_amount": 2684.11,
    "payment_date": "2023-06-28",
    "payment_method": "bank_transfer"
  }
  ```
- **Response Example (404 Not Found)**:
  ```json
  {
    "error": "Repayment not found"
  }
  ```

#### 17.3 Failed Payment Recording (Already Paid)
- **Actor**: Authenticated user with appropriate permissions
- **Description**: User attempts to record payment for already paid repayment
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has permission to record payments
  - Repayment exists but is already marked as paid
- **Steps**:
  1. User sends authenticated POST request with application ID and already paid repayment ID
  2. System validates authentication token
  3. System verifies user has permission to record payments
  4. System finds repayment is already paid
  5. System returns already paid error
- **Postconditions**: Repayment payment details remain unchanged
- **Request Example**:
  ```
  POST /api/applications/123/record_payment/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "repayment_id": 601,
    "payment_amount": 2684.11,
    "payment_date": "2023-06-29",
    "payment_method": "credit_card"
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "error": "Repayment has already been paid"
  }
  ```

## 18. Get Application Ledger API

### API Details
- **Endpoint**: `/api/applications/{id}/ledger/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases

#### 18.1 Get Application Ledger
- **Actor**: Authenticated user
- **Description**: User retrieves ledger entries for an application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated GET request with application ID
  2. System validates authentication token
  3. System verifies user has access to application
  4. System retrieves paginated ledger entries for application
  5. System returns ledger entries
- **Postconditions**: User receives application ledger entries
- **Request Example**:
  ```
  GET /api/applications/123/ledger/?limit=10&offset=0
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
        "id": 701,
        "entry_type": "fee_added",
        "amount": 500.00,
        "date": "2023-04-15T11:30:00Z",
        "description": "Application fee added",
        "balance": -500.00
      },
      {
        "id": 702,
        "entry_type": "fee_paid",
        "amount": 500.00,
        "date": "2023-04-19T14:45:00Z",
        "description": "Application fee paid",
        "balance": 0.00
      },
      {
        "id": 703,
        "entry_type": "fee_added",
        "amount": 750.00,
        "date": "2023-04-18T10:15:00Z",
        "description": "Valuation fee added",
        "balance": -750.00
      },
      {
        "id": 704,
        "entry_type": "repayment_added",
        "amount": 2684.11,
        "date": "2023-04-20T09:30:00Z",
        "description": "June 2023 repayment scheduled",
        "balance": -750.00
      },
      {
        "id": 705,
        "entry_type": "repayment_received",
        "amount": 2684.11,
        "date": "2023-06-28T15:20:00Z",
        "description": "June 2023 repayment received",
        "balance": 1934.11
      }
    ]
  }
  ```

#### 18.2 Filter Ledger by Entry Type and Date Range
- **Actor**: Authenticated user
- **Description**: User filters ledger entries by type and date range
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Application exists and user has access to it
- **Steps**:
  1. User sends authenticated GET request with application ID, entry type, and date range filters
  2. System validates authentication token
  3. System verifies user has access to application
  4. System retrieves ledger entries matching the filters
  5. System returns filtered ledger entries
- **Postconditions**: User receives filtered ledger entries
- **Request Example**:
  ```
  GET /api/applications/123/ledger/?entry_type=fee_added&date_from=2023-04-01&date_to=2023-04-30&limit=10
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 701,
        "entry_type": "fee_added",
        "amount": 500.00,
        "date": "2023-04-15T11:30:00Z",
        "description": "Application fee added",
        "balance": -500.00
      },
      {
        "id": 703,
        "entry_type": "fee_added",
        "amount": 750.00,
        "date": "2023-04-18T10:15:00Z",
        "description": "Valuation fee added",
        "balance": -750.00
      }
    ]
  }
  ```
