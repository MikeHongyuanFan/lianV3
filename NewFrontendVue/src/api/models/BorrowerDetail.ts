/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BlankEnum } from './BlankEnum';
import type { EmploymentTypeEnum } from './EmploymentTypeEnum';
import type { MaritalStatusEnum } from './MaritalStatusEnum';
import type { NullEnum } from './NullEnum';
import type { ResidencyStatusEnum } from './ResidencyStatusEnum';
import type { User } from './User';
/**
 * Serializer for detailed borrower information
 */
export type BorrowerDetail = {
    readonly id: number;
    readonly created_by: User;
    first_name?: string | null;
    last_name?: string | null;
    date_of_birth?: string | null;
    email?: string | null;
    phone?: string | null;
    residential_address?: string | null;
    mailing_address?: string | null;
    /**
     * Tax File Number or equivalent
     */
    tax_id?: string | null;
    marital_status?: (MaritalStatusEnum | BlankEnum | NullEnum) | null;
    residency_status?: (ResidencyStatusEnum | BlankEnum | NullEnum) | null;
    employment_type?: (EmploymentTypeEnum | BlankEnum | NullEnum) | null;
    employer_name?: string | null;
    employer_address?: string | null;
    job_title?: string | null;
    /**
     * Duration in months
     */
    employment_duration?: number | null;
    annual_income?: string | null;
    other_income?: string | null;
    monthly_expenses?: string | null;
    bank_name?: string | null;
    bank_account_name?: string | null;
    bank_account_number?: string | null;
    bank_bsb?: string | null;
    referral_source?: string | null;
    tags?: string | null;
    notes_text?: string | null;
    is_company?: boolean;
    company_name?: string | null;
    company_abn?: string | null;
    company_acn?: string | null;
    company_address?: string | null;
    readonly created_at: string;
    readonly updated_at: string;
    user?: number | null;
};

