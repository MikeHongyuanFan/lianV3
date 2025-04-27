"""
Extended application services for loan metrics, eligibility, and approvals.
"""
import math
from decimal import Decimal
from django.utils import timezone
from .models import Application
from documents.models import Document, Note
from users.models import Notification


def calculate_loan_metrics(application_id):
    """
    Calculate loan metrics for an application
    
    Args:
        application_id: ID of the application
        
    Returns:
        Dictionary with loan metrics or None if application not found
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return None
    
    # Extract loan details
    loan_amount = application.loan_amount or 0
    loan_term_years = (application.loan_term or 0) / 12  # Convert months to years
    annual_interest_rate = application.interest_rate or 0
    
    # Calculate monthly interest rate
    monthly_interest_rate = annual_interest_rate / 100 / 12
    
    # Calculate monthly repayment using the formula:
    # P = L[c(1 + c)^n]/[(1 + c)^n - 1]
    # where:
    # P = monthly payment
    # L = loan amount
    # c = monthly interest rate (annual rate / 12)
    # n = number of payments (loan term in years * 12)
    
    if monthly_interest_rate > 0 and loan_term_years > 0:
        n = float(loan_term_years * 12)
        monthly_interest_rate_float = float(monthly_interest_rate)
        loan_amount_float = float(loan_amount)
        monthly_repayment = loan_amount_float * (monthly_interest_rate_float * (1 + monthly_interest_rate_float) ** n) / ((1 + monthly_interest_rate_float) ** n - 1)
    else:
        # Simple division if no interest or term
        monthly_repayment = float(loan_amount) / (float(loan_term_years) * 12) if loan_term_years > 0 else 0
    
    # Calculate total repayment
    total_repayment = monthly_repayment * float(loan_term_years) * 12
    
    # Calculate total interest
    total_interest = total_repayment - float(loan_amount)
    
    # Calculate loan to value ratio
    security_value = application.security_value or 0
    ltv_ratio = (float(loan_amount) / float(security_value)) * 100 if security_value > 0 else 0
    
    return {
        'monthly_repayment': round(monthly_repayment, 2),
        'total_repayment': round(total_repayment, 2),
        'total_interest': round(total_interest, 2),
        'loan_to_value_ratio': round(ltv_ratio, 2),
        'interest_rate': annual_interest_rate,
        'loan_term_years': loan_term_years
    }


def validate_borrower_eligibility(application_id):
    """
    Validate borrower eligibility for a loan
    
    Args:
        application_id: ID of the application
        
    Returns:
        Dictionary with eligibility results
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return {
            'is_eligible': False,
            'debt_to_income_ratio': 0,
            'serviceability_ratio': 0,
            'reasons': ['Application not found']
        }
    
    # Get borrowers
    borrowers = application.borrowers.all()
    if not borrowers.exists():
        return {
            'is_eligible': False,
            'debt_to_income_ratio': 0,
            'serviceability_ratio': 0,
            'reasons': ['No borrowers associated with this application']
        }
    
    # Calculate combined income and expenses
    total_annual_income = sum(float(borrower.annual_income or 0) for borrower in borrowers)
    total_monthly_income = total_annual_income / 12
    total_monthly_expenses = sum(float(borrower.monthly_expenses or 0) for borrower in borrowers)
    
    # Calculate total monthly debt payments
    total_monthly_debt = 0
    for borrower in borrowers:
        for liability in borrower.liabilities.all():
            total_monthly_debt += float(liability.monthly_payment or 0)
    
    # Calculate debt to income ratio
    debt_to_income_ratio = total_monthly_debt / total_monthly_income if total_monthly_income > 0 else float('inf')
    
    # Calculate loan metrics to get estimated monthly repayment
    metrics = calculate_loan_metrics(application_id)
    estimated_monthly_repayment = metrics['monthly_repayment'] if metrics else 0
    
    # Calculate serviceability ratio
    disposable_income = total_monthly_income - total_monthly_expenses - total_monthly_debt
    serviceability_ratio = disposable_income / estimated_monthly_repayment if estimated_monthly_repayment > 0 else float('inf')
    
    # Determine eligibility based on ratios
    is_eligible = True
    reasons = []
    
    if debt_to_income_ratio > 0.43:  # Industry standard max DTI
        is_eligible = False
        reasons.append(f'Debt-to-income ratio too high: {debt_to_income_ratio:.2f}')
    
    if serviceability_ratio < 1.2:  # Minimum serviceability buffer
        is_eligible = False
        reasons.append(f'Insufficient income to service the loan: {serviceability_ratio:.2f}')
    
    if application.loan_amount > 0 and application.security_value > 0:
        ltv_ratio = (application.loan_amount / application.security_value) * 100
        if ltv_ratio > 80:  # Standard LTV threshold
            reasons.append(f'Loan-to-value ratio above 80%: {ltv_ratio:.2f}%')
    
    return {
        'is_eligible': is_eligible,
        'debt_to_income_ratio': round(debt_to_income_ratio, 2),
        'serviceability_ratio': round(serviceability_ratio, 2),
        'disposable_income': round(disposable_income, 2),
        'estimated_monthly_repayment': round(estimated_monthly_repayment, 2),
        'reasons': reasons
    }


def generate_application_documents(application_id, user):
    """
    Generate all required documents for an application
    
    Args:
        application_id: ID of the application
        user: User generating the documents
        
    Returns:
        List of generated Document objects
    """
    from documents.services_mock import generate_document_from_template
    
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return []
    
    documents = []
    
    # Generate application form
    application_form = generate_document_from_template(
        template_name='applications/application_form.html',
        context={'application': application},
        output_filename=f'Application_Form_{application.reference_number}',
        document_type='application_form',
        application=application,
        user=user
    )
    if application_form:
        documents.append(application_form)
    
    # Generate loan agreement
    loan_agreement = generate_document_from_template(
        template_name='applications/loan_agreement.html',
        context={'application': application},
        output_filename=f'Loan_Agreement_{application.reference_number}',
        document_type='loan_agreement',
        application=application,
        user=user
    )
    if loan_agreement:
        documents.append(loan_agreement)
    
    # Generate privacy consent
    privacy_consent = generate_document_from_template(
        template_name='applications/privacy_consent.html',
        context={'application': application},
        output_filename=f'Privacy_Consent_{application.reference_number}',
        document_type='privacy_consent',
        application=application,
        user=user
    )
    if privacy_consent:
        documents.append(privacy_consent)
    
    return documents


def send_application_notifications(application_id, notification_type, message, include_borrowers=True, include_broker=True, include_bd=True):
    """
    Send notifications to all relevant parties for an application
    
    Args:
        application_id: ID of the application
        notification_type: Type of notification
        message: Notification message
        include_borrowers: Whether to include borrowers
        include_broker: Whether to include broker
        include_bd: Whether to include BD
        
    Returns:
        List of created Notification objects
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return []
    
    notifications = []
    
    # Create notification for borrowers
    if include_borrowers:
        for borrower in application.borrowers.all():
            if borrower.user:
                notification = Notification.objects.create(
                    user=borrower.user,
                    title=f"Application {application.reference_number} Update",
                    message=message,
                    notification_type=notification_type,
                    related_object_id=application.id,
                    related_object_type='application'
                )
                notifications.append(notification)
                
                # Mock sending email notification
                send_email_notification(
                    recipient_email=borrower.email,
                    subject=f"Application {application.reference_number} Update",
                    message=message
                )
                
                # Mock sending websocket notification
                send_websocket_notification(
                    user_id=borrower.user.id,
                    notification=notification
                )
    
    # Create notification for broker
    if include_broker and application.broker and application.broker.user:
        notification = Notification.objects.create(
            user=application.broker.user,
            title=f"Application {application.reference_number} Update",
            message=message,
            notification_type=notification_type,
            related_object_id=application.id,
            related_object_type='application'
        )
        notifications.append(notification)
        
        # Mock sending email notification
        send_email_notification(
            recipient_email=application.broker.email,
            subject=f"Application {application.reference_number} Update",
            message=message
        )
        
        # Mock sending websocket notification
        send_websocket_notification(
            user_id=application.broker.user.id,
            notification=notification
        )
    
    # Create notification for BD
    if include_bd and application.bd and application.bd.user:
        notification = Notification.objects.create(
            user=application.bd.user,
            title=f"Application {application.reference_number} Update",
            message=message,
            notification_type=notification_type,
            related_object_id=application.id,
            related_object_type='application'
        )
        notifications.append(notification)
        
        # Mock sending email notification
        send_email_notification(
            recipient_email=application.bd.email,
            subject=f"Application {application.reference_number} Update",
            message=message
        )
        
        # Mock sending websocket notification
        send_websocket_notification(
            user_id=application.bd.user.id,
            notification=notification
        )
    
    return notifications


def process_application_approval(application_id, approval_data, user):
    """
    Process application approval
    
    Args:
        application_id: ID of the application
        approval_data: Dictionary with approval details
        user: User processing the approval
        
    Returns:
        Dictionary with results
    """
    from applications.services_impl import update_application_stage
    
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return {
            'success': False,
            'error': 'Application not found'
        }
    
    # Update application with approval data
    application.approved_amount = approval_data.get('approved_amount')
    application.approved_term = approval_data.get('approved_term')
    application.approved_rate = approval_data.get('approved_rate')
    application.approval_expiry = approval_data.get('approval_expiry')
    application.save()
    
    # Create note with approval conditions
    conditions = approval_data.get('approval_conditions', [])
    if conditions:
        conditions_text = "\n".join([f"- {condition}" for condition in conditions])
        Note.objects.create(
            application=application,
            title="Approval Conditions",
            content=f"The application has been approved with the following conditions:\n{conditions_text}",
            created_by=user
        )
    
    # Update application stage to approved
    updated_application = update_application_stage(application_id, 'approved', user)
    
    # Generate approval documents
    documents = generate_application_documents(application_id, user)
    
    # Send notifications
    notifications = send_application_notifications(
        application_id=application_id,
        notification_type='application_status',
        message=f"Application {application.reference_number} has been approved",
        include_borrowers=True,
        include_broker=True,
        include_bd=True
    )
    
    return {
        'success': True,
        'application': updated_application,
        'documents': documents,
        'notifications': notifications
    }


# Mock functions for notifications
def send_email_notification(recipient_email, subject, message):
    """Mock function to send email notifications"""
    # In a real implementation, this would send an actual email
    return True


def send_websocket_notification(user_id, notification):
    """Mock function to send websocket notifications"""
    # In a real implementation, this would send a websocket message
    return True
