/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AddressRequest } from './AddressRequest';
import type { DirectorRequest } from './DirectorRequest';
import type { FinancialInfoRequest } from './FinancialInfoRequest';
export type CompanyBorrowerRequest = {
    company_name?: string | null;
    company_abn?: string | null;
    company_acn?: string | null;
    registered_address: AddressRequest;
    directors: Array<DirectorRequest>;
    financial_info: FinancialInfoRequest;
};

