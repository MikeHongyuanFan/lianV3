import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'
import api from '../api'
import authService from '../auth'
import applicationService from '../applicationService'

// Mock axios for testing
vi.mock('axios', () => {
  return {
    default: {
      create: vi.fn(() => ({
        interceptors: {
          request: { use: vi.fn() },
          response: { use: vi.fn() }
        },
        get: vi.fn(),
        post: vi.fn(),
        put: vi.fn(),
        delete: vi.fn()
      })),
      post: vi.fn()
    }
  }
})

describe('Backend API Connection Tests', () => {
  let axiosInstance;
  
  beforeEach(() => {
    vi.clearAllMocks();
    axiosInstance = axios.create();
  });
  
  describe('Authentication Endpoints', () => {
    it('should call the correct login endpoint', async () => {
      // Setup
      const credentials = { email: 'test@example.com', password: 'password123' };
      axiosInstance.post.mockResolvedValue({ data: { access: 'token', refresh: 'refresh' } });
      
      // Execute
      await authService.login(credentials);
      
      // Verify
      expect(axiosInstance.post).toHaveBeenCalledWith('/api/users/auth/login/', credentials);
    });
    
    it('should call the correct register endpoint', async () => {
      // Setup
      const userData = { 
        email: 'new@example.com', 
        password: 'password123',
        name: 'Test User',
        role: 'client'
      };
      axiosInstance.post.mockResolvedValue({ data: { access: 'token', refresh: 'refresh' } });
      
      // Execute
      await authService.register(userData);
      
      // Verify
      expect(axiosInstance.post).toHaveBeenCalledWith('/api/users/auth/register/', userData);
    });
    
    it('should call the correct token refresh endpoint', async () => {
      // Setup
      const refreshToken = { refresh: 'refresh-token' };
      axiosInstance.post.mockResolvedValue({ data: { access: 'new-token' } });
      
      // Execute
      await authService.refreshToken(refreshToken);
      
      // Verify
      expect(axiosInstance.post).toHaveBeenCalledWith('/api/users/auth/refresh/', refreshToken);
    });
  });
  
  describe('Application Endpoints', () => {
    it('should call the correct applications list endpoint', async () => {
      // Setup
      axiosInstance.get.mockResolvedValue({ data: [] });
      
      // Execute
      await applicationService.getApplications();
      
      // Verify
      expect(axiosInstance.get).toHaveBeenCalledWith('/api/applications/');
    });
    
    it('should call the correct application detail endpoint', async () => {
      // Setup
      const id = 123;
      axiosInstance.get.mockResolvedValue({ data: {} });
      
      // Execute
      await applicationService.getApplication(id);
      
      // Verify
      expect(axiosInstance.get).toHaveBeenCalledWith('/api/applications/123/');
    });
    
    it('should call the correct application create endpoint', async () => {
      // Setup
      const applicationData = { loan_amount: 500000 };
      axiosInstance.post.mockResolvedValue({ data: {} });
      
      // Execute
      await applicationService.createApplication(applicationData);
      
      // Verify
      expect(axiosInstance.post).toHaveBeenCalledWith('/api/applications/', applicationData);
    });
  });
  
  describe('API Base URL Configuration', () => {
    it('should use the correct base URL for API requests', () => {
      // Check that axios.create was called with the correct baseURL
      expect(axios.create).toHaveBeenCalledWith(expect.objectContaining({
        baseURL: expect.stringMatching(/^https?:\/\/.+|http:\/\/localhost:8000$/)
      }));
    });
  });
});