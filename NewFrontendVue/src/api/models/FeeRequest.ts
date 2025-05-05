/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FeeTypeEnum } from './FeeTypeEnum';
/**
 * Serializer for fees
 */
export type FeeRequest = {
    fee_type: FeeTypeEnum;
    description?: string | null;
    amount: string;
    due_date?: string | null;
    paid_date?: string | null;
    invoice?: Blob | null;
    application: number;
};

