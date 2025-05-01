# Broker API Use Cases

This document outlines the use cases for the Broker APIs in the CRM Loan Management System.

## 1. List or Create Brokers API

### API Details
- **Endpoint**: `/api/brokers/`
- **HTTP Methods**: `GET`, `POST`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 1.1 List All Brokers
- **Actor**: Authenticated user (Admin, BD, Broker)
- **Description**: User retrieves a paginated list of brokers
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System filters brokers based on user role:
     - Admin: All brokers
     - BD: Only brokers associated with the BD
     - Broker: Only their own broker profile
  4. System returns paginated list of brokers with minimal information
- **Response**: List of brokers with fields: id, name, company, email, phone, branch_name, application_count
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 1.2 Filter Brokers
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User filters brokers by various criteria
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System applies filters and returns matching brokers
- **Query Parameters**:
  - `branch`: Filter by branch ID
  - `search`: Search across name, company, email, phone
  - `min_applications`: Filter brokers with at least a certain number of applications
- **Response**: Filtered list of brokers
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 1.3 Search Brokers
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User searches for brokers by name, company, email, or phone
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with search parameter
  2. System searches across name, company, email, phone fields
  3. System returns matching brokers
- **Query Parameters**:
  - `search`: Search term
- **Response**: List of matching brokers
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

### Use Cases for POST Method

#### 1.4 Create New Broker
- **Actor**: Authenticated user (Admin)
- **Description**: User creates a new broker
- **Preconditions**: User is authenticated with valid JWT token and has admin role
- **Steps**:
  1. User sends authenticated POST request with broker data
  2. System validates the data
  3. System creates new broker and associates it with the creator
  4. System returns the created broker details
- **Request Body**:
  ```json
  {
    "name": "John Smith",
    "company": "ABC Brokers",
    "email": "john.smith@abcbrokers.com",
    "phone": "0412345678",
    "address": "123 Broker St, Sydney NSW 2000",
    "branch_id": 1,
    "commission_bank_name": "Commonwealth Bank",
    "commission_account_name": "John Smith",
    "commission_account_number": "12345678",
    "commission_bsb": "062-000"
  }
  ```
- **Response**: Created broker details
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden

## 2. Broker Detail Operations API

### API Details
- **Endpoint**: `/api/brokers/{id}/`
- **HTTP Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 2.1 Retrieve Broker Details
- **Actor**: Authenticated user (Admin, BD, Broker)
- **Description**: User retrieves detailed information about a specific broker
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested broker
- **Steps**:
  1. User sends authenticated GET request with broker ID
  2. System validates user has access to the broker
  3. System returns detailed broker information
- **Response**: Detailed broker information including all fields
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PUT Method

#### 2.2 Update Broker (Full Update)
- **Actor**: Authenticated user (Admin)
- **Description**: User updates all information for a broker
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has admin role
- **Steps**:
  1. User sends authenticated PUT request with complete broker data
  2. System validates the data
  3. System updates the broker
  4. System returns the updated broker details
- **Request Body**: Complete broker data (all fields required)
- **Response**: Updated broker details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PATCH Method

#### 2.3 Update Broker (Partial Update)
- **Actor**: Authenticated user (Admin)
- **Description**: User updates specific information for a broker
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has admin role
- **Steps**:
  1. User sends authenticated PATCH request with partial broker data
  2. System validates the data
  3. System updates only the provided fields
  4. System returns the updated broker details
- **Request Body**: Partial broker data (only fields to update)
  ```json
  {
    "phone": "0487654321",
    "address": "456 New St, Melbourne VIC 3000"
  }
  ```
- **Response**: Updated broker details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for DELETE Method

#### 2.4 Delete Broker
- **Actor**: Authenticated user (Admin)
- **Description**: User deletes a broker
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has admin role
- **Steps**:
  1. User sends authenticated DELETE request with broker ID
  2. System validates user has permission to delete
  3. System deletes the broker
- **Response**: No content
- **Status Codes**:
  - 204: No Content (success)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 3. List or Create Branches API

### API Details
- **Endpoint**: `/api/brokers/branches/`
- **HTTP Methods**: `GET`, `POST`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 3.1 List All Branches
- **Actor**: Authenticated user
- **Description**: User retrieves a list of all branches
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System returns list of branches
- **Response**: List of branches with their details
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized

#### 3.2 Filter Branches
- **Actor**: Authenticated user
- **Description**: User filters branches by search term
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with search parameter
  2. System searches across name and address fields
  3. System returns matching branches
- **Query Parameters**:
  - `search`: Search term
- **Response**: Filtered list of branches
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized

### Use Cases for POST Method

#### 3.3 Create New Branch
- **Actor**: Authenticated user (Admin)
- **Description**: User creates a new branch
- **Preconditions**: User is authenticated with valid JWT token and has admin role
- **Steps**:
  1. User sends authenticated POST request with branch data
  2. System validates the data
  3. System creates new branch and associates it with the creator
  4. System returns the created branch details
- **Request Body**:
  ```json
  {
    "name": "Sydney CBD Branch",
    "address": "123 George St, Sydney NSW 2000",
    "phone": "0298765432",
    "email": "sydney@example.com"
  }
  ```
- **Response**: Created branch details
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden

## 4. Branch Detail Operations API

### API Details
- **Endpoint**: `/api/brokers/branches/{id}/`
- **HTTP Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 4.1 Retrieve Branch Details
- **Actor**: Authenticated user
- **Description**: User retrieves detailed information about a specific branch
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with branch ID
  2. System returns detailed branch information
- **Response**: Detailed branch information including all fields
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 404: Not Found

### Use Cases for PUT Method

#### 4.2 Update Branch (Full Update)
- **Actor**: Authenticated user (Admin)
- **Description**: User updates all information for a branch
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has admin role
- **Steps**:
  1. User sends authenticated PUT request with complete branch data
  2. System validates the data
  3. System updates the branch
  4. System returns the updated branch details
- **Request Body**: Complete branch data (all fields required)
- **Response**: Updated branch details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PATCH Method

#### 4.3 Update Branch (Partial Update)
- **Actor**: Authenticated user (Admin)
- **Description**: User updates specific information for a branch
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has admin role
- **Steps**:
  1. User sends authenticated PATCH request with partial branch data
  2. System validates the data
  3. System updates only the provided fields
  4. System returns the updated branch details
- **Request Body**: Partial branch data (only fields to update)
  ```json
  {
    "phone": "0287654321",
    "email": "sydney.cbd@example.com"
  }
  ```
- **Response**: Updated branch details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for DELETE Method

#### 4.4 Delete Branch
- **Actor**: Authenticated user (Admin)
- **Description**: User deletes a branch
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has admin role
- **Steps**:
  1. User sends authenticated DELETE request with branch ID
  2. System validates user has permission to delete
  3. System deletes the branch
- **Response**: No content
- **Status Codes**:
  - 204: No Content (success)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 5. List or Create BDMs API

### API Details
- **Endpoint**: `/api/brokers/bdms/`
- **HTTP Methods**: `GET`, `POST`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 5.1 List All BDMs
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User retrieves a list of BDMs
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System filters BDMs based on user role:
     - Admin: All BDMs
     - BD: Only their own BDM profile
  3. System returns list of BDMs
- **Response**: List of BDMs with their details
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

#### 5.2 Filter BDMs
- **Actor**: Authenticated user (Admin)
- **Description**: User filters BDMs by various criteria
- **Preconditions**: User is authenticated with valid JWT token and has admin role
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System applies filters and returns matching BDMs
- **Query Parameters**:
  - `branch`: Filter by branch ID
  - `search`: Search across name, email, phone
- **Response**: Filtered list of BDMs
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden

### Use Cases for POST Method

#### 5.3 Create New BDM
- **Actor**: Authenticated user (Admin)
- **Description**: User creates a new BDM
- **Preconditions**: User is authenticated with valid JWT token and has admin role
- **Steps**:
  1. User sends authenticated POST request with BDM data
  2. System validates the data
  3. System creates new BDM and associates it with the creator
  4. System returns the created BDM details
- **Request Body**:
  ```json
  {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "phone": "0412345678",
    "branch_id": 1,
    "user": 5
  }
  ```
- **Response**: Created BDM details
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden

## 6. BDM Detail Operations API

### API Details
- **Endpoint**: `/api/brokers/bdms/{id}/`
- **HTTP Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 6.1 Retrieve BDM Details
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User retrieves detailed information about a specific BDM
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested BDM
- **Steps**:
  1. User sends authenticated GET request with BDM ID
  2. System validates user has access to the BDM
  3. System returns detailed BDM information
- **Response**: Detailed BDM information including all fields
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PUT Method

#### 6.2 Update BDM (Full Update)
- **Actor**: Authenticated user (Admin)
- **Description**: User updates all information for a BDM
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has admin role
- **Steps**:
  1. User sends authenticated PUT request with complete BDM data
  2. System validates the data
  3. System updates the BDM
  4. System returns the updated BDM details
- **Request Body**: Complete BDM data (all fields required)
- **Response**: Updated BDM details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for PATCH Method

#### 6.3 Update BDM (Partial Update)
- **Actor**: Authenticated user (Admin)
- **Description**: User updates specific information for a BDM
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has admin role
- **Steps**:
  1. User sends authenticated PATCH request with partial BDM data
  2. System validates the data
  3. System updates only the provided fields
  4. System returns the updated BDM details
- **Request Body**: Partial BDM data (only fields to update)
  ```json
  {
    "phone": "0487654321",
    "branch_id": 2
  }
  ```
- **Response**: Updated BDM details
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

### Use Cases for DELETE Method

#### 6.4 Delete BDM
- **Actor**: Authenticated user (Admin)
- **Description**: User deletes a BDM
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has admin role
- **Steps**:
  1. User sends authenticated DELETE request with BDM ID
  2. System validates user has permission to delete
  3. System deletes the BDM
- **Response**: No content
- **Status Codes**:
  - 204: No Content (success)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 7. Get Brokers in Branch API

### API Details
- **Endpoint**: `/api/brokers/branches/{id}/brokers/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 7.1 List Brokers in Branch
- **Actor**: Authenticated user
- **Description**: User retrieves all brokers associated with a specific branch
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with branch ID
  2. System retrieves all brokers associated with the branch
  3. System returns the list of brokers
- **Response**: List of brokers with summary information
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 404: Not Found

## 8. Get BDMs in Branch API

### API Details
- **Endpoint**: `/api/brokers/branches/{id}/bdms/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 8.1 List BDMs in Branch
- **Actor**: Authenticated user
- **Description**: User retrieves all BDMs associated with a specific branch
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with branch ID
  2. System retrieves all BDMs associated with the branch
  3. System returns the list of BDMs
- **Response**: List of BDMs with their details
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 404: Not Found

## 9. Get Broker Applications API

### API Details
- **Endpoint**: `/api/brokers/{id}/applications/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 9.1 List Broker Applications
- **Actor**: Authenticated user (Admin, BD, Broker)
- **Description**: User retrieves all applications for a specific broker
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested broker
- **Steps**:
  1. User sends authenticated GET request with broker ID
  2. System validates user has access to the broker
  3. System retrieves all applications associated with the broker
  4. System returns the list of applications
- **Response**: List of applications with summary information
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 10. Get Broker Stats API

### API Details
- **Endpoint**: `/api/brokers/{id}/stats/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 10.1 Retrieve Broker Statistics
- **Actor**: Authenticated user (Admin, BD, Broker)
- **Description**: User retrieves statistics for a specific broker
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested broker
- **Steps**:
  1. User sends authenticated GET request with broker ID
  2. System validates user has access to the broker
  3. System calculates statistics including:
     - Total applications
     - Total loan amount
     - Applications by stage
     - Applications by type
  4. System returns the statistics
- **Response**: 
  ```json
  {
    "total_applications": 25,
    "total_loan_amount": 5750000.00,
    "applications_by_stage": {
      "inquiry": 5,
      "pre_approval": 8,
      "valuation": 3,
      "formal_approval": 4,
      "settlement": 2,
      "funded": 3
    },
    "applications_by_type": {
      "residential": 12,
      "commercial": 5,
      "refinance": 8
    }
  }
  ```
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found

## 11. Get BDM Applications API

### API Details
- **Endpoint**: `/api/brokers/bdms/{id}/applications/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 11.1 List BDM Applications
- **Actor**: Authenticated user (Admin, BD)
- **Description**: User retrieves all applications for a specific BDM
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has access to the requested BDM
- **Steps**:
  1. User sends authenticated GET request with BDM ID
  2. System validates user has access to the BDM
  3. System retrieves all applications associated with the BDM
  4. System returns the list of applications
- **Response**: List of applications with summary information
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found
