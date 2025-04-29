<template>
  <div class="profile-container">
    <header class="dashboard-header">
      <div class="container">
        <div class="header-content">
          <h1>User Profile</h1>
          <div class="user-actions">
            <router-link to="/dashboard" class="btn btn-sm btn-secondary">Back to Dashboard</router-link>
          </div>
        </div>
      </div>
    </header>

    <main class="container">
      <div class="profile-content">
        <div class="card">
          <div class="card-header">
            <h2>Profile Information</h2>
          </div>
          <div class="card-body">
            <AlertMessage 
              v-if="error" 
              type="danger" 
              :dismissible="true" 
              @dismissed="clearError"
            >
              {{ errorMessage }}
            </AlertMessage>

            <AlertMessage 
              v-if="updateSuccess" 
              type="success" 
              :dismissible="true" 
              :timeout="3000" 
              @dismissed="updateSuccess = false"
            >
              Profile updated successfully!
            </AlertMessage>

            <form @submit.prevent="handleUpdateProfile">
              <BaseInput
                id="first_name"
                label="First Name"
                type="text"
                v-model="profileData.first_name"
                placeholder="Enter your first name"
                :error="errors.first_name"
                required
              />

              <BaseInput
                id="last_name"
                label="Last Name"
                type="text"
                v-model="profileData.last_name"
                placeholder="Enter your last name"
                :error="errors.last_name"
                required
              />

              <BaseInput
                id="email"
                label="Email"
                type="email"
                v-model="profileData.email"
                placeholder="Enter your email"
                :error="errors.email"
                required
              />

              <BaseInput
                id="phone"
                label="Phone Number"
                type="tel"
                v-model="profileData.phone"
                placeholder="Enter your phone number"
                :error="errors.phone"
              />

              <div class="form-group">
                <label class="form-label">Role</label>
                <input 
                  type="text" 
                  class="form-control" 
                  :value="userRole" 
                  disabled 
                />
                <small class="form-text text-muted">Role cannot be changed</small>
              </div>

              <div class="form-group">
                <BaseButton 
                  type="submit" 
                  variant="primary" 
                  :loading="loading"
                >
                  Update Profile
                </BaseButton>
              </div>
            </form>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import BaseInput from '../components/BaseInput.vue'
import BaseButton from '../components/BaseButton.vue'
import AlertMessage from '../components/AlertMessage.vue'
import AuthService from '../services/auth.service'

export default {
  name: 'ProfileView',
  components: {
    BaseInput,
    BaseButton,
    AlertMessage
  },
  setup() {
    const authStore = useAuthStore()
    
    // Form data
    const profileData = reactive({
      first_name: '',
      last_name: '',
      email: '',
      phone: ''
    })
    
    const errors = reactive({
      first_name: '',
      last_name: '',
      email: '',
      phone: ''
    })
    
    const updateSuccess = ref(false)
    
    // Computed properties
    const loading = computed(() => authStore.loading)
    const error = computed(() => authStore.error)
    const userRole = computed(() => {
      const role = authStore.userRole
      if (!role) return 'User'
      
      // Convert role to title case
      return role.charAt(0).toUpperCase() + role.slice(1)
    })
    
    const errorMessage = computed(() => {
      if (!error.value) return ''
      
      if (error.value.status === 400) {
        // Process validation errors from the API
        const apiErrors = error.value.errors
        
        // Update the local errors object with API errors
        if (apiErrors) {
          Object.keys(apiErrors).forEach(key => {
            if (errors[key] !== undefined) {
              errors[key] = Array.isArray(apiErrors[key]) 
                ? apiErrors[key][0] 
                : apiErrors[key]
            }
          })
        }
        
        return 'Please correct the errors in the form.'
      } else {
        return 'An error occurred while updating your profile. Please try again later.'
      }
    })
    
    // Methods
    const loadUserProfile = async () => {
      try {
        const userData = await AuthService.getUserProfile()
        
        // Update form data with user profile information
        profileData.first_name = userData.first_name || ''
        profileData.last_name = userData.last_name || ''
        profileData.email = userData.email || ''
        profileData.phone = userData.phone || ''
      } catch (error) {
        console.error('Error loading user profile:', error)
      }
    }
    
    const validateForm = () => {
      let isValid = true
      
      // Reset errors
      Object.keys(errors).forEach(key => {
        errors[key] = ''
      })
      
      // Validate first name
      if (!profileData.first_name.trim()) {
        errors.first_name = 'First name is required'
        isValid = false
      }
      
      // Validate last name
      if (!profileData.last_name.trim()) {
        errors.last_name = 'Last name is required'
        isValid = false
      }
      
      // Validate email
      if (!profileData.email) {
        errors.email = 'Email is required'
        isValid = false
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(profileData.email)) {
        errors.email = 'Please enter a valid email address'
        isValid = false
      }
      
      // Validate phone (optional)
      if (profileData.phone && !/^\+?[0-9]{10,15}$/.test(profileData.phone)) {
        errors.phone = 'Please enter a valid phone number'
        isValid = false
      }
      
      return isValid
    }
    
    const handleUpdateProfile = async () => {
      if (!validateForm()) return
      
      try {
        await authStore.updateUserProfile(profileData)
        updateSuccess.value = true
      } catch (error) {
        // Error is handled by the store and displayed via the error computed property
        console.error('Profile update error:', error)
      }
    }
    
    const clearError = () => {
      authStore.clearError()
    }
    
    // Load user profile on component mount
    onMounted(loadUserProfile)
    
    return {
      profileData,
      errors,
      loading,
      error,
      errorMessage,
      userRole,
      updateSuccess,
      handleUpdateProfile,
      clearError
    }
  }
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  background-color: #343a40;
  color: white;
  padding: 1rem 0;
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-content {
  max-width: 600px;
  margin: 0 auto;
}
</style>
