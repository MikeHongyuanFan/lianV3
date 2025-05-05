/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Notification } from '../models/Notification';
import type { NotificationPreference } from '../models/NotificationPreference';
import type { NotificationPreferenceRequest } from '../models/NotificationPreferenceRequest';
import type { NotificationRequest } from '../models/NotificationRequest';
import type { PaginatedNotificationListList } from '../models/PaginatedNotificationListList';
import type { PaginatedUserList } from '../models/PaginatedUserList';
import type { PatchedUserRequest } from '../models/PatchedUserRequest';
import type { TokenRefresh } from '../models/TokenRefresh';
import type { TokenRefreshRequest } from '../models/TokenRefreshRequest';
import type { User } from '../models/User';
import type { UserCreate } from '../models/UserCreate';
import type { UserCreateRequest } from '../models/UserCreateRequest';
import type { UserRequest } from '../models/UserRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class UsersService {
    /**
     * API endpoint for user login
     * @returns any No response body
     * @throws ApiError
     */
    public static usersAuthLoginCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/auth/login/',
        });
    }
    /**
     * Takes a refresh type JSON web token and returns an access type JSON web
     * token if the refresh token is valid.
     * @param requestBody
     * @returns TokenRefresh
     * @throws ApiError
     */
    public static usersAuthRefreshCreate(
        requestBody: TokenRefreshRequest,
    ): CancelablePromise<TokenRefresh> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/auth/refresh/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for user registration
     * @returns any No response body
     * @throws ApiError
     */
    public static usersAuthRegisterCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/auth/register/',
        });
    }
    /**
     * Get notification preferences for the current user
     * @returns NotificationPreference
     * @throws ApiError
     */
    public static usersNotificationPreferencesRetrieve(): CancelablePromise<NotificationPreference> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/notification-preferences/',
        });
    }
    /**
     * Update notification preferences for the current user
     * @param requestBody
     * @returns NotificationPreference
     * @throws ApiError
     */
    public static usersNotificationPreferencesUpdate(
        requestBody?: NotificationPreferenceRequest,
    ): CancelablePromise<NotificationPreference> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/users/notification-preferences/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for listing user notifications
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @returns PaginatedNotificationListList
     * @throws ApiError
     */
    public static usersNotificationsList(
        ordering?: string,
        page?: number,
    ): CancelablePromise<PaginatedNotificationListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/notifications/',
            query: {
                'ordering': ordering,
                'page': page,
            },
        });
    }
    /**
     * API endpoint for managing notifications
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @returns PaginatedNotificationListList
     * @throws ApiError
     */
    public static usersNotificationsViewsetList(
        ordering?: string,
        page?: number,
    ): CancelablePromise<PaginatedNotificationListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/notifications-viewset/',
            query: {
                'ordering': ordering,
                'page': page,
            },
        });
    }
    /**
     * API endpoint for managing notifications
     * @param id
     * @returns Notification
     * @throws ApiError
     */
    public static usersNotificationsViewsetRetrieve(
        id: string,
    ): CancelablePromise<Notification> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/notifications-viewset/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Mark a notification as read
     * @param id
     * @param requestBody
     * @returns Notification
     * @throws ApiError
     */
    public static usersNotificationsViewsetMarkAsReadCreate(
        id: string,
        requestBody: NotificationRequest,
    ): CancelablePromise<Notification> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/notifications-viewset/{id}/mark_as_read/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Mark all notifications as read
     * @param requestBody
     * @returns Notification
     * @throws ApiError
     */
    public static usersNotificationsViewsetMarkAllAsReadCreate(
        requestBody: NotificationRequest,
    ): CancelablePromise<Notification> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/notifications-viewset/mark_all_as_read/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Get count of unread notifications
     * @returns Notification
     * @throws ApiError
     */
    public static usersNotificationsViewsetUnreadCountRetrieve(): CancelablePromise<Notification> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/notifications-viewset/unread_count/',
        });
    }
    /**
     * API endpoint for getting unread notification count
     * @returns any No response body
     * @throws ApiError
     */
    public static usersNotificationsCountRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/notifications/count/',
        });
    }
    /**
     * API endpoint for marking notifications as read
     * @returns any No response body
     * @throws ApiError
     */
    public static usersNotificationsMarkReadCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/notifications/mark-read/',
        });
    }
    /**
     * API endpoint for retrieving user profile
     * @returns User
     * @throws ApiError
     */
    public static usersProfileRetrieve(): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/profile/',
        });
    }
    /**
     * API endpoint for updating user profile
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static usersProfileUpdateUpdate(
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/users/profile/update/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for updating user profile
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static usersProfileUpdatePartialUpdate(
        requestBody?: PatchedUserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/users/profile/update/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing users
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserList
     * @throws ApiError
     */
    public static usersUsersList(
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/users/',
            query: {
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * API endpoint for managing users
     * @param requestBody
     * @returns UserCreate
     * @throws ApiError
     */
    public static usersUsersCreate(
        requestBody: UserCreateRequest,
    ): CancelablePromise<UserCreate> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/users/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing users
     * @param id A unique integer value identifying this user.
     * @returns User
     * @throws ApiError
     */
    public static usersUsersRetrieve(
        id: number,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/users/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing users
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static usersUsersUpdate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/users/users/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing users
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static usersUsersPartialUpdate(
        id: number,
        requestBody?: PatchedUserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/users/users/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing users
     * @param id A unique integer value identifying this user.
     * @returns void
     * @throws ApiError
     */
    public static usersUsersDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/users/users/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Get current user information
     * @returns User
     * @throws ApiError
     */
    public static usersUsersMeRetrieve(): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/users/me/',
        });
    }
}
