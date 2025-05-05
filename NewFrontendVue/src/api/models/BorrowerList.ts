/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Serializer for listing borrowers with minimal information
 */
export type BorrowerList = {
    readonly id: number;
    first_name?: string | null;
    last_name?: string | null;
    email?: string | null;
    phone?: string | null;
    readonly created_at: string;
    readonly application_count: string;
};

