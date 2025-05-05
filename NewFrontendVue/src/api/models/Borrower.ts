/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BlankEnum } from './BlankEnum';
import type { MaritalStatusEnum } from './MaritalStatusEnum';
import type { NullEnum } from './NullEnum';
import type { ResidencyStatusEnum } from './ResidencyStatusEnum';
export type Borrower = {
    readonly id: number;
    first_name?: string | null;
    last_name?: string | null;
    email?: string | null;
    phone?: string | null;
    date_of_birth?: string | null;
    readonly address: string;
    readonly employment_info: string;
    /**
     * Tax File Number or equivalent
     */
    tax_id?: string | null;
    marital_status?: (MaritalStatusEnum | BlankEnum | NullEnum) | null;
    residency_status?: (ResidencyStatusEnum | BlankEnum | NullEnum) | null;
    referral_source?: string | null;
    tags?: string | null;
};

