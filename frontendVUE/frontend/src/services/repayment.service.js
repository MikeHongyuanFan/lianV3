import api from './api'

/**
 * Repayment service for handling repayment-related API calls
 */
class RepaymentService {
  /**
   * Get list of repayments with optional filters
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with repayments response
   */
  async getRepayments(params = {}) {
    try {
      const response = await api.get('/documents/repayments/', { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get repayment details by ID
   * @param {number} id - Repayment ID
   * @returns {Promise} - Promise with repayment details
   */
  async getRepaymentById(id) {
    try {
      const response = await api.get(`/documents/repayments/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Create a new repayment
   * @param {Object} repaymentData - Repayment data
   * @returns {Promise} - Promise with created repayment
   */
  async createRepayment(repaymentData) {
    try {
      const response = await api.post('/documents/repayments/', repaymentData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update an existing repayment
   * @param {number} id - Repayment ID
   * @param {Object} repaymentData - Updated repayment data
   * @returns {Promise} - Promise with updated repayment
   */
  async updateRepayment(id, repaymentData) {
    try {
      const response = await api.patch(`/documents/repayments/${id}/`, repaymentData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Delete a repayment
   * @param {number} id - Repayment ID
   * @returns {Promise} - Promise with deletion response
   */
  async deleteRepayment(id) {
    try {
      const response = await api.delete(`/documents/repayments/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Mark a repayment as paid
   * @param {number} id - Repayment ID
   * @param {Object} paymentData - Payment data (paid_date)
   * @returns {Promise} - Promise with updated repayment
   */
  async markRepaymentPaid(id, paymentData = {}) {
    try {
      const response = await api.post(`/documents/repayments/${id}/mark-paid/`, paymentData)
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

export default new RepaymentService()
