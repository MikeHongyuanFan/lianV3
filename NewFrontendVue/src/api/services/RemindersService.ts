/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedReminderList } from '../models/PaginatedReminderList';
import type { PatchedReminderRequest } from '../models/PatchedReminderRequest';
import type { Reminder } from '../models/Reminder';
import type { ReminderRequest } from '../models/ReminderRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class RemindersService {
    /**
     * API endpoint for managing reminders
     * @param isSent
     * @param page A page number within the paginated result set.
     * @param recipientType * `client` - Client
     * * `bdm` - Business Development Manager
     * * `broker` - Broker
     * * `custom` - Custom Email
     * @param relatedApplication
     * @param relatedBorrower
     * @param search A search term.
     * @returns PaginatedReminderList
     * @throws ApiError
     */
    public static remindersList(
        isSent?: boolean,
        page?: number,
        recipientType?: 'bdm' | 'broker' | 'client' | 'custom',
        relatedApplication?: number,
        relatedBorrower?: number,
        search?: string,
    ): CancelablePromise<PaginatedReminderList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/reminders/',
            query: {
                'is_sent': isSent,
                'page': page,
                'recipient_type': recipientType,
                'related_application': relatedApplication,
                'related_borrower': relatedBorrower,
                'search': search,
            },
        });
    }
    /**
     * API endpoint for managing reminders
     * @param requestBody
     * @returns Reminder
     * @throws ApiError
     */
    public static remindersCreate(
        requestBody: ReminderRequest,
    ): CancelablePromise<Reminder> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/reminders/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing reminders
     * @param id A unique integer value identifying this reminder.
     * @returns Reminder
     * @throws ApiError
     */
    public static remindersRetrieve(
        id: number,
    ): CancelablePromise<Reminder> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/reminders/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing reminders
     * @param id A unique integer value identifying this reminder.
     * @param requestBody
     * @returns Reminder
     * @throws ApiError
     */
    public static remindersUpdate(
        id: number,
        requestBody: ReminderRequest,
    ): CancelablePromise<Reminder> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/reminders/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing reminders
     * @param id A unique integer value identifying this reminder.
     * @param requestBody
     * @returns Reminder
     * @throws ApiError
     */
    public static remindersPartialUpdate(
        id: number,
        requestBody?: PatchedReminderRequest,
    ): CancelablePromise<Reminder> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/reminders/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing reminders
     * @param id A unique integer value identifying this reminder.
     * @returns void
     * @throws ApiError
     */
    public static remindersDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/reminders/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
