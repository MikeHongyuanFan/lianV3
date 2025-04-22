<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Notification Preferences</h1>
    
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>
    
    <div v-else class="bg-white shadow rounded-lg overflow-hidden">
      <div class="p-6">
        <form @submit.prevent="savePreferences">
          <!-- In-app Notifications Section -->
          <div class="mb-8">
            <h2 class="text-lg font-medium text-gray-900 mb-4">In-app Notifications</h2>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Application Status Changes</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.application_status_in_app" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Repayment Upcoming</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.repayment_upcoming_in_app" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Repayment Overdue</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.repayment_overdue_in_app" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Note Reminders</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.note_reminder_in_app" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Document Uploaded</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.document_uploaded_in_app" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Signature Required</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.signature_required_in_app" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">System Notifications</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.system_in_app" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Email Notifications Section -->
          <div class="mb-8">
            <h2 class="text-lg font-medium text-gray-900 mb-4">Email Notifications</h2>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Application Status Changes</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.application_status_email" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Repayment Upcoming</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.repayment_upcoming_email" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Repayment Overdue</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.repayment_overdue_email" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Note Reminders</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.note_reminder_email" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Document Uploaded</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.document_uploaded_email" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Signature Required</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.signature_required_email" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">System Notifications</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.system_email" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Email Digest Section -->
          <div class="mb-8">
            <h2 class="text-lg font-medium text-gray-900 mb-4">Email Digest</h2>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Daily Digest</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.daily_digest" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Weekly Digest</label>
                <div class="relative inline-block w-10 mr-2 align-middle select-none">
                  <input 
                    type="checkbox" 
                    v-model="preferences.weekly_digest" 
                    class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                  />
                  <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Save Button -->
          <div class="flex justify-end">
            <button 
              type="submit" 
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              :disabled="saving"
            >
              <span v-if="saving">Saving...</span>
              <span v-else>Save Preferences</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const preferences = ref({
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
  document_uploaded_email: false,
  signature_required_email: true,
  system_email: false,
  
  daily_digest: false,
  weekly_digest: false
})

const loading = ref(true)
const saving = ref(false)
const error = ref(null)

const fetchPreferences = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get('/api/notification-preferences/')
    preferences.value = response.data
  } catch (err) {
    console.error('Error fetching notification preferences:', err)
    error.value = 'Failed to load notification preferences'
  } finally {
    loading.value = false
  }
}

const savePreferences = async () => {
  saving.value = true
  error.value = null
  
  try {
    await axios.put('/api/notification-preferences/', preferences.value)
    // Show success message or toast
  } catch (err) {
    console.error('Error saving notification preferences:', err)
    error.value = 'Failed to save notification preferences'
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchPreferences()
})
</script>

<style scoped>
.toggle-checkbox:checked {
  right: 0;
  border-color: #68D391;
}
.toggle-checkbox:checked + .toggle-label {
  background-color: #68D391;
}
.toggle-checkbox {
  right: 0;
  z-index: 1;
  border-color: #D1D5DB;
  transition: all 0.3s;
}
.toggle-label {
  transition: background-color 0.3s;
}
</style>
