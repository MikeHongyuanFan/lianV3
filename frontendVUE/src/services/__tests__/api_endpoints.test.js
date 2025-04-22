import { describe, it, expect, vi, beforeEach } from 'vitest'
import authService from '../auth'
import applicationService from '../applicationService'
import notificationService from '../notificationService'
import api from '../api'

// Mock api
vi.mock('../api', () => {
  return {
    default: {
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      patch: vi.fn(),
      delete: vi.fn()
    }
  }
})

describe('API Endpoints Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })
  
  describe('Auth Service', () => {
    it('should call the correct login endpoint', async () => {
      const credentials = { email: 'test@example.com', password: 'password' }
      await authService.login(credentials)
      expect(api.post).toHaveBeenCalledWith('/api/users/auth/login/', credentials)
    })
    
    it('should call the correct register endpoint', async () => {
      const userData = { email: 'test@example.com', password: 'password', name: 'Test User' }
      await authService.register(userData)
      expect(api.post).toHaveBeenCalledWith('/api/users/auth/register/', userData)
    })
    
    it('should call the correct refresh token endpoint', async () => {
      const refreshToken = { refresh: 'refresh-token' }
      await authService.refreshToken(refreshToken)
      expect(api.post).toHaveBeenCalledWith('/api/users/auth/refresh/', refreshToken)
    })
    
    it('should call the correct profile update endpoint', async () => {
      const userData = { name: 'Updated Name' }
      await authService.updateProfile(userData)
      expect(api.patch).toHaveBeenCalledWith('/api/users/profile/update/', userData)
    })
  })
  
  describe('Application Service', () => {
    it('should call the correct application list endpoint', async () => {
      await applicationService.getApplications()
      expect(api.get).toHaveBeenCalledWith('/api/applications/')
    })
    
    it('should call the correct application detail endpoint', async () => {
      const id = 123
      await applicationService.getApplication(id)
      expect(api.get).toHaveBeenCalledWith(`/api/applications/${id}/`)
    })
    
    it('should call the correct application create endpoint', async () => {
      const applicationData = { loan_amount: 500000, purpose: 'Purchase' }
      await applicationService.createApplication(applicationData)
      expect(api.post).toHaveBeenCalledWith('/api/applications/', applicationData)
    })
    
    it('should call the correct application stage update endpoint', async () => {
      const id = 123
      const stage = 'approved'
      await applicationService.updateApplicationStage(id, stage)
      expect(api.post).toHaveBeenCalledWith(`/api/applications/${id}/update_stage/`, { stage })
    })
    
    it('should call the correct signature endpoint', async () => {
      const id = 123
      const signatureData = 'base64-signature'
      const signedBy = 'John Doe'
      await applicationService.processSignature(id, signatureData, signedBy)
      expect(api.post).toHaveBeenCalledWith(`/api/applications/${id}/signature/`, {
        signature_data: signatureData,
        signed_by: signedBy
      })
    })
  })
  
  describe('Notification Service', () => {
    it('should call the correct notifications list endpoint', async () => {
      await notificationService.getNotifications()
      expect(api.get).toHaveBeenCalledWith('/api/users/notifications/')
    })
    
    it('should call the correct mark as read endpoint', async () => {
      const id = 123
      await notificationService.markAsRead(id)
      expect(api.post).toHaveBeenCalledWith(`/api/users/notifications/${id}/mark-read/`)
    })
    
    it('should call the correct mark all as read endpoint', async () => {
      await notificationService.markAllAsRead()
      expect(api.post).toHaveBeenCalledWith('/api/users/notifications/mark-read/')
    })
    
    it('should call the correct notification preferences endpoint', async () => {
      await notificationService.getPreferences()
      expect(api.get).toHaveBeenCalledWith('/api/users/notification-preferences/')
    })
    
    it('should call the correct update preferences endpoint', async () => {
      const preferences = { emailNotifications: true }
      await notificationService.updatePreferences(preferences)
      expect(api.put).toHaveBeenCalledWith('/api/users/notification-preferences/', preferences)
    })
  })
})