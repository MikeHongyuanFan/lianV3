/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Serializer for NotificationPreference model
 */
export type NotificationPreference = {
    readonly id: number;
    application_status_in_app?: boolean;
    repayment_upcoming_in_app?: boolean;
    repayment_overdue_in_app?: boolean;
    note_reminder_in_app?: boolean;
    document_uploaded_in_app?: boolean;
    signature_required_in_app?: boolean;
    system_in_app?: boolean;
    application_status_email?: boolean;
    repayment_upcoming_email?: boolean;
    repayment_overdue_email?: boolean;
    note_reminder_email?: boolean;
    document_uploaded_email?: boolean;
    signature_required_email?: boolean;
    system_email?: boolean;
    daily_digest?: boolean;
    weekly_digest?: boolean;
};

