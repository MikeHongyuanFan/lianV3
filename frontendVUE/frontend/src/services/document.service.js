import api from './api'

/**
 * Document service for handling document-related API calls
 */
class DocumentService {
  /**
   * Get list of documents with optional filters
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with documents response
   */
  async getDocuments(params = {}) {
    try {
      const response = await api.get('/documents/documents/', { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get document details by ID
   * @param {number} id - Document ID
   * @returns {Promise} - Promise with document details
   */
  async getDocumentById(id) {
    try {
      const response = await api.get(`/documents/documents/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Create a new document
   * @param {FormData} documentData - Document data as FormData (for file upload)
   * @returns {Promise} - Promise with created document
   */
  async createDocument(documentData) {
    try {
      const response = await api.post('/documents/documents/', documentData, {
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
   * Update an existing document
   * @param {number} id - Document ID
   * @param {FormData|Object} documentData - Updated document data
   * @returns {Promise} - Promise with updated document
   */
  async updateDocument(id, documentData) {
    try {
      // Check if documentData is FormData (contains file) or regular object
      const headers = documentData instanceof FormData 
        ? { 'Content-Type': 'multipart/form-data' }
        : {}
      
      const response = await api.patch(`/documents/documents/${id}/`, documentData, { headers })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Delete a document
   * @param {number} id - Document ID
   * @returns {Promise} - Promise with deletion response
   */
  async deleteDocument(id) {
    try {
      const response = await api.delete(`/documents/documents/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Download a document
   * @param {number} id - Document ID
   * @returns {Promise} - Promise with document blob
   */
  async downloadDocument(id) {
    try {
      const response = await api.get(`/documents/documents/${id}/download/`, {
        responseType: 'blob'
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Create a new version of a document
   * @param {number} id - Document ID
   * @param {FormData} versionData - Version data as FormData (for file upload)
   * @returns {Promise} - Promise with new version response
   */
  async createDocumentVersion(id, versionData) {
    try {
      const response = await api.post(`/documents/documents/${id}/create-version/`, versionData, {
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

export default new DocumentService()
