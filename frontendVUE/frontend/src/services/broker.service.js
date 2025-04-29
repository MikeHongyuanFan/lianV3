import api from './api'

/**
 * Broker service for handling broker-related API calls
 */
class BrokerService {
  /**
   * Get list of brokers with optional filters
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with brokers response
   */
  async getBrokers(params = {}) {
    try {
      const response = await api.get('/brokers/', { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get broker details by ID
   * @param {number} id - Broker ID
   * @returns {Promise} - Promise with broker details
   */
  async getBrokerById(id) {
    try {
      const response = await api.get(`/brokers/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Create a new broker
   * @param {Object} brokerData - Broker data to create
   * @returns {Promise} - Promise with created broker
   */
  async createBroker(brokerData) {
    try {
      const response = await api.post('/brokers/', brokerData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update an existing broker
   * @param {number} id - Broker ID
   * @param {Object} brokerData - Broker data to update
   * @returns {Promise} - Promise with updated broker
   */
  async updateBroker(id, brokerData) {
    try {
      const response = await api.patch(`/brokers/${id}/`, brokerData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Delete a broker
   * @param {number} id - Broker ID
   * @returns {Promise} - Promise with deletion status
   */
  async deleteBroker(id) {
    try {
      const response = await api.delete(`/brokers/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get list of branches with optional filters
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with branches response
   */
  async getBranches(params = {}) {
    try {
      const response = await api.get('/brokers/branches/', { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get branch details by ID
   * @param {number} id - Branch ID
   * @returns {Promise} - Promise with branch details
   */
  async getBranchById(id) {
    try {
      const response = await api.get(`/brokers/branches/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Create a new branch
   * @param {Object} branchData - Branch data to create
   * @returns {Promise} - Promise with created branch
   */
  async createBranch(branchData) {
    try {
      const response = await api.post('/brokers/branches/', branchData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update an existing branch
   * @param {number} id - Branch ID
   * @param {Object} branchData - Branch data to update
   * @returns {Promise} - Promise with updated branch
   */
  async updateBranch(id, branchData) {
    try {
      const response = await api.patch(`/brokers/branches/${id}/`, branchData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Delete a branch
   * @param {number} id - Branch ID
   * @returns {Promise} - Promise with deletion status
   */
  async deleteBranch(id) {
    try {
      const response = await api.delete(`/brokers/branches/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get list of BDMs with optional filters
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with BDMs response
   */
  async getBDMs(params = {}) {
    try {
      const response = await api.get('/brokers/bdms/', { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get BDM details by ID
   * @param {number} id - BDM ID
   * @returns {Promise} - Promise with BDM details
   */
  async getBDMById(id) {
    try {
      const response = await api.get(`/brokers/bdms/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Create a new BDM
   * @param {Object} bdmData - BDM data to create
   * @returns {Promise} - Promise with created BDM
   */
  async createBDM(bdmData) {
    try {
      const response = await api.post('/brokers/bdms/', bdmData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update an existing BDM
   * @param {number} id - BDM ID
   * @param {Object} bdmData - BDM data to update
   * @returns {Promise} - Promise with updated BDM
   */
  async updateBDM(id, bdmData) {
    try {
      const response = await api.patch(`/brokers/bdms/${id}/`, bdmData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Delete a BDM
   * @param {number} id - BDM ID
   * @returns {Promise} - Promise with deletion status
   */
  async deleteBDM(id) {
    try {
      const response = await api.delete(`/brokers/bdms/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get brokers in branch
   * @param {number} branchId - Branch ID
   * @returns {Promise} - Promise with brokers in branch
   */
  async getBrokersInBranch(branchId) {
    try {
      const response = await api.get(`/brokers/branches/${branchId}/brokers/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get BDMs in branch
   * @param {number} branchId - Branch ID
   * @returns {Promise} - Promise with BDMs in branch
   */
  async getBDMsInBranch(branchId) {
    try {
      const response = await api.get(`/brokers/branches/${branchId}/bdms/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get broker applications
   * @param {number} brokerId - Broker ID
   * @returns {Promise} - Promise with broker applications
   */
  async getBrokerApplications(brokerId) {
    try {
      const response = await api.get(`/brokers/${brokerId}/applications/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get broker stats
   * @param {number} brokerId - Broker ID
   * @returns {Promise} - Promise with broker stats
   */
  async getBrokerStats(brokerId) {
    try {
      const response = await api.get(`/brokers/${brokerId}/stats/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get BDM applications
   * @param {number} bdmId - BDM ID
   * @returns {Promise} - Promise with BDM applications
   */
  async getBDMApplications(bdmId) {
    try {
      const response = await api.get(`/brokers/bdms/${bdmId}/applications/`)
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

export default new BrokerService()
