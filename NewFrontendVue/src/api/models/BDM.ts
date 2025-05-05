/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Branch } from './Branch';
import type { User } from './User';
/**
 * Serializer for BDM information
 */
export type BDM = {
    readonly id: number;
    readonly branch: Branch;
    readonly created_by: User;
    name: string;
    email?: string | null;
    phone?: string | null;
    readonly created_at: string;
    readonly updated_at: string;
    user?: number | null;
};

