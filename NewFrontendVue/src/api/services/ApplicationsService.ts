/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApplicationBorrower } from '../models/ApplicationBorrower';
import type { ApplicationBorrowerRequest } from '../models/ApplicationBorrowerRequest';
import type { ApplicationCreate } from '../models/ApplicationCreate';
import type { ApplicationCreateRequest } from '../models/ApplicationCreateRequest';
import type { ApplicationDetail } from '../models/ApplicationDetail';
import type { ApplicationDetailRequest } from '../models/ApplicationDetailRequest';
import type { ApplicationSignature } from '../models/ApplicationSignature';
import type { ApplicationSignatureRequest } from '../models/ApplicationSignatureRequest';
import type { ApplicationStageUpdate } from '../models/ApplicationStageUpdate';
import type { ApplicationStageUpdateRequest } from '../models/ApplicationStageUpdateRequest';
import type { FundingCalculationHistory } from '../models/FundingCalculationHistory';
import type { FundingCalculationInput } from '../models/FundingCalculationInput';
import type { FundingCalculationInputRequest } from '../models/FundingCalculationInputRequest';
import type { LoanExtension } from '../models/LoanExtension';
import type { LoanExtensionRequest } from '../models/LoanExtensionRequest';
import type { PaginatedApplicationDetailList } from '../models/PaginatedApplicationDetailList';
import type { PatchedApplicationDetailRequest } from '../models/PatchedApplicationDetailRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ApplicationsService {
    /**
     * Update borrowers for an application
     * @param id
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsBorrowersUpdate(
        id: number,
        requestBody?: ApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/applications/{id}/borrowers/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Extend a loan with new terms and regenerate repayment schedule
     * @param id
     * @param requestBody
     * @returns LoanExtension
     * @throws ApiError
     */
    public static applicationsExtendLoanCreate(
        id: number,
        requestBody: LoanExtensionRequest,
    ): CancelablePromise<LoanExtension> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/{id}/extend-loan/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Create or update funding calculation for an application
     * @param id
     * @param requestBody
     * @returns FundingCalculationInput
     * @throws ApiError
     */
    public static applicationsFundingCalculationCreate(
        id: number,
        requestBody: FundingCalculationInputRequest,
    ): CancelablePromise<FundingCalculationInput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/{id}/funding-calculation/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Get funding calculation history for an application
     * @param id
     * @returns FundingCalculationHistory
     * @throws ApiError
     */
    public static applicationsFundingCalculationHistoryRetrieve(
        id: number,
    ): CancelablePromise<FundingCalculationHistory> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/applications/{id}/funding-calculation-history/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Sign an application
     * @param id
     * @param requestBody
     * @returns ApplicationSignature
     * @throws ApiError
     */
    public static applicationsSignCreate(
        id: number,
        requestBody: ApplicationSignatureRequest,
    ): CancelablePromise<ApplicationSignature> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/{id}/sign/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Process signature for an application
     * @param id
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsSignatureCreate(
        id: number,
        requestBody?: ApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/{id}/signature/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Update application stage
     * @param id
     * @param requestBody
     * @returns ApplicationStageUpdate
     * @throws ApiError
     */
    public static applicationsStageUpdate(
        id: number,
        requestBody: ApplicationStageUpdateRequest,
    ): CancelablePromise<ApplicationStageUpdate> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/applications/{id}/stage/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing loan applications
     * @param applicationType * `residential` - Residential
     * * `commercial` - Commercial
     * * `construction` - Construction
     * * `refinance` - Refinance
     * * `investment` - Investment
     * * `smsf` - SMSF
     * @param bd
     * @param branch
     * @param broker
     * @param createdAfter
     * @param createdBefore
     * @param maxInterestRate
     * @param maxLoanAmount
     * @param minInterestRate
     * @param minLoanAmount
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param repaymentFrequency * `weekly` - Weekly
     * * `fortnightly` - Fortnightly
     * * `monthly` - Monthly
     * * `quarterly` - Quarterly
     * * `annually` - Annually
     * @param search A search term.
     * @param stage * `inquiry` - Inquiry
     * * `sent_to_lender` - Sent to Lender
     * * `funding_table_issued` - Funding Table Issued
     * * `iloo_issued` - ILOO Issued
     * * `iloo_signed` - ILOO Signed
     * * `commitment_fee_paid` - Commitment Fee Paid
     * * `app_submitted` - App Submitted
     * * `valuation_ordered` - Valuation Ordered
     * * `valuation_received` - Valuation Received
     * * `more_info_required` - More Info Required
     * * `formal_approval` - Formal Approval
     * * `loan_docs_instructed` - Loan Docs Instructed
     * * `loan_docs_issued` - Loan Docs Issued
     * * `loan_docs_signed` - Loan Docs Signed
     * * `settlement_conditions` - Settlement Conditions
     * * `settled` - Settled
     * * `closed` - Closed
     * * `declined` - Declined
     * * `withdrawn` - Withdrawn
     * @returns PaginatedApplicationDetailList
     * @throws ApiError
     */
    public static applicationsApplicationsList(
        applicationType?: 'commercial' | 'construction' | 'investment' | 'refinance' | 'residential' | 'smsf' | null,
        bd?: number,
        branch?: number,
        broker?: number,
        createdAfter?: string,
        createdBefore?: string,
        maxInterestRate?: number,
        maxLoanAmount?: number,
        minInterestRate?: number,
        minLoanAmount?: number,
        ordering?: string,
        page?: number,
        repaymentFrequency?: 'annually' | 'fortnightly' | 'monthly' | 'quarterly' | 'weekly',
        search?: string,
        stage?: 'app_submitted' | 'closed' | 'commitment_fee_paid' | 'declined' | 'formal_approval' | 'funding_table_issued' | 'iloo_issued' | 'iloo_signed' | 'inquiry' | 'loan_docs_instructed' | 'loan_docs_issued' | 'loan_docs_signed' | 'more_info_required' | 'sent_to_lender' | 'settled' | 'settlement_conditions' | 'valuation_ordered' | 'valuation_received' | 'withdrawn',
    ): CancelablePromise<PaginatedApplicationDetailList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/applications/applications/',
            query: {
                'application_type': applicationType,
                'bd': bd,
                'branch': branch,
                'broker': broker,
                'created_after': createdAfter,
                'created_before': createdBefore,
                'max_interest_rate': maxInterestRate,
                'max_loan_amount': maxLoanAmount,
                'min_interest_rate': minInterestRate,
                'min_loan_amount': minLoanAmount,
                'ordering': ordering,
                'page': page,
                'repayment_frequency': repaymentFrequency,
                'search': search,
                'stage': stage,
            },
        });
    }
    /**
     * API endpoint for managing loan applications
     * @param requestBody
     * @returns ApplicationCreate
     * @throws ApiError
     */
    public static applicationsApplicationsCreate(
        requestBody?: ApplicationCreateRequest,
    ): CancelablePromise<ApplicationCreate> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing loan applications
     * @param id A unique integer value identifying this application.
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsRetrieve(
        id: number,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/applications/applications/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing loan applications
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsUpdate(
        id: number,
        requestBody?: ApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/applications/applications/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing loan applications
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsPartialUpdate(
        id: number,
        requestBody?: PatchedApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/applications/applications/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing loan applications
     * @param id A unique integer value identifying this application.
     * @returns void
     * @throws ApiError
     */
    public static applicationsApplicationsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/applications/applications/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Add a fee to an application
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsAddFeeCreate(
        id: number,
        requestBody?: ApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/{id}/add_fee/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Add a note to an application
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsAddNoteCreate(
        id: number,
        requestBody?: ApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/{id}/add_note/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Add a repayment to an application
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsAddRepaymentCreate(
        id: number,
        requestBody?: ApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/{id}/add_repayment/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Update borrowers for an application
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsBorrowersUpdate(
        id: number,
        requestBody?: ApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/applications/applications/{id}/borrowers/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Get all documents for an application
     * @param id A unique integer value identifying this application.
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsDocumentsRetrieve(
        id: number,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/applications/applications/{id}/documents/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Extend a loan with new terms and regenerate repayment schedule
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns LoanExtension
     * @throws ApiError
     */
    public static applicationsApplicationsExtendLoanCreate(
        id: number,
        requestBody: LoanExtensionRequest,
    ): CancelablePromise<LoanExtension> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/{id}/extend_loan/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Get all fees for an application
     * @param id A unique integer value identifying this application.
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsFeesRetrieve(
        id: number,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/applications/applications/{id}/fees/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Create or update funding calculation for an application
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns FundingCalculationInput
     * @throws ApiError
     */
    public static applicationsApplicationsFundingCalculationCreate(
        id: number,
        requestBody: FundingCalculationInputRequest,
    ): CancelablePromise<FundingCalculationInput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/{id}/funding_calculation/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Get funding calculation history for an application
     * @param id A unique integer value identifying this application.
     * @returns FundingCalculationHistory
     * @throws ApiError
     */
    public static applicationsApplicationsFundingCalculationHistoryRetrieve(
        id: number,
    ): CancelablePromise<FundingCalculationHistory> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/applications/applications/{id}/funding_calculation_history/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Get ledger entries for an application
     * @param id A unique integer value identifying this application.
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsLedgerRetrieve(
        id: number,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/applications/applications/{id}/ledger/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Get all notes for an application
     * @param id A unique integer value identifying this application.
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsNotesRetrieve(
        id: number,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/applications/applications/{id}/notes/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Record a payment for a repayment
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsRecordPaymentCreate(
        id: number,
        requestBody?: ApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/{id}/record_payment/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Remove borrowers from application
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns ApplicationBorrower
     * @throws ApiError
     */
    public static applicationsApplicationsRemoveBorrowersCreate(
        id: number,
        requestBody: ApplicationBorrowerRequest,
    ): CancelablePromise<ApplicationBorrower> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/{id}/remove_borrowers/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Get all repayments for an application
     * @param id A unique integer value identifying this application.
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsRepaymentsRetrieve(
        id: number,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/applications/applications/{id}/repayments/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Sign an application
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns ApplicationSignature
     * @throws ApiError
     */
    public static applicationsApplicationsSignCreate(
        id: number,
        requestBody: ApplicationSignatureRequest,
    ): CancelablePromise<ApplicationSignature> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/{id}/sign/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Process signature for an application
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsSignatureCreate(
        id: number,
        requestBody?: ApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/{id}/signature/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Update application stage
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns ApplicationStageUpdate
     * @throws ApiError
     */
    public static applicationsApplicationsUpdateStageCreate(
        id: number,
        requestBody: ApplicationStageUpdateRequest,
    ): CancelablePromise<ApplicationStageUpdate> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/{id}/update_stage/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Upload a document for an application
     * @param id A unique integer value identifying this application.
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsUploadDocumentCreate(
        id: number,
        requestBody?: ApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/{id}/upload_document/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Validate application schema
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsApplicationsValidateSchemaCreate(
        requestBody?: ApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/applications/validate_schema/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing loan applications
     * @param requestBody
     * @returns ApplicationCreate
     * @throws ApiError
     */
    public static applicationsCreateWithCascadeCreate(
        requestBody?: ApplicationCreateRequest,
    ): CancelablePromise<ApplicationCreate> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/create-with-cascade/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Validate application schema
     * @param requestBody
     * @returns ApplicationDetail
     * @throws ApiError
     */
    public static applicationsValidateSchemaCreate(
        requestBody?: ApplicationDetailRequest,
    ): CancelablePromise<ApplicationDetail> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/applications/validate-schema/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
}
