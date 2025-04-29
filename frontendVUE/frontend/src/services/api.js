import axios from 'axios'
import AuthService from './auth.service'

// Create axios instance with base URL
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Log the API URL being used (for debugging)
console.log('API URL:', import.meta.env.VITE_API_URL || 'http://localhost:8000/api')

// Request interceptor for adding auth token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor for token refresh
api.interceptors.response.use(
  response => {
    return response
  },
  async error => {
    const originalRequest = error.config
    
    // If error is 401 and not already retrying
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        // Use the AuthService to refresh the token
        // This ensures we're using the correct endpoint as defined in the API documentation
        const refreshResponse = await AuthService.refreshToken()
        
        // If successful, update authorization header and retry original request
        originalRequest.headers['Authorization'] = `Bearer ${refreshResponse.access}`
        return api(originalRequest)
      } catch (refreshError) {
        // If refresh fails, logout and redirect to login
        AuthService.logout()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
