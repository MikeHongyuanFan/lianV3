/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { User } from './User';
/**
 * Serializer for funding calculation history
 */
export type FundingCalculationHistory = {
    readonly id: number;
    application: number;
    /**
     * Full set of manual input fields used during calculation
     */
    calculation_input: any;
    /**
     * Computed funding breakdown (all fees, funds available)
     */
    calculation_result: any;
    readonly created_by: number | null;
    readonly created_by_details: User;
    readonly created_at: string;
};

