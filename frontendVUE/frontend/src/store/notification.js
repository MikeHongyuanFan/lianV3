/**
 * Notification Store
 * Manages notification state using Pinia
 */
import { defineStore } from 'pinia';
import notificationService from '../services/notification.service';
import websocketService from '../services/websocket.service';
import { useAuthStore } from './auth';

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notifications: [],
    unreadCount: 0,
    loading: false,
    error: null,
    pagination: {
      limit: 10,
      offset: 0,
      total: 0
    },
    filters: {
      search: '',
      notification_type: '',
      is_read: '',
      date_from: '',
      date_to: ''
    },
    preferences: {
      application_status_in_app: true,
      repayment_upcoming_in_app: true,
      repayment_overdue_in_app: true,
      note_reminder_in_app: true,
      document_uploaded_in_app: true,
      signature_required_in_app: true,
      system_in_app: true,
      application_status_email: true,
      repayment_upcoming_email: true,
      repayment_overdue_email: true,
      note_reminder_email: true,
      document_uploaded_email: true,
      signature_required_email: true,
      system_email: true,
      daily_digest: false,
      weekly_digest: false
    },
    websocketConnected: false,
    pollingInterval: null,
    pollingIntervalTime: 60000 // 1 minute
  }),

  getters: {
    /**
     * Get notifications sorted by creation date (newest first)
     * @returns {Array} Sorted notifications
     */
    sortedNotifications: (state) => {
      return [...state.notifications].sort((a, b) => {
        return new Date(b.created_at) - new Date(a.created_at);
      });
    },

    /**
     * Get unread notifications
     * @returns {Array} Unread notifications
     */
    unreadNotifications: (state) => {
      return state.notifications.filter(notification => !notification.is_read);
    },

    /**
     * Get notifications by type
     * @returns {Function} Function that returns notifications of a specific type
     */
    notificationsByType: (state) => (type) => {
      return state.notifications.filter(notification => notification.notification_type === type);
    },

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
      const authStore = useAuthStore();
      return authStore.isAuthenticated;
    }
  },

  actions: {
    /**
     * Fetch notifications with pagination and filtering
     * @param {Object} params - Additional query parameters
     */
    async fetchNotifications(params = {}) {
      // Check if user is authenticated
      if (!this.isAuthenticated) {
        console.log('User not authenticated, skipping notification fetch');
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const queryParams = {
          limit: this.pagination.limit,
          offset: this.pagination.offset,
          ...this.filters,
          ...params
        };

        const response = await notificationService.getNotifications(queryParams);
        
        this.notifications = response.data.results || response.data;
        
        // Update pagination if response includes it
        if (response.data.count !== undefined) {
          this.pagination.total = response.data.count;
        }
        
      } catch (error) {
        this.error = error.response?.data?.message || error.message;
        console.error('Error fetching notifications:', error);
      } finally {
        this.loading = false;
      }
    },

    /**
     * Fetch unread notification count
     */
    async fetchUnreadCount() {
      // Check if user is authenticated
      if (!this.isAuthenticated) {
        console.log('User not authenticated, skipping unread count fetch');
        return;
      }

      try {
        const response = await notificationService.getUnreadCount();
        this.unreadCount = response.data.unread_count;
      } catch (error) {
        console.error('Error fetching unread count:', error);
      }
    },

    /**
     * Mark a notification as read
     * @param {number} id - Notification ID
     */
    async markAsRead(id) {
      try {
        await notificationService.markAsRead(id);
        
        // Update local state
        const notification = this.notifications.find(n => n.id === id);
        if (notification) {
          notification.is_read = true;
        }
        
        // Update unread count
        await this.fetchUnreadCount();
      } catch (error) {
        console.error('Error marking notification as read:', error);
      }
    },

    /**
     * Mark all notifications as read
     */
    async markAllAsRead() {
      try {
        await notificationService.markAllAsRead();
        
        // Update local state
        this.notifications.forEach(notification => {
          notification.is_read = true;
        });
        
        // Update unread count
        this.unreadCount = 0;
      } catch (error) {
        console.error('Error marking all notifications as read:', error);
      }
    },

    /**
     * Advanced search for notifications
     * @param {Object} searchParams - Search parameters
     */
    async advancedSearch(searchParams = {}) {
      this.loading = true;
      this.error = null;

      try {
        const queryParams = {
          limit: this.pagination.limit,
          offset: this.pagination.offset,
          ...searchParams
        };

        const response = await notificationService.advancedSearch(queryParams);
        
        this.notifications = response.data.results || response.data;
        
        // Update pagination if response includes it
        if (response.data.count !== undefined) {
          this.pagination.total = response.data.count;
        }
        
        // Update filters
        this.filters = { ...this.filters, ...searchParams };
      } catch (error) {
        this.error = error.response?.data?.message || error.message;
        console.error('Error performing advanced search:', error);
      } finally {
        this.loading = false;
      }
    },

    /**
     * Fetch notification preferences
     */
    async fetchNotificationPreferences() {
      // Check if user is authenticated
      if (!this.isAuthenticated) {
        console.log('User not authenticated, skipping preferences fetch');
        return;
      }

      try {
        this.loading = true;
        this.error = null;
        const response = await notificationService.getNotificationPreferences();
        this.preferences = response.data;
      } catch (error) {
        console.error('Error fetching notification preferences:', error);
        this.error = error.message || 'Failed to fetch notification preferences';
      } finally {
        this.loading = false;
      }
    },

    /**
     * Update notification preferences
     * @param {Object} preferences - Updated preferences
     */
    async updateNotificationPreferences(preferences) {
      try {
        this.loading = true;
        this.error = null;
        const response = await notificationService.updateNotificationPreferences(preferences);
        this.preferences = response.data;
      } catch (error) {
        console.error('Error updating notification preferences:', error);
        this.error = error.message || 'Failed to update notification preferences';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Connect to WebSocket for real-time notifications
     */
    async connectToWebSocket() {
      // Check if user is authenticated
      if (!this.isAuthenticated) {
        console.log('User not authenticated, skipping WebSocket connection');
        return;
      }

      const authStore = useAuthStore();
      if (!authStore.accessToken) {
        console.log('No access token available, skipping WebSocket connection');
        this.startPolling();
        return;
      }

      if (this.websocketConnected) return;

      try {
        await websocketService.connect();
        this.websocketConnected = true;

        // Subscribe to notification events
        // According to AmazonQ.md, the WebSocket consumer handles these message types
        websocketService.subscribe('notification', this.handleNewNotification.bind(this));
        websocketService.subscribe('notification_read', this.handleNotificationRead.bind(this));
        websocketService.subscribe('unread_count', this.handleUnreadCountUpdate.bind(this));
        
        // Stop polling if WebSocket is connected
        this.stopPolling();
        
        // Fetch initial unread count
        this.fetchUnreadCount();
      } catch (error) {
        console.error('Error connecting to WebSocket:', error);
        // Fall back to polling if WebSocket connection fails
        this.startPolling();
      }
    },

    /**
     * Disconnect from WebSocket
     */
    disconnectWebSocket() {
      websocketService.disconnect();
      this.websocketConnected = false;
    },

    /**
     * Start polling for notifications
     */
    startPolling() {
      // Clear existing interval if any
      this.stopPolling();
      
      console.log('Starting notification polling');
      
      // Fetch unread count immediately
      this.fetchUnreadCount();
      
      // Start new polling interval
      this.pollingInterval = setInterval(() => {
        this.fetchUnreadCount();
      }, this.pollingIntervalTime);
    },

    /**
     * Stop polling for notifications
     */
    stopPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
        this.pollingInterval = null;
      }
    },

    /**
     * Handle new notification from WebSocket
     * @param {Object} notification - New notification data
     */
    handleNewNotification(notification) {
      if (!notification) return;
      
      // Add new notification to the beginning of the list
      this.notifications.unshift(notification);
      
      // Update unread count
      this.unreadCount++;
    },

    /**
     * Handle notification read event from WebSocket
     * @param {Object} data - Notification read data
     */
    handleNotificationRead(data) {
      if (!data) return;
      
      const { notification_id } = data;
      
      // Update local state
      const notification = this.notifications.find(n => n.id === notification_id);
      if (notification) {
        notification.is_read = true;
      }
      
      // Update unread count if provided
      if (data.unread_count !== undefined) {
        this.unreadCount = data.unread_count;
      }
    },

    /**
     * Handle unread count update from WebSocket
     * @param {Object|number} data - Unread count data or direct count value
     */
    handleUnreadCountUpdate(data) {
      // Handle case where payload might be the direct count value
      if (typeof data === 'number') {
        this.unreadCount = data;
        return;
      }
      
      // Handle case where payload is an object with unread_count property
      if (data && typeof data.unread_count !== 'undefined') {
        this.unreadCount = data.unread_count;
        return;
      }
      
      // Handle case where payload is an object with count property (from backend format)
      if (data && typeof data.count !== 'undefined') {
        this.unreadCount = data.count;
        return;
      }
      
      console.warn('Received invalid unread count data:', data);
    },

    /**
     * Add a new notification to the store
     * @param {Object} notification - Notification data
     */
    addNotification(notification) {
      this.notifications.unshift(notification);
      if (!notification.is_read) {
        this.unreadCount++;
      }
    },

    /**
     * Reset filters
     */
    resetFilters() {
      this.filters = {
        search: '',
        notification_type: '',
        is_read: '',
        date_from: '',
        date_to: ''
      };
    },

    /**
     * Update pagination
     * @param {Object} pagination - Pagination data
     */
    updatePagination(pagination) {
      this.pagination = { ...this.pagination, ...pagination };
    }
  }
});
