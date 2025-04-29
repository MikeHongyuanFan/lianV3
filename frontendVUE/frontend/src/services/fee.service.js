import api from './api'

/**
 * Fee service for handling fee-related API calls
 */
class FeeService {
  /**
   * Get list of fees with optional filters
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with fees response
   */
  async getFees(params = {}) {
    try {
      const response = await api.get('/documents/fees/', { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get fee details by ID
   * @param {number} id - Fee ID
   * @returns {Promise} - Promise with fee details
   */
  async getFeeById(id) {
    try {
      const response = await api.get(`/documents/fees/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Create a new fee
   * @param {Object} feeData - Fee data
   * @returns {Promise} - Promise with created fee
   */
  async createFee(feeData) {
    try {
      const response = await api.post('/documents/fees/', feeData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update an existing fee
   * @param {number} id - Fee ID
   * @param {Object} feeData - Updated fee data
   * @returns {Promise} - Promise with updated fee
   */
  async updateFee(id, feeData) {
    try {
      const response = await api.patch(`/documents/fees/${id}/`, feeData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Delete a fee
   * @param {number} id - Fee ID
   * @returns {Promise} - Promise with deletion response
   */
  async deleteFee(id) {
    try {
      const response = await api.delete(`/documents/fees/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Mark a fee as paid
   * @param {number} id - Fee ID
   * @param {Object} paymentData - Payment data (paid_date)
   * @returns {Promise} - Promise with updated fee
   */
  async markFeePaid(id, paymentData = {}) {
    try {
      const response = await api.post(`/documents/fees/${id}/mark-paid/`, paymentData)
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

export default new FeeService()
