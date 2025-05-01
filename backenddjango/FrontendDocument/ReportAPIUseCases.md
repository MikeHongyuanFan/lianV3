# Report API Use Cases

This document outlines the use cases for the Report APIs in the CRM Loan Management System.

> **Verification Status**: This documentation has been verified against the actual implementation as of 2023-07-10. All API endpoints, parameters, and response structures accurately reflect the implemented functionality.

## 1. Application Volume Report API

### API Details
- **Endpoint**: `/api/reports/application-volume/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 1.1 Retrieve Application Volume Report
- **Actor**: Authenticated user
- **Description**: User retrieves a report on application volumes, including totals, breakdowns by time period, stage, BD, and application type
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System calculates application volume metrics
  4. System returns the report data
- **Query Parameters**:
  - `start_date`: Filter applications created on or after this date (YYYY-MM-DD)
  - `end_date`: Filter applications created on or before this date (YYYY-MM-DD)
  - `bd_id`: Filter applications by Business Development Manager ID
  - `broker_id`: Filter applications by Broker ID
  - `time_grouping`: Group time breakdown by 'day', 'week', or 'month' (default: 'month')
- **Response**: 
  ```json
  {
    "total_applications": 125,
    "total_loan_amount": 25000000.00,
    "average_loan_amount": 200000.00,
    "stage_breakdown": {
      "inquiry": 20,
      "pre_approval": 35,
      "valuation": 15,
      "formal_approval": 25,
      "settlement": 20,
      "funded": 5,
      "declined": 3,
      "withdrawn": 2
    },
    "time_breakdown": [
      {
        "period": "2025-01",
        "count": 40,
        "total_amount": 8000000.00
      },
      {
        "period": "2025-02",
        "count": 45,
        "total_amount": 9000000.00
      },
      {
        "period": "2025-03",
        "count": 40,
        "total_amount": 8000000.00
      }
    ],
    "bd_breakdown": [
      {
        "bd_id": 1,
        "bd_name": "John Smith",
        "count": 50,
        "total_amount": 10000000.00
      },
      {
        "bd_id": 2,
        "bd_name": "Jane Doe",
        "count": 45,
        "total_amount": 9000000.00
      },
      {
        "bd_id": null,
        "bd_name": "No BD",
        "count": 30,
        "total_amount": 6000000.00
      }
    ],
    "type_breakdown": {
      "residential": 60,
      "commercial": 25,
      "construction": 15,
      "refinance": 20,
      "investment": 5
    }
  }
  ```
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized

#### 1.2 Retrieve Filtered Application Volume Report
- **Actor**: Authenticated user
- **Description**: User retrieves a filtered report on application volumes for a specific time period, BD, or broker
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System validates authentication token
  3. System applies filters to the data
  4. System calculates application volume metrics for the filtered data
  5. System returns the filtered report data
- **Query Parameters**:
  - `start_date`: "2025-01-01" (Filter applications created on or after January 1, 2025)
  - `end_date`: "2025-03-31" (Filter applications created on or before March 31, 2025)
  - `bd_id`: 1 (Filter applications by BD with ID 1)
  - `time_grouping`: "week" (Group time breakdown by week)
- **Response**: Application volume report data filtered according to the parameters
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized

## 2. Application Status Report API

### API Details
- **Endpoint**: `/api/reports/application-status/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 2.1 Retrieve Application Status Report
- **Actor**: Authenticated user
- **Description**: User retrieves a report on application statuses, including active, settled, declined, and withdrawn applications, as well as conversion rates. Note that the avg_time_in_stage field currently returns placeholder values (0) as the actual implementation would require tracking stage changes over time.
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System calculates application status metrics
  4. System returns the report data
- **Query Parameters**:
  - `start_date`: Filter applications created on or after this date (YYYY-MM-DD)
  - `end_date`: Filter applications created on or before this date (YYYY-MM-DD)
- **Response**: 
  ```json
  {
    "total_active": 95,
    "total_settled": 25,
    "total_declined": 3,
    "total_withdrawn": 2,
    "active_by_stage": {
      "inquiry": 20,
      "pre_approval": 35,
      "valuation": 15,
      "formal_approval": 25
    },
    "avg_time_in_stage": {
      "inquiry": 0,
      "pre_approval": 0,
      "valuation": 0,
      "formal_approval": 0
    },
    "inquiry_to_approval_rate": 75.20,
    "approval_to_settlement_rate": 83.33,
    "overall_success_rate": 62.67
  }
  ```
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized

#### 2.2 Retrieve Filtered Application Status Report
- **Actor**: Authenticated user
- **Description**: User retrieves a filtered report on application statuses for a specific time period. Note that the avg_time_in_stage field currently returns placeholder values (0) as the actual implementation would require tracking stage changes over time.
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System validates authentication token
  3. System applies filters to the data
  4. System calculates application status metrics for the filtered data
  5. System returns the filtered report data
- **Query Parameters**:
  - `start_date`: "2025-01-01" (Filter applications created on or after January 1, 2025)
  - `end_date`: "2025-03-31" (Filter applications created on or before March 31, 2025)
- **Response**: Application status report data filtered according to the parameters
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized

## 3. Repayment Compliance Report API

### API Details
- **Endpoint**: `/api/reports/repayment-compliance/`
- **HTTP Method**: `GET`
- **Authentication Required**: Yes

### Use Cases for GET Method

#### 3.1 Retrieve Repayment Compliance Report
- **Actor**: Authenticated user
- **Description**: User retrieves a report on repayment compliance, including on-time payments, late payments, missed payments, and compliance rates
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request
  2. System validates authentication token
  3. System calculates repayment compliance metrics
  4. System returns the report data
- **Query Parameters**:
  - `start_date`: Filter repayments due on or after this date (YYYY-MM-DD)
  - `end_date`: Filter repayments due on or before this date (YYYY-MM-DD)
  - `application_id`: Filter repayments by application ID
- **Response**: 
  ```json
  {
    "total_repayments": 250,
    "paid_on_time": 200,
    "paid_late": 30,
    "missed": 20,
    "compliance_rate": 80.00,
    "average_days_late": 5.25,
    "total_amount_due": 500000.00,
    "total_amount_paid": 460000.00,
    "payment_rate": 92.00,
    "monthly_breakdown": [
      {
        "month": "2025-01",
        "total_repayments": 80,
        "paid_on_time": 70,
        "paid_late": 5,
        "missed": 5,
        "compliance_rate": 87.50,
        "amount_due": 160000.00,
        "amount_paid": 150000.00,
        "payment_rate": 93.75
      },
      {
        "month": "2025-02",
        "total_repayments": 85,
        "paid_on_time": 65,
        "paid_late": 15,
        "missed": 5,
        "compliance_rate": 76.47,
        "amount_due": 170000.00,
        "amount_paid": 160000.00,
        "payment_rate": 94.12
      },
      {
        "month": "2025-03",
        "total_repayments": 85,
        "paid_on_time": 65,
        "paid_late": 10,
        "missed": 10,
        "compliance_rate": 76.47,
        "amount_due": 170000.00,
        "amount_paid": 150000.00,
        "payment_rate": 88.24
      }
    ]
  }
  ```
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized

#### 3.2 Retrieve Filtered Repayment Compliance Report
- **Actor**: Authenticated user
- **Description**: User retrieves a filtered report on repayment compliance for a specific time period or application
- **Preconditions**: User is authenticated with valid JWT token
- **Steps**:
  1. User sends authenticated GET request with filter parameters
  2. System validates authentication token
  3. System applies filters to the data
  4. System calculates repayment compliance metrics for the filtered data
  5. System returns the filtered report data
- **Query Parameters**:
  - `start_date`: "2025-01-01" (Filter repayments due on or after January 1, 2025)
  - `end_date`: "2025-03-31" (Filter repayments due on or before March 31, 2025)
  - `application_id`: 1 (Filter repayments for application with ID 1)
- **Response**: Repayment compliance report data filtered according to the parameters
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized
