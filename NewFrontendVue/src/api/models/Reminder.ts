/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RecipientTypeEnum } from './RecipientTypeEnum';
/**
 * Serializer for reminders
 */
export type Reminder = {
    readonly id: number;
    recipient_type: RecipientTypeEnum;
    recipient_email: string;
    send_datetime: string;
    email_body: string;
    subject: string;
    readonly created_by: number;
    readonly created_by_name: string;
    send_as_user?: number | null;
    readonly send_as_user_email: string;
    reply_to_user?: number | null;
    readonly reply_to_user_email: string;
    readonly is_sent: boolean;
    readonly sent_at: string | null;
    readonly error_message: string | null;
    related_application?: number | null;
    related_borrower?: number | null;
    readonly created_at: string;
    readonly updated_at: string;
};

