/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Serializer for repayments
 */
export type PatchedRepaymentRequest = {
    amount?: string;
    due_date?: string | null;
    paid_date?: string | null;
    invoice?: Blob | null;
    application?: number;
};

