/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Address } from './Address';
import type { Director } from './Director';
import type { FinancialInfo } from './FinancialInfo';
export type CompanyBorrower = {
    readonly id: number;
    company_name?: string | null;
    company_abn?: string | null;
    company_acn?: string | null;
    registered_address: Address;
    directors: Array<Director>;
    financial_info: FinancialInfo;
};

