import axios from 'axios'
import { useAuthStore } from '../store/auth'

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Add request interceptor for authentication
api.interceptors.request.use(
  config => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers['Authorization'] = `Bearer ${authStore.token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Add response interceptor for token refresh
api.interceptors.response.use(
  response => {
    return response
  },
  async error => {
    const originalRequest = error.config
    const authStore = useAuthStore()
    
    // If error is 401 and not already retrying
    if (error.response.status === 401 && !originalRequest._retry && authStore.refreshToken) {
      originalRequest._retry = true
      
      try {
        // Try to refresh the token
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/users/token/refresh/`,
          { refresh: authStore.refreshToken }
        )
        
        // Update tokens in store
        authStore.setTokens(response.data.access, authStore.refreshToken)
        
        // Update authorization header
        originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`
        
        // Retry the original request
        return api(originalRequest)
      } catch (refreshError) {
        // If refresh fails, logout user
        authStore.logout()
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
