/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DocumentTypeEnum } from './DocumentTypeEnum';
/**
 * Serializer for documents
 */
export type PatchedDocumentRequest = {
    title?: string | null;
    description?: string | null;
    document_type?: DocumentTypeEnum;
    file?: Blob;
    previous_version?: number | null;
    application?: number | null;
    borrower?: number | null;
};

