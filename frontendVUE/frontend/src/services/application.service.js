import api from './api'

/**
 * Application service for handling application-related API calls
 */
class ApplicationService {
  /**
   * Get list of applications with optional filters
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with applications response
   */
  async getApplications(params = {}) {
    try {
      // First check if we need to use the nested endpoint
      const response = await api.get('/applications/applications/', { params })
      // Ensure we always return an object with results array and count
      return {
        results: Array.isArray(response.data.results) ? response.data.results : [],
        count: response.data.count || 0
      }
    } catch (error) {
      console.error('Error fetching applications:', error)
      // Return empty results on error
      return {
        results: [],
        count: 0
      }
    }
  }

  /**
   * Get application details by ID
   * @param {number} id - Application ID
   * @returns {Promise} - Promise with application details
   */
  async getApplicationById(id) {
    try {
      const response = await api.get(`/applications/applications/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Create a new application
   * @param {Object} applicationData - Application data
   * @returns {Promise} - Promise with created application
   */
  async createApplication(applicationData) {
    try {
      const response = await api.post('/applications/', applicationData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Create application with cascade (including related entities)
   * @param {Object} applicationData - Application data with related entities
   * @returns {Promise} - Promise with created application
   */
  async createApplicationWithCascade(applicationData) {
    try {
      const response = await api.post('/applications/create-with-cascade/', applicationData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update an existing application
   * @param {number} id - Application ID
   * @param {Object} applicationData - Updated application data
   * @returns {Promise} - Promise with updated application
   */
  async updateApplication(id, applicationData) {
    try {
      const response = await api.patch(`/applications/${id}/`, applicationData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Delete an application
   * @param {number} id - Application ID
   * @returns {Promise} - Promise with deletion response
   */
  async deleteApplication(id) {
    try {
      const response = await api.delete(`/applications/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Validate application schema
   * @param {Object} schemaData - Schema data to validate
   * @returns {Promise} - Promise with validation response
   */
  async validateSchema(schemaData) {
    try {
      const response = await api.post('/applications/validate-schema/', schemaData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update application stage
   * @param {number} id - Application ID
   * @param {Object} stageData - Stage data
   * @returns {Promise} - Promise with updated stage response
   */
  async updateStage(id, stageData) {
    try {
      const response = await api.put(`/applications/${id}/stage/`, stageData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update application borrowers
   * @param {number} id - Application ID
   * @param {Object} borrowerData - Borrower data
   * @returns {Promise} - Promise with updated borrowers response
   */
  async updateBorrowers(id, borrowerData) {
    try {
      const response = await api.put(`/applications/${id}/borrowers/`, borrowerData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Sign application
   * @param {number} id - Application ID
   * @param {Object} signatureData - Signature data
   * @returns {Promise} - Promise with signature response
   */
  async signApplication(id, signatureData) {
    try {
      const response = await api.post(`/applications/${id}/signature/`, signatureData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get application guarantors
   * @param {number} id - Application ID
   * @returns {Promise} - Promise with guarantors response
   */
  async getGuarantors(id) {
    try {
      const response = await api.get(`/applications/${id}/guarantors/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get application notes
   * @param {number} id - Application ID
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with notes response
   */
  async getNotes(id, params = {}) {
    try {
      const response = await api.get(`/applications/${id}/notes/`, { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Add note to application
   * @param {number} id - Application ID
   * @param {Object} noteData - Note data
   * @returns {Promise} - Promise with created note
   */
  async addNote(id, noteData) {
    try {
      const response = await api.post(`/applications/${id}/add-note/`, noteData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get application documents
   * @param {number} id - Application ID
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with documents response
   */
  async getDocuments(id, params = {}) {
    try {
      const response = await api.get(`/applications/${id}/documents/`, { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Upload document to application
   * @param {number} id - Application ID
   * @param {FormData} documentData - Document form data
   * @returns {Promise} - Promise with uploaded document
   */
  async uploadDocument(id, documentData) {
    try {
      const response = await api.post(`/applications/${id}/upload-document/`, documentData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get application fees
   * @param {number} id - Application ID
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with fees response
   */
  async getFees(id, params = {}) {
    try {
      const response = await api.get(`/applications/${id}/fees/`, { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Add fee to application
   * @param {number} id - Application ID
   * @param {Object} feeData - Fee data
   * @returns {Promise} - Promise with created fee
   */
  async addFee(id, feeData) {
    try {
      const response = await api.post(`/applications/${id}/add-fee/`, feeData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get application repayments
   * @param {number} id - Application ID
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with repayments response
   */
  async getRepayments(id, params = {}) {
    try {
      const response = await api.get(`/applications/${id}/repayments/`, { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Add repayment to application
   * @param {number} id - Application ID
   * @param {Object} repaymentData - Repayment data
   * @returns {Promise} - Promise with created repayment
   */
  async addRepayment(id, repaymentData) {
    try {
      const response = await api.post(`/applications/${id}/add-repayment/`, repaymentData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Record payment for application
   * @param {number} id - Application ID
   * @param {Object} paymentData - Payment data
   * @returns {Promise} - Promise with payment response
   */
  async recordPayment(id, paymentData) {
    try {
      const response = await api.post(`/applications/${id}/record-payment/`, paymentData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get application ledger
   * @param {number} id - Application ID
   * @param {number} limit - Number of entries to return
   * @param {number} offset - Offset for pagination
   * @param {Object} params - Additional query parameters
   * @returns {Promise} - Promise with ledger response
   */
  async getLedger(id, limit = 10, offset = 0, params = {}) {
    try {
      const queryParams = { 
        limit, 
        offset,
        ...params
      }
      const response = await api.get(`/applications/${id}/ledger/`, { params: queryParams })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Handle API errors
   * @param {Error} error - Error object
   * @returns {Error} - Processed error
   */
  handleError(error) {
    if (error.response) {
      // Server responded with error status
      return {
        status: error.response.status,
        message: error.response.data.detail || 'An error occurred',
        errors: error.response.data
      }
    } else if (error.request) {
      // Request made but no response received
      return {
        status: 0,
        message: 'No response from server. Please check your internet connection.'
      }
    } else {
      // Error in request setup
      return {
        status: 0,
        message: error.message || 'An unexpected error occurred'
      }
    }
  }
}

export default new ApplicationService()


