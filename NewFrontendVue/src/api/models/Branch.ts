/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { User } from './User';
/**
 * Serializer for branch information
 */
export type Branch = {
    readonly id: number;
    readonly created_by: User;
    name: string;
    address?: string | null;
    phone?: string | null;
    email?: string | null;
    readonly created_at: string;
    readonly updated_at: string;
};

