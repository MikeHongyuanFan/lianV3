import api from './api'

/**
 * Service for managing notifications
 */
export default {
  /**
   * Get all notifications
   * @returns {Promise} - Promise with notifications data
   */
  getNotifications() {
    return api.get('/api/users/notifications/')
  },
  
  /**
   * Mark notification as read
   * @param {Number} id - Notification ID
   * @returns {Promise} - Promise with updated notification
   */
  markAsRead(id) {
    return api.post(`/api/users/notifications/${id}/mark-read/`)
  },
  
  /**
   * Mark all notifications as read
   * @returns {Promise} - Promise with result
   */
  markAllAsRead() {
    return api.post('/api/users/notifications/mark-read/')
  },
  
  /**
   * Get unread notification count
   * @returns {Promise} - Promise with count data
   */
  getUnreadCount() {
    return api.get('/api/users/notifications/unread_count/')
  },
  
  /**
   * Get notification preferences
   * @returns {Promise} - Promise with preferences data
   */
  getPreferences() {
    return api.get('/api/users/notification-preferences/')
  },
  
  /**
   * Update notification preferences
   * @param {Object} preferences - Updated preferences
   * @returns {Promise} - Promise with updated preferences
   */
  updatePreferences(preferences) {
    return api.put('/api/users/notification-preferences/', preferences)
  }
}