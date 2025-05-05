/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ReportsService {
    /**
     * API endpoint for application status reports
     * @returns any No response body
     * @throws ApiError
     */
    public static reportsApplicationStatusRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/reports/application-status/',
        });
    }
    /**
     * API endpoint for application volume reports
     * @returns any No response body
     * @throws ApiError
     */
    public static reportsApplicationVolumeRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/reports/application-volume/',
        });
    }
    /**
     * API endpoint for repayment compliance reports
     * @returns any No response body
     * @throws ApiError
     */
    public static reportsRepaymentComplianceRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/reports/repayment-compliance/',
        });
    }
}
