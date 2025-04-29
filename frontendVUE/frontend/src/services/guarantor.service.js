import api from './api'

/**
 * Guarantor service for handling guarantor-related API calls
 */
class GuarantorService {
  /**
   * Get list of guarantors with optional filters
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with guarantors response
   */
  async getGuarantors(params = {}) {
    try {
      const response = await api.get('/guarantors/', { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get guarantor details by ID
   * @param {number} id - Guarantor ID
   * @returns {Promise} - Promise with guarantor details
   */
  async getGuarantorById(id) {
    try {
      const response = await api.get(`/guarantors/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Create a new guarantor
   * @param {Object} guarantorData - Guarantor data
   * @returns {Promise} - Promise with created guarantor
   */
  async createGuarantor(guarantorData) {
    try {
      const response = await api.post('/guarantors/', guarantorData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update an existing guarantor
   * @param {number} id - Guarantor ID
   * @param {Object} guarantorData - Updated guarantor data
   * @returns {Promise} - Promise with updated guarantor
   */
  async updateGuarantor(id, guarantorData) {
    try {
      const response = await api.patch(`/guarantors/${id}/`, guarantorData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Delete a guarantor
   * @param {number} id - Guarantor ID
   * @returns {Promise} - Promise with deletion response
   */
  async deleteGuarantor(id) {
    try {
      const response = await api.delete(`/guarantors/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get applications guaranteed by guarantor
   * @param {number} id - Guarantor ID
   * @returns {Promise} - Promise with guaranteed applications
   */
  async getGuaranteedApplications(id) {
    try {
      const response = await api.get(`/guarantors/${id}/guaranteed_applications/`)
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

export default new GuarantorService()
