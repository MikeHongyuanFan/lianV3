/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Serializer for repayments
 */
export type Repayment = {
    readonly id: number;
    readonly created_by_name: string;
    readonly status: string;
    readonly invoice_url: string;
    amount: string;
    due_date?: string | null;
    paid_date?: string | null;
    invoice?: string | null;
    readonly created_at: string;
    readonly updated_at: string;
    readonly reminder_sent: boolean;
    readonly overdue_3_day_sent: boolean;
    readonly overdue_7_day_sent: boolean;
    readonly overdue_10_day_sent: boolean;
    application: number;
    readonly created_by: number | null;
};

