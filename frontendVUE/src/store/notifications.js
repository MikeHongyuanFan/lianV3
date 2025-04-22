import { defineStore } from 'pinia'
import notificationService from '../services/notificationService'

export const useNotificationStore = defineStore('notifications', {
  state: () => ({
    notifications: [],
    unreadCount: 0,
    preferences: {
      emailNotifications: true,
      inAppNotifications: true,
      dailyDigest: false,
      weeklyDigest: false
    },
    loading: false,
    error: null
  }),
  
  getters: {
    getUnreadNotifications: (state) => {
      return state.notifications.filter(notification => !notification.read)
    },
    
    getReadNotifications: (state) => {
      return state.notifications.filter(notification => notification.read)
    }
  },
  
  actions: {
    async fetchNotifications() {
      this.loading = true
      this.error = null
      
      try {
        const response = await notificationService.getNotifications()
        this.notifications = response.data
        this.unreadCount = this.notifications.filter(notification => !notification.read).length
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch notifications'
        console.error('Error fetching notifications:', error)
      } finally {
        this.loading = false
      }
    },
    
    async markAsRead(notificationId) {
      try {
        await notificationService.markAsRead(notificationId)
        
        // Update local state
        const notification = this.notifications.find(n => n.id === notificationId)
        if (notification && !notification.read) {
          notification.read = true
          this.unreadCount--
        }
      } catch (error) {
        console.error('Error marking notification as read:', error)
      }
    },
    
    async markAllAsRead() {
      try {
        await notificationService.markAllAsRead()
        
        // Update local state
        this.notifications.forEach(notification => {
          notification.read = true
        })
        this.unreadCount = 0
      } catch (error) {
        console.error('Error marking all notifications as read:', error)
      }
    },
    
    async fetchPreferences() {
      try {
        const response = await notificationService.getPreferences()
        this.preferences = response.data
      } catch (error) {
        console.error('Error fetching notification preferences:', error)
      }
    },
    
    async updatePreferences(preferences) {
      try {
        await notificationService.updatePreferences(preferences)
        this.preferences = preferences
      } catch (error) {
        console.error('Error updating notification preferences:', error)
      }
    },
    
    // Handle WebSocket notification
    addNotification(notification) {
      this.notifications.unshift(notification)
      if (!notification.read) {
        this.unreadCount++
      }
    }
  }
})
