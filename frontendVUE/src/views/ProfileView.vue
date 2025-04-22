<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Your Profile</h1>
    
    <div v-if="loading" class="flex justify-center">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>
    
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
    </div>
    
    <div v-else class="bg-white shadow rounded-lg p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h2 class="text-lg font-semibold mb-4">Personal Information</h2>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Username</label>
            <p>{{ user.username }}</p>
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Email</label>
            <p>{{ user.email }}</p>
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Full Name</label>
            <p>{{ user.first_name }} {{ user.last_name }}</p>
          </div>
        </div>
        
        <div>
          <h2 class="text-lg font-semibold mb-4">Account Information</h2>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Role</label>
            <p>{{ userRole }}</p>
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Date Joined</label>
            <p>{{ formatDate(user.date_joined) }}</p>
          </div>
        </div>
      </div>
      
      <div class="mt-6">
        <button 
          @click="showEditForm = !showEditForm" 
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          {{ showEditForm ? 'Cancel' : 'Edit Profile' }}
        </button>
      </div>
      
      <div v-if="showEditForm" class="mt-6 border-t pt-6">
        <h2 class="text-lg font-semibold mb-4">Edit Profile</h2>
        <form @submit.prevent="updateProfile">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="first_name">First Name</label>
            <input 
              id="first_name" 
              v-model="form.first_name" 
              type="text" 
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            >
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="last_name">Last Name</label>
            <input 
              id="last_name" 
              v-model="form.last_name" 
              type="text" 
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            >
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="email">Email</label>
            <input 
              id="email" 
              v-model="form.email" 
              type="email" 
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            >
          </div>
          <div class="flex items-center justify-between">
            <button 
              type="submit" 
              class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              :disabled="updating"
            >
              {{ updating ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import authService from '../services/auth'

export default {
  name: 'ProfileView',
  setup() {
    const authStore = useAuthStore()
    const user = ref({})
    const loading = ref(true)
    const error = ref(null)
    const showEditForm = ref(false)
    const updating = ref(false)
    const form = ref({
      first_name: '',
      last_name: '',
      email: ''
    })

    const userRole = computed(() => {
      if (authStore.isAdmin) return 'Administrator'
      if (authStore.isBroker) return 'Broker'
      if (authStore.isBD) return 'Business Development'
      return 'User'
    })

    const fetchUserProfile = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await authService.getUserProfile()
        user.value = response.data
        
        // Initialize form with current values
        form.value = {
          first_name: response.data.first_name || '',
          last_name: response.data.last_name || '',
          email: response.data.email || ''
        }
      } catch (err) {
        console.error('Error fetching user profile:', err)
        error.value = 'Failed to load profile information. Please try again later.'
      } finally {
        loading.value = false
      }
    }

    const updateProfile = async () => {
      updating.value = true
      
      try {
        // This is a placeholder - you'll need to implement the update profile API endpoint
        // await authService.updateProfile(form.value)
        
        // Update local user data
        user.value = {
          ...user.value,
          ...form.value
        }
        
        showEditForm.value = false
        // Show success message or notification here
      } catch (err) {
        console.error('Error updating profile:', err)
        error.value = 'Failed to update profile. Please try again later.'
      } finally {
        updating.value = false
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }

    onMounted(fetchUserProfile)

    return {
      user,
      loading,
      error,
      userRole,
      showEditForm,
      form,
      updating,
      updateProfile,
      formatDate
    }
  }
}
</script>