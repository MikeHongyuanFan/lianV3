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
        "notification_type": "application_status",
        "notification_type_display": "Application Status Change",
        "is_read": false,
        "created_at": "2023-04-30T14:30:00Z"
      },
      {
        "id": 122,
        "title": "Repayment Due Soon",
        "notification_type": "repayment_upcoming",
        "notification_type_display": "Repayment Upcoming",
        "is_read": true,
        "created_at": "2023-04-29T10:15:00Z"
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
        "notification_type": "application_status",
        "notification_type_display": "Application Status Change",
        "is_read": false,
        "created_at": "2023-04-30T14:30:00Z"
      },
      // ... more unread application status notifications
    ]
  }
  ```

#### 1.3 Search Notifications
- **Actor**: Authenticated user
- **Description**: User searches notifications by title
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
        "notification_type": "application_status",
        "notification_type_display": "Application Status Change",
        "is_read": false,
        "created_at": "2023-04-30T14:30:00Z"
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
- **Endpoint Options**:
  - **Option 1**: `/api/users/notifications/mark-read/` (with notification_id in body)
  - **Option 2**: `/api/users/notifications-viewset/{id}/mark_as_read/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes

### Use Cases

#### 2.1 Mark Single Notification as Read (Option 1)
- **Actor**: Authenticated user
- **Description**: User marks a specific notification as read using the mark-read endpoint
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Notification exists and belongs to the user
  - Notification is currently unread
- **Steps**:
  1. User sends authenticated POST request with notification ID in request body
  2. System validates authentication token
  3. System verifies notification belongs to user
  4. System marks notification as read
  5. System returns confirmation
- **Postconditions**: 
  - Notification is marked as read
  - User's unread notification count is decreased
- **Request Example**:
  ```
  POST /api/users/notifications/mark-read/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "notification_id": 123
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "status": "notification marked as read"
  }
  ```

#### 2.2 Mark Single Notification as Read (Option 2)
- **Actor**: Authenticated user
- **Description**: User marks a specific notification as read using the viewset endpoint
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - Notification exists and belongs to the user
  - Notification is currently unread
- **Steps**:
  1. User sends authenticated POST request with notification ID in URL path
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
  POST /api/users/notifications-viewset/123/mark_as_read/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "status": "notification marked as read"
  }
  ```
- **WebSocket Update**:
  ```json
  {
    "type": "unread_count",
    "count": 7
  }
  ```

#### 2.3 Mark Already Read Notification
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
- **Postconditions**: Notification remains marked as read
- **Request Example (Option 1)**:
  ```
  POST /api/users/notifications/mark-read/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "notification_id": 122
  }
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "status": "notification marked as read"
  }
  ```

#### 2.4 Failed Mark as Read (Notification Not Found)
- **Actor**: Authenticated user
- **Description**: User attempts to mark a non-existent notification as read
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated POST request with invalid notification ID
  2. System validates authentication token
  3. System attempts to find notification and fails
  4. System returns not found error
- **Postconditions**: No notification is marked as read
- **Request Example (Option 1)**:
  ```
  POST /api/users/notifications/mark-read/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "notification_id": 9999
  }
  ```
- **Response Example (404 Not Found)**:
  ```json
  {
    "error": "Notification not found"
  }
  ```

## 3. Mark All Notifications as Read API

### API Details
- **Endpoint Options**:
  - **Option 1**: `/api/users/notifications/mark-read/` (without notification_id)
  - **Option 2**: `/api/users/notifications-viewset/mark_all_as_read/`
- **HTTP Method**: `POST`
- **Authentication Required**: Yes

### Use Cases

#### 3.1 Mark All Notifications as Read (Option 1)
- **Actor**: Authenticated user
- **Description**: User marks all their unread notifications as read using the mark-read endpoint
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User has at least one unread notification
- **Steps**:
  1. User sends authenticated POST request without notification_id
  2. System validates authentication token
  3. System marks all user's unread notifications as read
  4. System returns confirmation
- **Postconditions**: 
  - All user's notifications are marked as read
  - User's unread notification count is zero
- **Request Example**:
  ```
  POST /api/users/notifications/mark-read/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "status": "all notifications marked as read"
  }
  ```

#### 3.2 Mark All Notifications as Read (Option 2)
- **Actor**: Authenticated user
- **Description**: User marks all their unread notifications as read using the viewset endpoint
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
  POST /api/users/notifications-viewset/mark_all_as_read/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "status": "all notifications marked as read"
  }
  ```
- **WebSocket Update**:
  ```json
  {
    "type": "unread_count",
    "count": 0
  }
  ```

#### 3.3 Mark All When No Unread Notifications
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
- **Postconditions**: All notifications remain marked as read
- **Request Example**:
  ```
  POST /api/users/notifications/mark-read/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response Example (200 OK)**:
  ```json
  {
    "status": "all notifications marked as read"
  }
  ```

## 4. Get Unread Notification Count API

### API Details
- **Endpoint Options**:
  - **Option 1**: `/api/users/notifications/count/`
  - **Option 2**: `/api/users/notifications-viewset/unread_count/`
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
- **Request Example (Option 1)**:
  ```
  GET /api/users/notifications/count/
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
  GET /api/users/notifications/count/
  ```
- **Response Example (401 Unauthorized)**:
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```

## 5. Notification Preferences API

### API Details
- **Endpoint**: `/api/users/notification-preferences/`
- **HTTP Methods**: `GET`, `PUT`
- **Authentication Required**: Yes

### Use Cases

#### 5.1 Get Notification Preferences
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
    "note_reminder_email": true,
    "document_uploaded_email": false,
    "signature_required_email": true,
    "system_email": false,
    "daily_digest": false,
    "weekly_digest": false
  }
  ```

#### 5.2 Update Notification Preferences
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

#### 5.3 Partial Update of Notification Preferences
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
    "note_reminder_email": true,
    "document_uploaded_email": false,
    "signature_required_email": true,
    "system_email": true,
    "daily_digest": true,
    "weekly_digest": false
  }
  ```

#### 5.4 Failed Preferences Update (Invalid Data)
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

## 6. WebSocket Notifications

### API Details
- **WebSocket Endpoint**: `/ws/notifications/`
- **Authentication Required**: Yes (via JWT token in query parameter)

### Use Cases

#### 6.1 Connect to WebSocket for Real-time Notifications
- **Actor**: Authenticated user
- **Description**: User connects to WebSocket to receive real-time notifications
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User establishes WebSocket connection with authentication token
  2. System validates authentication token
  3. System adds user to their notification group
  4. System sends initial unread count
- **Postconditions**: User is connected to WebSocket and ready to receive notifications
- **Connection Example**:
  ```
  ws://example.com/ws/notifications/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Initial Message (Received)**:
  ```json
  {
    "type": "unread_count",
    "count": 7
  }
  ```

#### 6.2 Receive Real-time Notification
- **Actor**: Authenticated user
- **Description**: User receives a new notification in real-time
- **Preconditions**: 
  - User is authenticated with valid JWT token
  - User is connected to WebSocket
  - A new notification is created for the user
- **Steps**:
  1. System creates a new notification for the user
  2. System sends notification data via WebSocket
  3. System updates unread count via WebSocket
- **Postconditions**: User receives notification data and updated count
- **Notification Message (Received)**:
  ```json
  {
    "type": "notification",
    "notification": {
      "id": 124,
      "title": "Document Uploaded",
      "message": "A new document has been uploaded for Application #A12345",
      "notification_type": "document_uploaded",
      "is_read": false,
      "created_at": "2023-05-01T09:15:00Z"
    }
  }
  ```
- **Count Update Message (Received)**:
  ```json
  {
    "type": "unread_count",
    "count": 8
  }
  ```