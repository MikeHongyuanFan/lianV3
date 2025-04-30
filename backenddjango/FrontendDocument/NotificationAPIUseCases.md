# Notification API Use Cases

This document outlines the use cases for the Notification APIs in the CRM Loan Management System.

## 1. List Notifications API

### API Details
- **Endpoint**: `/api/users/notifications/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases

#### 1.1 List User Notifications
- **Actor**: Authenticated user
- **Description**: User retrieves their notifications with pagination
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System retrieves paginated list of notifications for the user
  4. System returns notification list
- **Postconditions**: User receives their notifications
- **Request Example**:
  ```
  GET /api/users/notifications/?limit=10&offset=0
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "count": 25,
    "next": "http://example.com/api/users/notifications/?limit=10&offset=10",
    "previous": null,
    "results": [
      {
        "id": 123,
        "title": "Application Status Update",
        "message": "Application #A12345 has been moved to formal approval stage",
        "notification_type": "application_status",
        "notification_type_display": "Application Status",
        "is_read": false,
        "created_at": "2023-04-30T14:30:00Z",
        "related_object_id": 456,
        "related_object_type": "application",
        "related_object_info": {
          "reference_number": "A12345",
          "stage": "formal_approval"
        }
      },
      {
        "id": 122,
        "title": "Repayment Due Soon",
        "message": "Repayment of $1,500 is due in 3 days",
        "notification_type": "repayment_upcoming",
        "notification_type_display": "Upcoming Repayment",
        "is_read": true,
        "created_at": "2023-04-29T10:15:00Z",
        "related_object_id": 789,
        "related_object_type": "repayment",
        "related_object_info": {
          "amount": 1500,
          "due_date": "2023-05-03"
        }
      },
      // ... more notifications
    ]
  }
  ```

#### 1.2 Filter Notifications by Type and Read Status
- **Actor**: Authenticated user
- **Description**: User retrieves filtered notifications
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System validates authentication token
  3. System applies filters to retrieve matching notifications
  4. System returns filtered notification list
- **Postconditions**: User receives filtered notifications
- **Request Example**:
  ```
  GET /api/users/notifications/?notification_type=application_status&is_read=false&limit=10
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
        "title": "Application Status Update",
        "message": "Application #A12345 has been moved to formal approval stage",
        "notification_type": "application_status",
        "notification_type_display": "Application Status",
        "is_read": false,
        "created_at": "2023-04-30T14:30:00Z",
        "related_object_id": 456,
        "related_object_type": "application",
        "related_object_info": {
          "reference_number": "A12345",
          "stage": "formal_approval"
        }
      },
      // ... more unread application status notifications
    ]
  }
  ```

#### 1.3 Search Notifications
- **Actor**: Authenticated user
- **Description**: User searches notifications by title or message content
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with search parameter
  2. System validates authentication token
  3. System searches notifications for matching content
  4. System returns matching notifications
- **Postconditions**: User receives notifications matching search criteria
- **Request Example**:
  ```
  GET /api/users/notifications/?search=approval&limit=10
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
        "id": 123,
        "title": "Application Status Update",
        "message": "Application #A12345 has been moved to formal approval stage",
        "notification_type": "application_status",
        "notification_type_display": "Application Status",
        "is_read": false,
        "created_at": "2023-04-30T14:30:00Z",
        "related_object_id": 456,
        "related_object_type": "application",
        "related_object_info": {
          "reference_number": "A12345",
          "stage": "formal_approval"
        }
      },
      // ... more notifications containing "approval"
    ]
  }
  ```

#### 1.4 Failed Notification List Retrieval (Unauthenticated)
- **Actor**: Unauthenticated user
- **Description**: User attempts to retrieve notifications without authentication
- **Preconditions**: None
- **Steps**:
  1. User sends GET request without authentication token
  2. System checks for authentication and finds none
  3. System returns authentication error
- **Postconditions**: No notifications are returned
- **Request Example**:
  ```
  GET /api/users/notifications/
  ```
- **Response Example (401 Unauthorized)**:
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```

## 2. Mark Notification as Read API

### API Details
- **Endpoint**: `/api/users/notifications/{id}/mark_as_read/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes

### Use Cases

#### 2.1 Mark Single Notification as Read
- **Actor**: Authenticated user
- **Description**: User marks a specific notification as read
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Notification exists and belongs to the user
  - Notification is currently unread
- **Steps**:
  1. User sends authenticated POST request with notification ID
  2. System validates authentication token
  3. System verifies notification belongs to user
  4. System marks notification as read
  5. System returns confirmation
  6. System sends WebSocket update with new unread count
- **Postconditions**: 
  - Notification is marked as read
  - User's unread notification count is decreased
  - WebSocket notification is sent to update UI
- **Request Example**:
  ```
  POST /api/users/notifications/123/mark_as_read/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "status": "Notification marked as read"
  }
  ```
- **WebSocket Update**:
  ```json
  {
    "type": "unread_count_update",
    "unread_count": 7
  }
  ```

#### 2.2 Mark Already Read Notification
- **Actor**: Authenticated user
- **Description**: User attempts to mark an already read notification as read
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Notification exists and belongs to the user
  - Notification is already marked as read
- **Steps**:
  1. User sends authenticated POST request with notification ID
  2. System validates authentication token
  3. System verifies notification belongs to user
  4. System detects notification is already read
  5. System returns confirmation without changing state
  6. No WebSocket update is sent (count unchanged)
- **Postconditions**: Notification remains marked as read
- **Request Example**:
  ```
  POST /api/users/notifications/122/mark_as_read/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "status": "Notification was already read"
  }
  ```

#### 2.3 Failed Mark as Read (Notification Not Found)
- **Actor**: Authenticated user
- **Description**: User attempts to mark a non-existent notification as read
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated POST request with invalid notification ID
  2. System validates authentication token
  3. System attempts to find notification and fails
  4. System returns not found error
- **Postconditions**: No notification is marked as read
- **Request Example**:
  ```
  POST /api/users/notifications/9999/mark_as_read/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (404 Not Found)**:
  ```json
  {
    "detail": "Not found."
  }
  ```

## 3. Mark All Notifications as Read API

### API Details
- **Endpoint**: `/api/users/notifications/mark_all_as_read/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes

### Use Cases

#### 3.1 Mark All Notifications as Read
- **Actor**: Authenticated user
- **Description**: User marks all their unread notifications as read
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has at least one unread notification
- **Steps**:
  1. User sends authenticated POST request
  2. System validates authentication token
  3. System marks all user's unread notifications as read
  4. System returns confirmation
  5. System sends WebSocket update with zero unread count
- **Postconditions**: 
  - All user's notifications are marked as read
  - User's unread notification count is zero
  - WebSocket notification is sent to update UI
- **Request Example**:
  ```
  POST /api/users/notifications/mark_all_as_read/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "status": "All notifications marked as read"
  }
  ```
- **WebSocket Update**:
  ```json
  {
    "type": "unread_count_update",
    "unread_count": 0
  }
  ```

#### 3.2 Mark All When No Unread Notifications
- **Actor**: Authenticated user
- **Description**: User attempts to mark all notifications as read when none are unread
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has no unread notifications
- **Steps**:
  1. User sends authenticated POST request
  2. System validates authentication token
  3. System finds no unread notifications
  4. System returns confirmation
  5. No WebSocket update is sent (count already zero)
- **Postconditions**: All notifications remain marked as read
- **Request Example**:
  ```
  POST /api/users/notifications/mark_all_as_read/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "status": "No unread notifications found"
  }
  ```

## 4. Get Unread Notification Count API

### API Details
- **Endpoint**: `/api/users/notifications/unread_count/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases

#### 4.1 Get Unread Notification Count
- **Actor**: Authenticated user
- **Description**: User retrieves their unread notification count
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System counts user's unread notifications
  4. System returns count
- **Postconditions**: User receives unread notification count
- **Request Example**:
  ```
  GET /api/users/notifications/unread_count/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "unread_count": 7
  }
  ```

#### 4.2 Failed Unread Count Retrieval (Unauthenticated)
- **Actor**: Unauthenticated user
- **Description**: User attempts to retrieve unread count without authentication
- **Preconditions**: None
- **Steps**:
  1. User sends GET request without authentication token
  2. System checks for authentication and finds none
  3. System returns authentication error
- **Postconditions**: No count is returned
- **Request Example**:
  ```
  GET /api/users/notifications/unread_count/
  ```
- **Response Example (401 Unauthorized)**:
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```

## 5. Advanced Notification Search API

### API Details
- **Endpoint**: `/api/users/notifications/advanced_search/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases

#### 5.1 Advanced Search with Multiple Filters
- **Actor**: Authenticated user
- **Description**: User performs advanced search with multiple filters
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with multiple filter parameters
  2. System validates authentication token
  3. System applies all filters to retrieve matching notifications
  4. System returns filtered notification list
- **Postconditions**: User receives notifications matching all criteria
- **Request Example**:
  ```
  GET /api/users/notifications/advanced_search/?notification_type=repayment_upcoming&is_read=false&date_from=2023-04-01&date_to=2023-04-30&limit=10
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
        "id": 120,
        "title": "Repayment Due Soon",
        "message": "Repayment of $2,000 is due in 5 days",
        "notification_type": "repayment_upcoming",
        "notification_type_display": "Upcoming Repayment",
        "is_read": false,
        "created_at": "2023-04-25T09:30:00Z",
        "related_object_id": 790,
        "related_object_type": "repayment",
        "related_object_info": {
          "amount": 2000,
          "due_date": "2023-04-30"
        }
      },
      // ... more notifications matching all criteria
    ]
  }
  ```

#### 5.2 Advanced Search by Date Range
- **Actor**: Authenticated user
- **Description**: User searches notifications within a specific date range
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with date range parameters
  2. System validates authentication token
  3. System retrieves notifications within date range
  4. System returns matching notifications
- **Postconditions**: User receives notifications within specified date range
- **Request Example**:
  ```
  GET /api/users/notifications/advanced_search/?date_from=2023-04-01&date_to=2023-04-15&limit=10
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "count": 12,
    "next": "http://example.com/api/users/notifications/advanced_search/?date_from=2023-04-01&date_to=2023-04-15&limit=10&offset=10",
    "previous": null,
    "results": [
      {
        "id": 115,
        "title": "Document Uploaded",
        "message": "A new document has been uploaded for Application #A12340",
        "notification_type": "document_uploaded",
        "notification_type_display": "Document Uploaded",
        "is_read": true,
        "created_at": "2023-04-12T11:45:00Z",
        "related_object_id": 567,
        "related_object_type": "document",
        "related_object_info": {
          "title": "Income Statement",
          "application_reference": "A12340"
        }
      },
      // ... more notifications within date range
    ]
  }
  ```

#### 5.3 Advanced Search with No Results
- **Actor**: Authenticated user
- **Description**: User performs advanced search that yields no results
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System validates authentication token
  3. System applies filters and finds no matching notifications
  4. System returns empty result set
- **Postconditions**: User receives empty notification list
- **Request Example**:
  ```
  GET /api/users/notifications/advanced_search/?notification_type=signature_required&date_from=2023-04-01&date_to=2023-04-05
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
  }
  ```

## 6. Notification Preferences API

### API Details
- **Endpoint**: `/api/users/notification-preferences/`
- **HTTP Methods**: `GET`, `PUT`
- **Authentication Required**: Yes

### Use Cases

#### 6.1 Get Notification Preferences
- **Actor**: Authenticated user
- **Description**: User retrieves their notification preferences
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System retrieves user's notification preferences
  4. System returns preferences
- **Postconditions**: User receives their notification preferences
- **Request Example**:
  ```
  GET /api/users/notification-preferences/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "application_status_in_app": true,
    "repayment_upcoming_in_app": true,
    "repayment_overdue_in_app": true,
    "note_reminder_in_app": true,
    "document_uploaded_in_app": true,
    "signature_required_in_app": true,
    "system_in_app": true,
    "application_status_email": true,
    "repayment_upcoming_email": true,
    "repayment_overdue_email": true,
    "note_reminder_email": false,
    "document_uploaded_email": false,
    "signature_required_email": true,
    "system_email": false,
    "daily_digest": false,
    "weekly_digest": true
  }
  ```

#### 6.2 Update Notification Preferences
- **Actor**: Authenticated user
- **Description**: User updates their notification preferences
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated PUT request with updated preferences
  2. System validates authentication token
  3. System validates input data
  4. System updates user's notification preferences
  5. System returns updated preferences
- **Postconditions**: User's notification preferences are updated
- **Request Example**:
  ```
  PUT /api/users/notification-preferences/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "application_status_in_app": true,
    "repayment_upcoming_in_app": true,
    "repayment_overdue_in_app": true,
    "note_reminder_in_app": false,
    "document_uploaded_in_app": false,
    "signature_required_in_app": true,
    "system_in_app": false,
    "application_status_email": true,
    "repayment_upcoming_email": true,
    "repayment_overdue_email": true,
    "note_reminder_email": false,
    "document_uploaded_email": false,
    "signature_required_email": true,
    "system_email": false,
    "daily_digest": true,
    "weekly_digest": false
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "application_status_in_app": true,
    "repayment_upcoming_in_app": true,
    "repayment_overdue_in_app": true,
    "note_reminder_in_app": false,
    "document_uploaded_in_app": false,
    "signature_required_in_app": true,
    "system_in_app": false,
    "application_status_email": true,
    "repayment_upcoming_email": true,
    "repayment_overdue_email": true,
    "note_reminder_email": false,
    "document_uploaded_email": false,
    "signature_required_email": true,
    "system_email": false,
    "daily_digest": true,
    "weekly_digest": false
  }
  ```

#### 6.3 Partial Update of Notification Preferences
- **Actor**: Authenticated user
- **Description**: User updates only specific notification preferences
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated PUT request with specific preferences
  2. System validates authentication token
  3. System validates input data
  4. System updates only the provided preferences
  5. System returns complete updated preferences
- **Postconditions**: Specified notification preferences are updated
- **Request Example**:
  ```
  PUT /api/users/notification-preferences/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "daily_digest": true,
    "weekly_digest": false,
    "system_email": true
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "application_status_in_app": true,
    "repayment_upcoming_in_app": true,
    "repayment_overdue_in_app": true,
    "note_reminder_in_app": true,
    "document_uploaded_in_app": true,
    "signature_required_in_app": true,
    "system_in_app": true,
    "application_status_email": true,
    "repayment_upcoming_email": true,
    "repayment_overdue_email": true,
    "note_reminder_email": false,
    "document_uploaded_email": false,
    "signature_required_email": true,
    "system_email": true,
    "daily_digest": true,
    "weekly_digest": false
  }
  ```

#### 6.4 Failed Preferences Update (Invalid Data)
- **Actor**: Authenticated user
- **Description**: User attempts to update preferences with invalid data
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated PUT request with invalid data
  2. System validates authentication token
  3. System validates input data and finds errors
  4. System returns validation error
- **Postconditions**: User's notification preferences remain unchanged
- **Request Example**:
  ```
  PUT /api/users/notification-preferences/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "daily_digest": "yes",
    "weekly_digest": "no"
  }
  ```
- **Response Example (400 Bad Request)**:
  ```json
  {
    "daily_digest": ["Must be a boolean value."],
    "weekly_digest": ["Must be a boolean value."]
  }
  ```
