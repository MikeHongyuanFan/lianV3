/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GuarantorTypeEnum } from './GuarantorTypeEnum';
export type Guarantor = {
    readonly id: number;
    first_name?: string | null;
    last_name?: string | null;
    email?: string | null;
    phone?: string | null;
    date_of_birth?: string | null;
    readonly address: string;
    guarantor_type?: GuarantorTypeEnum;
    borrower?: number | null;
    application?: number | null;
};

