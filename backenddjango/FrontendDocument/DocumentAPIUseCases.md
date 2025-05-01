# Document API Use Cases

This document outlines the use cases for the Document APIs in the CRM Loan Management System.

## 1. List or Create Documents API

### API Details
- **Endpoint**: `/api/documents/documents/`
- **HTTP Methods**: `GET`, `POST`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 1.1 List All Documents
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User retrieves a paginated list of documents
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System filters documents based on user role:
     - Admin: All documents
     - Broker: Only documents associated with applications where the user is the broker
     - BD: Only documents associated with applications where the user is the BD
     - Client: Only documents associated with their borrower profile or applications
  4. System returns paginated list of documents
- **Response**: List of documents with their details
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 1.2 Filter Documents
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User filters documents by various criteria
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System applies filters and returns matching documents
- **Query Parameters**:
  - `document_type`: Filter by document type
  - `application`: Filter by application ID
  - `borrower`: Filter by borrower ID
  - `search`: Search across title, description, file_name
  - `created_after`: Filter by creation date (after)
  - `created_before`: Filter by creation date (before)
- **Response**: Filtered list of documents
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 1.3 Search Documents
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User searches for documents by title, description, or file name
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with search parameter
  2. System searches across title, description, file_name fields
  3. System returns matching documents
- **Query Parameters**:
  - `search`: Search term
- **Response**: List of matching documents
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

### Use Cases for POST Method

#### 1.4 Upload New Document
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User uploads a new document
- **Preconditions**: User is authenticated with valid JWT token and has appropriate permissions
- **Steps**:
  1. User sends authenticated POST request with document data and file
  2. System validates the data
  3. System creates new document and associates it with the creator
  4. System returns the created document details
- **Request Body**:
  ```
  Content-Type: multipart/form-data
  
  title: "Loan Application Form"
  description: "Completed application form for John Doe"
  document_type: "application_form"
  application: 1
  borrower: 2
  file: [binary file data]
  ```
- **Response**: Created document details including file URL
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden

## 2. Document Detail Operations API

### API Details
- **Endpoint**: `/api/documents/documents/{id}/`
- **HTTP Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 2.1 Retrieve Document Details
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User retrieves detailed information about a specific document
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested document
- **Steps**:
  1. User sends authenticated GET request with document ID
  2. System validates user has access to the document
  3. System returns detailed document information
- **Response**: Detailed document information including all fields and file URL
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PUT Method

#### 2.2 Update Document (Full Update)
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User updates all information for a document
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the document
- **Steps**:
  1. User sends authenticated PUT request with complete document data
  2. System validates the data
  3. If file is included, system creates a new version of the document
  4. If only metadata is updated, system updates the existing document
  5. System returns the updated document details
- **Request Body**: Complete document data (all fields required)
- **Response**: Updated document details or new version details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PATCH Method

#### 2.3 Update Document (Partial Update)
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User updates specific information for a document
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the document
- **Steps**:
  1. User sends authenticated PATCH request with partial document data
  2. System validates the data
  3. If file is included, system creates a new version of the document
  4. If only metadata is updated, system updates only the provided fields
  5. System returns the updated document details
- **Request Body**: Partial document data (only fields to update)
  ```json
  {
    "title": "Updated Title",
    "description": "Updated description for the document"
  }
  ```
- **Response**: Updated document details or new version details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for DELETE Method

#### 2.4 Delete Document
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User deletes a document
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the document
- **Steps**:
  1. User sends authenticated DELETE request with document ID
  2. System validates user has permission to delete
  3. System deletes the document
- **Response**: No content
- **Status Codes**:
  - 204: No Content (success)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 3. Download Document API

### API Details
- **Endpoint**: `/api/documents/documents/{id}/download/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 3.1 Download Document File
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User downloads a document file
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested document
- **Steps**:
  1. User sends authenticated GET request with document ID
  2. System validates user has access to the document
  3. System retrieves the document file
  4. System returns the file as a download
- **Response**: Binary file data with appropriate Content-Disposition header
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found (document or file not found)

## 4. Create Document Version API

### API Details
- **Endpoint**: `/api/documents/documents/{id}/create-version/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes

### Use Cases for POST Method

#### 4.1 Create New Document Version
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User creates a new version of an existing document
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the document
- **Steps**:
  1. User sends authenticated POST request with document ID and new file
  2. System validates the data
  3. System creates a new version of the document with incremented version number
  4. System links the new version to the previous version
  5. System returns the new version details
- **Request Body**:
  ```
  Content-Type: multipart/form-data
  
  description: "Updated version with corrections"
  file: [binary file data]
  ```
- **Response**: 
  ```json
  {
    "message": "New version created successfully",
    "document_id": 5,
    "version": 2,
    "document_url": "http://example.com/media/documents/APP-12345678/document.pdf"
  }
  ```
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error or no file provided)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 5. List or Create Notes API

### API Details
- **Endpoint**: `/api/documents/notes/`
- **HTTP Methods**: `GET`, `POST`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 5.1 List All Notes
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User retrieves a paginated list of notes
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System filters notes based on user role:
     - Admin: All notes
     - Broker: Only notes associated with applications where the user is the broker
     - BD: Only notes associated with applications where the user is the BD
     - Client: Only notes associated with their borrower profile or applications
  4. System returns paginated list of notes
- **Response**: List of notes with their details
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 5.2 Filter Notes
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User filters notes by various criteria
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System applies filters and returns matching notes
- **Query Parameters**:
  - `application`: Filter by application ID
  - `borrower`: Filter by borrower ID
  - `search`: Search across title, content
  - `created_after`: Filter by creation date (after)
  - `created_before`: Filter by creation date (before)
- **Response**: Filtered list of notes
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

### Use Cases for POST Method

#### 5.3 Create New Note
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User creates a new note
- **Preconditions**: User is authenticated with valid JWT token and has appropriate permissions
- **Steps**:
  1. User sends authenticated POST request with note data
  2. System validates the data
  3. System creates new note and associates it with the creator
  4. System returns the created note details
- **Request Body**:
  ```json
  {
    "title": "Follow-up Required",
    "content": "Need to contact borrower about missing bank statements",
    "remind_date": "2025-05-15T10:00:00Z",
    "application": 1,
    "borrower": 2
  }
  ```
- **Response**: Created note details
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden

## 6. Note Detail Operations API

### API Details
- **Endpoint**: `/api/documents/notes/{id}/`
- **HTTP Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 6.1 Retrieve Note Details
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User retrieves detailed information about a specific note
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested note
- **Steps**:
  1. User sends authenticated GET request with note ID
  2. System validates user has access to the note
  3. System returns detailed note information
- **Response**: Detailed note information including all fields
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PUT/PATCH Methods

#### 6.2 Update Note
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User updates information for a note
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the note
- **Steps**:
  1. User sends authenticated PUT/PATCH request with note data
  2. System validates the data
  3. System updates the note
  4. System returns the updated note details
- **Request Body**: Complete or partial note data
  ```json
  {
    "title": "Updated Title",
    "content": "Updated content with additional information",
    "remind_date": "2025-05-20T14:00:00Z"
  }
  ```
- **Response**: Updated note details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for DELETE Method

#### 6.3 Delete Note
- **Actor**: Authenticated user (Admin, Broker)
- **Description**: User deletes a note
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the note
- **Steps**:
  1. User sends authenticated DELETE request with note ID
  2. System validates user has permission to delete
  3. System deletes the note
- **Response**: No content
- **Status Codes**:
  - 204: No Content (success)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 7. List or Create Fees API

### API Details
- **Endpoint**: `/api/documents/fees/`
- **HTTP Methods**: `GET`, `POST`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 7.1 List All Fees
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User retrieves a paginated list of fees
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System filters fees based on user role:
     - Admin: All fees
     - Broker: Only fees associated with applications where the user is the broker
     - BD: Only fees associated with applications where the user is the BD
     - Client: Only fees associated with their applications
  4. System returns paginated list of fees
- **Response**: List of fees with their details
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 7.2 Filter Fees
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User filters fees by various criteria
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System applies filters and returns matching fees
- **Query Parameters**:
  - `fee_type`: Filter by fee type
  - `application`: Filter by application ID
  - `min_amount`: Filter by minimum amount
  - `max_amount`: Filter by maximum amount
  - `due_after`: Filter by due date (after)
  - `due_before`: Filter by due date (before)
  - `is_paid`: Filter by paid status (true/false)
- **Response**: Filtered list of fees
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

### Use Cases for POST Method

#### 7.3 Create New Fee
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User creates a new fee
- **Preconditions**: User is authenticated with valid JWT token and has appropriate permissions
- **Steps**:
  1. User sends authenticated POST request with fee data
  2. System validates the data
  3. System creates new fee and associates it with the creator
  4. System returns the created fee details
- **Request Body**:
  ```json
  {
    "fee_type": "application",
    "description": "Application processing fee",
    "amount": 500.00,
    "due_date": "2025-05-15",
    "application": 1
  }
  ```
- **Response**: Created fee details
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden

## 8. Fee Detail Operations API

### API Details
- **Endpoint**: `/api/documents/fees/{id}/`
- **HTTP Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 8.1 Retrieve Fee Details
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User retrieves detailed information about a specific fee
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested fee
- **Steps**:
  1. User sends authenticated GET request with fee ID
  2. System validates user has access to the fee
  3. System returns detailed fee information
- **Response**: Detailed fee information including all fields
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PUT/PATCH Methods

#### 8.2 Update Fee
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User updates information for a fee
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the fee
- **Steps**:
  1. User sends authenticated PUT/PATCH request with fee data
  2. System validates the data
  3. System updates the fee
  4. System returns the updated fee details
- **Request Body**: Complete or partial fee data
  ```json
  {
    "description": "Updated fee description",
    "amount": 550.00,
    "due_date": "2025-05-20"
  }
  ```
- **Response**: Updated fee details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for DELETE Method

#### 8.3 Delete Fee
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User deletes a fee
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the fee
- **Steps**:
  1. User sends authenticated DELETE request with fee ID
  2. System validates user has permission to delete
  3. System deletes the fee
- **Response**: No content
- **Status Codes**:
  - 204: No Content (success)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 9. Mark Fee as Paid API

### API Details
- **Endpoint**: `/api/documents/fees/{id}/mark-paid/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes

### Use Cases for POST Method

#### 9.1 Mark Fee as Paid
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User marks a fee as paid
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the fee
- **Steps**:
  1. User sends authenticated POST request with fee ID
  2. System validates user has permission to update the fee
  3. System updates the fee's paid_date field
  4. System returns the updated fee details
- **Request Body**:
  ```json
  {
    "paid_date": "2025-05-10"
  }
  ```
  Note: If paid_date is not provided, the current date is used.
- **Response**: 
  ```json
  {
    "message": "Fee marked as paid",
    "fee_id": 1,
    "paid_date": "2025-05-10"
  }
  ```
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 10. List or Create Repayments API

### API Details
- **Endpoint**: `/api/documents/repayments/`
- **HTTP Methods**: `GET`, `POST`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 10.1 List All Repayments
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User retrieves a paginated list of repayments
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System filters repayments based on user role:
     - Admin: All repayments
     - Broker: Only repayments associated with applications where the user is the broker
     - BD: Only repayments associated with applications where the user is the BD
     - Client: Only repayments associated with their applications
  4. System returns paginated list of repayments
- **Response**: List of repayments with their details
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 10.2 Filter Repayments
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User filters repayments by various criteria
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System applies filters and returns matching repayments
- **Query Parameters**:
  - `application`: Filter by application ID
  - `min_amount`: Filter by minimum amount
  - `max_amount`: Filter by maximum amount
  - `due_after`: Filter by due date (after)
  - `due_before`: Filter by due date (before)
  - `is_paid`: Filter by paid status (true/false)
- **Response**: Filtered list of repayments
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

### Use Cases for POST Method

#### 10.3 Create New Repayment
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User creates a new repayment
- **Preconditions**: User is authenticated with valid JWT token and has appropriate permissions
- **Steps**:
  1. User sends authenticated POST request with repayment data
  2. System validates the data
  3. System creates new repayment and associates it with the creator
  4. System returns the created repayment details
- **Request Body**:
  ```json
  {
    "amount": 1000.00,
    "due_date": "2025-06-15",
    "application": 1
  }
  ```
- **Response**: Created repayment details
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden

## 11. Repayment Detail Operations API

### API Details
- **Endpoint**: `/api/documents/repayments/{id}/`
- **HTTP Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 11.1 Retrieve Repayment Details
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User retrieves detailed information about a specific repayment
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested repayment
- **Steps**:
  1. User sends authenticated GET request with repayment ID
  2. System validates user has access to the repayment
  3. System returns detailed repayment information
- **Response**: Detailed repayment information including all fields
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PUT/PATCH Methods

#### 11.2 Update Repayment
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User updates information for a repayment
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the repayment
- **Steps**:
  1. User sends authenticated PUT/PATCH request with repayment data
  2. System validates the data
  3. System updates the repayment
  4. System returns the updated repayment details
- **Request Body**: Complete or partial repayment data
  ```json
  {
    "amount": 1050.00,
    "due_date": "2025-06-20"
  }
  ```
- **Response**: Updated repayment details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for DELETE Method

#### 11.3 Delete Repayment
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User deletes a repayment
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the repayment
- **Steps**:
  1. User sends authenticated DELETE request with repayment ID
  2. System validates user has permission to delete
  3. System deletes the repayment
- **Response**: No content
- **Status Codes**:
  - 204: No Content (success)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 12. Mark Repayment as Paid API

### API Details
- **Endpoint**: `/api/documents/repayments/{id}/mark-paid/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes

### Use Cases for POST Method

#### 12.1 Mark Repayment as Paid
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User marks a repayment as paid
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has appropriate permissions
  - User has access to the repayment
- **Steps**:
  1. User sends authenticated POST request with repayment ID
  2. System validates user has permission to update the repayment
  3. System updates the repayment's paid_date field
  4. System returns the updated repayment details
- **Request Body**:
  ```json
  {
    "paid_date": "2025-06-10"
  }
  ```
  Note: If paid_date is not provided, the current date is used.
- **Response**: 
  ```json
  {
    "message": "Repayment marked as paid",
    "repayment_id": 1,
    "paid_date": "2025-06-10"
  }
  ```
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 13. Get Application Ledger API

### API Details
- **Endpoint**: `/api/documents/applications/{application_id}/ledger/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 13.1 Retrieve Application Ledger
- **Actor**: Authenticated user (Admin, Broker, BD, Client)
- **Description**: User retrieves the financial ledger for a specific application
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested application
- **Steps**:
  1. User sends authenticated GET request with application ID
  2. System validates user has access to the application
  3. System retrieves all ledger entries for the application
  4. System returns the ledger entries
- **Response**: List of ledger entries with their details
  ```json
  [
    {
      "id": 1,
      "application": 1,
      "transaction_type": "fee_created",
      "transaction_type_display": "Fee Created",
      "amount": 500.00,
      "description": "Application fee created",
      "transaction_date": "2025-05-01T10:30:00Z",
      "related_fee": 1,
      "related_fee_type": "Application Fee",
      "related_repayment": null,
      "created_by": 1,
      "created_at": "2025-05-01T10:30:00Z"
    },
    {
      "id": 2,
      "application": 1,
      "transaction_type": "fee_paid",
      "transaction_type_display": "Fee Paid",
      "amount": 500.00,
      "description": "Application fee paid",
      "transaction_date": "2025-05-05T14:20:00Z",
      "related_fee": 1,
      "related_fee_type": "Application Fee",
      "related_repayment": null,
      "created_by": 1,
      "created_at": "2025-05-05T14:20:00Z"
    },
    {
      "id": 3,
      "application": 1,
      "transaction_type": "repayment_scheduled",
      "transaction_type_display": "Repayment Scheduled",
      "amount": 1000.00,
      "description": "Monthly repayment scheduled",
      "transaction_date": "2025-05-10T09:00:00Z",
      "related_fee": null,
      "related_fee_type": null,
      "related_repayment": 1,
      "created_by": 1,
      "created_at": "2025-05-10T09:00:00Z"
    }
  ]
  ```
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found
