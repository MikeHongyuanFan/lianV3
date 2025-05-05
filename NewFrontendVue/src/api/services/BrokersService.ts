/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BDM } from '../models/BDM';
import type { BDMRequest } from '../models/BDMRequest';
import type { Branch } from '../models/Branch';
import type { BranchRequest } from '../models/BranchRequest';
import type { BrokerDetail } from '../models/BrokerDetail';
import type { BrokerDetailRequest } from '../models/BrokerDetailRequest';
import type { PaginatedBDMList } from '../models/PaginatedBDMList';
import type { PaginatedBranchList } from '../models/PaginatedBranchList';
import type { PaginatedBrokerListList } from '../models/PaginatedBrokerListList';
import type { PatchedBDMRequest } from '../models/PatchedBDMRequest';
import type { PatchedBranchRequest } from '../models/PatchedBranchRequest';
import type { PatchedBrokerDetailRequest } from '../models/PatchedBrokerDetailRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class BrokersService {
    /**
     * API endpoint for managing brokers
     * @param branch
     * @param minApplications
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedBrokerListList
     * @throws ApiError
     */
    public static brokersList(
        branch?: number,
        minApplications?: number,
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedBrokerListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/brokers/',
            query: {
                'branch': branch,
                'min_applications': minApplications,
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * API endpoint for managing brokers
     * @param requestBody
     * @returns BrokerDetail
     * @throws ApiError
     */
    public static brokersCreate(
        requestBody: BrokerDetailRequest,
    ): CancelablePromise<BrokerDetail> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/brokers/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing brokers
     * @param id A unique integer value identifying this broker.
     * @returns BrokerDetail
     * @throws ApiError
     */
    public static brokersRetrieve(
        id: number,
    ): CancelablePromise<BrokerDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/brokers/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing brokers
     * @param id A unique integer value identifying this broker.
     * @param requestBody
     * @returns BrokerDetail
     * @throws ApiError
     */
    public static brokersUpdate(
        id: number,
        requestBody: BrokerDetailRequest,
    ): CancelablePromise<BrokerDetail> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/brokers/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing brokers
     * @param id A unique integer value identifying this broker.
     * @param requestBody
     * @returns BrokerDetail
     * @throws ApiError
     */
    public static brokersPartialUpdate(
        id: number,
        requestBody?: PatchedBrokerDetailRequest,
    ): CancelablePromise<BrokerDetail> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/brokers/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing brokers
     * @param id A unique integer value identifying this broker.
     * @returns void
     * @throws ApiError
     */
    public static brokersDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/brokers/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Get all applications for a broker
     * @param id A unique integer value identifying this broker.
     * @returns BrokerDetail
     * @throws ApiError
     */
    public static brokersApplicationsRetrieve(
        id: number,
    ): CancelablePromise<BrokerDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/brokers/{id}/applications/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Get statistics for a broker
     * @param id A unique integer value identifying this broker.
     * @returns BrokerDetail
     * @throws ApiError
     */
    public static brokersStatsRetrieve(
        id: number,
    ): CancelablePromise<BrokerDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/brokers/{id}/stats/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing BDMs
     * @param branch
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedBDMList
     * @throws ApiError
     */
    public static brokersBdmsList(
        branch?: number,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedBDMList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/brokers/bdms/',
            query: {
                'branch': branch,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * API endpoint for managing BDMs
     * @param requestBody
     * @returns BDM
     * @throws ApiError
     */
    public static brokersBdmsCreate(
        requestBody: BDMRequest,
    ): CancelablePromise<BDM> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/brokers/bdms/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing BDMs
     * @param id A unique integer value identifying this BDM.
     * @returns BDM
     * @throws ApiError
     */
    public static brokersBdmsRetrieve(
        id: number,
    ): CancelablePromise<BDM> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/brokers/bdms/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing BDMs
     * @param id A unique integer value identifying this BDM.
     * @param requestBody
     * @returns BDM
     * @throws ApiError
     */
    public static brokersBdmsUpdate(
        id: number,
        requestBody: BDMRequest,
    ): CancelablePromise<BDM> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/brokers/bdms/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing BDMs
     * @param id A unique integer value identifying this BDM.
     * @param requestBody
     * @returns BDM
     * @throws ApiError
     */
    public static brokersBdmsPartialUpdate(
        id: number,
        requestBody?: PatchedBDMRequest,
    ): CancelablePromise<BDM> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/brokers/bdms/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing BDMs
     * @param id A unique integer value identifying this BDM.
     * @returns void
     * @throws ApiError
     */
    public static brokersBdmsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/brokers/bdms/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Get all applications for a BDM
     * @param id A unique integer value identifying this BDM.
     * @returns BDM
     * @throws ApiError
     */
    public static brokersBdmsApplicationsRetrieve(
        id: number,
    ): CancelablePromise<BDM> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/brokers/bdms/{id}/applications/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing branches
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedBranchList
     * @throws ApiError
     */
    public static brokersBranchesList(
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedBranchList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/brokers/branches/',
            query: {
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * API endpoint for managing branches
     * @param requestBody
     * @returns Branch
     * @throws ApiError
     */
    public static brokersBranchesCreate(
        requestBody: BranchRequest,
    ): CancelablePromise<Branch> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/brokers/branches/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing branches
     * @param id A unique integer value identifying this branch.
     * @returns Branch
     * @throws ApiError
     */
    public static brokersBranchesRetrieve(
        id: number,
    ): CancelablePromise<Branch> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/brokers/branches/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing branches
     * @param id A unique integer value identifying this branch.
     * @param requestBody
     * @returns Branch
     * @throws ApiError
     */
    public static brokersBranchesUpdate(
        id: number,
        requestBody: BranchRequest,
    ): CancelablePromise<Branch> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/brokers/branches/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing branches
     * @param id A unique integer value identifying this branch.
     * @param requestBody
     * @returns Branch
     * @throws ApiError
     */
    public static brokersBranchesPartialUpdate(
        id: number,
        requestBody?: PatchedBranchRequest,
    ): CancelablePromise<Branch> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/brokers/branches/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing branches
     * @param id A unique integer value identifying this branch.
     * @returns void
     * @throws ApiError
     */
    public static brokersBranchesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/brokers/branches/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Get all BDMs for a branch
     * @param id A unique integer value identifying this branch.
     * @returns Branch
     * @throws ApiError
     */
    public static brokersBranchesBdmsRetrieve(
        id: number,
    ): CancelablePromise<Branch> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/brokers/branches/{id}/bdms/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Get all brokers for a branch
     * @param id A unique integer value identifying this branch.
     * @returns Branch
     * @throws ApiError
     */
    public static brokersBranchesBrokersRetrieve(
        id: number,
    ): CancelablePromise<Branch> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/brokers/branches/{id}/brokers/',
            path: {
                'id': id,
            },
        });
    }
}
