/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApplicationTypeEnum } from './ApplicationTypeEnum';
import type { BlankEnum } from './BlankEnum';
import type { NullEnum } from './NullEnum';
import type { RepaymentFrequencyEnum } from './RepaymentFrequencyEnum';
import type { StageEnum } from './StageEnum';
export type PatchedApplicationDetailRequest = {
    reference_number?: string;
    loan_amount?: string | null;
    /**
     * Loan term in months
     */
    loan_term?: number | null;
    interest_rate?: string | null;
    purpose?: string | null;
    repayment_frequency?: RepaymentFrequencyEnum;
    application_type?: (ApplicationTypeEnum | BlankEnum | NullEnum) | null;
    product_id?: string | null;
    estimated_settlement_date?: string | null;
    stage?: StageEnum;
    security_address?: string | null;
    security_type?: string | null;
    security_value?: string | null;
    valuer_company_name?: string | null;
    valuer_contact_name?: string | null;
    valuer_phone?: string | null;
    valuer_email?: string | null;
    valuation_date?: string | null;
    valuation_amount?: string | null;
    qs_company_name?: string | null;
    qs_contact_name?: string | null;
    qs_phone?: string | null;
    qs_email?: string | null;
    qs_report_date?: string | null;
    signed_by?: string | null;
    signature_date?: string | null;
    uploaded_pdf_path?: Blob | null;
    /**
     * Stores the current funding calculation result
     */
    funding_result?: any;
};

