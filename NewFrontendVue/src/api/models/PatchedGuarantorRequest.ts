/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GuarantorTypeEnum } from './GuarantorTypeEnum';
/**
 * Serializer for guarantor information
 */
export type PatchedGuarantorRequest = {
    guarantor_type?: GuarantorTypeEnum;
    first_name?: string | null;
    last_name?: string | null;
    date_of_birth?: string | null;
    email?: string | null;
    phone?: string | null;
    address?: string | null;
    company_name?: string | null;
    company_abn?: string | null;
    company_acn?: string | null;
    borrower?: number | null;
    application?: number | null;
};

