# API Documentation - CRM Loan Management System

This document records all API endpoints found in the CRM Loan Management System backend.

## Table of Contents
- [Authentication APIs](#authentication-apis)
- [User APIs](#user-apis)
- [Notification APIs](#notification-apis)
- [Application APIs](#application-apis)
- [Borrower APIs](#borrower-apis)
- [Guarantor APIs](#guarantor-apis)
- [Broker APIs](#broker-apis)
- [Document APIs](#document-apis)
- [Report APIs](#report-apis)
- [Error Handling and Validation](#error-handling-and-validation)

## Authentication APIs

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/api/users/auth/login/` | `POST` | User login |
| `/api/users/auth/register/` | `POST` | User registration |
| `/api/users/auth/refresh/` | `POST` | Refresh authentication token |

### Login
- **API URL**: `/api/users/auth/login/`
- **HTTP Method**: `POST`
- **Required Input Fields**: 
  - `email` (string): User's email address
  - `password` (string): User's password
- **Response Fields**: 
  - `access` (string): JWT access token
  - `refresh` (string): JWT refresh token
  - `user_id` (integer): User's ID
  - `email` (string): User's email address
  - `role` (string): User's role (admin, broker, bd, client)
  - `name` (string): User's full name
- **Status Codes**: `200`, `400`, `401`, `500`
- **Authentication Required?**: No
- **Pagination?**: No
- **Search/Filter Support?**: No

### Register
- **API URL**: `/api/users/auth/register/`
- **HTTP Method**: `POST`
- **Required Input Fields**: 
  - `email` (string): User's email address
  - `password` (string): User's password
  - `password2` (string): Password confirmation
  - `first_name` (string): User's first name
  - `last_name` (string): User's last name
  - `role` (string): User's role (admin, broker, bd, client)
- **Response Fields**: 
  - `refresh` (string): JWT refresh token
  - `access` (string): JWT access token
  - `user_id` (integer): User's ID
  - `email` (string): User's email address
  - `role` (string): User's role
  - `name` (string): User's full name
- **Status Codes**: `201`, `400`, `500`
- **Authentication Required?**: No
- **Pagination?**: No
- **Search/Filter Support?**: No

### Token Refresh
- **API URL**: `/api/users/auth/refresh/`
- **HTTP Method**: `POST`
- **Required Input Fields**: 
  - `refresh` (string): JWT refresh token
- **Response Fields**: 
  - `access` (string): New JWT access token
- **Status Codes**: `200`, `401`
- **Authentication Required?**: No
- **Pagination?**: No
- **Search/Filter Support?**: No

## User APIs

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/api/users/profile/` | `GET` | Get user profile |
| `/api/users/profile/update/` | `PUT`, `PATCH` | Update user profile |
| `/api/users/users/` | `GET` | List all users |
| `/api/users/users/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | User detail operations |
| `/api/users/users/me/` | `GET` | Get current user information |

### User Profile
- **API URL**: `/api/users/profile/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: 
  - `id` (integer): User's ID
  - `email` (string): User's email address
  - `first_name` (string): User's first name
  - `last_name` (string): User's last name
  - `role` (string): User's role (admin, broker, bd, client)
  - `phone` (string): User's phone number
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Update User Profile
- **API URL**: `/api/users/profile/update/`
- **HTTP Method**: `PUT`, `PATCH`
- **Required Input Fields**: Any of the following:
  - `first_name` (string): User's first name
  - `last_name` (string): User's last name
  - `email` (string): User's email address
  - `phone` (string): User's phone number
- **Response Fields**: 
  - `id` (integer): User's ID
  - `email` (string): User's email address
  - `first_name` (string): User's first name
  - `last_name` (string): User's last name
  - `role` (string): User's role
  - `phone` (string): User's phone number
- **Status Codes**: `200`, `400`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### User List
- **API URL**: `/api/users/users/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of users with the following fields:
  - `id` (integer): User's ID
  - `email` (string): User's email address
  - `first_name` (string): User's first name
  - `last_name` (string): User's last name
  - `role` (string): User's role
  - `phone` (string): User's phone number
- **Status Codes**: `200`, `401`, `403`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by username, email, first name, or last name
  - `role`: Filter by role (admin, broker, bd, client)

### User Detail
- **API URL**: `/api/users/users/{id}/`
- **HTTP Method**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Required Input Fields**: None for GET, any of the following for PUT/PATCH:
  - `first_name` (string): User's first name
  - `last_name` (string): User's last name
  - `email` (string): User's email address
  - `phone` (string): User's phone number
  - `role` (string): User's role (admin, broker, bd, client)
- **Response Fields**: 
  - `id` (integer): User's ID
  - `email` (string): User's email address
  - `first_name` (string): User's first name
  - `last_name` (string): User's last name
  - `role` (string): User's role
  - `phone` (string): User's phone number
- **Status Codes**: `200`, `401`, `403`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

## Notification APIs

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/api/users/notifications/` | `GET` | List notifications |
| `/api/users/notifications/{id}/mark_as_read/` | `POST` | Mark notification as read |
| `/api/users/notifications/mark_all_as_read/` | `POST` | Mark all notifications as read |
| `/api/users/notifications/unread_count/` | `GET` | Get unread notification count |
| `/api/users/notifications/advanced_search/` | `GET` | Advanced notification search |
| `/api/users/notification-preferences/` | `GET`, `PUT` | Manage notification preferences |

### Notification List
- **API URL**: `/api/users/notifications/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of notifications with the following fields:
  - `id` (integer): Notification ID
  - `title` (string): Notification title
  - `message` (string): Notification message
  - `notification_type` (string): Type of notification (application_status, repayment_upcoming, etc.)
  - `notification_type_display` (string): Human-readable notification type
  - `is_read` (boolean): Whether the notification has been read
  - `created_at` (datetime): When the notification was created
  - `related_object_id` (integer): ID of the related object (e.g., application ID)
  - `related_object_type` (string): Type of the related object (e.g., application)
  - `related_object_info` (object): Additional information about the related object
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by title or message
  - `notification_type`: Filter by notification type
  - `is_read`: Filter by read status (true/false)

### Mark Notification as Read
- **API URL**: `/api/users/notifications/{id}/mark_as_read/`
- **HTTP Method**: `POST`
- **Required Input Fields**: None
- **Response Fields**: 
  - `status` (string): Confirmation message
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No
- **WebSocket Updates**: Yes, sends unread notification count update to the user's notification channel

### Mark All Notifications as Read
- **API URL**: `/api/users/notifications/mark_all_as_read/`
- **HTTP Method**: `POST`
- **Required Input Fields**: None
- **Response Fields**: 
  - `status` (string): Confirmation message
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No
- **WebSocket Updates**: Yes, sends unread notification count update (zero) to the user's notification channel

### Get Unread Notification Count
- **API URL**: `/api/users/notifications/unread_count/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: 
  - `unread_count` (integer): Number of unread notifications
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Advanced Notification Search
- **API URL**: `/api/users/notifications/advanced_search/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of notifications with the same fields as Notification List
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by title or message
  - `notification_type`: Filter by notification type
  - `is_read`: Filter by read status (true/false)
  - `date_from`: Filter by date (YYYY-MM-DD format)
  - `date_to`: Filter by date (YYYY-MM-DD format)

### Notification Preferences
- **API URL**: `/api/users/notification-preferences/`
- **HTTP Method**: `GET`, `PUT`
- **Required Input Fields** (for PUT): Any of the following boolean fields:
  - `application_status_in_app` (boolean): Receive in-app notifications for application status changes
  - `repayment_upcoming_in_app` (boolean): Receive in-app notifications for upcoming repayments
  - `repayment_overdue_in_app` (boolean): Receive in-app notifications for overdue repayments
  - `note_reminder_in_app` (boolean): Receive in-app notifications for note reminders
  - `document_uploaded_in_app` (boolean): Receive in-app notifications when documents are uploaded
  - `signature_required_in_app` (boolean): Receive in-app notifications when signatures are required
  - `system_in_app` (boolean): Receive in-app notifications for system messages
  - `application_status_email` (boolean): Receive email notifications for application status changes
  - `repayment_upcoming_email` (boolean): Receive email notifications for upcoming repayments
  - `repayment_overdue_email` (boolean): Receive email notifications for overdue repayments
  - `note_reminder_email` (boolean): Receive email notifications for note reminders
  - `document_uploaded_email` (boolean): Receive email notifications when documents are uploaded
  - `signature_required_email` (boolean): Receive email notifications when signatures are required
  - `system_email` (boolean): Receive email notifications for system messages
  - `daily_digest` (boolean): Receive daily digest emails
  - `weekly_digest` (boolean): Receive weekly digest emails
- **Response Fields**: All notification preference fields excluding `user`, `created_at`, `updated_at`
- **Status Codes**: `200`, `400`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No
## Application APIs

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/api/applications/` | `GET`, `POST` | List or create applications |
| `/api/applications/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | Application detail operations |
| `/api/applications/create-with-cascade/` | `POST` | Create application with related entities |
| `/api/applications/validate-schema/` | `POST` | Validate application schema |
| `/api/applications/{id}/stage/` | `PUT` | Update application stage |
| `/api/applications/{id}/borrowers/` | `PUT` | Update application borrowers |
| `/api/applications/{id}/signature/` | `POST` | Sign application |
| `/api/applications/{id}/guarantors/` | `GET` | Get application guarantors |
| `/api/applications/{id}/notes/` | `GET` | Get application notes |
| `/api/applications/{id}/add-note/` | `POST` | Add application note |
| `/api/applications/{id}/documents/` | `GET` | Get application documents |
| `/api/applications/{id}/upload-document/` | `POST` | Upload application document |
| `/api/applications/{id}/fees/` | `GET` | Get application fees |
| `/api/applications/{id}/add-fee/` | `POST` | Add application fee |
| `/api/applications/{id}/repayments/` | `GET` | Get application repayments |
| `/api/applications/{id}/add-repayment/` | `POST` | Add application repayment |
| `/api/applications/{id}/record-payment/` | `POST` | Record payment for application |
| `/api/applications/{id}/ledger/` | `GET` | Get application ledger |

### Application List
- **API URL**: `/api/applications/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of applications with the following fields:
  - `id` (integer): Application ID
  - `reference_number` (string): Unique reference number
  - `application_type` (string): Type of application (residential, commercial, etc.)
  - `purpose` (string): Purpose of the loan
  - `loan_amount` (decimal): Amount of the loan
  - `stage` (string): Current stage of the application
  - `stage_display` (string): Human-readable stage
  - `created_at` (datetime): When the application was created
  - `broker_name` (string): Name of the broker
  - `borrower_count` (integer): Number of borrowers
  - `estimated_settlement_date` (date): Estimated settlement date
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by reference number or purpose
  - `status`: Filter by status
  - `stage`: Filter by stage
  - `borrower`: Filter by borrower ID
  - `date_from`: Filter by date (YYYY-MM-DD format)
  - `date_to`: Filter by date (YYYY-MM-DD format)

### Application Detail
- **API URL**: `/api/applications/{id}/`
- **HTTP Method**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Required Input Fields**: None for GET, various fields for PUT/PATCH including:
  - `loan_amount` (decimal): Amount of the loan
  - `loan_term` (integer): Term of the loan in months
  - `interest_rate` (decimal): Interest rate
  - `purpose` (string): Purpose of the loan
  - `repayment_frequency` (string): Frequency of repayments (weekly, fortnightly, monthly)
  - `application_type` (string): Type of application
  - `product_id` (string): Product ID
  - `estimated_settlement_date` (date): Estimated settlement date
  - `stage` (string): Current stage of the application
  - `broker` (integer): Broker ID
  - `bd` (integer): BDM ID
  - `branch` (integer): Branch ID
  - `security_address` (string): Address of the security property
  - `security_type` (string): Type of security
  - `security_value` (decimal): Value of the security
- **Response Fields**: Comprehensive application details including:
  - Basic application fields (id, reference_number, loan_amount, etc.)
  - Related entities (borrowers, guarantors, broker, bd, branch)
  - Documents and notes
  - Financial tracking (fees, repayments, ledger entries)
  - Security property details
  - Valuer information
  - QS information
  - Signature and PDF information
  - Metadata
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Create Application
- **API URL**: `/api/applications/`
- **HTTP Method**: `POST`
- **Description**: Creates a new loan application with basic information. For creating an application with related entities in a single request, use the `/api/applications/create-with-cascade/` endpoint.
- **Required Input Fields**:
  - `loan_amount` (decimal): Amount of the loan
  - `loan_term` (integer): Term of the loan in months
  - `interest_rate` (decimal): Interest rate
  - `purpose` (string): Purpose of the loan
  - `repayment_frequency` (string): Frequency of repayments (weekly, fortnightly, monthly)
  - `application_type` (string): Type of application (residential, commercial, etc.)
  - `product_id` (string): Product ID
  - `estimated_settlement_date` (date): Estimated settlement date
  - `stage` (string): Current stage of the application
  - `broker` (integer): Broker ID
  - `bd` (integer): BDM ID
  - `branch` (integer): Branch ID
  - `security_address` (string): Address of the security property
  - `security_type` (string): Type of security
  - `security_value` (decimal): Value of the security
- **Response Fields**: Application details as in Application Detail
- **Status Codes**: `201`, `400`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Create Application with Cascade
- **API URL**: `/api/applications/create-with-cascade/`
- **HTTP Method**: `POST`
- **Description**: This endpoint uses the same view as the regular create endpoint (`ApplicationViewSet.create`), but is specifically designed for creating an application along with related entities (borrowers, guarantors, company borrowers) in a single request. It handles the creation of all related entities in a database transaction to ensure data consistency.
- **Required Input Fields**:
  - `loan_amount` (decimal): Amount of the loan
  - `loan_term` (integer): Term of the loan in months
  - `interest_rate` (decimal): Interest rate
  - `purpose` (string): Purpose of the loan
  - `repayment_frequency` (string): Frequency of repayments
  - `application_type` (string): Type of application
  - `product_id` (string): Product ID
  - `estimated_settlement_date` (date): Estimated settlement date
  - `stage` (string): Current stage of the application
  - `broker` (integer): Broker ID
  - `bd` (integer): BDM ID
  - `branch` (integer): Branch ID
  - `security_address` (string): Address of the security property
  - `security_type` (string): Type of security
  - `security_value` (decimal): Value of the security
  - `borrowers` (array): Array of borrower objects
  - `guarantors` (array): Array of guarantor objects
  - `company_borrowers` (array): Array of company borrower objects
- **Response Fields**: Application details as in Application Detail
- **Status Codes**: `201`, `400`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Validate Application Schema
- **API URL**: `/api/applications/validate-schema/`
- **HTTP Method**: `POST`
- **Required Input Fields**:
  - `application_type` (string): Type of application (residential, commercial, etc.)
  - `purpose` (string): Purpose of the loan
  - `loan_amount` (decimal): Amount of the loan
  - `loan_term` (integer): Term of the loan in months
  - `repayment_frequency` (string): Frequency of repayments
- **Response Fields**:
  - `valid` (boolean): Whether the schema is valid
  - `error` (string, optional): Error message if not valid
- **Status Codes**: `200`, `400`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Update Application Stage
- **API URL**: `/api/applications/{id}/stage/`
- **HTTP Method**: `PUT`
- **Required Input Fields**:
  - `stage` (string): New stage for the application (inquiry, pre_approval, valuation, formal_approval, settlement, funded, declined, withdrawn)
- **Response Fields**:
  - `id` (integer): Application ID
  - `reference_number` (string): Application reference number
  - `stage` (string): Updated stage
  - `status` (string): Status message
- **Status Codes**: `200`, `400`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Update Application Borrowers
- **API URL**: `/api/applications/{id}/borrowers/`
- **HTTP Method**: `PUT`
- **Required Input Fields**:
  - `borrowers` (array): Array of borrower IDs
- **Response Fields**:
  - `id` (integer): Application ID
  - `reference_number` (string): Application reference number
  - `borrowers` (array): Updated list of borrowers
- **Status Codes**: `200`, `400`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Application Signature
- **API URL**: `/api/applications/{id}/signature/`
- **HTTP Method**: `POST`
- **Required Input Fields**:
  - `signature` (string): Base64-encoded signature data
  - `name` (string): Name of the person signing
  - `signature_date` (date, optional): Date of signature (defaults to current date)
- **Response Fields**: Application details as in Application Detail
- **Status Codes**: `200`, `400`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Application Guarantors
- **API URL**: `/api/applications/{id}/guarantors/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of guarantors with the following fields:
  - `id` (integer): Guarantor ID
  - `first_name` (string): First name
  - `last_name` (string): Last name
  - `email` (string): Email address
  - `phone_number` (string): Phone number
  - Additional guarantor fields
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Application Notes
- **API URL**: `/api/applications/{id}/notes/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of notes with the following fields:
  - `id` (integer): Note ID
  - `content` (string): Note content
  - `created_by` (object): User who created the note
  - `created_at` (datetime): When the note was created
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by content
  - `date_from`: Filter by date (YYYY-MM-DD format)
  - `date_to`: Filter by date (YYYY-MM-DD format)

### Add Application Note
- **API URL**: `/api/applications/{id}/add-note/`
- **HTTP Method**: `POST`
- **Required Input Fields**:
  - `content` (string): Note content
- **Response Fields**:
  - `id` (integer): Note ID
  - `content` (string): Note content
  - `created_by` (object): User who created the note
  - `created_at` (datetime): When the note was created
- **Status Codes**: `201`, `400`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Application Documents
- **API URL**: `/api/applications/{id}/documents/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of documents with the following fields:
  - `id` (integer): Document ID
  - `title` (string): Document title
  - `file` (string): File path
  - `document_type` (string): Type of document
  - `uploaded_at` (datetime): When the document was uploaded
  - `uploaded_by` (object): User who uploaded the document
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `document_type`: Filter by document type

### Upload Application Document
- **API URL**: `/api/applications/{id}/upload-document/`
- **HTTP Method**: `POST`
- **Required Input Fields**:
  - `title` (string): Document title
  - `file` (file): Document file
  - `document_type` (string): Type of document
- **Response Fields**:
  - `id` (integer): Document ID
  - `title` (string): Document title
  - `file` (string): File path
  - `document_type` (string): Type of document
  - `uploaded_at` (datetime): When the document was uploaded
  - `uploaded_by` (object): User who uploaded the document
- **Status Codes**: `201`, `400`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Application Fees
- **API URL**: `/api/applications/{id}/fees/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of fees with the following fields:
  - `id` (integer): Fee ID
  - `fee_type` (string): Type of fee
  - `amount` (decimal): Fee amount
  - `is_paid` (boolean): Whether the fee has been paid
  - `due_date` (date): When the fee is due
  - `paid_date` (date, nullable): When the fee was paid
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `is_paid`: Filter by payment status (true/false)
  - `fee_type`: Filter by fee type

### Add Application Fee
- **API URL**: `/api/applications/{id}/add-fee/`
- **HTTP Method**: `POST`
- **Required Input Fields**:
  - `fee_type` (string): Type of fee (application, valuation, legal, broker, settlement, other)
  - `amount` (decimal): Fee amount
  - `due_date` (date): When the fee is due
- **Response Fields**:
  - `id` (integer): Fee ID
  - `fee_type` (string): Type of fee
  - `amount` (decimal): Fee amount
  - `is_paid` (boolean): Whether the fee has been paid
  - `due_date` (date): When the fee is due
  - `paid_date` (date, nullable): When the fee was paid
- **Status Codes**: `201`, `400`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Application Repayments
- **API URL**: `/api/applications/{id}/repayments/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of repayments with the following fields:
  - `id` (integer): Repayment ID
  - `amount` (decimal): Repayment amount
  - `due_date` (date): When the repayment is due
  - `is_paid` (boolean): Whether the repayment has been paid
  - `paid_date` (date, nullable): When the repayment was paid
  - `payment_method` (string, nullable): Method of payment
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `is_paid`: Filter by payment status (true/false)
  - `date_from`: Filter by date (YYYY-MM-DD format)
  - `date_to`: Filter by date (YYYY-MM-DD format)

### Add Application Repayment
- **API URL**: `/api/applications/{id}/add-repayment/`
- **HTTP Method**: `POST`
- **Required Input Fields**:
  - `amount` (decimal): Repayment amount
  - `due_date` (date): When the repayment is due
- **Response Fields**:
  - `id` (integer): Repayment ID
  - `amount` (decimal): Repayment amount
  - `due_date` (date): When the repayment is due
  - `is_paid` (boolean): Whether the repayment has been paid
  - `paid_date` (date, nullable): When the repayment was paid
  - `payment_method` (string, nullable): Method of payment
- **Status Codes**: `201`, `400`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Record Payment
- **API URL**: `/api/applications/{id}/record-payment/`
- **HTTP Method**: `POST`
- **Required Input Fields**:
  - `repayment_id` (integer): ID of the repayment
  - `payment_amount` (decimal): Amount of the payment
  - `payment_date` (date): Date of payment
  - `payment_method` (string): Method of payment
- **Response Fields**:
  - `id` (integer): Repayment ID
  - `amount` (decimal): Repayment amount
  - `due_date` (date): When the repayment is due
  - `is_paid` (boolean): Whether the repayment has been paid
  - `paid_date` (date): When the repayment was paid
  - `payment_method` (string): Method of payment
- **Status Codes**: `200`, `400`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Application Ledger
- **API URL**: `/api/applications/{id}/ledger/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of ledger entries with the following fields:
  - `id` (integer): Ledger entry ID
  - `entry_type` (string): Type of entry (fee_added, fee_paid, repayment_added, repayment_received, etc.)
  - `amount` (decimal): Amount of the entry
  - `date` (datetime): Date of the entry
  - `description` (string): Description of the entry
  - `balance` (decimal): Running balance after this entry
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `entry_type`: Filter by entry type
  - `date_from`: Filter by date (YYYY-MM-DD format)
  - `date_to`: Filter by date (YYYY-MM-DD format)
## Borrower APIs

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/api/borrowers/` | `GET`, `POST` | List or create borrowers |
| `/api/borrowers/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | Borrower detail operations |
| `/api/borrowers/company/` | `GET` | List company borrowers |
| `/api/borrowers/{id}/financial-summary/` | `GET` | Get borrower financial summary |
| `/api/borrowers/{id}/applications/` | `GET` | Get borrower applications |
| `/api/borrowers/{id}/guarantors/` | `GET` | Get borrower guarantors |

### Borrower List
- **API URL**: `/api/borrowers/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of borrowers with the following fields:
  - `id` (integer): Borrower ID
  - `first_name` (string): First name
  - `last_name` (string): Last name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `is_company` (boolean): Whether the borrower is a company
  - `company_name` (string): Company name (if is_company is true)
  - `created_at` (datetime): When the borrower was created
  - `application_count` (integer): Number of applications associated with this borrower
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by first name, last name, or email
  - `is_company`: Filter by company status

### Borrower Detail
- **API URL**: `/api/borrowers/{id}/`
- **HTTP Method**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Required Input Fields**: None for GET, any of the following for PUT/PATCH:
  - `first_name` (string): First name
  - `last_name` (string): Last name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `residential_address` (string): Residential address
  - `mailing_address` (string): Mailing address
  - `is_company` (boolean): Whether the borrower is a company
  - `company_name` (string): Company name (if is_company is true)
  - `date_of_birth` (date): Date of birth
  - `employment_type` (string): Employment type (full_time, part_time, casual, self_employed, contractor, unemployed, retired)
  - `annual_income` (decimal): Annual income
- **Response Fields**:
  - `id` (integer): Borrower ID
  - `first_name` (string): First name
  - `last_name` (string): Last name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `residential_address` (string): Residential address
  - `mailing_address` (string): Mailing address
  - `is_company` (boolean): Whether the borrower is a company
  - `company_name` (string): Company name (if is_company is true)
  - `created_at` (datetime): When the borrower was created
  - `updated_at` (datetime): When the borrower was last updated
  - `date_of_birth` (date): Date of birth
  - `employment_type` (string): Employment type
  - `annual_income` (decimal): Annual income
  - Additional borrower fields
- **Status Codes**: `200`, `400`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Create Borrower
- **API URL**: `/api/borrowers/`
- **HTTP Method**: `POST`
- **Required Input Fields**:
  - `first_name` (string): First name
  - `last_name` (string): Last name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `is_company` (boolean, optional): Whether the borrower is a company (defaults to false)
  - `company_name` (string, optional): Company name (required if is_company is true)
- **Response Fields**:
  - `id` (integer): Borrower ID
  - `first_name` (string): First name
  - `last_name` (string): Last name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `is_company` (boolean): Whether the borrower is a company
  - `company_name` (string): Company name (if is_company is true)
  - `created_at` (datetime): When the borrower was created
- **Status Codes**: `201`, `400`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Company Borrower List
- **API URL**: `/api/borrowers/company/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of company borrowers with the following fields:
  - `id` (integer): Company borrower ID
  - `company_name` (string): Company name
  - `first_name` (string): First name (may be null)
  - `last_name` (string): Last name (may be null)
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `created_at` (datetime): When the company borrower was created
  - `application_count` (integer): Number of applications associated with this borrower
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by company name, first name, or last name

### Borrower Financial Summary
- **API URL**: `/api/borrowers/{id}/financial-summary/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**:
  - `borrower_id` (integer): Borrower ID
  - `total_loans` (integer): Total number of loans
  - `active_loans` (integer): Number of active loans
  - `total_loan_amount` (decimal): Total amount of all loans
  - `outstanding_amount` (decimal): Outstanding amount
  - `repayment_history` (object): Repayment history information
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Borrower Applications
- **API URL**: `/api/borrowers/{id}/applications/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of applications with basic details including:
  - `id` (integer): Application ID
  - `reference_number` (string): Application reference number
  - `application_type` (string): Type of application
  - `purpose` (string): Purpose of the loan
  - `loan_amount` (decimal): Amount of the loan
  - `stage` (string): Current stage of the application
  - `stage_display` (string): Human-readable stage
  - `created_at` (datetime): When the application was created
  - Other basic application fields
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Borrower Guarantors
- **API URL**: `/api/borrowers/{id}/guarantors/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of guarantors with basic details including:
  - `id` (integer): Guarantor ID
  - `first_name` (string): First name
  - `last_name` (string): Last name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `address` (string): Address
  - `guarantor_type` (string): Type of guarantor (individual, company)
  - Other basic guarantor fields
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

## Guarantor APIs

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/api/guarantors/` | `GET`, `POST` | List or create guarantors |
| `/api/guarantors/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | Guarantor detail operations |
| `/api/guarantors/{id}/guaranteed_applications/` | `GET` | Get applications guaranteed by guarantor |

### Guarantor List
- **API URL**: `/api/guarantors/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of guarantors with the following fields:
  - `id` (integer): Guarantor ID
  - `first_name` (string): First name
  - `last_name` (string): Last name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `address` (string): Address
  - `guarantor_type` (string): Type of guarantor (individual, company)
  - `relationship_to_borrower` (string): Relationship to the borrower (spouse, parent, child, sibling, business_partner, friend, other)
  - `created_at` (datetime): When the guarantor was created
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by first name, last name, email, or company name
  - `guarantor_type`: Filter by guarantor type
  - `relationship_to_borrower`: Filter by relationship to borrower

### Guarantor Detail
- **API URL**: `/api/guarantors/{id}/`
- **HTTP Method**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Required Input Fields**: None for GET, any of the following for PUT/PATCH:
  - `first_name` (string): First name
  - `last_name` (string): Last name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `address` (string): Address
  - `guarantor_type` (string): Type of guarantor (individual, company)
  - `relationship_to_borrower` (string): Relationship to the borrower (spouse, parent, child, sibling, business_partner, friend, other)
  - `borrower` (integer): Borrower ID
  - `application` (integer): Application ID
  - `company_name` (string): Company name (for company guarantors)
  - `company_abn` (string): Company ABN (for company guarantors)
  - `company_acn` (string): Company ACN (for company guarantors)
- **Response Fields**:
  - `id` (integer): Guarantor ID
  - `first_name` (string): First name
  - `last_name` (string): Last name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `address` (string): Address
  - `guarantor_type` (string): Type of guarantor
  - `relationship_to_borrower` (string): Relationship to the borrower
  - `borrower` (integer): Borrower ID
  - `borrower_name` (string): Name of the borrower
  - `application` (integer): Application ID
  - `company_name` (string): Company name (for company guarantors)
  - `company_abn` (string): Company ABN (for company guarantors)
  - `company_acn` (string): Company ACN (for company guarantors)
  - `created_at` (datetime): When the guarantor was created
  - `updated_at` (datetime): When the guarantor was last updated
  - `guaranteed_applications` (array): List of applications guaranteed by this guarantor
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Create Guarantor
- **API URL**: `/api/guarantors/`
- **HTTP Method**: `POST`
- **Required Input Fields**:
  - `guarantor_type` (string): Type of guarantor (individual, company)
  - For individual guarantors:
    - `first_name` (string): First name
    - `last_name` (string): Last name
  - For company guarantors:
    - `company_name` (string): Company name
  - Optional fields:
    - `email` (string): Email address
    - `phone` (string): Phone number
    - `address` (string): Address
    - `relationship_to_borrower` (string): Relationship to the borrower (spouse, parent, child, sibling, business_partner, friend, other)
    - `borrower` (integer): Borrower ID
    - `application` (integer): Application ID
    - `date_of_birth` (date): Date of birth (for individual guarantors)
    - `company_abn` (string): Company ABN (for company guarantors)
    - `company_acn` (string): Company ACN (for company guarantors)
- **Response Fields**:
  - `id` (integer): Guarantor ID
  - `guarantor_type` (string): Type of guarantor
  - `first_name` (string): First name
  - `last_name` (string): Last name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `address` (string): Address
  - `relationship_to_borrower` (string): Relationship to the borrower
  - `borrower` (integer): Borrower ID
  - `application` (integer): Application ID
  - `company_name` (string): Company name (for company guarantors)
  - `created_at` (datetime): When the guarantor was created
- **Status Codes**: `201`, `400`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Applications Guaranteed by Guarantor
- **API URL**: `/api/guarantors/{id}/guaranteed_applications/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of applications with basic details including:
  - `id` (integer): Application ID
  - `reference_number` (string): Application reference number
  - `application_type` (string): Type of application
  - `purpose` (string): Purpose of the loan
  - `loan_amount` (decimal): Amount of the loan
  - `stage` (string): Current stage of the application
  - `stage_display` (string): Human-readable stage
  - `created_at` (datetime): When the application was created
  - Other basic application fields
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No
## Broker APIs

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/api/brokers/` | `GET`, `POST` | List or create brokers |
| `/api/brokers/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | Broker detail operations |
| `/api/brokers/branches/` | `GET`, `POST` | List or create branches |
| `/api/brokers/branches/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | Branch detail operations |
| `/api/brokers/bdms/` | `GET`, `POST` | List or create BDMs |
| `/api/brokers/bdms/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | BDM detail operations |
| `/api/brokers/branches/{id}/brokers/` | `GET` | Get brokers in branch |
| `/api/brokers/branches/{id}/bdms/` | `GET` | Get BDMs in branch |
| `/api/brokers/{id}/applications/` | `GET` | Get broker applications |
| `/api/brokers/{id}/stats/` | `GET` | Get broker stats |
| `/api/brokers/bdms/{id}/applications/` | `GET` | Get BDM applications |

### Broker List
- **API URL**: `/api/brokers/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of brokers with the following fields:
  - `id` (integer): Broker ID
  - `name` (string): Broker name
  - `company` (string): Company name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `branch_name` (string): Name of the associated branch
  - `application_count` (integer): Number of applications
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by name, company, email, or phone
  - `branch`: Filter by branch ID
  - `min_applications`: Filter by minimum number of applications

### Broker Detail
- **API URL**: `/api/brokers/{id}/`
- **HTTP Method**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Required Input Fields**: None for GET, any of the following for PUT/PATCH:
  - `name` (string): Broker name
  - `company` (string): Company name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `address` (string): Address
  - `branch_id` (integer): Branch ID (write-only)
  - `user` (integer): Associated user ID
  - `commission_bank_name` (string): Bank name for commission payments
  - `commission_account_name` (string): Account name for commission payments
  - `commission_account_number` (string): Account number for commission payments
  - `commission_bsb` (string): BSB for commission payments
- **Response Fields**:
  - `id` (integer): Broker ID
  - `name` (string): Broker name
  - `company` (string): Company name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `address` (string): Address
  - `branch` (object): Branch details
  - `user` (object): Associated user details
  - `created_at` (datetime): When the broker was created
  - `updated_at` (datetime): When the broker was last updated
  - `commission_bank_name` (string): Bank name for commission payments
  - `commission_account_name` (string): Account name for commission payments
  - `commission_account_number` (string): Account number for commission payments
  - `commission_bsb` (string): BSB for commission payments
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Branch List
- **API URL**: `/api/brokers/branches/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of branches with the following fields:
  - `id` (integer): Branch ID
  - `name` (string): Branch name
  - `address` (string): Branch address
  - `phone` (string): Branch phone number
  - `email` (string): Branch email address
  - `created_at` (datetime): When the branch was created
  - `created_by` (object): User who created the branch
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by name or address

### Branch Detail
- **API URL**: `/api/brokers/branches/{id}/`
- **HTTP Method**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Required Input Fields**: None for GET, any of the following for PUT/PATCH:
  - `name` (string): Branch name
  - `address` (string): Branch address
  - `phone` (string): Branch phone number
  - `email` (string): Branch email address
- **Response Fields**:
  - `id` (integer): Branch ID
  - `name` (string): Branch name
  - `address` (string): Branch address
  - `phone` (string): Branch phone number
  - `email` (string): Branch email address
  - `created_at` (datetime): When the branch was created
  - `updated_at` (datetime): When the branch was last updated
  - `created_by` (object): User who created the branch
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### BDM List
- **API URL**: `/api/brokers/bdms/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of BDMs with the following fields:
  - `id` (integer): BDM ID
  - `name` (string): BDM name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `branch` (object): Branch details
  - `user` (object): Associated user details
  - `created_at` (datetime): When the BDM was created
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by name, email, or phone
  - `branch`: Filter by branch ID

### BDM Detail
- **API URL**: `/api/brokers/bdms/{id}/`
- **HTTP Method**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Required Input Fields**: None for GET, any of the following for PUT/PATCH:
  - `name` (string): BDM name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `branch_id` (integer): Branch ID (write-only)
  - `user` (integer): Associated user ID
- **Response Fields**:
  - `id` (integer): BDM ID
  - `name` (string): BDM name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `branch` (object): Branch details
  - `user` (object): Associated user details
  - `created_at` (datetime): When the BDM was created
  - `updated_at` (datetime): When the BDM was last updated
  - `created_by` (object): User who created the BDM
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Branch Brokers
- **API URL**: `/api/brokers/branches/{id}/brokers/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of brokers with the following fields:
  - `id` (integer): Broker ID
  - `name` (string): Broker name
  - `company` (string): Company name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `branch_name` (string): Branch name
  - `application_count` (integer): Number of applications
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Branch BDMs
- **API URL**: `/api/brokers/branches/{id}/bdms/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of BDMs with the following fields:
  - `id` (integer): BDM ID
  - `name` (string): BDM name
  - `email` (string): Email address
  - `phone` (string): Phone number
  - `branch` (object): Branch details
  - `user` (object): Associated user details
  - `created_at` (datetime): When the BDM was created
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Broker Applications
- **API URL**: `/api/brokers/{id}/applications/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of applications with the following fields:
  - `id` (integer): Application ID
  - `reference_number` (string): Application reference number
  - `application_type` (string): Type of application
  - `purpose` (string): Purpose of the loan
  - `loan_amount` (decimal): Amount of the loan
  - `stage` (string): Current stage of the application
  - `stage_display` (string): Human-readable stage
  - `created_at` (datetime): When the application was created
  - `broker_name` (string): Name of the broker
  - `borrower_count` (integer): Number of borrowers
  - `estimated_settlement_date` (date): Estimated settlement date
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get Broker Stats
- **API URL**: `/api/brokers/{id}/stats/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**:
  - `total_applications` (integer): Total number of applications
  - `total_loan_amount` (decimal): Total loan amount
  - `applications_by_stage` (object): Applications grouped by stage
  - `applications_by_type` (object): Applications grouped by type
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Get BDM Applications
- **API URL**: `/api/brokers/bdms/{id}/applications/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of applications with the following fields:
  - `id` (integer): Application ID
  - `reference_number` (string): Application reference number
  - `application_type` (string): Type of application
  - `purpose` (string): Purpose of the loan
  - `loan_amount` (decimal): Amount of the loan
  - `stage` (string): Current stage of the application
  - `stage_display` (string): Human-readable stage
  - `created_at` (datetime): When the application was created
  - `broker_name` (string): Name of the broker
  - `borrower_count` (integer): Number of borrowers
  - `estimated_settlement_date` (date): Estimated settlement date
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No
## Document APIs

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/api/documents/documents/` | `GET`, `POST` | List or create documents |
| `/api/documents/documents/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | Document detail operations |
| `/api/documents/documents/{id}/download/` | `GET` | Download document |
| `/api/documents/documents/{id}/create-version/` | `POST` | Create new document version |
| `/api/documents/notes/` | `GET`, `POST` | List or create notes |
| `/api/documents/notes/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | Note detail operations |
| `/api/documents/fees/` | `GET`, `POST` | List or create fees |
| `/api/documents/fees/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | Fee detail operations |
| `/api/documents/fees/{id}/mark-paid/` | `POST` | Mark fee as paid |
| `/api/documents/repayments/` | `GET`, `POST` | List or create repayments |
| `/api/documents/repayments/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | Repayment detail operations |
| `/api/documents/repayments/{id}/mark-paid/` | `POST` | Mark repayment as paid |
| `/api/documents/applications/{application_id}/ledger/` | `GET` | Get application ledger |

### Document List
- **API URL**: `/api/documents/documents/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of documents with the following fields:
  - `id` (integer): Document ID
  - `title` (string): Document title
  - `description` (string): Document description
  - `document_type` (string): Type of document
  - `document_type_display` (string): Human-readable document type
  - `file` (string): File path
  - `file_url` (string): Full URL to the file
  - `file_name` (string): File name
  - `file_size` (integer): File size in bytes
  - `file_type` (string): MIME type of the file
  - `version` (integer): Document version
  - `previous_version` (integer): ID of the previous version
  - `application` (integer): Associated application ID
  - `borrower` (integer): Associated borrower ID
  - `created_by` (integer): ID of the user who created the document
  - `created_by_name` (string): Name of the user who created the document
  - `created_at` (datetime): When the document was created
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by title, description, or file name
  - `document_type`: Filter by document type
  - `application`: Filter by application ID
  - `borrower`: Filter by borrower ID

### Document Detail
- **API URL**: `/api/documents/documents/{id}/`
- **HTTP Method**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Required Input Fields**: None for GET, any of the following for PUT/PATCH:
  - `title` (string): Document title
  - `description` (string): Document description
  - `document_type` (string): Type of document
  - `file` (file): Document file (for creating a new version)
  - `application` (integer): Associated application ID
  - `borrower` (integer): Associated borrower ID
- **Response Fields**:
  - `id` (integer): Document ID
  - `title` (string): Document title
  - `description` (string): Document description
  - `document_type` (string): Type of document
  - `document_type_display` (string): Human-readable document type
  - `file` (string): File path
  - `file_url` (string): Full URL to the file
  - `file_name` (string): File name
  - `file_size` (integer): File size in bytes
  - `file_type` (string): MIME type of the file
  - `version` (integer): Document version
  - `previous_version` (integer): ID of the previous version
  - `application` (integer): Associated application ID
  - `borrower` (integer): Associated borrower ID
  - `created_by` (integer): ID of the user who created the document
  - `created_by_name` (string): Name of the user who created the document
  - `created_at` (datetime): When the document was created
  - `updated_at` (datetime): When the document was last updated
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Download Document
- **API URL**: `/api/documents/documents/{id}/download/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: File download (binary data with appropriate Content-Type and Content-Disposition headers)
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Document Create Version
- **API URL**: `/api/documents/documents/{id}/create-version/`
- **HTTP Method**: `POST`
- **Required Input Fields**:
  - `file` (file): New version of the document file
  - `description` (string, optional): Description of the changes in this version
- **Response Fields**:
  - `message` (string): Success message
  - `document_id` (integer): ID of the new document version
  - `version` (integer): Version number of the new document
  - `document_url` (string): URL to access the new document
- **Status Codes**: `201`, `400`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Note List
- **API URL**: `/api/documents/notes/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of notes with the following fields:
  - `id` (integer): Note ID
  - `content` (string): Note content
  - `application` (integer): Associated application ID
  - `created_by` (integer): ID of the user who created the note
  - `created_at` (datetime): When the note was created
  - `created_by_name` (string): Name of the user who created the note
  - `title` (string): Note title
  - `remind_date` (datetime, nullable): Reminder date
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `search`: Search by content or title
  - `application`: Filter by application ID
  - `date_from`: Filter by date (YYYY-MM-DD format)
  - `date_to`: Filter by date (YYYY-MM-DD format)

### Note Detail
- **API URL**: `/api/documents/notes/{id}/`
- **HTTP Method**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Required Input Fields**: None for GET, any of the following for PUT/PATCH:
  - `content` (string): Note content
  - `title` (string): Note title
  - `application` (integer): Associated application ID
  - `borrower` (integer): Associated borrower ID
  - `remind_date` (datetime): Reminder date
- **Response Fields**:
  - `id` (integer): Note ID
  - `content` (string): Note content
  - `title` (string): Note title
  - `application` (integer): Associated application ID
  - `borrower` (integer): Associated borrower ID
  - `created_by` (integer): ID of the user who created the note
  - `created_at` (datetime): When the note was created
  - `updated_at` (datetime): When the note was last updated
  - `remind_date` (datetime, nullable): Reminder date
  - `created_by_name` (string): Name of the user who created the note
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Fee List
- **API URL**: `/api/documents/fees/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of fees with the following fields:
  - `id` (integer): Fee ID
  - `fee_type` (string): Type of fee (application, valuation, legal, broker, settlement, other)
  - `fee_type_display` (string): Human-readable fee type
  - `amount` (decimal): Fee amount
  - `application` (integer): Associated application ID
  - `is_paid` (boolean): Whether the fee has been paid
  - `due_date` (date): When the fee is due
  - `paid_date` (date, nullable): When the fee was paid
  - `status` (string): Fee status (pending, paid)
  - `invoice_url` (string, nullable): URL to the invoice file
  - `description` (string): Fee description
  - `created_by_name` (string): Name of the user who created the fee
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `application`: Filter by application ID
  - `is_paid`: Filter by payment status (true/false)
  - `fee_type`: Filter by fee type
  - `date_from`: Filter by date (YYYY-MM-DD format)
  - `date_to`: Filter by date (YYYY-MM-DD format)

### Fee Detail
- **API URL**: `/api/documents/fees/{id}/`
- **HTTP Method**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Required Input Fields**: None for GET, any of the following for PUT/PATCH:
  - `fee_type` (string): Type of fee
  - `amount` (decimal): Fee amount
  - `application` (integer): Associated application ID
  - `due_date` (date): When the fee is due
  - `description` (string): Fee description
  - `invoice` (file): Invoice file
- **Response Fields**:
  - `id` (integer): Fee ID
  - `fee_type` (string): Type of fee
  - `fee_type_display` (string): Human-readable fee type
  - `amount` (decimal): Fee amount
  - `application` (integer): Associated application ID
  - `is_paid` (boolean): Whether the fee has been paid
  - `due_date` (date): When the fee is due
  - `paid_date` (date, nullable): When the fee was paid
  - `status` (string): Fee status (pending, paid)
  - `invoice_url` (string, nullable): URL to the invoice file
  - `description` (string): Fee description
  - `created_by` (integer): ID of the user who created the fee
  - `created_by_name` (string): Name of the user who created the fee
  - `created_at` (datetime): When the fee was created
  - `updated_at` (datetime): When the fee was last updated
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Fee Mark Paid
- **API URL**: `/api/documents/fees/{id}/mark-paid/`
- **HTTP Method**: `POST`
- **Required Input Fields**:
  - `paid_date` (date, optional): Date when the fee was paid (defaults to current date)
- **Response Fields**:
  - `message` (string): Success message
  - `fee_id` (integer): Fee ID
  - `paid_date` (date): Date when the fee was paid
  - `status` (string): Updated status (paid)
  - `fee` (object): Complete fee object with all fields
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Repayment List
- **API URL**: `/api/documents/repayments/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of repayments with the following fields:
  - `id` (integer): Repayment ID
  - `amount` (decimal): Repayment amount
  - `application` (integer): Associated application ID
  - `due_date` (date): When the repayment is due
  - `paid_date` (date, nullable): When the repayment was paid
  - `invoice` (string, nullable): Path to the invoice file
  - `invoice_url` (string, nullable): URL to the invoice file
  - `status` (string): Repayment status (scheduled, paid, overdue_X_days, due_soon_X_days)
  - `created_by` (integer): ID of the user who created the repayment
  - `created_by_name` (string): Name of the user who created the repayment
  - `created_at` (datetime): When the repayment was created
  - `updated_at` (datetime): When the repayment was last updated
  - `reminder_sent` (boolean): Whether a reminder has been sent
  - `overdue_3_day_sent` (boolean): Whether a 3-day overdue notification has been sent
  - `overdue_7_day_sent` (boolean): Whether a 7-day overdue notification has been sent
  - `overdue_10_day_sent` (boolean): Whether a 10-day overdue notification has been sent
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: Yes (`limit`, `offset`)
- **Search/Filter Support?**: Yes
  - `application`: Filter by application ID
  - `is_paid`: Filter by payment status (true/false)
  - `date_from`: Filter by date (YYYY-MM-DD format)
  - `date_to`: Filter by date (YYYY-MM-DD format)

### Repayment Detail
- **API URL**: `/api/documents/repayments/{id}/`
- **HTTP Method**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Required Input Fields**: None for GET, any of the following for PUT/PATCH:
  - `amount` (decimal): Repayment amount
  - `application` (integer): Associated application ID
  - `due_date` (date): When the repayment is due
  - `invoice` (file): Invoice file
- **Response Fields**:
  - `id` (integer): Repayment ID
  - `amount` (decimal): Repayment amount
  - `application` (integer): Associated application ID
  - `due_date` (date): When the repayment is due
  - `is_paid` (boolean): Whether the repayment has been paid
  - `paid_date` (date, nullable): When the repayment was paid
  - `payment_method` (string, nullable): Method of payment
  - `status` (string): Repayment status
  - `invoice_url` (string, nullable): URL to the invoice file
  - `created_by` (integer): ID of the user who created the repayment
  - `created_by_name` (string): Name of the user who created the repayment
  - `created_at` (datetime): When the repayment was created
  - `updated_at` (datetime): When the repayment was last updated
  - `reminder_sent` (boolean): Whether a reminder has been sent
  - `overdue_3_day_sent` (boolean): Whether a 3-day overdue notification has been sent
  - `overdue_7_day_sent` (boolean): Whether a 7-day overdue notification has been sent
  - `overdue_10_day_sent` (boolean): Whether a 10-day overdue notification has been sent
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Repayment Mark Paid
- **API URL**: `/api/documents/repayments/{id}/mark-paid/`
- **HTTP Method**: `POST`
- **Required Input Fields**:
  - `paid_date` (date, optional): Date when the repayment was paid (defaults to current date)
- **Response Fields**:
  - `message` (string): Success message
  - `repayment_id` (integer): Repayment ID
  - `paid_date` (date): Date when the repayment was paid
  - `status` (string): Updated status (paid)
  - `repayment` (object): Complete repayment object with all fields
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No

### Application Ledger
- **API URL**: `/api/documents/applications/{application_id}/ledger/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: List of ledger entries with the following fields:
  - `id` (integer): Ledger entry ID
  - `application` (integer): Associated application ID
  - `transaction_type` (string): Type of transaction (fee_created, fee_paid, repayment_scheduled, repayment_received, adjustment)
  - `transaction_type_display` (string): Human-readable transaction type
  - `amount` (decimal): Amount of the transaction
  - `description` (string): Description of the transaction
  - `transaction_date` (datetime): Date of the transaction
  - `related_fee` (integer, nullable): ID of the related fee
  - `related_fee_type` (string, nullable): Type of the related fee
  - `related_repayment` (integer, nullable): ID of the related repayment
  - `created_by` (integer): ID of the user who created the entry
  - `created_at` (datetime): When the entry was created
- **Status Codes**: `200`, `401`, `404`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: No
## Report APIs

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/api/reports/application-volume/` | `GET` | Get application volume report |
| `/api/reports/application-status/` | `GET` | Get application status report |
| `/api/reports/repayment-compliance/` | `GET` | Get repayment compliance report |

### Application Volume Report
- **API URL**: `/api/reports/application-volume/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: 
  - `total_applications` (integer): Total number of applications
  - `total_loan_amount` (decimal): Total loan amount across all applications
  - `average_loan_amount` (decimal): Average loan amount per application
  - `stage_breakdown` (object): Count of applications by stage
  - `time_breakdown` (array): Applications grouped by time period with the following fields:
    - `period` (string): Time period (format depends on time_grouping parameter)
    - `count` (integer): Number of applications in this period
    - `total_amount` (decimal): Total loan amount in this period
  - `bd_breakdown` (array): Applications grouped by BDM with the following fields:
    - `bd_id` (integer): BDM ID
    - `bd_name` (string): BDM name
    - `count` (integer): Number of applications for this BDM
    - `total_amount` (decimal): Total loan amount for this BDM
  - `type_breakdown` (object): Count of applications by application type
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: Yes
  - `start_date` (date): Filter by applications created on or after this date
  - `end_date` (date): Filter by applications created on or before this date
  - `bd_id` (integer): Filter by BDM ID
  - `broker_id` (integer): Filter by broker ID
  - `time_grouping` (string): Group by 'day', 'week', or 'month' (default: 'month')

### Application Status Report
- **API URL**: `/api/reports/application-status/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: 
  - `total_active` (integer): Total number of active applications
  - `total_settled` (integer): Total number of settled applications
  - `total_declined` (integer): Total number of declined applications
  - `total_withdrawn` (integer): Total number of withdrawn applications
  - `active_by_stage` (object): Count of active applications by stage
  - `avg_time_in_stage` (object): Average time spent in each stage (in days)
  - `inquiry_to_approval_rate` (float): Percentage of inquiries that reach approval
  - `approval_to_settlement_rate` (float): Percentage of approvals that reach settlement
  - `overall_success_rate` (float): Percentage of inquiries that reach settlement
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: Yes
  - `start_date` (date): Filter by applications created on or after this date
  - `end_date` (date): Filter by applications created on or before this date

### Repayment Compliance Report
- **API URL**: `/api/reports/repayment-compliance/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**: 
  - `total_repayments` (integer): Total number of repayments
  - `paid_on_time` (integer): Number of repayments paid on time
  - `paid_late` (integer): Number of repayments paid late
  - `missed` (integer): Number of missed repayments
  - `compliance_rate` (float): Percentage of repayments paid on time
  - `average_days_late` (float): Average number of days late for late payments
  - `total_amount_due` (decimal): Total amount due across all repayments
  - `total_amount_paid` (decimal): Total amount paid across all repayments
  - `payment_rate` (float): Percentage of total amount paid vs. amount due
  - `monthly_breakdown` (array): Repayments grouped by month with the following fields:
    - `month` (string): Month in YYYY-MM format
    - `total_repayments` (integer): Number of repayments in this month
    - `paid_on_time` (integer): Number of repayments paid on time in this month
    - `paid_late` (integer): Number of repayments paid late in this month
    - `missed` (integer): Number of missed repayments in this month
    - `compliance_rate` (float): Percentage of repayments paid on time in this month
    - `amount_due` (decimal): Total amount due in this month
    - `amount_paid` (decimal): Total amount paid in this month
    - `payment_rate` (float): Percentage of amount paid vs. amount due in this month
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: Yes
  - `start_date` (date): Filter by repayments due on or after this date
  - `end_date` (date): Filter by repayments due on or before this date
  - `application_id` (integer): Filter by application ID
## Pagination, Search, and Filtering

This section documents the pagination, search, and filtering capabilities for list APIs in the system.

### Pagination Method
The system uses **limit/offset pagination** for all list endpoints. This pagination method allows clients to:
- Specify how many records to return (`limit`)
- Specify how many records to skip (`offset`)

**Example Query Parameters:**
```
/api/applications/?limit=10&offset=20
```

### List APIs with Pagination, Search, and Filtering

| Endpoint | Pagination | Searchable Fields | Filterable Fields | Example Query |
|----------|------------|------------------|-------------------|---------------|
| `/api/users/users/` | `limit`, `offset` | Email, first name, last name | `role` | `/api/users/users/?search=john&role=broker&limit=10` |
| `/api/users/notifications/` | `limit`, `offset` | Title, message | `notification_type`, `is_read` | `/api/users/notifications/?notification_type=application_status&is_read=false&limit=20` |
| `/api/users/notifications/advanced_search/` | `limit`, `offset` | Title, message | `notification_type`, `is_read`, `date_from`, `date_to` | `/api/users/notifications/advanced_search/?date_from=2023-01-01&date_to=2023-12-31` |
| `/api/applications/` | `limit`, `offset` | Reference number, purpose | `status`, `stage`, `borrower`, `date_from`, `date_to` | `/api/applications/?stage=inquiry&date_from=2023-01-01&limit=15` |
| `/api/applications/{id}/notes/` | `limit`, `offset` | Content | `date_from`, `date_to` | `/api/applications/123/notes/?search=urgent&limit=10` |
| `/api/applications/{id}/documents/` | `limit`, `offset` | Title | `document_type` | `/api/applications/123/documents/?document_type=contract&limit=5` |
| `/api/applications/{id}/fees/` | `limit`, `offset` | None | `is_paid`, `fee_type` | `/api/applications/123/fees/?is_paid=false&fee_type=application` |
| `/api/applications/{id}/repayments/` | `limit`, `offset` | None | `is_paid`, `date_from`, `date_to` | `/api/applications/123/repayments/?is_paid=false&limit=10` |
| `/api/applications/{id}/ledger/` | `limit`, `offset` | None | `entry_type`, `date_from`, `date_to` | `/api/applications/123/ledger/?entry_type=fee_paid&limit=20` |
| `/api/borrowers/` | `limit`, `offset` | First name, last name, email | `borrower_type` | `/api/borrowers/?search=smith&borrower_type=individual&limit=10` |
| `/api/borrowers/company/` | `limit`, `offset` | Company name, contact person | None | `/api/borrowers/company/?search=acme&limit=10` |
| `/api/guarantors/` | `limit`, `offset` | First name, last name, email | `relationship_to_borrower` | `/api/guarantors/?search=jones&limit=10` |
| `/api/brokers/` | `limit`, `offset` | Name, email | `branch` | `/api/brokers/?search=michael&branch=5&limit=10` |
| `/api/brokers/branches/` | `limit`, `offset` | Name, address | `manager` | `/api/brokers/branches/?search=sydney&limit=10` |
| `/api/brokers/bdms/` | `limit`, `offset` | Name, email | `branch` | `/api/brokers/bdms/?branch=3&limit=10` |
| `/api/documents/documents/` | `limit`, `offset` | Title, description | `document_type`, `application`, `borrower` | `/api/documents/documents/?document_type=contract&application=42&limit=10` |
| `/api/documents/notes/` | `limit`, `offset` | Content | `application`, `date_from`, `date_to` | `/api/documents/notes/?application=42&search=follow-up&limit=10` |
| `/api/documents/fees/` | `limit`, `offset` | None | `application`, `is_paid`, `fee_type`, `date_from`, `date_to` | `/api/documents/fees/?application=42&is_paid=false&limit=10` |
| `/api/documents/repayments/` | `limit`, `offset` | None | `application`, `is_paid`, `date_from`, `date_to` | `/api/documents/repayments/?application=42&is_paid=true&limit=10` |

### Report APIs with Filtering (No Pagination)

| Endpoint | Pagination | Filterable Fields | Example Query |
|----------|------------|-------------------|---------------|
| `/api/reports/application-volume/` | None | `start_date`, `end_date`, `broker_id`, `branch_id` | `/api/reports/application-volume/?start_date=2023-01-01&end_date=2023-12-31&broker_id=5` |
| `/api/reports/application-status/` | None | `start_date`, `end_date` | `/api/reports/application-status/?start_date=2023-01-01&end_date=2023-12-31` |
| `/api/reports/repayment-compliance/` | None | `start_date`, `end_date`, `application_id` | `/api/reports/repayment-compliance/?application_id=42` |
| `/api/reports/broker-performance/` | None | `start_date`, `end_date`, `branch_id` | `/api/reports/broker-performance/?branch_id=3&start_date=2023-01-01` |
| `/api/reports/loan-portfolio/` | None | `start_date`, `end_date` | `/api/reports/loan-portfolio/?start_date=2023-01-01&end_date=2023-12-31` |

### APIs Missing Pagination

The following list endpoints do not implement pagination and return all results:

1. `/api/borrowers/{id}/applications/` - Returns all applications for a borrower
2. `/api/borrowers/{id}/guarantors/` - Returns all guarantors for a borrower
3. `/api/guarantors/{id}/guaranteed_applications/` - Returns all applications guaranteed by a guarantor
4. `/api/brokers/branches/{id}/brokers/` - Returns all brokers in a branch
5. `/api/brokers/branches/{id}/bdms/` - Returns all BDMs in a branch
6. `/api/brokers/{id}/applications/` - Returns all applications for a broker
7. `/api/brokers/bdms/{id}/applications/` - Returns all applications for a BDM

These endpoints may need pagination implementation in the future if the result sets grow large.

## API Relationships Documentation

This section documents the relationships between API endpoints and the models they interact with, focusing on foreign keys and relationships that need to be considered when using these endpoints.

### Authentication APIs

No foreign key relationships required for authentication endpoints.

### User APIs

| Endpoint | Foreign Keys/Relationships | Source | Creation |
|----------|---------------------------|--------|----------|
| `/api/users/profile/` | None | N/A | N/A |
| `/api/users/profile/update/` | None | N/A | N/A |
| `/api/users/users/` | None | N/A | N/A |
| `/api/users/users/{id}/` | None | N/A | N/A |
| `/api/users/users/me/` | None | N/A | N/A |

### Notification APIs

| Endpoint | Foreign Keys/Relationships | Source | Creation |
|----------|---------------------------|--------|----------|
| `/api/users/notifications/` | `user` (User) | Automatically set to current user | N/A |
| `/api/users/notifications/{id}/mark_as_read/` | `user` (User) | Automatically set to current user | N/A |
| `/api/users/notifications/mark_all_as_read/` | `user` (User) | Automatically set to current user | N/A |
| `/api/users/notifications/unread_count/` | `user` (User) | Automatically set to current user | N/A |
| `/api/users/notifications/advanced_search/` | `user` (User) | Automatically set to current user | N/A |
| `/api/users/notification-preferences/` | `user` (User) | Automatically set to current user | N/A |

### Application APIs

| Endpoint | Foreign Keys/Relationships | Source | Creation |
|----------|---------------------------|--------|----------|
| `/api/applications/` (GET) | None | N/A | N/A |
| `/api/applications/` (POST) | `broker` (Broker), `branch` (Branch), `bd` (BDM) | Must be selected from existing records via dropdown | Must exist |
| `/api/applications/{id}/` | None for GET, same as POST for PUT/PATCH | Same as POST | Same as POST |
| `/api/applications/create-with-cascade/` | `broker` (Broker), `branch` (Branch), `bd` (BDM), `borrowers` (array of Borrower objects), `guarantors` (array of Guarantor objects), `company_borrowers` (array of Company Borrower objects) | Broker, branch, bd must exist; borrowers, guarantors, company_borrowers can be created in the same request as full objects | Broker, branch, bd must exist; borrowers, guarantors, company_borrowers can be created |
| `/api/applications/validate-schema/` | None | N/A | N/A |
| `/api/applications/{id}/stage/` | None | N/A | N/A |
| `/api/applications/{id}/borrowers/` | `borrowers` (array of Borrower IDs) | Must be selected from existing records via dropdown | Must exist |
| `/api/applications/{id}/signature/` | None | N/A | N/A |
| `/api/applications/{id}/guarantors/` | None | N/A | N/A |
| `/api/applications/{id}/notes/` | None | N/A | N/A |
| `/api/applications/{id}/add-note/` | `application` (Application) | Automatically set from URL parameter | Must exist |
| `/api/applications/{id}/documents/` | None | N/A | N/A |
| `/api/applications/{id}/upload-document/` | `application` (Application) | Automatically set from URL parameter | Must exist |
| `/api/applications/{id}/fees/` | None | N/A | N/A |
| `/api/applications/{id}/add-fee/` | `application` (Application) | Automatically set from URL parameter | Must exist |
| `/api/applications/{id}/repayments/` | None | N/A | N/A |
| `/api/applications/{id}/add-repayment/` | `application` (Application) | Automatically set from URL parameter | Must exist |
| `/api/applications/{id}/record-payment/` | `repayment_id` (Repayment) | Must be provided in request body | Must exist |
| `/api/applications/{id}/ledger/` | None | N/A | N/A |

### Borrower APIs

| Endpoint | Foreign Keys/Relationships | Source | Creation |
|----------|---------------------------|--------|----------|
| `/api/borrowers/` (GET) | None | N/A | N/A |
| `/api/borrowers/` (POST) | None | N/A | N/A |
| `/api/borrowers/{id}/` | None | N/A | N/A |
| `/api/borrowers/company/` | None | N/A | N/A |
| `/api/borrowers/{id}/financial-summary/` | None | N/A | N/A |
| `/api/borrowers/{id}/applications/` | None | N/A | N/A |
| `/api/borrowers/{id}/guarantors/` | None | N/A | N/A |

### Guarantor APIs

| Endpoint | Foreign Keys/Relationships | Source | Creation |
|----------|---------------------------|--------|----------|
| `/api/guarantors/` (GET) | None | N/A | N/A |
| `/api/guarantors/` (POST) | `borrower` (Borrower), `application` (Application) | Optional, can be selected from dropdown. A guarantor can be linked to either a borrower, an application, or both | Can be null or must exist |
| `/api/guarantors/{id}/` | Same as POST for PUT/PATCH | Same as POST | Same as POST |
| `/api/guarantors/{id}/guaranteed_applications/` | None | N/A | N/A |

### Broker APIs

| Endpoint | Foreign Keys/Relationships | Source | Creation |
|----------|---------------------------|--------|----------|
| `/api/brokers/` (GET) | None | N/A | N/A |
| `/api/brokers/` (POST) | `branch` (Branch), `user` (User) | Must be selected from existing records via dropdown | Must exist |
| `/api/brokers/{id}/` | Same as POST for PUT/PATCH | Same as POST | Same as POST |
| `/api/brokers/branches/` (GET) | None | N/A | N/A |
| `/api/brokers/branches/` (POST) | None | N/A | N/A |
| `/api/brokers/branches/{id}/` | None | N/A | N/A |
| `/api/brokers/bdms/` (GET) | None | N/A | N/A |
| `/api/brokers/bdms/` (POST) | `branch` (Branch), `user` (User) | Branch must be selected from existing records via dropdown; user is optional | Branch must exist; user can be null or must exist |
| `/api/brokers/bdms/{id}/` | Same as POST for PUT/PATCH | Same as POST | Same as POST |
| `/api/brokers/branches/{id}/brokers/` | None | N/A | N/A |
| `/api/brokers/branches/{id}/bdms/` | None | N/A | N/A |
| `/api/brokers/{id}/applications/` | None | N/A | N/A |
| `/api/brokers/{id}/stats/` | None | N/A | N/A |
| `/api/brokers/bdms/{id}/applications/` | None | N/A | N/A |

### Document APIs

| Endpoint | Foreign Keys/Relationships | Source | Creation |
|----------|---------------------------|--------|----------|
| `/api/documents/documents/` (GET) | None | N/A | N/A |
| `/api/documents/documents/` (POST) | `application` (Application), `borrower` (Borrower), `previous_version` (Document), `file` (File upload) | Application and borrower are optional, can be selected from dropdown; file is required | Application and borrower can be null or must exist; file must be provided |
| `/api/documents/documents/{id}/` | Same as POST for PUT/PATCH | Same as POST | Same as POST |
| `/api/documents/documents/{id}/download/` | None | N/A | N/A |
| `/api/documents/documents/{id}/create-version/` | `previous_version` (Document), `file` (File upload) | Previous version automatically set from URL parameter; file is required | Previous version must exist; file must be provided |
| `/api/documents/notes/` (GET) | None | N/A | N/A |
| `/api/documents/notes/` (POST) | `application` (Application), `borrower` (Borrower) | At least one must be provided, selected from dropdown | At least one must exist |
| `/api/documents/notes/{id}/` | Same as POST for PUT/PATCH | Same as POST | Same as POST |
| `/api/documents/fees/` (GET) | None | N/A | N/A |
| `/api/documents/fees/` (POST) | `application` (Application) | Must be selected from dropdown | Must exist |
| `/api/documents/fees/{id}/` | Same as POST for PUT/PATCH | Same as POST | Same as POST |
| `/api/documents/fees/{id}/mark-paid/` | None | N/A | N/A |
| `/api/documents/repayments/` (GET) | None | N/A | N/A |
| `/api/documents/repayments/` (POST) | `application` (Application) | Must be selected from dropdown | Must exist |
| `/api/documents/repayments/{id}/` | Same as POST for PUT/PATCH | Same as POST | Same as POST |
| `/api/documents/repayments/{id}/mark-paid/` | None | N/A | N/A |
| `/api/documents/applications/{application_id}/ledger/` | `application_id` (Application) | From URL parameter | Must exist |

### Report APIs

| Endpoint | Foreign Keys/Relationships | Source | Creation |
|----------|---------------------------|--------|----------|
| `/api/reports/application-volume/` | `broker_id` (Broker), `branch_id` (Branch) | Optional filter parameters | Must exist if provided |
| `/api/reports/application-status/` | None | N/A | N/A |
| `/api/reports/repayment-compliance/` | `application_id` (Application) | Optional filter parameter | Must exist if provided |
| `/api/reports/broker-performance/` | `branch_id` (Branch) | Optional filter parameter | Must exist if provided |
| `/api/reports/loan-portfolio/` | None | N/A | N/A |

## API Endpoint Verification

This section verifies that all endpoints in the codebase are correctly documented above.

### Broker Endpoints
- ✅ `/api/brokers/` (BrokerViewSet)
- ✅ `/api/brokers/{id}/` (BrokerViewSet)
- ✅ `/api/brokers/{id}/applications/` (BrokerViewSet.applications)
- ✅ `/api/brokers/{id}/stats/` (BrokerViewSet.stats)
- ✅ `/api/brokers/bdms/` (BDMViewSet)
- ✅ `/api/brokers/bdms/{id}/` (BDMViewSet)
- ✅ `/api/brokers/bdms/{id}/applications/` (BDMViewSet.applications)
- ✅ `/api/brokers/branches/` (BranchViewSet)
- ✅ `/api/brokers/branches/{id}/` (BranchViewSet)
- ✅ `/api/brokers/branches/{id}/brokers/` (BranchViewSet.brokers)
- ✅ `/api/brokers/branches/{id}/bdms/` (BranchViewSet.bdms)

### Borrower Endpoints
- ✅ `/api/borrowers/` (BorrowerViewSet)
- ✅ `/api/borrowers/{id}/` (BorrowerViewSet)
- ✅ `/api/borrowers/company/` (CompanyBorrowerListView)
- ✅ `/api/borrowers/{id}/financial-summary/` (BorrowerFinancialSummaryView)
- ✅ `/api/guarantors/` (GuarantorViewSet)
- ✅ `/api/guarantors/{id}/` (GuarantorViewSet)
- ✅ `/api/guarantors/{id}/guaranteed_applications/` (GuarantorViewSet.guaranteed_applications)

### Application Endpoints
- ✅ `/api/applications/` (ApplicationViewSet)
- ✅ `/api/applications/{id}/` (ApplicationViewSet)
- ✅ `/api/applications/create-with-cascade/` (ApplicationViewSet.create)
- ✅ `/api/applications/validate-schema/` (ApplicationViewSet.validate_schema)
- ✅ `/api/applications/{id}/stage/` (ApplicationViewSet.update_stage)
- ✅ `/api/applications/{id}/borrowers/` (ApplicationViewSet.borrowers)
- ✅ `/api/applications/{id}/signature/` (ApplicationViewSet.sign)
- ✅ `/api/applications/{id}/guarantors/` (ApplicationViewSet.guarantors)
- ✅ `/api/applications/{id}/notes/` (ApplicationViewSet.notes)
- ✅ `/api/applications/{id}/add-note/` (ApplicationViewSet.add_note)
- ✅ `/api/applications/{id}/documents/` (ApplicationViewSet.documents)
- ✅ `/api/applications/{id}/upload-document/` (ApplicationViewSet.upload_document)
- ✅ `/api/applications/{id}/fees/` (ApplicationViewSet.fees)
- ✅ `/api/applications/{id}/add-fee/` (ApplicationViewSet.add_fee)
- ✅ `/api/applications/{id}/repayments/` (ApplicationViewSet.repayments)
- ✅ `/api/applications/{id}/add-repayment/` (ApplicationViewSet.add_repayment)
- ✅ `/api/applications/{id}/record-payment/` (ApplicationViewSet.record_payment)
- ✅ `/api/applications/{id}/ledger/` (ApplicationViewSet.ledger)

### Document Endpoints
- ✅ `/api/documents/documents/` (DocumentViewSet)
- ✅ `/api/documents/documents/{id}/` (DocumentViewSet)
- ✅ `/api/documents/documents/{id}/download/` (DocumentViewSet.download)
- ✅ `/api/documents/documents/{id}/create-version/` (DocumentCreateVersionView)
- ✅ `/api/documents/notes/` (NoteViewSet)
- ✅ `/api/documents/notes/{id}/` (NoteViewSet)
- ✅ `/api/documents/fees/` (FeeViewSet)
- ✅ `/api/documents/fees/{id}/` (FeeViewSet)
- ✅ `/api/documents/fees/{id}/mark-paid/` (FeeMarkPaidView)
- ✅ `/api/documents/repayments/` (RepaymentViewSet)
- ✅ `/api/documents/repayments/{id}/` (RepaymentViewSet)
- ✅ `/api/documents/repayments/{id}/mark-paid/` (RepaymentMarkPaidView)
- ✅ `/api/documents/applications/{application_id}/ledger/` (ApplicationLedgerView)

### Report Endpoints
- ✅ `/api/reports/application-volume/` (ApplicationVolumeReportView)
- ✅ `/api/reports/application-status/` (ApplicationStatusReportView)
- ✅ `/api/reports/repayment-compliance/` (RepaymentComplianceReportView)

### User and Notification Endpoints
- ✅ `/api/users/auth/login/` (LoginView)
- ✅ `/api/users/auth/register/` (RegisterView)
- ✅ `/api/users/auth/refresh/` (TokenRefreshView)
- ✅ `/api/users/profile/` (UserProfileView)
- ✅ `/api/users/profile/update/` (UserProfileUpdateView)
- ✅ `/api/users/users/` (UserViewSet)
- ✅ `/api/users/users/{id}/` (UserViewSet)
- ✅ `/api/users/users/me/` (UserViewSet.me)
- ✅ `/api/users/notifications/` (NotificationViewSet)
- ✅ `/api/users/notifications/{id}/` (NotificationViewSet)
- ✅ `/api/users/notifications/{id}/mark_as_read/` (NotificationViewSet.mark_as_read)
- ✅ `/api/users/notifications/mark_all_as_read/` (NotificationViewSet.mark_all_as_read)
- ✅ `/api/users/notifications/unread_count/` (NotificationViewSet.unread_count)
- ✅ `/api/users/notifications/advanced_search/` (NotificationViewSet.advanced_search)
- ✅ `/api/users/notification-preferences/` (NotificationPreferenceView)

All endpoints from the codebase have been verified and are correctly documented in this API documentation.

## Error Handling and Validation

This section documents common HTTP error codes, their causes, and example error responses for each API endpoint category.

### Authentication APIs

#### Common Error Codes

**401 Unauthorized**
- **When it happens**: Invalid credentials during login, expired or invalid token
- **Example response**:
```json
{
  "error": "Invalid credentials"
}
```

**400 Bad Request**
- **When it happens**: Invalid registration data (e.g., password mismatch, missing required fields)
- **Example response**:
```json
{
  "email": ["This field is required."],
  "password": ["This field is required."],
  "password2": ["Passwords must match."]
}
```

**500 Internal Server Error**
- **When it happens**: Server-side error during registration or login
- **Example response**:
```json
{
  "error": "An unexpected error occurred. Please try again later."
}
```

### User APIs

#### Common Error Codes

**401 Unauthorized**
- **When it happens**: Missing or invalid authentication token
- **Example response**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden**
- **When it happens**: User doesn't have permission to perform the action (e.g., non-admin trying to access user list)
- **Example response**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found**
- **When it happens**: Requested user doesn't exist
- **Example response**:
```json
{
  "detail": "Not found."
}
```

**400 Bad Request**
- **When it happens**: Invalid data in profile update
- **Example response**:
```json
{
  "email": ["Enter a valid email address."],
  "phone": ["Phone number must be in the format +1234567890."]
}
```

### Notification APIs

#### Common Error Codes

**401 Unauthorized**
- **When it happens**: Missing or invalid authentication token
- **Example response**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**404 Not Found**
- **When it happens**: Notification ID doesn't exist or doesn't belong to the user
- **Example response**:
```json
{
  "detail": "Not found."
}
```

**400 Bad Request**
- **When it happens**: Invalid data in notification preferences update
- **Example response**:
```json
{
  "application_status_email": ["Must be a boolean value."]
}
```

### Application APIs

#### Common Error Codes

**401 Unauthorized**
- **When it happens**: Missing or invalid authentication token
- **Example response**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden**
- **When it happens**: User doesn't have permission to perform the action (e.g., client trying to update application stage)
- **Example response**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found**
- **When it happens**: Application ID doesn't exist or user doesn't have access to it
- **Example response**:
```json
{
  "detail": "Not found."
}
```

**400 Bad Request**
- **When it happens**: Invalid data in application creation or update
- **Example response**:
```json
{
  "loan_amount": ["This field is required."],
  "stage": ["Invalid stage value. Choose from: inquiry, pre_approval, valuation, formal_approval, settlement, funded, declined, withdrawn."],
  "borrowers": ["This field is required and must be a list of IDs."]
}
```

**Special validation rules**:
- Application stage transitions must follow the defined workflow (e.g., cannot go from "inquiry" directly to "settlement")
- Borrower IDs must exist in the system when updating application borrowers
- Signature data must be a valid Base64 encoded string

#### Specific Endpoint Errors

**`/api/applications/validate-schema/`**
- **400 Bad Request**:
```json
{
  "valid": false,
  "error": "Invalid application_type"
}
```

**`/api/applications/{id}/borrowers/`**
- **400 Bad Request**:
```json
{
  "error": "Borrowers with IDs {1, 2} not found"
}
```

**`/api/applications/{id}/sign/`**
- **400 Bad Request**:
```json
{
  "error": "Failed to process signature"
}
```

### Borrower APIs

#### Common Error Codes

**401 Unauthorized**
- **When it happens**: Missing or invalid authentication token
- **Example response**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden**
- **When it happens**: User doesn't have permission to perform the action
- **Example response**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found**
- **When it happens**: Borrower ID doesn't exist or user doesn't have access to it
- **Example response**:
```json
{
  "detail": "Not found."
}
```

**400 Bad Request**
- **When it happens**: Invalid data in borrower creation or update
- **Example response**:
```json
{
  "email": ["Enter a valid email address."],
  "phone_number": ["Phone number must be in the format +1234567890."],
  "date_of_birth": ["Date has wrong format. Use YYYY-MM-DD format."]
}
```

**Special validation rules**:
- Email addresses must be unique across borrowers
- Phone numbers must follow the required format

### Guarantor APIs

#### Common Error Codes

**401 Unauthorized**
- **When it happens**: Missing or invalid authentication token
- **Example response**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden**
- **When it happens**: User doesn't have permission to perform the action
- **Example response**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found**
- **When it happens**: Guarantor ID doesn't exist or user doesn't have access to it
- **Example response**:
```json
{
  "detail": "Not found."
}
```

**400 Bad Request**
- **When it happens**: Invalid data in guarantor creation or update
- **Example response**:
```json
{
  "email": ["Enter a valid email address."],
  "relationship_to_borrower": ["This field is required."]
}
```

### Broker APIs

#### Common Error Codes

**401 Unauthorized**
- **When it happens**: Missing or invalid authentication token
- **Example response**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden**
- **When it happens**: User doesn't have permission to perform the action (e.g., non-admin trying to create a broker)
- **Example response**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found**
- **When it happens**: Broker, Branch, or BDM ID doesn't exist or user doesn't have access to it
- **Example response**:
```json
{
  "detail": "Not found."
}
```

**400 Bad Request**
- **When it happens**: Invalid data in broker, branch, or BDM creation or update
- **Example response**:
```json
{
  "email": ["Enter a valid email address."],
  "branch": ["This field is required."],
  "license_number": ["This field is required."]
}
```

### Document APIs

#### Common Error Codes

**401 Unauthorized**
- **When it happens**: Missing or invalid authentication token
- **Example response**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden**
- **When it happens**: User doesn't have permission to perform the action
- **Example response**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found**
- **When it happens**: Document, Note, Fee, or Repayment ID doesn't exist or user doesn't have access to it
- **Example response**:
```json
{
  "detail": "Not found."
}
```

**400 Bad Request**
- **When it happens**: Invalid data in document, note, fee, or repayment creation or update
- **Example response**:
```json
{
  "file": ["No file was submitted."],
  "title": ["This field is required."],
  "document_type": ["Invalid document type."]
}
```

#### Specific Endpoint Errors

**`/api/documents/documents/{id}/download/`**
- **404 Not Found**:
```json
{
  "error": "File not found"
}
```

**`/api/documents/documents/{id}/create-version/`**
- **400 Bad Request**:
```json
{
  "error": "No file provided"
}
```

**`/api/documents/fees/{id}/mark-paid/`**
- **404 Not Found**:
```json
{
  "error": "Fee not found"
}
```

**`/api/documents/repayments/{id}/mark-paid/`**
- **404 Not Found**:
```json
{
  "error": "Repayment not found"
}
```

### Report APIs

#### Common Error Codes

**401 Unauthorized**
- **When it happens**: Missing or invalid authentication token
- **Example response**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**400 Bad Request**
- **When it happens**: Invalid query parameters
- **Example response**:
```json
{
  "error": "Invalid date format. Use YYYY-MM-DD format."
}
```

**Special validation rules**:
- Date parameters must be in YYYY-MM-DD format
- If both start_date and end_date are provided, start_date must be before end_date
### Application Volume Report
- **API URL**: `/api/reports/application-volume/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**:
  - `total_applications` (integer): Total number of applications
  - `total_loan_amount` (decimal): Total loan amount
  - `average_loan_amount` (decimal): Average loan amount
  - `stage_breakdown` (object): Applications grouped by stage
  - `time_breakdown` (array): Applications grouped by time period
  - `bd_breakdown` (array): Applications grouped by BDM
  - `type_breakdown` (object): Applications grouped by type
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: Yes
  - `start_date`: Filter by start date (YYYY-MM-DD format)
  - `end_date`: Filter by end date (YYYY-MM-DD format)
  - `broker_id`: Filter by broker ID
  - `branch_id`: Filter by branch ID
  - `time_grouping`: Group by time period (day, week, month)

### Application Status Report
- **API URL**: `/api/reports/application-status/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**:
  - `total_active` (integer): Total number of active applications
  - `total_settled` (integer): Total number of settled applications
  - `total_declined` (integer): Total number of declined applications
  - `total_withdrawn` (integer): Total number of withdrawn applications
  - `active_by_stage` (object): Active applications grouped by stage
  - `avg_time_in_stage` (object): Average time spent in each stage (days)
  - `inquiry_to_approval_rate` (float): Conversion rate from inquiry to approval (%)
  - `approval_to_settlement_rate` (float): Conversion rate from approval to settlement (%)
  - `overall_success_rate` (float): Overall success rate (%)
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: Yes
  - `start_date`: Filter by start date (YYYY-MM-DD format)
  - `end_date`: Filter by end date (YYYY-MM-DD format)
### Repayment Compliance Report
- **API URL**: `/api/reports/repayment-compliance/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**:
  - `total_repayments` (integer): Total number of repayments
  - `paid_on_time` (integer): Number of repayments paid on time
  - `paid_late` (integer): Number of repayments paid late
  - `missed` (integer): Number of missed repayments
  - `compliance_rate` (float): Compliance rate (%)
  - `average_days_late` (float): Average number of days late
  - `total_amount_due` (decimal): Total amount due
  - `total_amount_paid` (decimal): Total amount paid
  - `payment_rate` (float): Payment rate (%)
  - `monthly_breakdown` (array): Monthly breakdown of repayment compliance
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: Yes
  - `start_date`: Filter by start date (YYYY-MM-DD format)
  - `end_date`: Filter by end date (YYYY-MM-DD format)
  - `application_id`: Filter by application ID
### Broker Performance Report
- **API URL**: `/api/reports/broker-performance/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**:
  - `brokers` (array): List of brokers
  - `applications_by_broker` (object): Applications grouped by broker
  - `loan_amount_by_broker` (object): Loan amounts grouped by broker
  - `success_rate_by_broker` (object): Success rates grouped by broker
  - `avg_processing_time_by_broker` (object): Average processing times grouped by broker
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: Yes
  - `start_date`: Filter by start date (YYYY-MM-DD format)
  - `end_date`: Filter by end date (YYYY-MM-DD format)
  - `branch_id`: Filter by branch ID
### Loan Portfolio Report
- **API URL**: `/api/reports/loan-portfolio/`
- **HTTP Method**: `GET`
- **Required Input Fields**: None
- **Response Fields**:
  - `total_active_loans` (integer): Total number of active loans
  - `total_loan_amount` (decimal): Total loan amount
  - `avg_interest_rate` (float): Average interest rate
  - `avg_loan_term` (float): Average loan term (months)
  - `loans_by_type` (object): Loans grouped by type
  - `loans_by_purpose` (object): Loans grouped by purpose
  - `risk_distribution` (object): Risk distribution of loans
- **Status Codes**: `200`, `401`
- **Authentication Required?**: Yes
- **Pagination?**: No
- **Search/Filter Support?**: Yes
  - `start_date`: Filter by start date (YYYY-MM-DD format)
  - `end_date`: Filter by end date (YYYY-MM-DD format)
