/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Serializer for listing brokers with minimal information
 */
export type BrokerList = {
    readonly id: number;
    name: string;
    company?: string | null;
    email?: string | null;
    phone?: string | null;
    readonly branch_name: string;
    readonly application_count: string;
};

