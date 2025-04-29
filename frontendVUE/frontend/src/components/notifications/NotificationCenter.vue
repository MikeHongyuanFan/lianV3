<template>
  <div class="notification-center">
    <div class="notification-header">
      <h3>Notifications <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span></h3>
      <div class="notification-actions">
        <button 
          v-if="unreadCount > 0" 
          @click="markAllAsRead" 
          class="mark-all-read"
          :disabled="loading"
        >
          Mark all as read
        </button>
        <button @click="$emit('close')" class="close-btn">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
    </div>

    <div class="notification-filters">
      <select v-model="filters.notification_type" @change="applyFilters">
        <option value="">All Types</option>
        <option value="application_status">Application Status</option>
        <option value="repayment_upcoming">Upcoming Repayment</option>
        <option value="repayment_overdue">Overdue Repayment</option>
        <option value="note_reminder">Note Reminder</option>
        <option value="document_uploaded">Document Uploaded</option>
        <option value="signature_required">Signature Required</option>
        <option value="system">System</option>
      </select>

      <select v-model="filters.is_read" @change="applyFilters">
        <option value="">All Status</option>
        <option value="false">Unread</option>
        <option value="true">Read</option>
      </select>
    </div>

    <div v-if="loading && !notifications.length" class="loading">
      Loading notifications...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else-if="notifications.length === 0" class="empty-state">
      No notifications found
    </div>

    <div v-else class="notification-list">
      <notification-item
        v-for="notification in notifications"
        :key="notification.id"
        :notification="notification"
        @mark-as-read="markAsRead"
      />

      <div v-if="pagination.total > notifications.length" class="load-more">
        <button 
          @click="loadMore" 
          :disabled="loading"
          class="load-more-btn"
        >
          Load More
        </button>
      </div>
    </div>

    <div class="notification-footer">
      <router-link to="/notifications" @click="$emit('close')">
        View All Notifications
      </router-link>
      <router-link to="/notification-preferences" @click="$emit('close')">
        Notification Settings
      </router-link>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref, watch } from 'vue';
import { useNotificationStore } from '../../store/notification';
import { useAuthStore } from '../../store/auth';
import NotificationItem from './NotificationItem.vue';

export default {
  name: 'NotificationCenter',
  components: {
    NotificationItem
  },
  emits: ['close'],
  setup() {
    const notificationStore = useNotificationStore();
    const authStore = useAuthStore();
    const filters = ref({
      notification_type: '',
      is_read: ''
    });

    // Computed properties
    const notifications = computed(() => notificationStore.sortedNotifications);
    const unreadCount = computed(() => notificationStore.unreadCount);
    const loading = computed(() => notificationStore.loading);
    const error = computed(() => notificationStore.error);
    const pagination = computed(() => notificationStore.pagination);
    const isAuthenticated = computed(() => authStore.isAuthenticated);

    // Methods
    const fetchNotifications = async () => {
      if (isAuthenticated.value) {
        await notificationStore.fetchNotifications({
          ...filters.value
        });
      }
    };

    const markAsRead = async (id) => {
      await notificationStore.markAsRead(id);
    };

    const markAllAsRead = async () => {
      await notificationStore.markAllAsRead();
    };

    const loadMore = async () => {
      const newOffset = notificationStore.pagination.offset + notificationStore.pagination.limit;
      notificationStore.updatePagination({ offset: newOffset });
      await fetchNotifications();
    };

    const applyFilters = async () => {
      notificationStore.updatePagination({ offset: 0 });
      await fetchNotifications();
    };

    // Watch for authentication state changes
    watch(
      () => isAuthenticated.value,
      (authenticated) => {
        if (authenticated) {
          fetchNotifications();
          
          // Connect to WebSocket for real-time updates
          if (!notificationStore.websocketConnected) {
            notificationStore.connectToWebSocket().catch(() => {
              // If WebSocket connection fails, fall back to polling
              notificationStore.startPolling();
            });
          }
        }
      }
    );

    // Lifecycle hooks
    onMounted(async () => {
      // Fetch initial notifications if authenticated
      if (isAuthenticated.value) {
        await fetchNotifications();
        
        // Fetch unread count
        await notificationStore.fetchUnreadCount();
        
        // Connect to WebSocket for real-time updates
        if (!notificationStore.websocketConnected) {
          notificationStore.connectToWebSocket().catch(() => {
            // If WebSocket connection fails, fall back to polling
            notificationStore.startPolling();
          });
        }
      }
    });

    return {
      notifications,
      unreadCount,
      loading,
      error,
      pagination,
      filters,
      fetchNotifications,
      markAsRead,
      markAllAsRead,
      loadMore,
      applyFilters
    };
  }
};
</script>

<style scoped>
.notification-center {
  width: 100%;
  max-width: 400px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  max-height: 500px;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e1e4e8;
}

.notification-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.badge {
  background-color: #ff4757;
  color: white;
  border-radius: 10px;
  padding: 2px 8px;
  font-size: 12px;
  margin-left: 8px;
}

.notification-actions {
  display: flex;
  align-items: center;
}

.mark-all-read {
  background: none;
  border: none;
  color: #0366d6;
  cursor: pointer;
  font-size: 14px;
  margin-right: 12px;
}

.mark-all-read:hover {
  text-decoration: underline;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #586069;
}

.notification-filters {
  display: flex;
  padding: 8px 16px;
  border-bottom: 1px solid #e1e4e8;
}

.notification-filters select {
  margin-right: 8px;
  padding: 4px 8px;
  border: 1px solid #e1e4e8;
  border-radius: 4px;
  font-size: 14px;
}

.notification-list {
  overflow-y: auto;
  flex-grow: 1;
  padding: 0;
}

.loading, .error, .empty-state {
  padding: 16px;
  text-align: center;
  color: #586069;
}

.error {
  color: #cb2431;
}

.load-more {
  text-align: center;
  padding: 12px;
  border-top: 1px solid #e1e4e8;
}

.load-more-btn {
  background: none;
  border: 1px solid #e1e4e8;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
}

.load-more-btn:hover {
  background-color: #f6f8fa;
}

.notification-footer {
  display: flex;
  justify-content: space-between;
  padding: 12px 16px;
  border-top: 1px solid #e1e4e8;
  font-size: 14px;
}

.notification-footer a {
  color: #0366d6;
  text-decoration: none;
}

.notification-footer a:hover {
  text-decoration: underline;
}
</style>
