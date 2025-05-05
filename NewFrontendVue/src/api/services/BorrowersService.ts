/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BorrowerDetail } from '../models/BorrowerDetail';
import type { BorrowerDetailRequest } from '../models/BorrowerDetailRequest';
import type { Guarantor } from '../models/Guarantor';
import type { GuarantorRequest } from '../models/GuarantorRequest';
import type { PaginatedBorrowerListList } from '../models/PaginatedBorrowerListList';
import type { PaginatedGuarantorList } from '../models/PaginatedGuarantorList';
import type { PatchedBorrowerDetailRequest } from '../models/PatchedBorrowerDetailRequest';
import type { PatchedGuarantorRequest } from '../models/PatchedGuarantorRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class BorrowersService {
    /**
     * API endpoint for managing borrowers
     * @param hasApplications
     * @param maritalStatus * `single` - Single
     * * `married` - Married
     * * `de_facto` - De Facto
     * * `divorced` - Divorced
     * * `widowed` - Widowed
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param residencyStatus * `citizen` - Citizen
     * * `permanent_resident` - Permanent Resident
     * * `temporary_resident` - Temporary Resident
     * * `foreign_investor` - Foreign Investor
     * @param search A search term.
     * @returns PaginatedBorrowerListList
     * @throws ApiError
     */
    public static borrowersList(
        hasApplications?: boolean,
        maritalStatus?: 'de_facto' | 'divorced' | 'married' | 'single' | 'widowed' | null,
        ordering?: string,
        page?: number,
        residencyStatus?: 'citizen' | 'foreign_investor' | 'permanent_resident' | 'temporary_resident' | null,
        search?: string,
    ): CancelablePromise<PaginatedBorrowerListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/borrowers/',
            query: {
                'has_applications': hasApplications,
                'marital_status': maritalStatus,
                'ordering': ordering,
                'page': page,
                'residency_status': residencyStatus,
                'search': search,
            },
        });
    }
    /**
     * API endpoint for managing borrowers
     * @param requestBody
     * @returns BorrowerDetail
     * @throws ApiError
     */
    public static borrowersCreate(
        requestBody?: BorrowerDetailRequest,
    ): CancelablePromise<BorrowerDetail> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/borrowers/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing borrowers
     * @param id A unique integer value identifying this borrower.
     * @returns BorrowerDetail
     * @throws ApiError
     */
    public static borrowersRetrieve(
        id: number,
    ): CancelablePromise<BorrowerDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/borrowers/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing borrowers
     * @param id A unique integer value identifying this borrower.
     * @param requestBody
     * @returns BorrowerDetail
     * @throws ApiError
     */
    public static borrowersUpdate(
        id: number,
        requestBody?: BorrowerDetailRequest,
    ): CancelablePromise<BorrowerDetail> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/borrowers/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing borrowers
     * @param id A unique integer value identifying this borrower.
     * @param requestBody
     * @returns BorrowerDetail
     * @throws ApiError
     */
    public static borrowersPartialUpdate(
        id: number,
        requestBody?: PatchedBorrowerDetailRequest,
    ): CancelablePromise<BorrowerDetail> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/borrowers/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing borrowers
     * @param id A unique integer value identifying this borrower.
     * @returns void
     * @throws ApiError
     */
    public static borrowersDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/borrowers/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Get all applications for a borrower
     * @param id A unique integer value identifying this borrower.
     * @returns BorrowerDetail
     * @throws ApiError
     */
    public static borrowersApplicationsRetrieve(
        id: number,
    ): CancelablePromise<BorrowerDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/borrowers/{id}/applications/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Get a financial summary for a borrower
     * @param id
     * @returns any No response body
     * @throws ApiError
     */
    public static borrowersFinancialSummaryRetrieve(
        id: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/borrowers/{id}/financial-summary/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Get all guarantors for a borrower
     * @param id A unique integer value identifying this borrower.
     * @returns BorrowerDetail
     * @throws ApiError
     */
    public static borrowersGuarantorsRetrieve2(
        id: number,
    ): CancelablePromise<BorrowerDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/borrowers/{id}/guarantors/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * View for listing company borrowers
     * @param page A page number within the paginated result set.
     * @returns PaginatedBorrowerListList
     * @throws ApiError
     */
    public static borrowersCompanyList(
        page?: number,
    ): CancelablePromise<PaginatedBorrowerListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/borrowers/company/',
            query: {
                'page': page,
            },
        });
    }
    /**
     * API endpoint for managing guarantors
     * @param application
     * @param borrower
     * @param guarantorType * `individual` - Individual
     * * `company` - Company
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedGuarantorList
     * @throws ApiError
     */
    public static borrowersGuarantorsList(
        application?: number,
        borrower?: number,
        guarantorType?: 'company' | 'individual',
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedGuarantorList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/borrowers/guarantors/',
            query: {
                'application': application,
                'borrower': borrower,
                'guarantor_type': guarantorType,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * API endpoint for managing guarantors
     * @param requestBody
     * @returns Guarantor
     * @throws ApiError
     */
    public static borrowersGuarantorsCreate(
        requestBody?: GuarantorRequest,
    ): CancelablePromise<Guarantor> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/borrowers/guarantors/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing guarantors
     * @param id A unique integer value identifying this guarantor.
     * @returns Guarantor
     * @throws ApiError
     */
    public static borrowersGuarantorsRetrieve(
        id: number,
    ): CancelablePromise<Guarantor> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/borrowers/guarantors/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing guarantors
     * @param id A unique integer value identifying this guarantor.
     * @param requestBody
     * @returns Guarantor
     * @throws ApiError
     */
    public static borrowersGuarantorsUpdate(
        id: number,
        requestBody?: GuarantorRequest,
    ): CancelablePromise<Guarantor> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/borrowers/guarantors/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing guarantors
     * @param id A unique integer value identifying this guarantor.
     * @param requestBody
     * @returns Guarantor
     * @throws ApiError
     */
    public static borrowersGuarantorsPartialUpdate(
        id: number,
        requestBody?: PatchedGuarantorRequest,
    ): CancelablePromise<Guarantor> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/borrowers/guarantors/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing guarantors
     * @param id A unique integer value identifying this guarantor.
     * @returns void
     * @throws ApiError
     */
    public static borrowersGuarantorsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/borrowers/guarantors/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Get all applications guaranteed by a guarantor
     * @param id A unique integer value identifying this guarantor.
     * @returns Guarantor
     * @throws ApiError
     */
    public static borrowersGuarantorsGuaranteedApplicationsRetrieve(
        id: number,
    ): CancelablePromise<Guarantor> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/borrowers/guarantors/{id}/guaranteed_applications/',
            path: {
                'id': id,
            },
        });
    }
}
