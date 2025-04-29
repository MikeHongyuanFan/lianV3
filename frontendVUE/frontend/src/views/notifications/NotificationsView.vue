<template>
  <div class="notifications-view">
    <div class="page-header">
      <h1>Notifications</h1>
      <div class="header-actions">
        <button 
          v-if="unreadCount > 0" 
          @click="markAllAsRead" 
          class="mark-all-read-btn"
          :disabled="loading"
        >
          Mark all as read
        </button>
      </div>
    </div>

    <div class="filters-section">
      <div class="search-box">
        <input 
          type="text" 
          v-model="filters.search" 
          placeholder="Search notifications..." 
          @input="debounceSearch"
        />
      </div>

      <div class="filter-controls">
        <div class="filter-group">
          <label>Type:</label>
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
        </div>

        <div class="filter-group">
          <label>Status:</label>
          <select v-model="filters.is_read" @change="applyFilters">
            <option value="">All Status</option>
            <option value="false">Unread</option>
            <option value="true">Read</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Date From:</label>
          <input 
            type="date" 
            v-model="filters.date_from" 
            @change="applyFilters"
          />
        </div>

        <div class="filter-group">
          <label>Date To:</label>
          <input 
            type="date" 
            v-model="filters.date_to" 
            @change="applyFilters"
          />
        </div>

        <button @click="resetFilters" class="reset-filters-btn">
          Reset Filters
        </button>
      </div>
    </div>

    <div v-if="loading && !notifications.length" class="loading-state">
      <div class="spinner"></div>
      <p>Loading notifications...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchNotifications" class="retry-btn">Retry</button>
    </div>

    <div v-else-if="!notifications.length" class="empty-state">
      <div class="empty-icon">
        <i class="fas fa-bell-slash"></i>
      </div>
      <h3>No notifications found</h3>
      <p>Adjust your filters or check back later for new notifications.</p>
    </div>

    <div v-else class="notifications-list">
      <notification-item
        v-for="notification in notifications"
        :key="notification.id"
        :notification="notification"
        @mark-as-read="markAsRead"
      />

      <div v-if="loading" class="loading-more">
        <div class="spinner"></div>
        <p>Loading more notifications...</p>
      </div>

      <div v-if="pagination.total > notifications.length && !loading" class="load-more">
        <button @click="loadMore" class="load-more-btn">
          Load More
        </button>
      </div>
    </div>

    <div class="pagination-info" v-if="notifications.length">
      Showing {{ notifications.length }} of {{ pagination.total }} notifications
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useNotificationStore } from '../../store/notification';
import { useAuthStore } from '../../store/auth';
import NotificationItem from '../../components/notifications/NotificationItem.vue';

export default {
  name: 'NotificationsView',
  components: {
    NotificationItem
  },
  setup() {
    const notificationStore = useNotificationStore();
    const authStore = useAuthStore();
    const searchTimeout = ref(null);
    const filters = ref({
      search: '',
      notification_type: '',
      is_read: '',
      date_from: '',
      date_to: ''
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

    const resetFilters = async () => {
      filters.value = {
        search: '',
        notification_type: '',
        is_read: '',
        date_from: '',
        date_to: ''
      };
      notificationStore.resetFilters();
      notificationStore.updatePagination({ offset: 0 });
      await fetchNotifications();
    };

    const debounceSearch = () => {
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value);
      }
      searchTimeout.value = setTimeout(() => {
        applyFilters();
      }, 500);
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
      // Reset pagination
      notificationStore.updatePagination({ offset: 0 });
      
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
      applyFilters,
      resetFilters,
      debounceSearch
    };
  }
};
</script>

<style scoped>
.notifications-view {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.header-actions {
  display: flex;
}

.mark-all-read-btn {
  background-color: #0366d6;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
}

.mark-all-read-btn:hover {
  background-color: #0256b9;
}

.mark-all-read-btn:disabled {
  background-color: #a8bbd0;
  cursor: not-allowed;
}

.filters-section {
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 24px;
}

.search-box {
  margin-bottom: 16px;
}

.search-box input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e1e4e8;
  border-radius: 4px;
  font-size: 14px;
}

.filter-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  font-size: 12px;
  margin-bottom: 4px;
  color: #586069;
}

.filter-group select,
.filter-group input {
  padding: 6px 10px;
  border: 1px solid #e1e4e8;
  border-radius: 4px;
  font-size: 14px;
  min-width: 150px;
}

.reset-filters-btn {
  align-self: flex-end;
  background: none;
  border: 1px solid #e1e4e8;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 18px;
}

.reset-filters-btn:hover {
  background-color: #f1f1f1;
}

.notifications-list {
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  overflow: hidden;
}

.loading-state,
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 0;
  text-align: center;
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
}

.spinner {
  border: 3px solid #e1e4e8;
  border-top: 3px solid #0366d6;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state {
  color: #cb2431;
}

.retry-btn {
  background-color: #0366d6;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 16px;
}

.empty-icon {
  font-size: 48px;
  color: #959da5;
  margin-bottom: 16px;
}

.empty-state h3 {
  margin: 0 0 8px;
  font-size: 18px;
}

.empty-state p {
  color: #586069;
  margin: 0;
}

.loading-more {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background-color: #f6f8fa;
  border-top: 1px solid #e1e4e8;
}

.loading-more .spinner {
  margin: 0 8px 0 0;
}

.loading-more p {
  margin: 0;
  color: #586069;
}

.load-more {
  text-align: center;
  padding: 16px;
  border-top: 1px solid #e1e4e8;
}

.load-more-btn {
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
}

.load-more-btn:hover {
  background-color: #f1f1f1;
}

.pagination-info {
  text-align: center;
  margin-top: 16px;
  color: #586069;
  font-size: 14px;
}

/* Font awesome icons placeholder styles */
.fas {
  font-size: 48px;
}
</style>
