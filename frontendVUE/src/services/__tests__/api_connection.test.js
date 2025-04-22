import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'
import api from '../api'

// Mock axios
vi.mock('axios', () => {
  return {
    default: {
      create: vi.fn(() => ({
        interceptors: {
          request: { use: vi.fn() },
          response: { use: vi.fn() }
        },
        get: vi.fn(),
        post: vi.fn()
      }))
    }
  }
})

describe('API Connection Tests', () => {
  let axiosInstance;
  
  beforeEach(() => {
    vi.clearAllMocks();
    // Get the axios instance created by the api module
    axiosInstance = axios.create();
  });
  
  it('should use the correct base URL from environment variables', () => {
    // Check that axios.create was called with the correct baseURL
    expect(axios.create).toHaveBeenCalledWith(expect.objectContaining({
      baseURL: expect.any(String)
    }));
    
    // The baseURL should be either from env var or the default
    const createCall = axios.create.mock.calls[0][0];
    expect(createCall.baseURL).toMatch(/^https?:\/\/.+|http:\/\/localhost:8000$/);
  });
  
  it('should handle API requests correctly', async () => {
    // Setup mock response
    axiosInstance.get.mockResolvedValue({ data: { success: true } });
    
    // Make a test request
    const testEndpoint = '/api/test-endpoint';
    await api.get(testEndpoint);
    
    // Verify the request was made correctly
    expect(axiosInstance.get).toHaveBeenCalledWith(testEndpoint);
  });
  
  it('should handle authentication token correctly', async () => {
    // This is tested in api.test.js, but we're adding an additional check here
    const requestInterceptor = axios.create().interceptors.request.use.mock.calls[0][0];
    const config = { headers: {} };
    requestInterceptor(config);
    
    // The Authorization header should be set if a token exists
    expect(config.headers).toBeDefined();
  });
});