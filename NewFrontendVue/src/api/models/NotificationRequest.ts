/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { NotificationTypeEnum } from './NotificationTypeEnum';
/**
 * Serializer for Notification model
 */
export type NotificationRequest = {
    title: string;
    message: string;
    notification_type: NotificationTypeEnum;
    related_object_id?: number | null;
    related_object_type?: string | null;
    is_read?: boolean;
    read_at?: string | null;
    user: number;
};

