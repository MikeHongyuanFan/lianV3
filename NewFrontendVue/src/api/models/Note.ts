/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Serializer for notes
 */
export type Note = {
    readonly id: number;
    readonly created_by_name: string;
    readonly assigned_to_name: string;
    title?: string | null;
    content?: string | null;
    remind_date?: string | null;
    readonly created_at: string;
    readonly updated_at: string;
    application?: number | null;
    borrower?: number | null;
    assigned_to?: number | null;
    readonly created_by: number | null;
};

