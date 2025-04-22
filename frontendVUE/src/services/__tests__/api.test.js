import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import axios from 'axios'
import api from '../api'
import { useAuthStore } from '../../store/auth'

// Mock axios
vi.mock('axios', () => {
  return {
    default: {
      create: vi.fn(() => ({
        interceptors: {
          request: {
            use: vi.fn()
          },
          response: {
            use: vi.fn()
          }
        }
      }))
    }
  }
})

// Mock Pinia store
vi.mock('../../store/auth', () => ({
  useAuthStore: vi.fn()
}))

describe('API Service', () => {
  beforeEach(() => {
    // Reset mocks
    vi.clearAllMocks()
    
    // Mock auth store
    useAuthStore.mockReturnValue({
      token: 'fake-token',
      refreshToken: 'fake-refresh-token',
      setTokens: vi.fn(),
      logout: vi.fn()
    })
  })
  
  it('creates an axios instance with correct config', () => {
    expect(axios.create).toHaveBeenCalledWith({
      baseURL: expect.any(String),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    })
  })
  
  it('adds auth token to requests when available', () => {
    // Get the request interceptor function
    const requestInterceptor = axios.create().interceptors.request.use.mock.calls[0][0]
    
    // Create a mock config object
    const config = { headers: {} }
    
    // Call the interceptor
    const result = requestInterceptor(config)
    
    // Check that the token was added
    expect(result.headers['Authorization']).toBe('Bearer fake-token')
  })
  
  it('handles 401 errors and attempts token refresh', async () => {
    // Get the response interceptor function
    const responseErrorInterceptor = axios.create().interceptors.response.use.mock.calls[0][1]
    
    // Create a mock error object
    const error = {
      config: { _retry: false },
      response: { status: 401 }
    }
    
    // Mock axios.post for token refresh
    axios.post = vi.fn().mockResolvedValue({
      data: { access: 'new-token' }
    })
    
    // Call the interceptor
    try {
      await responseErrorInterceptor(error)
    } catch (e) {
      // Ignore errors
    }
    
    // Check that token refresh was attempted with correct endpoint
    expect(axios.post).toHaveBeenCalledWith(
      expect.stringContaining('/api/users/auth/refresh/'),
      { refresh: 'fake-refresh-token' }
    )
    expect(useAuthStore().setTokens).toHaveBeenCalledWith('new-token', 'fake-refresh-token')
  })
  
  it('logs out user when token refresh fails', async () => {
    // Get the response interceptor function
    const responseErrorInterceptor = axios.create().interceptors.response.use.mock.calls[0][1]
    
    // Create a mock error object
    const error = {
      config: { _retry: false },
      response: { status: 401 }
    }
    
    // Mock axios.post for token refresh failure
    axios.post = vi.fn().mockRejectedValue(new Error('Refresh failed'))
    
    // Call the interceptor
    try {
      await responseErrorInterceptor(error)
    } catch (e) {
      // Ignore errors
    }
    
    // Check that logout was called
    expect(useAuthStore().logout).toHaveBeenCalled()
  })
})
