import api from './api'

/**
 * Service for managing loan applications
 */
export default {
  /**
   * Get all applications with optional filters
   * @param {Object} filters - Optional filters
   * @returns {Promise} - Promise with applications data
   */
  getApplications(filters = {}) {
    const queryParams = new URLSearchParams()
    
    // Add filters to query params
    Object.keys(filters).forEach(key => {
      if (filters[key] !== null && filters[key] !== undefined) {
        queryParams.append(key, filters[key])
      }
    })
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : ''
    return api.get(`/applications/${queryString}`)
  },
  
  /**
   * Get application by ID
   * @param {Number} id - Application ID
   * @returns {Promise} - Promise with application data
   */
  getApplication(id) {
    return api.get(`/applications/${id}/`)
  },
  
  /**
   * Create new application
   * @param {Object} applicationData - Application data
   * @returns {Promise} - Promise with created application
   */
  createApplication(applicationData) {
    return api.post('/applications/', applicationData)
  },
  
  /**
   * Update application
   * @param {Number} id - Application ID
   * @param {Object} applicationData - Updated application data
   * @returns {Promise} - Promise with updated application
   */
  updateApplication(id, applicationData) {
    return api.put(`/applications/${id}/`, applicationData)
  },
  
  /**
   * Update application stage
   * @param {Number} id - Application ID
   * @param {String} stage - New stage value
   * @returns {Promise} - Promise with updated application
   */
  updateApplicationStage(id, stage) {
    return api.post(`/applications/${id}/update_stage/`, { stage })
  },
  
  /**
   * Add borrowers to application
   * @param {Number} id - Application ID
   * @param {Array} borrowerIds - Array of borrower IDs
   * @returns {Promise} - Promise with updated application
   */
  addBorrowers(id, borrowerIds) {
    return api.post(`/applications/${id}/add_borrowers/`, { borrower_ids: borrowerIds })
  },
  
  /**
   * Remove borrowers from application
   * @param {Number} id - Application ID
   * @param {Array} borrowerIds - Array of borrower IDs
   * @returns {Promise} - Promise with updated application
   */
  removeBorrowers(id, borrowerIds) {
    return api.post(`/applications/${id}/remove_borrowers/`, { borrower_ids: borrowerIds })
  },
  
  /**
   * Process signature for application
   * @param {Number} id - Application ID
   * @param {String} signatureData - Base64 encoded signature data
   * @param {String} signedBy - Name of person who signed
   * @returns {Promise} - Promise with updated application
   */
  processSignature(id, signatureData, signedBy) {
    return api.post(`/applications/${id}/process_signature/`, {
      signature_data: signatureData,
      signed_by: signedBy
    })
  },
  
  /**
   * Upload documents for application
   * @param {Number} id - Application ID
   * @param {FormData} formData - Form data with documents
   * @returns {Promise} - Promise with upload result
   */
  uploadDocuments(id, formData) {
    return api.post(`/applications/${id}/upload_document/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  /**
   * Upload signature for application
   * @param {Number} id - Application ID
   * @param {FormData} formData - Form data with signature
   * @returns {Promise} - Promise with upload result
   */
  uploadSignature(id, formData) {
    return api.post(`/applications/${id}/signature/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  /**
   * Get documents for application
   * @param {Number} id - Application ID
   * @returns {Promise} - Promise with documents data
   */
  getDocuments(id) {
    return api.get(`/applications/${id}/documents/`)
  },
  
  /**
   * Get notes for application
   * @param {Number} id - Application ID
   * @returns {Promise} - Promise with notes data
   */
  getNotes(id) {
    return api.get(`/applications/${id}/notes/`)
  },
  
  /**
   * Add note to application
   * @param {Number} id - Application ID
   * @param {Object} noteData - Note data
   * @returns {Promise} - Promise with created note
   */
  addNote(id, noteData) {
    return api.post(`/applications/${id}/add_note/`, noteData)
  },
  
  /**
   * Delete application
   * @param {Number} id - Application ID
   * @returns {Promise} - Promise with deletion result
   */
  deleteApplication(id) {
    return api.delete(`/applications/${id}/`)
  }
}


