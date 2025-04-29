/**
 * User interface representing the current authenticated user
 */
export interface User {
  id: number;
  email: string;
  role: string;
  name: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
}

/**
 * Authentication state for the auth store
 */
export interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  loading: boolean;
  error: AuthError | null;
}

/**
 * Standardized error format for authentication errors
 */
export interface AuthError {
  status: number;
  message: string;
  errors?: Record<string, string | string[]>;
}

/**
 * Login credentials for authentication
 * Based on API documentation for /api/users/auth/login/
 */
export interface LoginCredentials {
  email: string;
  password: string;
}

/**
 * Registration data for new user creation
 * Based on API documentation for /api/users/auth/register/
 */
export interface RegisterData {
  first_name: string;
  last_name: string;
  email: string;
  role: string;
  password: string;
  password2: string;
}

/**
 * Profile update data for updating user profiles
 * Based on API documentation for /api/users/profile/update/
 */
export interface ProfileUpdateData {
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
}

/**
 * Login response from the API
 * Based on API documentation for /api/users/auth/login/ and /api/users/auth/register/
 */
export interface LoginResponse {
  access: string;
  refresh: string;
  user_id: number;
  email: string;
  role: string;
  name: string;
}

/**
 * Refresh token response from the API
 * Based on API documentation for /api/users/auth/refresh/
 */
export interface RefreshTokenResponse {
  access: string;
}

/**
 * User profile data
 * Based on API documentation for /api/users/profile/
 */
export interface UserProfile {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  phone: string;
}

/**
 * Valid user roles in the system
 * Based on API documentation
 */
export type UserRole = 'admin' | 'broker' | 'bd' | 'client';

/**
 * Permission interface for role-based access control
 */
export interface Permission {
  name: string;
  description: string;
}

/**
 * Role permissions mapping
 */
export interface RolePermissions {
  [key: string]: Permission[];
}