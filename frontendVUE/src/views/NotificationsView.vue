<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Notifications</h1>
    
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <!-- Notification Filters -->
      <div class="p-4 border-b border-gray-200">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center space-x-4">
            <button 
              @click="activeFilter = 'all'" 
              class="px-3 py-1 rounded-full text-sm"
              :class="activeFilter === 'all' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'"
            >
              All
            </button>
            <button 
              @click="activeFilter = 'unread'" 
              class="px-3 py-1 rounded-full text-sm"
              :class="activeFilter === 'unread' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'"
            >
              Unread
            </button>
            <div class="relative">
              <select 
                v-model="typeFilter" 
                class="block w-full pl-3 pr-10 py-1 text-sm border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 rounded-md"
              >
                <option value="">All Types</option>
                <option value="application_status">Application Status</option>
                <option value="repayment_upcoming">Repayment Upcoming</option>
                <option value="repayment_overdue">Repayment Overdue</option>
                <option value="note_reminder">Note Reminder</option>
                <option value="document_uploaded">Document Uploaded</option>
                <option value="signature_required">Signature Required</option>
                <option value="system">System</option>
              </select>
            </div>
          </div>
          
          <div>
            <button 
              v-if="hasUnread" 
              @click="markAllAsRead" 
              class="text-sm text-blue-600 hover:text-blue-800"
            >
              Mark all as read
            </button>
          </div>
        </div>
      </div>
      
      <!-- Notifications List -->
      <div>
        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
        
        <div v-else-if="filteredNotifications.length === 0" class="py-12 text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No notifications</h3>
          <p class="mt-1 text-sm text-gray-500">
            {{ activeFilter === 'unread' ? 'You have no unread notifications.' : 'You have no notifications.' }}
          </p>
        </div>
        
        <div v-else>
          <div 
            v-for="notification in filteredNotifications" 
            :key="notification.id" 
            class="border-b border-gray-200 hover:bg-gray-50 cursor-pointer"
            :class="{ 'bg-blue-50': !notification.is_read }"
            @click="viewNotification(notification)"
          >
            <div class="p-4">
              <div class="flex items-start">
                <div class="flex-shrink-0 pt-0.5">
                  <span 
                    class="h-10 w-10 rounded-full flex items-center justify-center"
                    :class="getNotificationTypeClass(notification.notification_type)"
                  >
                    <svg class="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path v-if="notification.notification_type === 'application_status'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      <path v-else-if="notification.notification_type === 'repayment_upcoming'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      <path v-else-if="notification.notification_type === 'repayment_overdue'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      <path v-else-if="notification.notification_type === 'note_reminder'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                      <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </span>
                </div>
                <div class="ml-4 flex-1">
                  <div class="flex justify-between">
                    <p class="text-sm font-medium text-gray-900">{{ notification.title }}</p>
                    <p class="text-sm text-gray-500">{{ formatDate(notification.created_at) }}</p>
                  </div>
                  <p class="mt-1 text-sm text-gray-500">{{ notification.notification_type_display }}</p>
                </div>
                <div class="ml-4">
                  <button 
                    @click.stop="markAsRead(notification)" 
                    v-if="!notification.is_read"
                    class="text-sm text-blue-600 hover:text-blue-800"
                  >
                    Mark read
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Pagination -->
          <div class="px-4 py-3 flex items-center justify-between border-t border-gray-200">
            <div class="flex-1 flex justify-between">
              <button
                @click="prevPage"
                :disabled="currentPage === 1"
                :class="currentPage === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'"
                class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md"
              >
                Previous
              </button>
              <button
                @click="nextPage"
                :disabled="!hasMorePages"
                :class="!hasMorePages ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'"
                class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import websocketService from '../services/websocket'

const router = useRouter()
const notifications = ref([])
const loading = ref(false)
const activeFilter = ref('all')
const typeFilter = ref('')
const currentPage = ref(1)
const pageSize = 20
const totalCount = ref(0)

const fetchNotifications = async () => {
  loading.value = true
  
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize
    }
    
    if (activeFilter.value === 'unread') {
      params.is_read = false
    }
    
    if (typeFilter.value) {
      params.notification_type = typeFilter.value
    }
    
    const response = await axios.get('/api/notifications/', { params })
    notifications.value = response.data.results
    totalCount.value = response.data.count
  } catch (error) {
    console.error('Error fetching notifications:', error)
  } finally {
    loading.value = false
  }
}

const filteredNotifications = computed(() => {
  return notifications.value
})

const hasUnread = computed(() => {
  return notifications.value.some(notification => !notification.is_read)
})

const hasMorePages = computed(() => {
  return currentPage.value * pageSize < totalCount.value
})

const markAsRead = async (notification) => {
  try {
    await axios.post(`/api/notifications/${notification.id}/mark_as_read/`)
    notification.is_read = true
    // WebSocket will update the unread count
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
    // WebSocket will update the unread count
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
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString()
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

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (hasMorePages.value) {
    currentPage.value++
  }
}

// Handle WebSocket notifications
const handleNewNotification = (data) => {
  // If we're on the first page and the notification matches our filters, add it
  if (currentPage.value === 1) {
    // Check if the notification matches our filters
    let matchesFilter = true
    
    if (activeFilter.value === 'unread' && data.notification.is_read) {
      matchesFilter = false
    }
    
    if (typeFilter.value && data.notification.notification_type !== typeFilter.value) {
      matchesFilter = false
    }
    
    // If it matches, add it to the top of the list
    if (matchesFilter) {
      // Check if notification already exists
      const exists = notifications.value.some(n => n.id === data.notification.id)
      if (!exists) {
        notifications.value.unshift(data.notification)
        totalCount.value++
        
        // Remove the last item if we're at the page limit
        if (notifications.value.length > pageSize) {
          notifications.value.pop()
        }
      }
    }
  } else {
    // If we're not on the first page, just update the total count
    totalCount.value++
  }
}

// Setup WebSocket listeners
const setupWebSocketListeners = () => {
  websocketService.addListener('notification', handleNewNotification)
}

// Remove WebSocket listeners
const removeWebSocketListeners = () => {
  websocketService.removeListener('notification', handleNewNotification)
}

watch([activeFilter, typeFilter], () => {
  currentPage.value = 1
  fetchNotifications()
})

watch(currentPage, () => {
  fetchNotifications()
})

onMounted(() => {
  fetchNotifications()
  
  // Setup WebSocket listeners
  setupWebSocketListeners()
  
  // Connect to WebSocket if not already connected
  if (!websocketService.isConnected) {
    websocketService.connect()
  }
})

onUnmounted(() => {
  // Remove WebSocket listeners
  removeWebSocketListeners()
})
</script>
