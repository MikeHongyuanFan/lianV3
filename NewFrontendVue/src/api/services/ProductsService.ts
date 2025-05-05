/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedProductList } from '../models/PaginatedProductList';
import type { PatchedProductRequest } from '../models/PatchedProductRequest';
import type { Product } from '../models/Product';
import type { ProductRequest } from '../models/ProductRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ProductsService {
    /**
     * API endpoint for managing loan products
     * @param application
     * @param applications
     * @param borrower
     * @param borrowers
     * @param name
     * @param nameIcontains
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedProductList
     * @throws ApiError
     */
    public static productsProductsList(
        application?: number,
        applications?: Array<number>,
        borrower?: number,
        borrowers?: Array<number>,
        name?: string,
        nameIcontains?: string,
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedProductList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/products/products/',
            query: {
                'application': application,
                'applications': applications,
                'borrower': borrower,
                'borrowers': borrowers,
                'name': name,
                'name__icontains': nameIcontains,
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * API endpoint for managing loan products
     * @param requestBody
     * @returns Product
     * @throws ApiError
     */
    public static productsProductsCreate(
        requestBody: ProductRequest,
    ): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/products/products/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing loan products
     * @param id A unique integer value identifying this Product.
     * @returns Product
     * @throws ApiError
     */
    public static productsProductsRetrieve(
        id: number,
    ): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/products/products/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * API endpoint for managing loan products
     * @param id A unique integer value identifying this Product.
     * @param requestBody
     * @returns Product
     * @throws ApiError
     */
    public static productsProductsUpdate(
        id: number,
        requestBody: ProductRequest,
    ): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/products/products/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing loan products
     * @param id A unique integer value identifying this Product.
     * @param requestBody
     * @returns Product
     * @throws ApiError
     */
    public static productsProductsPartialUpdate(
        id: number,
        requestBody?: PatchedProductRequest,
    ): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/products/products/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * API endpoint for managing loan products
     * @param id A unique integer value identifying this Product.
     * @returns void
     * @throws ApiError
     */
    public static productsProductsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/products/products/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
