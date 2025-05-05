/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { NotificationTypeEnum } from './NotificationTypeEnum';
/**
 * Serializer for listing notifications
 */
export type NotificationList = {
    readonly id: number;
    title: string;
    notification_type: NotificationTypeEnum;
    readonly notification_type_display: string;
    is_read?: boolean;
    readonly created_at: string;
};

