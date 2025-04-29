<template>
  <div class="notification-preferences-view">
    <div class="page-header">
      <h1>Notification Preferences</h1>
      <div class="header-actions">
        <button 
          @click="savePreferences" 
          class="save-btn"
          :disabled="loading"
        >
          Save Changes
        </button>
      </div>
    </div>

    <div v-if="loading && !preferences" class="loading-state">
      <div class="spinner"></div>
      <p>Loading preferences...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchPreferences" class="retry-btn">Retry</button>
    </div>

    <div v-else-if="preferences" class="preferences-container">
      <div class="preferences-section">
        <h2>In-App Notifications</h2>
        <p class="section-description">
          Control which notifications appear in the notification center.
        </p>

        <div class="preferences-grid">
          <div class="preference-item">
            <div class="preference-label">
              <h3>Application Status Changes</h3>
              <p>Receive notifications when application statuses change</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.application_status_in_app"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>Upcoming Repayments</h3>
              <p>Receive notifications about upcoming repayments</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.repayment_upcoming_in_app"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>Overdue Repayments</h3>
              <p>Receive notifications about overdue repayments</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.repayment_overdue_in_app"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>Note Reminders</h3>
              <p>Receive notifications for note reminders</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.note_reminder_in_app"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>Document Uploads</h3>
              <p>Receive notifications when documents are uploaded</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.document_uploaded_in_app"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>Signature Required</h3>
              <p>Receive notifications when signatures are required</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.signature_required_in_app"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>System Messages</h3>
              <p>Receive system notifications and announcements</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.system_in_app"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="preferences-section">
        <h2>Email Notifications</h2>
        <p class="section-description">
          Control which notifications are sent to your email address.
        </p>

        <div class="preferences-grid">
          <div class="preference-item">
            <div class="preference-label">
              <h3>Application Status Changes</h3>
              <p>Receive emails when application statuses change</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.application_status_email"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>Upcoming Repayments</h3>
              <p>Receive emails about upcoming repayments</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.repayment_upcoming_email"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>Overdue Repayments</h3>
              <p>Receive emails about overdue repayments</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.repayment_overdue_email"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>Note Reminders</h3>
              <p>Receive emails for note reminders</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.note_reminder_email"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>Document Uploads</h3>
              <p>Receive emails when documents are uploaded</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.document_uploaded_email"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>Signature Required</h3>
              <p>Receive emails when signatures are required</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.signature_required_email"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>System Messages</h3>
              <p>Receive system emails and announcements</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.system_email"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="preferences-section">
        <h2>Digest Settings</h2>
        <p class="section-description">
          Configure email digest settings to receive summaries of your notifications.
        </p>

        <div class="preferences-grid">
          <div class="preference-item">
            <div class="preference-label">
              <h3>Daily Digest</h3>
              <p>Receive a daily summary of all notifications</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.daily_digest"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="preference-item">
            <div class="preference-label">
              <h3>Weekly Digest</h3>
              <p>Receive a weekly summary of all notifications</p>
            </div>
            <div class="preference-toggle">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.weekly_digest"
                >
                <span class="slider"></span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="actions-footer">
        <button @click="resetToDefaults" class="reset-btn">
          Reset to Defaults
        </button>
        <button 
          @click="savePreferences" 
          class="save-btn"
          :disabled="loading"
        >
          Save Changes
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useNotificationStore } from '../../store/notification';

export default {
  name: 'NotificationPreferencesView',
  setup() {
    const notificationStore = useNotificationStore();
    const preferences = ref(null);
    const defaultPreferences = {
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
    };

    // Computed properties
    const loading = computed(() => notificationStore.loading);
    const error = computed(() => notificationStore.error);

    // Methods
    const fetchPreferences = async () => {
      try {
        await notificationStore.fetchNotificationPreferences();
        preferences.value = { ...notificationStore.preferences };
      } catch (error) {
        console.error('Error fetching notification preferences:', error);
      }
    };

    const savePreferences = async () => {
      try {
        await notificationStore.updateNotificationPreferences(preferences.value);
        alert('Preferences saved successfully!');
      } catch (error) {
        console.error('Error saving notification preferences:', error);
        alert('Failed to save preferences. Please try again.');
      }
    };

    const resetToDefaults = () => {
      if (confirm('Are you sure you want to reset all notification preferences to default settings?')) {
        preferences.value = { ...defaultPreferences };
      }
    };

    // Lifecycle hooks
    onMounted(async () => {
      try {
        await fetchPreferences();
      } catch (error) {
        console.error('Error in onMounted:', error);
      }
    });

    return {
      preferences,
      loading,
      error,
      fetchPreferences,
      savePreferences,
      resetToDefaults
    };
  }
};
</script>

<style scoped>
.notification-preferences-view {
  padding: 24px;
  max-width: 1000px;
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

.save-btn {
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
}

.save-btn:hover {
  background-color: #27ae60;
}

.save-btn:disabled {
  background-color: #a8d8b9;
  cursor: not-allowed;
}

.loading-state,
.error-state {
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

.preferences-container {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.preferences-section {
  background-color: #fff;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  padding: 24px;
}

.preferences-section h2 {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
}

.section-description {
  color: #586069;
  margin: 0 0 24px;
  font-size: 14px;
}

.preferences-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

@media (min-width: 768px) {
  .preferences-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.preference-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
}

.preference-label {
  flex-grow: 1;
}

.preference-label h3 {
  margin: 0 0 4px;
  font-size: 16px;
  font-weight: 500;
}

.preference-label p {
  margin: 0;
  font-size: 14px;
  color: #586069;
}

.preference-toggle {
  margin-left: 16px;
}

/* Toggle Switch Styles */
.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #2ecc71;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2ecc71;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.actions-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
}

.reset-btn {
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
}

.reset-btn:hover {
  background-color: #f1f1f1;
}
</style>
