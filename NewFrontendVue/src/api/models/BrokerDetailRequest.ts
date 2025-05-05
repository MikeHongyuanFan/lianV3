/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Serializer for detailed broker information
 */
export type BrokerDetailRequest = {
    branch_id?: number | null;
    name: string;
    company?: string | null;
    email?: string | null;
    phone?: string | null;
    address?: string | null;
    commission_bank_name?: string | null;
    commission_account_name?: string | null;
    commission_account_number?: string | null;
    commission_bsb?: string | null;
    user?: number | null;
    bdms?: Array<number>;
};

