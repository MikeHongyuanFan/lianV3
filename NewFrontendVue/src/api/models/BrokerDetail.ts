/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Branch } from './Branch';
import type { User } from './User';
/**
 * Serializer for detailed broker information
 */
export type BrokerDetail = {
    readonly id: number;
    readonly branch: Branch;
    readonly created_by: User;
    name: string;
    company?: string | null;
    email?: string | null;
    phone?: string | null;
    address?: string | null;
    commission_bank_name?: string | null;
    commission_account_name?: string | null;
    commission_account_number?: string | null;
    commission_bsb?: string | null;
    readonly created_at: string;
    readonly updated_at: string;
    user?: number | null;
    bdms?: Array<number>;
};

