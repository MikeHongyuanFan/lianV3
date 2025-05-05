/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RoleEnum } from './RoleEnum';
/**
 * Serializer for creating users
 */
export type UserCreate = {
    readonly id: number;
    email: string;
    first_name?: string;
    last_name?: string;
    role?: RoleEnum;
    phone?: string | null;
    username?: string;
};

