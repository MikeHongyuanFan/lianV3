import api from './api'
import { 
  LoginCredentials, 
  RegisterData, 
  ProfileUpdateData, 
  LoginResponse, 
  RefreshTokenResponse, 
  UserProfile,
  AuthError
} from '../types/auth'

/**
 * Authentication service for handling user authentication operations
 * Based on the API documentation at /api/users/auth/ endpoints
 */
class AuthService {
  /**
   * Login user with email and password
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise<LoginResponse>} - Promise with login response
   */
  async login(email: string, password: string): Promise<LoginResponse> {
    try {
      // Using the exact endpoint from API documentation: /api/users/auth/login/
      const response = await api.post<LoginResponse>('/users/auth/login/', {
        email,
        password
      })
      
      if (response.data.access && response.data.refresh) {
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        localStorage.setItem('user', JSON.stringify({
          id: response.data.user_id,
          email: response.data.email,
          role: response.data.role,
          name: response.data.name
        }))
      }
      
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Register a new user
   * @param {RegisterData} userData - User registration data
   * @returns {Promise<LoginResponse>} - Promise with registration response
   */
  async register(userData: RegisterData): Promise<LoginResponse> {
    try {
      // Using the exact endpoint from API documentation: /api/users/auth/register/
      const response = await api.post<LoginResponse>('/users/auth/register/', userData)
      
      if (response.data.access && response.data.refresh) {
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        localStorage.setItem('user', JSON.stringify({
          id: response.data.user_id,
          email: response.data.email,
          role: response.data.role,
          name: response.data.name
        }))
      }
      
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Refresh authentication token
   * @returns {Promise<RefreshTokenResponse>} - Promise with refresh response
   */
  async refreshToken(): Promise<RefreshTokenResponse> {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        throw new Error('No refresh token available')
      }
      
      // Using the exact endpoint from API documentation: /api/users/auth/refresh/
      const response = await api.post<RefreshTokenResponse>('/users/auth/refresh/', {
        refresh: refreshToken
      })
      
      if (response.data.access) {
        localStorage.setItem('access_token', response.data.access)
      }
      
      return response.data
    } catch (error) {
      this.logout()
      throw this.handleError(error)
    }
  }

  /**
   * Get current user profile
   * @returns {Promise<UserProfile>} - Promise with user profile data
   */
  async getUserProfile(): Promise<UserProfile> {
    try {
      // Using the exact endpoint from API documentation: /api/users/profile/
      const response = await api.get<UserProfile>('/users/profile/')
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update user profile
   * @param {ProfileUpdateData} profileData - Profile data to update
   * @returns {Promise<UserProfile>} - Promise with updated profile data
   */
  async updateUserProfile(profileData: ProfileUpdateData): Promise<UserProfile> {
    try {
      // Using the exact endpoint from API documentation: /api/users/profile/update/
      const response = await api.put<UserProfile>('/users/profile/update/', profileData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get all users (admin only)
   * @param {number} limit - Number of users to fetch
   * @param {number} offset - Offset for pagination
   * @param {string} search - Search term
   * @param {string} role - Filter by role
   * @returns {Promise<{ results: UserProfile[], count: number }>} - Promise with users data
   */
  async getUsers(limit = 10, offset = 0, search = '', role = ''): Promise<{ results: UserProfile[], count: number }> {
    try {
      const params: Record<string, string | number> = { limit, offset }
      if (search) params.search = search
      if (role) params.role = role
      
      // Using the exact endpoint from API documentation: /api/users/users/
      const response = await api.get('/users/users/', { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get user by ID (admin only)
   * @param {number} id - User ID
   * @returns {Promise<UserProfile>} - Promise with user data
   */
  async getUserById(id: number): Promise<UserProfile> {
    try {
      // Using the exact endpoint from API documentation: /api/users/users/{id}/
      const response = await api.get<UserProfile>(`/users/users/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update user by ID (admin only)
   * @param {number} id - User ID
   * @param {ProfileUpdateData} userData - User data to update
   * @returns {Promise<UserProfile>} - Promise with updated user data
   */
  async updateUser(id: number, userData: ProfileUpdateData): Promise<UserProfile> {
    try {
      // Using the exact endpoint from API documentation: /api/users/users/{id}/
      const response = await api.put<UserProfile>(`/users/users/${id}/`, userData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Delete user by ID (admin only)
   * @param {number} id - User ID
   * @returns {Promise<void>} - Promise with deletion response
   */
  async deleteUser(id: number): Promise<void> {
    try {
      // Using the exact endpoint from API documentation: /api/users/users/{id}/
      await api.delete(`/users/users/${id}/`)
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get current user information
   * @returns {Promise<UserProfile>} - Promise with current user data
   */
  async getCurrentUserInfo(): Promise<UserProfile> {
    try {
      // Using the exact endpoint from API documentation: /api/users/users/me/
      const response = await api.get<UserProfile>('/users/users/me/')
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Logout current user
   */
  logout(): void {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }

  /**
   * Check if user is authenticated
   * @returns {boolean} - True if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token')
  }

  /**
   * Get current user data
   * @returns {Object|null} - User data or null if not authenticated
   */
  getCurrentUser() {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  }

  /**
   * Handle API errors
   * @param {any} error - Error object
   * @returns {AuthError} - Processed error
   */
  handleError(error: any): AuthError {
    if (error.response) {
      // Server responded with error status
      return {
        status: error.response.status,
        message: error.response.data.detail || 'An error occurred',
        errors: error.response.data
      }
    } else if (error.request) {
      // Request made but no response received
      return {
        status: 0,
        message: 'No response from server. Please check your internet connection.'
      }
    } else {
      // Error in request setup
      return {
        status: 0,
        message: error.message || 'An unexpected error occurred'
      }
    }
  }
}

export default new AuthService()
