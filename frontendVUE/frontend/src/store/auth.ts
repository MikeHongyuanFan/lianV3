import { defineStore } from 'pinia'
import AuthService from '../services/auth.service'
import { 
  AuthState, 
  User, 
  LoginCredentials, 
  RegisterData, 
  ProfileUpdateData,
  UserRole
} from '../types/auth'

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state): boolean => !!state.accessToken,
    userRole: (state): UserRole | null => state.user?.role as UserRole || null,
    userName: (state): string | null => state.user?.name || null,
    userId: (state): number | null => state.user?.id || null,
    
    // Role-based permission checks
    isAdmin: (state): boolean => state.user?.role === 'admin',
    isBroker: (state): boolean => state.user?.role === 'broker',
    isBD: (state): boolean => state.user?.role === 'bd',
    isClient: (state): boolean => state.user?.role === 'client',
    
    // Check if user has permission to access a specific feature
    hasPermission: (state) => (permission: string): boolean => {
      // Define permissions for each role
      const rolePermissions: Record<string, string[]> = {
        admin: ['manage_users', 'view_all_applications', 'manage_brokers', 'view_reports', 'manage_system'],
        broker: ['view_own_applications', 'create_applications', 'manage_borrowers', 'manage_guarantors'],
        bd: ['view_assigned_applications', 'update_application_status', 'view_brokers'],
        client: ['view_own_applications', 'view_own_profile', 'update_own_profile']
      }
      
      const userRole = state.user?.role
      if (!userRole) return false
      
      // Admin has all permissions
      if (userRole === 'admin') return true
      
      // Check if the user's role has the requested permission
      return rolePermissions[userRole]?.includes(permission) || false
    }
  },
  
  actions: {
    async login(email: string, password: string) {
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
      } catch (error: any) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async register(userData: RegisterData) {
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
      } catch (error: any) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    
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
    
    async getUserProfile() {
      this.loading = true
      
      try {
        const data = await AuthService.getUserProfile()
        // Update user data with additional profile information
        if (this.user) {
          this.user = {
            ...this.user,
            first_name: data.first_name,
            last_name: data.last_name,
            phone: data.phone
          }
        }
        return data
      } catch (error: any) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateUserProfile(profileData: ProfileUpdateData) {
      this.loading = true
      this.error = null
      
      try {
        const data = await AuthService.updateUserProfile(profileData)
        // Update user data with updated profile information
        if (this.user) {
          this.user = {
            ...this.user,
            first_name: data.first_name,
            last_name: data.last_name,
            email: data.email,
            phone: data.phone
          }
        }
        return data
      } catch (error: any) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // Admin actions for user management
    async getUsers(limit = 10, offset = 0, search = '', role = '') {
      this.loading = true
      this.error = null
      
      try {
        return await AuthService.getUsers(limit, offset, search, role)
      } catch (error: any) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async getUserById(id: number) {
      this.loading = true
      this.error = null
      
      try {
        return await AuthService.getUserById(id)
      } catch (error: any) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateUser(id: number, userData: ProfileUpdateData) {
      this.loading = true
      this.error = null
      
      try {
        return await AuthService.updateUser(id, userData)
      } catch (error: any) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteUser(id: number) {
      this.loading = true
      this.error = null
      
      try {
        await AuthService.deleteUser(id)
      } catch (error: any) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    
    logout() {
      AuthService.logout()
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      this.error = null
    },
    
    clearError() {
      this.error = null
    }
  }
})