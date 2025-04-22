import { describe, it, expect, vi, beforeEach } from 'vitest'
import applicationService from '../applicationService'
import api from '../api'

// Mock api
vi.mock('../api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn()
  }
}))

describe('Application Service', () => {
  beforeEach(() => {
    // Reset mocks
    vi.clearAllMocks()
  })
  
  describe('getApplications', () => {
    it('calls the correct API endpoint with no filters', async () => {
      // Setup
      api.get.mockResolvedValue({ data: [] })
      
      // Execute
      await applicationService.getApplications()
      
      // Verify
      expect(api.get).toHaveBeenCalledWith('/applications/')
    })
    
    it('calls the correct API endpoint with filters', async () => {
      // Setup
      api.get.mockResolvedValue({ data: [] })
      const filters = { stage: 'inquiry', broker: 1 }
      
      // Execute
      await applicationService.getApplications(filters)
      
      // Verify
      expect(api.get).toHaveBeenCalledWith('/applications/?stage=inquiry&broker=1')
    })
  })
  
  describe('getApplication', () => {
    it('calls the correct API endpoint with ID', async () => {
      // Setup
      api.get.mockResolvedValue({ data: {} })
      const id = 123
      
      // Execute
      await applicationService.getApplication(id)
      
      // Verify
      expect(api.get).toHaveBeenCalledWith('/applications/123/')
    })
  })
  
  describe('createApplication', () => {
    it('calls the correct API endpoint with data', async () => {
      // Setup
      api.post.mockResolvedValue({ data: {} })
      const applicationData = {
        loan_amount: 500000,
        loan_term: 30,
        purpose: 'Purchase'
      }
      
      // Execute
      await applicationService.createApplication(applicationData)
      
      // Verify
      expect(api.post).toHaveBeenCalledWith('/applications/', applicationData)
    })
  })
  
  describe('updateApplication', () => {
    it('calls the correct API endpoint with ID and data', async () => {
      // Setup
      api.put.mockResolvedValue({ data: {} })
      const id = 123
      const applicationData = {
        loan_amount: 600000,
        purpose: 'Refinance'
      }
      
      // Execute
      await applicationService.updateApplication(id, applicationData)
      
      // Verify
      expect(api.put).toHaveBeenCalledWith('/applications/123/', applicationData)
    })
  })
  
  describe('updateApplicationStage', () => {
    it('calls the correct API endpoint with ID and stage', async () => {
      // Setup
      api.post.mockResolvedValue({ data: {} })
      const id = 123
      const stage = 'pre_approval'
      
      // Execute
      await applicationService.updateApplicationStage(id, stage)
      
      // Verify
      expect(api.post).toHaveBeenCalledWith('/applications/123/update_stage/', { stage })
    })
  })
  
  describe('addBorrowers', () => {
    it('calls the correct API endpoint with ID and borrower IDs', async () => {
      // Setup
      api.post.mockResolvedValue({ data: {} })
      const id = 123
      const borrowerIds = [1, 2, 3]
      
      // Execute
      await applicationService.addBorrowers(id, borrowerIds)
      
      // Verify
      expect(api.post).toHaveBeenCalledWith('/applications/123/add_borrowers/', { borrower_ids: borrowerIds })
    })
  })
  
  describe('removeBorrowers', () => {
    it('calls the correct API endpoint with ID and borrower IDs', async () => {
      // Setup
      api.post.mockResolvedValue({ data: {} })
      const id = 123
      const borrowerIds = [1, 2]
      
      // Execute
      await applicationService.removeBorrowers(id, borrowerIds)
      
      // Verify
      expect(api.post).toHaveBeenCalledWith('/applications/123/remove_borrowers/', { borrower_ids: borrowerIds })
    })
  })
  
  describe('processSignature', () => {
    it('calls the correct API endpoint with ID, signature data, and signed by', async () => {
      // Setup
      api.post.mockResolvedValue({ data: {} })
      const id = 123
      const signatureData = 'base64-encoded-signature'
      const signedBy = 'John Doe'
      
      // Execute
      await applicationService.processSignature(id, signatureData, signedBy)
      
      // Verify
      expect(api.post).toHaveBeenCalledWith('/applications/123/process_signature/', {
        signature_data: signatureData,
        signed_by: signedBy
      })
    })
  })
  
  describe('uploadDocuments', () => {
    it('calls the correct API endpoint with ID and form data', async () => {
      // Setup
      api.post.mockResolvedValue({ data: {} })
      const id = 123
      const formData = new FormData()
      
      // Execute
      await applicationService.uploadDocuments(id, formData)
      
      // Verify
      expect(api.post).toHaveBeenCalledWith('/applications/123/upload_document/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    })
  })
  
  describe('uploadSignature', () => {
    it('calls the correct API endpoint with ID and form data', async () => {
      // Setup
      api.post.mockResolvedValue({ data: {} })
      const id = 123
      const formData = new FormData()
      
      // Execute
      await applicationService.uploadSignature(id, formData)
      
      // Verify
      expect(api.post).toHaveBeenCalledWith('/applications/123/signature/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    })
  })
  
  describe('getDocuments', () => {
    it('calls the correct API endpoint with ID', async () => {
      // Setup
      api.get.mockResolvedValue({ data: [] })
      const id = 123
      
      // Execute
      await applicationService.getDocuments(id)
      
      // Verify
      expect(api.get).toHaveBeenCalledWith('/applications/123/documents/')
    })
  })
  
  describe('getNotes', () => {
    it('calls the correct API endpoint with ID', async () => {
      // Setup
      api.get.mockResolvedValue({ data: [] })
      const id = 123
      
      // Execute
      await applicationService.getNotes(id)
      
      // Verify
      expect(api.get).toHaveBeenCalledWith('/applications/123/notes/')
    })
  })
  
  describe('addNote', () => {
    it('calls the correct API endpoint with ID and note data', async () => {
      // Setup
      api.post.mockResolvedValue({ data: {} })
      const id = 123
      const noteData = {
        content: 'Test note',
        remind_date: '2023-01-01'
      }
      
      // Execute
      await applicationService.addNote(id, noteData)
      
      // Verify
      expect(api.post).toHaveBeenCalledWith('/applications/123/add_note/', noteData)
    })
  })
  
  describe('deleteApplication', () => {
    it('calls the correct API endpoint with ID', async () => {
      // Setup
      api.delete.mockResolvedValue({ data: {} })
      const id = 123
      
      // Execute
      await applicationService.deleteApplication(id)
      
      // Verify
      expect(api.delete).toHaveBeenCalledWith('/applications/123/')
    })
  })
})

