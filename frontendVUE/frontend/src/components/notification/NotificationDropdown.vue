<template>
  <div class="notification-dropdown">
    <div class="dropdown">
      <button 
        class="btn btn-sm btn-outline-secondary position-relative" 
        type="button" 
        id="notificationDropdown" 
        @click.stop="toggleDropdown"
      >
        <i class="bi bi-bell"></i>
        <span 
          v-if="unreadCount > 0" 
          class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
        >
          {{ unreadCount > 99 ? '99+' : unreadCount }}
          <span class="visually-hidden">unread notifications</span>
        </span>
      </button>
      <div 
        class="dropdown-menu dropdown-menu-end notification-menu p-0" 
        :class="{'show': isOpen}"
        aria-labelledby="notificationDropdown"
      >
        <div class="notification-header d-flex justify-content-between align-items-center p-3 border-bottom">
          <h6 class="mb-0">Notifications</h6>
          <button 
            class="btn btn-sm btn-link text-decoration-none" 
            @click="markAllAsRead"
            :disabled="loading || notifications.length === 0"
          >
            Mark all as read
          </button>
        </div>
        
        <div class="notification-body">
          <div v-if="loading" class="text-center p-3">
            <div class="spinner-border spinner-border-sm" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mb-0 mt-2">Loading notifications...</p>
          </div>
          
          <div v-else-if="notifications.length === 0" class="text-center p-3">
            <i class="bi bi-bell-slash text-muted display-6"></i>
            <p class="mb-0 mt-2">No notifications</p>
          </div>
          
          <div v-else class="notification-list">
            <div 
              v-for="notification in notifications.slice(0, 5)" 
              :key="notification.id" 
              class="notification-item p-3 border-bottom"
              :class="{ 'unread': !notification.is_read }"
              @click="viewNotification(notification)"
            >
              <div class="d-flex">
                <div class="notification-icon me-3">
                  <i :class="getNotificationIcon(notification.notification_type)" class="bi"></i>
                </div>
                <div class="notification-content">
                  <h6 class="mb-1">{{ notification.title }}</h6>
                  <p class="mb-1 text-truncate">{{ notification.message }}</p>
                  <small class="text-muted">{{ formatDate(notification.created_at) }}</small>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="notification-footer p-2 text-center border-top">
          <router-link to="/notifications" class="btn btn-sm btn-link text-decoration-none" @click="closeDropdown">
            View all notifications
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useNotificationStore } from '@/store/notification'

export default {
  name: 'NotificationDropdown',
  setup() {
    const notificationStore = useNotificationStore()
    const loading = ref(false)
    const isOpen = ref(false)
    
    const notifications = computed(() => notificationStore.notifications)
    const unreadCount = computed(() => notificationStore.unreadCount)
    
    const fetchNotifications = async () => {
      loading.value = true
      try {
        await notificationStore.fetchNotifications({ limit: 5 })
      } catch (error) {
        console.error('Error fetching notifications:', error)
      } finally {
        loading.value = false
      }
    }
    
    const markAllAsRead = async () => {
      loading.value = true
      try {
        await notificationStore.markAllAsRead()
      } catch (error) {
        console.error('Error marking all notifications as read:', error)
      } finally {
        loading.value = false
      }
    }
    
    const toggleDropdown = () => {
      isOpen.value = !isOpen.value
      if (isOpen.value) {
        fetchNotifications()
      }
    }
    
    const closeDropdown = () => {
      isOpen.value = false
    }
    
    const viewNotification = async (notification) => {
      if (!notification.is_read) {
        try {
          await notificationStore.markAsRead(notification.id)
        } catch (error) {
          console.error('Error marking notification as read:', error)
        }
      }
      
      // Handle navigation based on notification type
      if (notification.related_object_type === 'application' && notification.related_object_id) {
        window.location.href = `/applications/${notification.related_object_id}`
      } else {
        window.location.href = '/notifications'
      }
      
      closeDropdown()
    }
    
    const getNotificationIcon = (type) => {
      const icons = {
        'application_status': 'bi-file-earmark-text',
        'repayment_upcoming': 'bi-calendar',
        'repayment_overdue': 'bi-exclamation-triangle',
        'note_reminder': 'bi-journal-text',
        'document_uploaded': 'bi-file-earmark-arrow-up',
        'signature_required': 'bi-pen',
        'system': 'bi-gear'
      }
      
      return icons[type] || 'bi-bell'
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      
      const date = new Date(dateString)
      const now = new Date()
      const diffMs = now - date
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMins / 60)
      const diffDays = Math.floor(diffHours / 24)
      
      if (diffMins < 1) {
        return 'Just now'
      } else if (diffMins < 60) {
        return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`
      } else if (diffHours < 24) {
        return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`
      } else if (diffDays < 7) {
        return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`
      } else {
        return date.toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'short', 
          day: 'numeric' 
        })
      }
    }
    
    // Handle clicks outside to close dropdown
    const handleClickOutside = (event) => {
      const dropdown = document.querySelector('.notification-dropdown')
      if (dropdown && !dropdown.contains(event.target) && isOpen.value) {
        closeDropdown()
      }
    }
    
    onMounted(() => {
      notificationStore.fetchUnreadCount()
      document.addEventListener('click', handleClickOutside)
    })
    
    onBeforeUnmount(() => {
      document.removeEventListener('click', handleClickOutside)
    })
    
    return {
      notifications,
      unreadCount,
      loading,
      isOpen,
      toggleDropdown,
      closeDropdown,
      markAllAsRead,
      viewNotification,
      getNotificationIcon,
      formatDate
    }
  }
}
</script>

<style scoped>
.notification-menu {
  width: 320px;
  max-height: 400px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.notification-body {
  overflow-y: auto;
  max-height: 300px;
}

.notification-item {
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background-color: #f8f9fa;
}

.notification-item.unread {
  background-color: #f0f7ff;
}

.notification-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #e9ecef;
}

.notification-icon i {
  font-size: 1.2rem;
}

.dropdown-menu.show {
  display: block;
}
</style>
