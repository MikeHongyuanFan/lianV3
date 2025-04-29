<template>
  <div class="notification-badge">
    <button 
      class="btn btn-sm btn-outline-secondary position-relative" 
      type="button" 
      id="notificationDropdown"
      @click.stop="toggleNotificationCenter"
    >
      <i class="bi bi-bell"></i>
      <span 
        v-if="unreadCount > 0" 
        class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
      >
        {{ displayCount }}
      </span>
    </button>
    
    <div 
      class="dropdown-menu dropdown-menu-end notification-menu p-0" 
      :class="{'show': isDropdownOpen}"
      aria-labelledby="notificationDropdown"
    >
      <div class="notification-header d-flex justify-content-between align-items-center p-3 border-bottom">
        <h6 class="mb-0">Notifications</h6>
        <button 
          class="btn btn-sm btn-link text-decoration-none" 
          :disabled="unreadCount === 0"
          @click="markAllAsRead"
        > 
          Mark all as read 
        </button>
      </div>
      <div class="notification-body">
        <div v-if="loading" class="text-center p-3">
          <div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
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
            :class="{ 'unread': !notification.read_at }"
            @click="viewNotification(notification)"
          >
            <div class="d-flex">
              <div class="notification-icon me-3">
                <i :class="getNotificationIcon(notification.notification_type)"></i>
              </div>
              <div class="notification-content">
                <div class="notification-title">{{ notification.title }}</div>
                <div class="notification-message">{{ notification.message }}</div>
                <div class="notification-time">{{ formatTime(notification.created_at) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="notification-footer p-2 text-center border-top">
        <router-link 
          to="/notifications" 
          class="btn btn-sm btn-link text-decoration-none"
          @click="closeNotificationCenter"
        > 
          View all notifications 
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useNotificationStore } from '../../store/notification';
import { useAuthStore } from '../../store/auth';

export default {
  name: 'NotificationBadge',
  setup() {
    const router = useRouter();
    const notificationStore = useNotificationStore();
    const authStore = useAuthStore();
    
    // Dedicated state variable for dropdown visibility
    const isDropdownOpen = ref(false);

    // Computed properties
    const notifications = computed(() => notificationStore.sortedNotifications);
    const unreadCount = computed(() => notificationStore.unreadCount);
    const loading = computed(() => notificationStore.loading);
    const displayCount = computed(() => {
      return unreadCount.value > 99 ? '99+' : unreadCount.value;
    });
    const isAuthenticated = computed(() => authStore.isAuthenticated);

    // Methods
    const toggleNotificationCenter = () => {
      isDropdownOpen.value = !isDropdownOpen.value;
    };

    const closeNotificationCenter = () => {
      isDropdownOpen.value = false;
    };

    const fetchNotifications = async () => {
      if (isAuthenticated.value) {
        await notificationStore.fetchNotifications();
      }
    };

    const fetchUnreadCount = async () => {
      if (isAuthenticated.value) {
        await notificationStore.fetchUnreadCount();
      }
    };

    const markAllAsRead = async () => {
      await notificationStore.markAllAsRead();
    };

    const viewNotification = (notification) => {
      // Mark as read
      notificationStore.markAsRead(notification.id);
      
      // Navigate to related object if available
      if (notification.related_object_type && notification.related_object_id) {
        navigateToRelatedObject(notification.related_object_type, notification.related_object_id);
      }
      
      // Close notification center
      closeNotificationCenter();
    };

    const navigateToRelatedObject = (type, id) => {
      switch (type) {
        case 'application':
          router.push(`/applications/${id}`);
          break;
        case 'borrower':
          router.push(`/borrowers/${id}`);
          break;
        case 'guarantor':
          router.push(`/guarantors/${id}`);
          break;
        case 'document':
          router.push(`/documents/${id}`);
          break;
        case 'repayment':
          router.push(`/repayments/${id}`);
          break;
        case 'fee':
          router.push(`/fees/${id}`);
          break;
        default:
          console.warn(`Unknown related object type: ${type}`);
      }
    };

    const getNotificationIcon = (type) => {
      switch (type) {
        case 'application_status':
          return 'bi bi-file-earmark-text';
        case 'repayment_upcoming':
          return 'bi bi-calendar';
        case 'repayment_overdue':
          return 'bi bi-exclamation-circle';
        case 'note_reminder':
          return 'bi bi-sticky';
        case 'document_uploaded':
          return 'bi bi-file-earmark-arrow-up';
        case 'signature_required':
          return 'bi bi-pen';
        case 'system':
          return 'bi bi-gear';
        default:
          return 'bi bi-bell';
      }
    };

    const formatTime = (timestamp) => {
      if (!timestamp) return '';
      
      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMins / 60);
      const diffDays = Math.floor(diffHours / 24);
      
      if (diffMins < 1) {
        return 'Just now';
      } else if (diffMins < 60) {
        return `${diffMins} min ago`;
      } else if (diffHours < 24) {
        return `${diffHours} hr ago`;
      } else if (diffDays < 7) {
        return `${diffDays} day ago`;
      } else {
        return date.toLocaleDateString();
      }
    };

    const handleClickOutside = (event) => {
      const badge = document.querySelector('.notification-badge');
      if (badge && !badge.contains(event.target) && isDropdownOpen.value) {
        closeNotificationCenter();
      }
    };

    // Watch for authentication state changes
    watch(
      () => isAuthenticated.value,
      (authenticated) => {
        if (authenticated) {
          // If user is authenticated, try to connect to WebSocket
          if (!notificationStore.websocketConnected) {
            notificationStore.connectToWebSocket().catch(() => {
              // If WebSocket connection fails, fall back to polling
              notificationStore.startPolling();
            });
          }
          
          // Fetch initial data
          fetchUnreadCount();
          fetchNotifications();
        } else {
          // If user is not authenticated, disconnect WebSocket
          notificationStore.disconnectWebSocket();
          notificationStore.stopPolling();
        }
      }
    );

    // Lifecycle hooks
    onMounted(async () => {
      // Fetch initial data if authenticated
      if (isAuthenticated.value && authStore.accessToken) {
        await fetchUnreadCount();
        await fetchNotifications();
        
        // Connect to WebSocket for real-time updates
        if (!notificationStore.websocketConnected) {
          notificationStore.connectToWebSocket().catch(() => {
            // If WebSocket connection fails, fall back to polling
            notificationStore.startPolling();
          });
        }
      }
      
      // Add click outside listener
      document.addEventListener('click', handleClickOutside);
    });

    onUnmounted(() => {
      // Clean up
      document.removeEventListener('click', handleClickOutside);
    });

    return {
      notifications,
      unreadCount,
      displayCount,
      loading,
      isDropdownOpen,
      toggleNotificationCenter,
      closeNotificationCenter,
      markAllAsRead,
      viewNotification,
      getNotificationIcon,
      formatTime
    };
  }
};
</script>

<style scoped>
.notification-badge {
  position: relative;
  display: inline-block;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  z-index: 1000;
  width: 350px;
  max-height: 500px;
  display: none;
}

.dropdown-menu.show {
  display: block;
}

.notification-body {
  max-height: 350px;
  overflow-y: auto;
}

.notification-item {
  cursor: pointer;
}

.notification-item:hover {
  background-color: #f8f9fa;
}

.notification-item.unread {
  background-color: #f0f7ff;
}

.notification-icon i {
  font-size: 1.2rem;
  color: #6c757d;
}

.notification-title {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.notification-message {
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.notification-time {
  font-size: 0.75rem;
  color: #adb5bd;
}
</style>
