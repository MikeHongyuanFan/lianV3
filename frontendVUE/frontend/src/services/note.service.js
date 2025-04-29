import api from './api'

/**
 * Note service for handling note-related API calls
 */
class NoteService {
  /**
   * Get list of notes with optional filters
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise} - Promise with notes response
   */
  async getNotes(params = {}) {
    try {
      const response = await api.get('/documents/notes/', { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get note details by ID
   * @param {number} id - Note ID
   * @returns {Promise} - Promise with note details
   */
  async getNoteById(id) {
    try {
      const response = await api.get(`/documents/notes/${id}/`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Create a new note
   * @param {Object} noteData - Note data
   * @returns {Promise} - Promise with created note
   */
  async createNote(noteData) {
    try {
      const response = await api.post('/documents/notes/', noteData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Update an existing note
   * @param {number} id - Note ID
   * @param {Object} noteData - Updated note data
   * @returns {Promise} - Promise with updated note
   */
  async updateNote(id, noteData) {
    try {
      const response = await api.patch(`/documents/notes/${id}/`, noteData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Delete a note
   * @param {number} id - Note ID
   * @returns {Promise} - Promise with deletion response
   */
  async deleteNote(id) {
    try {
      const response = await api.delete(`/documents/notes/${id}/`)
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

export default new NoteService()
