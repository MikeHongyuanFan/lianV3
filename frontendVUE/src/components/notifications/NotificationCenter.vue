<template>
  <div class="relative">
    <!-- Notification Bell Icon -->
    <button 
      @click="toggleNotifications" 
      class="relative p-1 rounded-full text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
    >
      <span class="sr-only">View notifications</span>
      <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>
      
      <!-- Notification Badge -->
      <span 
        v-if="unreadCount > 0" 
        class="absolute top-0 right-0 block h-4 w-4 rounded-full bg-red-500 text-xs text-white text-center"
      >
        {{ unreadCount > 9 ? '9+' : unreadCount }}
      </span>
    </button>
    
    <!-- Notification Dropdown -->
    <div 
      v-if="showNotifications" 
      class="origin-top-right absolute right-0 mt-2 w-80 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50"
    >
      <div class="py-1">
        <div class="px-4 py-2 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <h3 class="text-sm font-medium text-gray-900">Notifications</h3>
            <button 
              v-if="notifications.length > 0" 
              @click="markAllAsRead" 
              class="text-xs text-blue-600 hover:text-blue-800"
            >
              Mark all as read
            </button>
          </div>
        </div>
        
        <div class="max-h-96 overflow-y-auto">
          <div v-if="loading" class="flex justify-center items-center py-4">
            <div class="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-blue-500"></div>
          </div>
          
          <div v-else-if="notifications.length === 0" class="px-4 py-3 text-sm text-gray-500">
            No notifications
          </div>
          
          <div v-else>
            <div 
              v-for="notification in notifications" 
              :key="notification.id" 
              class="px-4 py-3 hover:bg-gray-50 border-b border-gray-100 cursor-pointer"
              :class="{ 'bg-blue-50': !notification.is_read }"
              @click="viewNotification(notification)"
            >
              <div class="flex items-start">
                <div class="flex-shrink-0 pt-0.5">
                  <span 
                    class="h-8 w-8 rounded-full flex items-center justify-center"
                    :class="getNotificationTypeClass(notification.notification_type)"
                  >
                    <svg class="h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path v-if="notification.notification_type === 'application_status'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      <path v-else-if="notification.notification_type === 'repayment_upcoming'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      <path v-else-if="notification.notification_type === 'repayment_overdue'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      <path v-else-if="notification.notification_type === 'note_reminder'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                      <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </span>
                </div>
                <div class="ml-3 flex-1">
                  <p class="text-sm font-medium text-gray-900">{{ notification.title }}</p>
                  <p class="mt-1 text-xs text-gray-500">{{ formatDate(notification.created_at) }}</p>
                </div>
                <div class="ml-2">
                  <button 
                    @click.stop="markAsRead(notification)" 
                    v-if="!notification.is_read"
                    class="text-xs text-blue-600 hover:text-blue-800"
                  >
                    Mark read
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="px-4 py-2 border-t border-gray-200">
          <router-link 
            to="/notifications" 
            class="text-xs text-blue-600 hover:text-blue-800"
            @click="showNotifications = false"
          >
            View all notifications
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import websocketService from '../../services/websocket'

const router = useRouter()
const showNotifications = ref(false)
const notifications = ref([])
const unreadCount = ref(0)
const loading = ref(false)
const pollingInterval = ref(null)

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  
  if (showNotifications.value) {
    fetchNotifications()
  }
}

const fetchNotifications = async () => {
  loading.value = true
  
  try {
    const response = await axios.get('/api/notifications/', {
      params: {
        limit: 10
      }
    })
    notifications.value = response.data
  } catch (error) {
    console.error('Error fetching notifications:', error)
  } finally {
    loading.value = false
  }
}

const fetchUnreadCount = async () => {
  try {
    const response = await axios.get('/api/notifications/unread_count/')
    unreadCount.value = response.data.unread_count
  } catch (error) {
    console.error('Error fetching unread count:', error)
  }
}

const markAsRead = async (notification) => {
  try {
    await axios.post(`/api/notifications/${notification.id}/mark_as_read/`)
    notification.is_read = true
    // No need to fetch unread count as it will be updated via WebSocket
  } catch (error) {
    console.error('Error marking notification as read:', error)
  }
}

const markAllAsRead = async () => {
  try {
    await axios.post('/api/notifications/mark_all_as_read/')
    notifications.value.forEach(notification => {
      notification.is_read = true
    })
    // No need to update unread count as it will be updated via WebSocket
  } catch (error) {
    console.error('Error marking all notifications as read:', error)
  }
}

const viewNotification = async (notification) => {
  // Mark as read
  if (!notification.is_read) {
    await markAsRead(notification)
  }
  
  // Navigate based on notification type
  if (notification.notification_type === 'application_status' && notification.related_object_id) {
    router.push(`/applications/${notification.related_object_id}`)
  } else if (notification.notification_type === 'repayment_upcoming' && notification.related_object_id) {
    router.push(`/applications/${notification.related_object_id}?tab=repayments`)
  } else if (notification.notification_type === 'repayment_overdue' && notification.related_object_id) {
    router.push(`/applications/${notification.related_object_id}?tab=repayments`)
  } else if (notification.notification_type === 'note_reminder' && notification.related_object_id) {
    router.push(`/applications/${notification.related_object_id}?tab=notes`)
  }
  
  showNotifications.value = false
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.round(diffMs / 60000)
  const diffHours = Math.round(diffMs / 3600000)
  const diffDays = Math.round(diffMs / 86400000)
  
  if (diffMins < 60) {
    return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`
  } else if (diffHours < 24) {
    return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`
  } else if (diffDays < 7) {
    return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`
  } else {
    return date.toLocaleDateString()
  }
}

const getNotificationTypeClass = (type) => {
  const typeClasses = {
    'application_status': 'bg-blue-500',
    'repayment_upcoming': 'bg-yellow-500',
    'repayment_overdue': 'bg-red-500',
    'note_reminder': 'bg-purple-500',
    'document_uploaded': 'bg-green-500',
    'signature_required': 'bg-orange-500',
    'system': 'bg-gray-500'
  }
  
  return typeClasses[type] || 'bg-gray-500'
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  const dropdown = document.querySelector('.origin-top-right')
  const button = document.querySelector('button[aria-label="View notifications"]')
  
  if (dropdown && !dropdown.contains(event.target) && !button.contains(event.target)) {
    showNotifications.value = false
  }
}

// Handle WebSocket notifications
const handleNewNotification = (data) => {
  // Add the new notification to the top of the list if we're showing notifications
  if (showNotifications.value) {
    // Check if notification already exists
    const exists = notifications.value.some(n => n.id === data.notification.id)
    if (!exists) {
      notifications.value.unshift(data.notification)
    }
  }
}

// Handle WebSocket unread count updates
const handleUnreadCount = (data) => {
  unreadCount.value = data.count
}

// Setup WebSocket listeners
const setupWebSocketListeners = () => {
  websocketService.addListener('notification', handleNewNotification)
  websocketService.addListener('unread_count', handleUnreadCount)
}

// Remove WebSocket listeners
const removeWebSocketListeners = () => {
  websocketService.removeListener('notification', handleNewNotification)
  websocketService.removeListener('unread_count', handleUnreadCount)
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  fetchUnreadCount()
  
  // Setup WebSocket listeners
  setupWebSocketListeners()
  
  // Connect to WebSocket
  websocketService.connect()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
  }
  
  // Remove WebSocket listeners
  removeWebSocketListeners()
})
</script>
