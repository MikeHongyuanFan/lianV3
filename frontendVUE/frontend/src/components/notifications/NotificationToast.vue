<template>
  <transition-group 
    name="toast" 
    tag="div" 
    class="notification-toast-container"
  >
    <div 
      v-for="toast in toasts" 
      :key="toast.id" 
      class="notification-toast"
      :class="getToastClass(toast.type)"
      @click="handleToastClick(toast)"
    >
      <div class="toast-icon">
        <i :class="getIconClass(toast.type)"></i>
      </div>
      <div class="toast-content">
        <div class="toast-title">{{ toast.title }}</div>
        <div class="toast-message">{{ toast.message }}</div>
      </div>
      <button class="toast-close" @click.stop="removeToast(toast.id)">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  </transition-group>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useNotificationStore } from '../../store/notification';
import { useAuthStore } from '../../store/auth';
import websocketService from '../../services/websocket.service';

export default {
  name: 'NotificationToast',
  setup() {
    const router = useRouter();
    const notificationStore = useNotificationStore();
    const authStore = useAuthStore();
    const toasts = ref([]);
    const toastTimeout = 5000; // 5 seconds
    let wsSubscription = null;

    // Computed properties
    const isAuthenticated = computed(() => authStore.isAuthenticated);

    // Methods
    const addToast = (notification) => {
      const toast = {
        id: Date.now(),
        title: notification.title,
        message: notification.message,
        type: notification.notification_type,
        relatedObjectId: notification.related_object_id,
        relatedObjectType: notification.related_object_type,
        timeout: setTimeout(() => {
          removeToast(toast.id);
        }, toastTimeout)
      };
      
      toasts.value.unshift(toast);
      
      // Limit the number of toasts shown
      if (toasts.value.length > 5) {
        const oldestToast = toasts.value.pop();
        clearTimeout(oldestToast.timeout);
      }
    };

    const removeToast = (id) => {
      const index = toasts.value.findIndex(toast => toast.id === id);
      if (index !== -1) {
        clearTimeout(toasts.value[index].timeout);
        toasts.value.splice(index, 1);
      }
    };

    const handleToastClick = (toast) => {
      // Navigate to related object if available
      if (toast.relatedObjectId && toast.relatedObjectType) {
        navigateToRelatedObject(toast.relatedObjectType, toast.relatedObjectId);
      }
      
      // Remove the toast
      removeToast(toast.id);
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

    const getToastClass = (type) => {
      switch (type) {
        case 'application_status':
          return 'toast-application';
        case 'repayment_upcoming':
          return 'toast-upcoming';
        case 'repayment_overdue':
          return 'toast-overdue';
        case 'note_reminder':
          return 'toast-reminder';
        case 'document_uploaded':
          return 'toast-document';
        case 'signature_required':
          return 'toast-signature';
        case 'system':
          return 'toast-system';
        default:
          return '';
      }
    };

    const getIconClass = (type) => {
      switch (type) {
        case 'application_status':
          return 'fas fa-file-alt';
        case 'repayment_upcoming':
          return 'fas fa-calendar-alt';
        case 'repayment_overdue':
          return 'fas fa-exclamation-circle';
        case 'note_reminder':
          return 'fas fa-sticky-note';
        case 'document_uploaded':
          return 'fas fa-file-upload';
        case 'signature_required':
          return 'fas fa-signature';
        case 'system':
          return 'fas fa-cog';
        default:
          return 'fas fa-bell';
      }
    };

    // Handle new notification from WebSocket
    const handleNewNotification = (notification) => {
      // Add toast notification
      addToast(notification);
      
      // Add to notification store
      notificationStore.addNotification(notification);
    };

    // Setup WebSocket subscription
    const setupWebSocketSubscription = () => {
      // Only set up subscription if authenticated and not already subscribed
      if (isAuthenticated.value && authStore.accessToken && !wsSubscription) {
        // Connect to WebSocket if not already connected
        if (!notificationStore.websocketConnected) {
          notificationStore.connectToWebSocket();
        }
        
        // Subscribe to notification events
        wsSubscription = websocketService.subscribe('notification', handleNewNotification);
      } else {
        console.log('Not authenticated, no token available, or already subscribed');
      }
    };

    // Cleanup WebSocket subscription
    const cleanupWebSocketSubscription = () => {
      if (wsSubscription) {
        wsSubscription();
        wsSubscription = null;
      }
    };

    // Lifecycle hooks
    onMounted(() => {
      setupWebSocketSubscription();
    });

    onUnmounted(() => {
      // Clean up all timeouts
      toasts.value.forEach(toast => {
        clearTimeout(toast.timeout);
      });
      
      // Unsubscribe from WebSocket events
      cleanupWebSocketSubscription();
    });

    return {
      toasts,
      removeToast,
      handleToastClick,
      getToastClass,
      getIconClass
    };
  }
};
</script>

<style scoped>
.notification-toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 350px;
}

.notification-toast {
  display: flex;
  align-items: flex-start;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 12px;
  cursor: pointer;
  overflow: hidden;
  border-left: 4px solid #0366d6;
}

.toast-application {
  border-left-color: #2ecc71;
}

.toast-upcoming {
  border-left-color: #3498db;
}

.toast-overdue {
  border-left-color: #e74c3c;
}

.toast-reminder {
  border-left-color: #f1c40f;
}

.toast-document {
  border-left-color: #9b59b6;
}

.toast-signature {
  border-left-color: #e67e22;
}

.toast-system {
  border-left-color: #95a5a6;
}

.toast-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #f6f8fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  flex-shrink: 0;
}

.toast-content {
  flex-grow: 1;
  min-width: 0;
}

.toast-title {
  font-weight: 600;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.toast-message {
  font-size: 14px;
  color: #586069;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.toast-close {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: #586069;
  padding: 0 0 0 8px;
  margin-left: 8px;
}

/* Toast animation */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* Font awesome icons placeholder styles */
.fas {
  font-size: 14px;
}
</style>
