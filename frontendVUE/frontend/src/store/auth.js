import { defineStore } from 'pinia'
import AuthService from '../services/auth.service'

/**
 * Authentication store for managing user authentication state
 * Uses the AuthService to interact with the authentication API endpoints
 */
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    userRole: (state) => state.user?.role || null,
    userName: (state) => state.user?.name || null,
    userId: (state) => state.user?.id || null
  },
  
  actions: {
    /**
     * Login user with email and password
     * @param {string} email - User email
     * @param {string} password - User password
     * @returns {Promise} - Promise with login response
     */
    async login(email, password) {
      this.loading = true
      this.error = null
      
      try {
        const data = await AuthService.login(email, password)
        this.accessToken = data.access
        this.refreshToken = data.refresh
        this.user = {
          id: data.user_id,
          email: data.email,
          role: data.role,
          name: data.name
        }
        return data
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    
    /**
     * Register a new user
     * @param {Object} userData - User registration data
     * @returns {Promise} - Promise with registration response
     */
    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        const data = await AuthService.register(userData)
        this.accessToken = data.access
        this.refreshToken = data.refresh
        this.user = {
          id: data.user_id,
          email: data.email,
          role: data.role,
          name: data.name
        }
        return data
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    
    /**
     * Refresh authentication token
     * @returns {Promise} - Promise with refresh response
     */
    async refreshToken() {
      this.loading = true
      
      try {
        const data = await AuthService.refreshToken()
        this.accessToken = data.access
        return data
      } catch (error) {
        this.logout()
        throw error
      } finally {
        this.loading = false
      }
    },
    
    /**
     * Get current user profile
     * @returns {Promise} - Promise with user profile data
     */
    async getUserProfile() {
      this.loading = true
      
      try {
        const data = await AuthService.getUserProfile()
        // Update user data with additional profile information
        this.user = {
          ...this.user,
          first_name: data.first_name,
          last_name: data.last_name,
          phone: data.phone
        }
        return data
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    
    /**
     * Update user profile
     * @param {Object} profileData - Profile data to update
     * @returns {Promise} - Promise with updated profile data
     */
    async updateUserProfile(profileData) {
      this.loading = true
      this.error = null
      
      try {
        const data = await AuthService.updateUserProfile(profileData)
        // Update user data with updated profile information
        this.user = {
          ...this.user,
          first_name: data.first_name,
          last_name: data.last_name,
          email: data.email,
          phone: data.phone
        }
        return data
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    
    /**
     * Logout current user
     */
    logout() {
      AuthService.logout()
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      this.error = null
    },
    
    /**
     * Clear error state
     */
    clearError() {
      this.error = null
    }
  }
})
