<template>
  <div class="auth-container">
    <div class="card">
      <div class="card-header">
        <h2 class="auth-title">Register</h2>
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

        <form @submit.prevent="handleRegister">
          <BaseInput
            id="first_name"
            label="First Name"
            type="text"
            v-model="formData.first_name"
            placeholder="Enter your first name"
            :error="errors.first_name"
            required
          />

          <BaseInput
            id="last_name"
            label="Last Name"
            type="text"
            v-model="formData.last_name"
            placeholder="Enter your last name"
            :error="errors.last_name"
            required
          />

          <BaseInput
            id="email"
            label="Email"
            type="email"
            v-model="formData.email"
            placeholder="Enter your email"
            :error="errors.email"
            required
          />

          <div class="form-group">
            <label for="role" class="form-label">Role</label>
            <select 
              id="role" 
              v-model="formData.role" 
              class="form-control" 
              :class="{ 'is-invalid': errors.role }"
              required
            >
              <option value="" disabled>Select your role</option>
              <option value="admin">Admin</option>
              <option value="broker">Broker</option>
              <option value="bd">Business Development</option>
              <option value="client">Client</option>
            </select>
            <div v-if="errors.role" class="invalid-feedback">{{ errors.role }}</div>
          </div>

          <BaseInput
            id="password"
            label="Password"
            type="password"
            v-model="formData.password"
            placeholder="Enter your password"
            :error="errors.password"
            required
          />

          <BaseInput
            id="password2"
            label="Confirm Password"
            type="password"
            v-model="formData.password2"
            placeholder="Confirm your password"
            :error="errors.password2"
            required
          />

          <div class="form-group">
            <BaseButton 
              type="submit" 
              variant="primary" 
              block 
              :loading="loading"
            >
              Register
            </BaseButton>
          </div>
        </form>
      </div>
      <div class="card-footer auth-footer">
        <p>Already have an account? <router-link to="/login" class="auth-link">Login</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import BaseInput from '../components/BaseInput.vue'
import BaseButton from '../components/BaseButton.vue'
import AlertMessage from '../components/AlertMessage.vue'

export default {
  name: 'RegisterView',
  components: {
    BaseInput,
    BaseButton,
    AlertMessage
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    // Form data
    const formData = reactive({
      first_name: '',
      last_name: '',
      email: '',
      role: '',
      password: '',
      password2: ''
    })
    
    const errors = reactive({
      first_name: '',
      last_name: '',
      email: '',
      role: '',
      password: '',
      password2: ''
    })
    
    // Computed properties
    const loading = computed(() => authStore.loading)
    const error = computed(() => authStore.error)
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
        return 'An error occurred during registration. Please try again later.'
      }
    })
    
    // Methods
    const validateForm = () => {
      let isValid = true
      
      // Reset errors
      Object.keys(errors).forEach(key => {
        errors[key] = ''
      })
      
      // Validate first name
      if (!formData.first_name.trim()) {
        errors.first_name = 'First name is required'
        isValid = false
      }
      
      // Validate last name
      if (!formData.last_name.trim()) {
        errors.last_name = 'Last name is required'
        isValid = false
      }
      
      // Validate email
      if (!formData.email) {
        errors.email = 'Email is required'
        isValid = false
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
        errors.email = 'Please enter a valid email address'
        isValid = false
      }
      
      // Validate role
      if (!formData.role) {
        errors.role = 'Please select a role'
        isValid = false
      }
      
      // Validate password
      if (!formData.password) {
        errors.password = 'Password is required'
        isValid = false
      } else if (formData.password.length < 8) {
        errors.password = 'Password must be at least 8 characters'
        isValid = false
      }
      
      // Validate password confirmation
      if (!formData.password2) {
        errors.password2 = 'Please confirm your password'
        isValid = false
      } else if (formData.password !== formData.password2) {
        errors.password2 = 'Passwords do not match'
        isValid = false
      }
      
      return isValid
    }
    
    const handleRegister = async () => {
      if (!validateForm()) return
      
      try {
        await authStore.register(formData)
        router.push('/dashboard')
      } catch (error) {
        // Error is handled by the store and displayed via the error computed property
        console.error('Registration error:', error)
      }
    }
    
    const clearError = () => {
      authStore.clearError()
    }
    
    return {
      formData,
      errors,
      loading,
      error,
      errorMessage,
      handleRegister,
      clearError
    }
  }
}
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 2rem auto;
}

.auth-title {
  text-align: center;
  margin-bottom: 1rem;
}

.auth-footer {
  text-align: center;
}

.auth-link {
  color: #007bff;
  text-decoration: none;
}

.auth-link:hover {
  text-decoration: underline;
}
</style>
