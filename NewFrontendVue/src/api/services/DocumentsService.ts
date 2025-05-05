/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Document } from '../models/Document';
import type { DocumentRequest } from '../models/DocumentRequest';
import type { Fee } from '../models/Fee';
import type { FeeRequest } from '../models/FeeRequest';
import type { Note } from '../models/Note';
import type { NoteRequest } from '../models/NoteRequest';
import type { PaginatedDocumentList } from '../models/PaginatedDocumentList';
import type { PaginatedFeeList } from '../models/PaginatedFeeList';
import type { PaginatedNoteList } from '../models/PaginatedNoteList';
import type { PaginatedRepaymentList } from '../models/PaginatedRepaymentList';
import type { PatchedDocumentRequest } from '../models/PatchedDocumentRequest';
import type { PatchedFeeRequest } from '../models/PatchedFeeRequest';
import type { PatchedNoteRequest } from '../models/PatchedNoteRequest';
import type { PatchedRepaymentRequest } from '../models/PatchedRepaymentRequest';
import type { Repayment } from '../models/Repayment';
import type { RepaymentRequest } from '../models/RepaymentRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DocumentsService {
    /**
     * Get ledger entries for an application
     * @param applicationId
     * @returns any No response body
     * @throws ApiError
     */
    public static documentsApplicationsLedgerRetrieve(
        applicationId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/applications/{application_id}/ledger/',
            path: {
                'application_id': applicationId,
            },
        });
    }
    /**
     * API endpoint for managing documents
     * @param application
     * @param borrower
     * @param createdAfter
     * @param createdBefore
     * @param documentType * `application_form` - Application Form
     * * `indicative_letter` - Indicative Letter
     * * `formal_approval` - Formal Approval
     * * `valuation_report` - Valuation Report
     * * `qs_report` - Quantity Surveyor Report
     * * `id_verification` - ID Verification
     * * `bank_statement` - Bank Statement
     * * `payslip` - Payslip
     * * `tax_return` - Tax Return
     * * `contract` - Contract
     * * `other` - Other
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedDocumentList
     * @throws ApiError
     */
    public static documentsDocumentsList(
        application?: number,
        borrower?: number,
        createdAfter?: string,
        createdBefore?: string,
        documentType?: 'application_form' | 'bank_statement' | 'contract' | 'formal_approval' | 'id_verification' | 'indicative_letter' | 'other' | 'payslip' | 'qs_report' | 'tax_return' | 'valuation_report',
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedDocumentList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/documents/',
            query: {
                'application': application,
                'borrower': borrower,
                'created_after': createdAfter,
                'created_before': createdBefore,
                'document_type': documentType,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * API endpoint for managing documents
     * @param formData
     * @returns Document
     * @throws ApiError
     */
    public static documentsDocumentsCreate(
        formData: DocumentRequest,
    ): CancelablePromise<Document> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/documents/documents/',
            formData: formData,
            mediaType: 'multipart/form-data',
        });
    }
    /**
     * API endpoint for managing documents
     * @param id A unique integer value identifying this document.
     * @returns Document
     * @throws ApiError
     */
    public static documentsDocumentsRetrieve(
        id: number,
    ): CancelablePromise<Document> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/documents/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Update a document
     * @param id A unique integer value identifying this document.
     * @param formData
     * @returns Document
     * @throws ApiError
     */
    public static documentsDocumentsUpdate(
        id: number,
        formData: DocumentRequest,
    ): CancelablePromise<Document> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/documents/documents/{id}/',
            path: {
                'id': id,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
        });
    }
    /**
     * API endpoint for managing documents
     * @param id A unique integer value identifying this document.
     * @param formData
     * @returns Document
     * @throws ApiError
     */
    public static documentsDocumentsPartialUpdate(
        id: number,
        formData?: PatchedDocumentRequest,
    ): CancelablePromise<Document> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/documents/documents/{id}/',
            path: {
                'id': id,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
        });
    }
    /**
     * API endpoint for managing documents
     * @param id A unique integer value identifying this document.
     * @returns void
     * @throws ApiError
     */
    public static documentsDocumentsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/documents/documents/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Create a new version of a document
     * @param id
     * @returns any No response body
     * @throws ApiError
     */
    public static documentsDocumentsCreateVersionCreate(
        id: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/documents/documents/{id}/create-version/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Download a document
     * @param id A unique integer value identifying this document.
     * @returns Document
     * @throws ApiError
     */
    public static documentsDocumentsDownloadRetrieve(
        id: number,
    ): CancelablePromise<Document> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/documents/{id}/download/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing fees
     * @param application
     * @param dueAfter
     * @param dueBefore
     * @param feeType * `application` - Application Fee
     * * `valuation` - Valuation Fee
     * * `legal` - Legal Fee
     * * `broker` - Broker Fee
     * * `settlement` - Settlement Fee
     * * `other` - Other Fee
     * @param isPaid
     * @param maxAmount
     * @param minAmount
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedFeeList
     * @throws ApiError
     */
    public static documentsFeesList(
        application?: number,
        dueAfter?: string,
        dueBefore?: string,
        feeType?: 'application' | 'broker' | 'legal' | 'other' | 'settlement' | 'valuation',
        isPaid?: boolean,
        maxAmount?: number,
        minAmount?: number,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedFeeList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/fees/',
            query: {
                'application': application,
                'due_after': dueAfter,
                'due_before': dueBefore,
                'fee_type': feeType,
                'is_paid': isPaid,
                'max_amount': maxAmount,
                'min_amount': minAmount,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * API endpoint for managing fees
     * @param requestBody
     * @returns Fee
     * @throws ApiError
     */
    public static documentsFeesCreate(
        requestBody: FeeRequest,
    ): CancelablePromise<Fee> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/documents/fees/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing fees
     * @param id A unique integer value identifying this fee.
     * @returns Fee
     * @throws ApiError
     */
    public static documentsFeesRetrieve(
        id: number,
    ): CancelablePromise<Fee> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/fees/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing fees
     * @param id A unique integer value identifying this fee.
     * @param requestBody
     * @returns Fee
     * @throws ApiError
     */
    public static documentsFeesUpdate(
        id: number,
        requestBody: FeeRequest,
    ): CancelablePromise<Fee> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/documents/fees/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing fees
     * @param id A unique integer value identifying this fee.
     * @param requestBody
     * @returns Fee
     * @throws ApiError
     */
    public static documentsFeesPartialUpdate(
        id: number,
        requestBody?: PatchedFeeRequest,
    ): CancelablePromise<Fee> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/documents/fees/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing fees
     * @param id A unique integer value identifying this fee.
     * @returns void
     * @throws ApiError
     */
    public static documentsFeesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/documents/fees/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Mark a fee as paid
     * @param id
     * @returns any No response body
     * @throws ApiError
     */
    public static documentsFeesMarkPaidCreate(
        id: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/documents/fees/{id}/mark-paid/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing notes
     * @param application
     * @param borrower
     * @param createdAfter
     * @param createdBefore
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedNoteList
     * @throws ApiError
     */
    public static documentsNotesList(
        application?: number,
        borrower?: number,
        createdAfter?: string,
        createdBefore?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedNoteList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/notes/',
            query: {
                'application': application,
                'borrower': borrower,
                'created_after': createdAfter,
                'created_before': createdBefore,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * API endpoint for managing notes
     * @param requestBody
     * @returns Note
     * @throws ApiError
     */
    public static documentsNotesCreate(
        requestBody?: NoteRequest,
    ): CancelablePromise<Note> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/documents/notes/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing notes
     * @param id A unique integer value identifying this note.
     * @returns Note
     * @throws ApiError
     */
    public static documentsNotesRetrieve(
        id: number,
    ): CancelablePromise<Note> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/notes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing notes
     * @param id A unique integer value identifying this note.
     * @param requestBody
     * @returns Note
     * @throws ApiError
     */
    public static documentsNotesUpdate(
        id: number,
        requestBody?: NoteRequest,
    ): CancelablePromise<Note> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/documents/notes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing notes
     * @param id A unique integer value identifying this note.
     * @param requestBody
     * @returns Note
     * @throws ApiError
     */
    public static documentsNotesPartialUpdate(
        id: number,
        requestBody?: PatchedNoteRequest,
    ): CancelablePromise<Note> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/documents/notes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing notes
     * @param id A unique integer value identifying this note.
     * @returns void
     * @throws ApiError
     */
    public static documentsNotesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/documents/notes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing repayments
     * @param application
     * @param dueAfter
     * @param dueBefore
     * @param isPaid
     * @param maxAmount
     * @param minAmount
     * @param page A page number within the paginated result set.
     * @returns PaginatedRepaymentList
     * @throws ApiError
     */
    public static documentsRepaymentsList(
        application?: number,
        dueAfter?: string,
        dueBefore?: string,
        isPaid?: boolean,
        maxAmount?: number,
        minAmount?: number,
        page?: number,
    ): CancelablePromise<PaginatedRepaymentList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/repayments/',
            query: {
                'application': application,
                'due_after': dueAfter,
                'due_before': dueBefore,
                'is_paid': isPaid,
                'max_amount': maxAmount,
                'min_amount': minAmount,
                'page': page,
            },
        });
    }
    /**
     * API endpoint for managing repayments
     * @param requestBody
     * @returns Repayment
     * @throws ApiError
     */
    public static documentsRepaymentsCreate(
        requestBody: RepaymentRequest,
    ): CancelablePromise<Repayment> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/documents/repayments/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing repayments
     * @param id A unique integer value identifying this repayment.
     * @returns Repayment
     * @throws ApiError
     */
    public static documentsRepaymentsRetrieve(
        id: number,
    ): CancelablePromise<Repayment> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/repayments/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing repayments
     * @param id A unique integer value identifying this repayment.
     * @param requestBody
     * @returns Repayment
     * @throws ApiError
     */
    public static documentsRepaymentsUpdate(
        id: number,
        requestBody: RepaymentRequest,
    ): CancelablePromise<Repayment> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/documents/repayments/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing repayments
     * @param id A unique integer value identifying this repayment.
     * @param requestBody
     * @returns Repayment
     * @throws ApiError
     */
    public static documentsRepaymentsPartialUpdate(
        id: number,
        requestBody?: PatchedRepaymentRequest,
    ): CancelablePromise<Repayment> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/documents/repayments/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing repayments
     * @param id A unique integer value identifying this repayment.
     * @returns void
     * @throws ApiError
     */
    public static documentsRepaymentsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/documents/repayments/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Mark a repayment as paid
     * @param id
     * @returns any No response body
     * @throws ApiError
     */
    public static documentsRepaymentsMarkPaidCreate(
        id: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/documents/repayments/{id}/mark-paid/',
            path: {
                'id': id,
            },
        });
    }
}
