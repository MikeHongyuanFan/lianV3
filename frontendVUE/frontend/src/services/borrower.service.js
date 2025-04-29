import api from './api'

/**
 * Borrower service for handling borrower-related API calls
 */
class BorrowerService {
  /**
   * Get list of borrowers with optional filters
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with borrowers response
   */
  async getBorrowers(params = {}) {
    try {
      const response = await api.get('/borrowers/', { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get borrower details by ID
   * @param {number} id - Borrower ID
   * @returns {Promise} - Promise with borrower details
   */
  async getBorrowerById(id) {
    try {
      const response = await api.get(`/borrowers/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Create a new borrower
   * @param {Object} borrowerData - Borrower data
   * @returns {Promise} - Promise with created borrower
   */
  async createBorrower(borrowerData) {
    try {
      const response = await api.post('/borrowers/', borrowerData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update an existing borrower
   * @param {number} id - Borrower ID
   * @param {Object} borrowerData - Updated borrower data
   * @returns {Promise} - Promise with updated borrower
   */
  async updateBorrower(id, borrowerData) {
    try {
      const response = await api.patch(`/borrowers/${id}/`, borrowerData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Delete a borrower
   * @param {number} id - Borrower ID
   * @returns {Promise} - Promise with deletion response
   */
  async deleteBorrower(id) {
    try {
      const response = await api.delete(`/borrowers/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get borrower financial summary
   * @param {number} id - Borrower ID
   * @returns {Promise} - Promise with financial summary
   */
  async getFinancialSummary(id) {
    try {
      const response = await api.get(`/borrowers/${id}/financial-summary/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get borrower applications
   * @param {number} id - Borrower ID
   * @returns {Promise} - Promise with applications
   */
  async getBorrowerApplications(id) {
    try {
      const response = await api.get(`/borrowers/${id}/applications/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get borrower guarantors
   * @param {number} id - Borrower ID
   * @returns {Promise} - Promise with guarantors
   */
  async getBorrowerGuarantors(id) {
    try {
      const response = await api.get(`/borrowers/${id}/guarantors/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get list of company borrowers
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with company borrowers response
   */
  async getCompanyBorrowers(params = {}) {
    try {
      const response = await api.get('/borrowers/company/', { params })
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

export default new BorrowerService()
