/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RecipientTypeEnum } from './RecipientTypeEnum';
/**
 * Serializer for reminders
 */
export type ReminderRequest = {
    recipient_type: RecipientTypeEnum;
    recipient_email: string;
    send_datetime: string;
    email_body: string;
    subject: string;
    send_as_user?: number | null;
    reply_to_user?: number | null;
    related_application?: number | null;
    related_borrower?: number | null;
};

