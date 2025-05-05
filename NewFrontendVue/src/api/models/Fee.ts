/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FeeTypeEnum } from './FeeTypeEnum';
/**
 * Serializer for fees
 */
export type Fee = {
    readonly id: number;
    readonly fee_type_display: string;
    readonly created_by_name: string;
    readonly status: string;
    readonly invoice_url: string;
    fee_type: FeeTypeEnum;
    description?: string | null;
    amount: string;
    due_date?: string | null;
    paid_date?: string | null;
    invoice?: string | null;
    readonly created_at: string;
    readonly updated_at: string;
    application: number;
    readonly created_by: number | null;
};

