/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DocumentTypeEnum } from './DocumentTypeEnum';
/**
 * Serializer for documents
 */
export type Document = {
    readonly id: number;
    readonly document_type_display: string;
    readonly created_by_name: string;
    readonly file_url: string;
    title?: string | null;
    description?: string | null;
    document_type?: DocumentTypeEnum;
    file: string;
    readonly file_name: string | null;
    /**
     * File size in bytes
     */
    readonly file_size: number | null;
    /**
     * MIME type
     */
    readonly file_type: string | null;
    readonly version: number;
    readonly created_at: string;
    readonly updated_at: string;
    previous_version?: number | null;
    application?: number | null;
    borrower?: number | null;
    readonly created_by: number | null;
};

