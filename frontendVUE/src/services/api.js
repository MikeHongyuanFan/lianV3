import axios from 'axios'
import { useAuthStore } from '../store/auth'

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
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
    
    // If there's no response, it's likely a network error
    if (!error.response) {
      console.error('Network Error: Unable to connect to the API server')
      return Promise.reject({
        ...error,
        message: 'Unable to connect to the server. Please check your internet connection.'
      })
    }
    
    // Handle different types of errors based on status code
    switch (error.response.status) {
      case 400: // Bad Request
        console.error('Bad Request:', error.response.data)
        return Promise.reject({
          ...error,
          message: 'The request was invalid. Please check your input and try again.'
        })
        
      case 401: // Unauthorized
        // If not already retrying and we have a refresh token
        if (!originalRequest._retry && authStore.refreshToken) {
          originalRequest._retry = true
          
          try {
            // Try to refresh the token
            const response = await axios.post(
              `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/users/auth/refresh/`,
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
            console.error('Token refresh failed:', refreshError)
            authStore.logout()
            return Promise.reject({
              ...error,
              message: 'Your session has expired. Please log in again.'
            })
          }
        } else {
          // If already retrying or no refresh token, logout user
          authStore.logout()
          return Promise.reject({
            ...error,
            message: 'Authentication required. Please log in.'
          })
        }
        
      case 403: // Forbidden
        console.error('Forbidden:', error.response.data)
        return Promise.reject({
          ...error,
          message: 'You do not have permission to perform this action.'
        })
        
      case 404: // Not Found
        console.error('Not Found:', error.response.data)
        return Promise.reject({
          ...error,
          message: 'The requested resource was not found.'
        })
        
      case 500: // Server Error
      case 502: // Bad Gateway
      case 503: // Service Unavailable
      case 504: // Gateway Timeout
        console.error('Server Error:', error.response.data)
        return Promise.reject({
          ...error,
          message: 'A server error occurred. Please try again later.'
        })
        
      default:
        console.error('API Error:', error.response.data)
        return Promise.reject(error)
    }
  }
)

export default api






