/**
 * Notification Service
 * Handles API calls for notifications
 */
import api from './api';

class NotificationService {
  /**
   * Get notifications with pagination and filtering
   * @param {Object} params - Query parameters
   * @returns {Promise} Promise with notification data
   */
  getNotifications(params = {}) {
    return api.get('/users/notifications/', { params });
  }

  /**
   * Mark a notification as read
   * @param {number} id - Notification ID
   * @returns {Promise} Promise with response data
   */
  markAsRead(id) {
    return api.post(`/users/notifications/${id}/mark_as_read/`);
  }

  /**
   * Mark all notifications as read
   * @returns {Promise} Promise with response data
   */
  markAllAsRead() {
    return api.post('/users/notifications/mark_all_as_read/');
  }

  /**
   * Get unread notification count
   * @returns {Promise} Promise with unread count data
   */
  getUnreadCount() {
    return api.get('/users/notifications/unread_count/');
  }

  /**
   * Advanced search for notifications
   * @param {Object} params - Search parameters
   * @returns {Promise} Promise with notification data
   */
  advancedSearch(params = {}) {
    return api.get('/users/notifications/advanced_search/', { params });
  }

  /**
   * Get notification preferences
   * @returns {Promise} Promise with notification preferences data
   */
  getNotificationPreferences() {
    return api.get('/users/notification-preferences/');
  }

  /**
   * Update notification preferences
   * @param {Object} preferences - Notification preferences
   * @returns {Promise} Promise with updated preferences data
   */
  updateNotificationPreferences(preferences) {
    return api.put('/users/notification-preferences/', preferences);
  }
}

export default new NotificationService();
