
# CRM Loan Management System API Documentation

## Overview

This document provides a comprehensive overview of all API services in the CRM Loan Management System, including their references, functions, and 
relationships. The system is built with Django and Django REST Framework on the backend, with Vue 3 and Pinia on the frontend.

## Authentication Services

### JWT Authentication API

Reference: /api/auth/

Functions:
• POST /api/auth/token/ - Obtain JWT token pair (access and refresh tokens)
• POST /api/auth/token/refresh/ - Refresh access token
• POST /api/auth/token/verify/ - Verify token validity

Relationships:
• Used by all frontend services for authentication
• Required for accessing protected API endpoints
• Integrated with user roles and permissions system

## User Management Services

### User API

Reference: /api/users/

Functions:
• GET /api/users/ - List all users (admin only)
• POST /api/users/ - Create new user
• GET /api/users/{id}/ - Retrieve user details
• PUT /api/users/{id}/ - Update user details
• DELETE /api/users/{id}/ - Delete user (admin only)
• GET /api/users/me/ - Get current user profile

Relationships:
• Connected to Broker, BDM, and Borrower models through one-to-one relationships
• Used by authentication services for user validation
• Referenced by notification services for user targeting

### Notification API

Reference: /api/notifications/

Functions:
• GET /api/notifications/ - List notifications for current user
• GET /api/notifications/{id}/ - Get notification details
• PUT /api/notifications/{id}/read/ - Mark notification as read
• PUT /api/notifications/read-all/ - Mark all notifications as read
• GET /api/notifications/unread-count/ - Get count of unread notifications

Relationships:
• Connected to User model (notifications belong to users)
• Used by WebSocket services for real-time notifications
• Referenced by application status changes, repayment reminders, and document uploads

### Notification Preferences API

Reference: /api/notification-preferences/

Functions:
• GET /api/notification-preferences/ - Get current user's notification preferences
• PUT /api/notification-preferences/ - Update notification preferences

Relationships:
• Connected to User model (one-to-one)
• Used by notification service to determine delivery methods
• Controls email and in-app notification behavior

## Application Management Services

### Application API

Reference: /api/applications/

Functions:
• GET /api/applications/ - List applications (filtered by user role)
• POST /api/applications/ - Create new application
• GET /api/applications/{id}/ - Get application details
• PUT /api/applications/{id}/ - Update application
• DELETE /api/applications/{id}/ - Delete application
• PUT /api/applications/{id}/stage/ - Update application stage
• POST /api/applications/{id}/sign/ - Process signature for application
• GET /api/applications/stats/ - Get application statistics

Relationships:
• Connected to Borrower models (many-to-many)
• Connected to Broker model (foreign key)
• Connected to BDM model (foreign key)
• Referenced by Documents, Repayments, Notes, and Fees
• Triggers notifications on status changes

### Application Search API

Reference: /api/applications/search/

Functions:
• GET /api/applications/search/ - Search applications with filters

Relationships:
• Uses Application model
• Provides advanced filtering capabilities for the frontend

## Borrower Management Services

### Borrower API

Reference: /api/borrowers/

Functions:
• GET /api/borrowers/ - List borrowers
• POST /api/borrowers/ - Create new borrower
• GET /api/borrowers/{id}/ - Get borrower details
• PUT /api/borrowers/{id}/ - Update borrower
• DELETE /api/borrowers/{id}/ - Delete borrower
• GET /api/borrowers/{id}/financial-summary/ - Get borrower financial summary

Relationships:
• Connected to User model (optional one-to-one)
• Connected to Application models (many-to-many)
• Referenced by Assets and Liabilities
• Referenced by Guarantors

### Asset API

Reference: /api/assets/

Functions:
• GET /api/assets/ - List assets for a borrower
• POST /api/assets/ - Create new asset
• GET /api/assets/{id}/ - Get asset details
• PUT /api/assets/{id}/ - Update asset
• DELETE /api/assets/{id}/ - Delete asset

Relationships:
• Connected to Borrower model (foreign key)
• Used in financial summary calculations

### Liability API

Reference: /api/liabilities/

Functions:
• GET /api/liabilities/ - List liabilities for a borrower
• POST /api/liabilities/ - Create new liability
• GET /api/liabilities/{id}/ - Get liability details
• PUT /api/liabilities/{id}/ - Update liability
• DELETE /api/liabilities/{id}/ - Delete liability

Relationships:
• Connected to Borrower model (foreign key)
• Used in financial summary calculations

### Guarantor API

Reference: /api/guarantors/

Functions:
• GET /api/guarantors/ - List guarantors for an application
• POST /api/guarantors/ - Create new guarantor
• GET /api/guarantors/{id}/ - Get guarantor details
• PUT /api/guarantors/{id}/ - Update guarantor
• DELETE /api/guarantors/{id}/ - Delete guarantor

Relationships:
• Connected to Borrower model (foreign key)
• Connected to Application model (foreign key)

## Broker Management Services

### Broker API

Reference: /api/brokers/

Functions:
• GET /api/brokers/ - List brokers
• POST /api/brokers/ - Create new broker
• GET /api/brokers/{id}/ - Get broker details
• PUT /api/brokers/{id}/ - Update broker
• DELETE /api/brokers/{id}/ - Delete broker
• GET /api/brokers/{id}/applications/ - Get broker's applications
• GET /api/brokers/{id}/commissions/ - Get broker's commissions

Relationships:
• Connected to User model (one-to-one)
• Connected to Branch model (foreign key)
• Referenced by Application model
• Referenced by Commission model

### Branch API

Reference: /api/branches/

Functions:
• GET /api/branches/ - List branches
• POST /api/branches/ - Create new branch
• GET /api/branches/{id}/ - Get branch details
• PUT /api/branches/{id}/ - Update branch
• DELETE /api/branches/{id}/ - Delete branch
• GET /api/branches/{id}/brokers/ - Get brokers in branch
• GET /api/branches/{id}/bdms/ - Get BDMs in branch

Relationships:
• Referenced by Broker model
• Referenced by BDM model

### BDM (Business Development Manager) API

Reference: /api/bdms/

Functions:
• GET /api/bdms/ - List BDMs
• POST /api/bdms/ - Create new BDM
• GET /api/bdms/{id}/ - Get BDM details
• PUT /api/bdms/{id}/ - Update BDM
• DELETE /api/bdms/{id}/ - Delete BDM
• GET /api/bdms/{id}/applications/ - Get BDM's applications

Relationships:
• Connected to User model (one-to-one)
• Connected to Branch model (foreign key)
• Referenced by Application model

## Document Management Services

### Document API

Reference: /api/documents/

Functions:
• GET /api/documents/ - List documents for an application
• POST /api/documents/ - Upload new document
• GET /api/documents/{id}/ - Get document details
• PUT /api/documents/{id}/ - Update document metadata
• DELETE /api/documents/{id}/ - Delete document
• GET /api/documents/{id}/download/ - Download document
• POST /api/documents/generate/{template}/ - Generate document from template

Relationships:
• Connected to Application model (foreign key)
• Triggers notifications on document upload
• Referenced by signature processes

### Note API

Reference: /api/notes/

Functions:
• GET /api/notes/ - List notes for an application
• POST /api/notes/ - Create new note
• GET /api/notes/{id}/ - Get note details
• PUT /api/notes/{id}/ - Update note
• DELETE /api/notes/{id}/ - Delete note
• GET /api/notes/reminders/ - Get notes with upcoming reminders

Relationships:
• Connected to Application model (foreign key)
• Triggers reminder notifications based on remind_date

## Financial Services

### Fee API

Reference: /api/fees/

Functions:
• GET /api/fees/ - List fees for an application
• POST /api/fees/ - Create new fee
• GET /api/fees/{id}/ - Get fee details
• PUT /api/fees/{id}/ - Update fee
• DELETE /api/fees/{id}/ - Delete fee
• POST /api/fees/standard/ - Create standard fees for an application

Relationships:
• Connected to Application model (foreign key)
• Referenced in financial calculations

### Repayment API

Reference: /api/repayments/

Functions:
• GET /api/repayments/ - List repayments for an application
• POST /api/repayments/ - Create new repayment
• GET /api/repayments/{id}/ - Get repayment details
• PUT /api/repayments/{id}/ - Update repayment
• DELETE /api/repayments/{id}/ - Delete repayment
• POST /api/repayments/schedule/ - Generate repayment schedule
• GET /api/repayments/upcoming/ - Get upcoming repayments
• GET /api/repayments/overdue/ - Get overdue repayments

Relationships:
• Connected to Application model (foreign key)
• Triggers notifications for upcoming and overdue repayments

### Commission API

Reference: /api/commissions/

Functions:
• GET /api/commissions/ - List commissions
• POST /api/commissions/ - Create new commission
• GET /api/commissions/{id}/ - Get commission details
• PUT /api/commissions/{id}/ - Update commission
• DELETE /api/commissions/{id}/ - Delete commission
• POST /api/commissions/calculate/ - Calculate commission for an application

Relationships:
• Connected to Application model (foreign key)
• Connected to Broker model (foreign key)
• Referenced in financial reports

## Real-time Services

### WebSocket Notification Service

Reference: /ws/notifications/

Functions:
• Real-time notification delivery
• Unread notification count updates
• Connection authentication via JWT

Relationships:
• Connected to User model for authentication
• Connected to Notification model for data
• Used by frontend notification center

## Reporting Services

### Report API

Reference: /api/reports/

Functions:
• GET /api/reports/applications/ - Get application reports
• GET /api/reports/repayments/ - Get repayment compliance reports
• GET /api/reports/brokers/ - Get broker performance reports
• GET /api/reports/revenue/ - Get revenue reports

Relationships:
• Uses data from Applications, Repayments, Brokers, and Fees
• Provides aggregated data for dashboard visualizations

## API Relationships Diagram

User ─┬─ Broker ─┬─ Application ─┬─ Document
      │          │               ├─ Note
      │          │               ├─ Fee
      │          │               ├─ Repayment
      │          │               └─ Commission
      │          │
      │          └─ Branch
      │
      ├─ BDM ────┬─ Application
      │          │
      │          └─ Branch
      │
      ├─ Borrower ┬─ Application
      │           ├─ Asset
      │           ├─ Liability
      │           └─ Guarantor
      │
      └─ Notification ─── NotificationPreference
                      │
                      └─── WebSocket Connection

