import axios from 'axios'

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
        // Try to refresh the token
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) {
          throw new Error('No refresh token available')
        }
        
        // Make a direct axios call to refresh endpoint to avoid circular dependency
        const refreshResponse = await axios.post(
          `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/users/auth/refresh/`,
          { refresh: refreshToken },
          { headers: { 'Content-Type': 'application/json' } }
        )
        
        // If successful, update tokens and retry original request
        if (refreshResponse.data && refreshResponse.data.access) {
          localStorage.setItem('access_token', refreshResponse.data.access)
          
          // Update authorization header and retry original request
          api.defaults.headers.common['Authorization'] = `Bearer ${refreshResponse.data.access}`
          originalRequest.headers['Authorization'] = `Bearer ${refreshResponse.data.access}`
          
          return api(originalRequest)
        } else {
          throw new Error('Failed to refresh token')
        }
      } catch (refreshError) {
        // If refresh fails, clear tokens and redirect to login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        
        // Only redirect to login if we're in a browser environment
        if (typeof window !== 'undefined') {
          window.location.href = '/login'
        }
        
        return Promise.reject(refreshError)
      }
    }
    
    // For all other errors, just reject the promise
    return Promise.reject(error)
  }
)

export default api
