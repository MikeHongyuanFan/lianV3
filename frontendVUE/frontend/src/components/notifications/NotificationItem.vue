<template>
  <div 
    class="notification-item" 
    :class="{ 'unread': !notification.is_read }"
    @click="handleClick"
  >
    <div class="notification-icon" :class="iconClass">
      <i :class="iconName"></i>
    </div>
    <div class="notification-content">
      <div class="notification-title">{{ notification.title }}</div>
      <div class="notification-message">{{ notification.message }}</div>
      <div class="notification-meta">
        <span class="notification-time">{{ formattedTime }}</span>
        <span class="notification-type">{{ notification.notification_type_display }}</span>
      </div>
    </div>
    <div class="notification-actions">
      <button 
        v-if="!notification.is_read" 
        @click.stop="markAsRead" 
        class="mark-read-btn"
        title="Mark as read"
      >
        <i class="icon-check"></i>
      </button>
      <button 
        v-if="hasRelatedObject" 
        @click.stop="navigateToRelatedObject" 
        class="view-btn"
        title="View related item"
      >
        <i class="icon-external-link"></i>
      </button>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'NotificationItem',
  props: {
    notification: {
      type: Object,
      required: true
    }
  },
  emits: ['mark-as-read'],
  setup(props, { emit }) {
    const router = useRouter();

    // Computed properties
    const formattedTime = computed(() => {
      const date = new Date(props.notification.created_at);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.round(diffMs / 60000);
      const diffHours = Math.round(diffMs / 3600000);
      const diffDays = Math.round(diffMs / 86400000);

      if (diffMins < 60) {
        return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
      } else if (diffHours < 24) {
        return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
      } else if (diffDays < 7) {
        return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
      } else {
        return date.toLocaleDateString();
      }
    });

    const iconClass = computed(() => {
      const type = props.notification.notification_type;
      switch (type) {
        case 'application_status':
          return 'icon-application';
        case 'repayment_upcoming':
        case 'repayment_overdue':
          return 'icon-payment';
        case 'note_reminder':
          return 'icon-note';
        case 'document_uploaded':
          return 'icon-document';
        case 'signature_required':
          return 'icon-signature';
        case 'system':
          return 'icon-system';
        default:
          return 'icon-bell';
      }
    });

    const iconName = computed(() => {
      const type = props.notification.notification_type;
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
    });

    const hasRelatedObject = computed(() => {
      return props.notification.related_object_id && props.notification.related_object_type;
    });

    // Methods
    const markAsRead = () => {
      if (!props.notification.is_read) {
        emit('mark-as-read', props.notification.id);
      }
    };

    const navigateToRelatedObject = () => {
      const { related_object_type, related_object_id } = props.notification;
      
      // Mark as read when navigating
      markAsRead();
      
      // Navigate based on object type
      switch (related_object_type) {
        case 'application':
          router.push(`/applications/${related_object_id}`);
          break;
        case 'borrower':
          router.push(`/borrowers/${related_object_id}`);
          break;
        case 'guarantor':
          router.push(`/guarantors/${related_object_id}`);
          break;
        case 'document':
          router.push(`/documents/${related_object_id}`);
          break;
        case 'repayment':
          router.push(`/repayments/${related_object_id}`);
          break;
        case 'fee':
          router.push(`/fees/${related_object_id}`);
          break;
        default:
          console.warn(`Unknown related object type: ${related_object_type}`);
      }
    };

    const handleClick = () => {
      // Mark as read when clicking on the notification
      markAsRead();
      
      // If there's a related object, navigate to it
      if (hasRelatedObject.value) {
        navigateToRelatedObject();
      }
    };

    return {
      formattedTime,
      iconClass,
      iconName,
      hasRelatedObject,
      markAsRead,
      navigateToRelatedObject,
      handleClick
    };
  }
};
</script>

<style scoped>
.notification-item {
  display: flex;
  padding: 12px 16px;
  border-bottom: 1px solid #e1e4e8;
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background-color: #f6f8fa;
}

.notification-item.unread {
  background-color: #f0f7ff;
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #e1e4e8;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  flex-shrink: 0;
}

.icon-application {
  background-color: #2ecc71;
  color: white;
}

.icon-payment {
  background-color: #3498db;
  color: white;
}

.icon-note {
  background-color: #f1c40f;
  color: white;
}

.icon-document {
  background-color: #9b59b6;
  color: white;
}

.icon-signature {
  background-color: #e74c3c;
  color: white;
}

.icon-system {
  background-color: #95a5a6;
  color: white;
}

.icon-bell {
  background-color: #34495e;
  color: white;
}

.notification-content {
  flex-grow: 1;
  min-width: 0;
}

.notification-title {
  font-weight: 600;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notification-message {
  font-size: 14px;
  color: #586069;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.notification-meta {
  display: flex;
  font-size: 12px;
  color: #6a737d;
}

.notification-time {
  margin-right: 8px;
}

.notification-type {
  background-color: #f1f8ff;
  border-radius: 12px;
  padding: 1px 8px;
}

.notification-actions {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-left: 12px;
}

.mark-read-btn, .view-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  margin-bottom: 4px;
  color: #586069;
}

.mark-read-btn:hover, .view-btn:hover {
  background-color: #e1e4e8;
}

/* Font awesome icons placeholder styles */
.fas {
  font-size: 14px;
}
</style>
