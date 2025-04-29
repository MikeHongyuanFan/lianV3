<template>
  <div class="auth-container">
    <div class="card">
      <div class="card-header">
        <h2 class="auth-title">Login</h2>
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

        <form @submit.prevent="handleLogin">
          <BaseInput
            id="email"
            label="Email"
            type="email"
            v-model="email"
            placeholder="Enter your email"
            :error="errors.email"
            required
          />

          <BaseInput
            id="password"
            label="Password"
            type="password"
            v-model="password"
            placeholder="Enter your password"
            :error="errors.password"
            required
          />

          <div class="form-group">
            <BaseButton 
              type="submit" 
              variant="primary" 
              block 
              :loading="loading"
            >
              Login
            </BaseButton>
          </div>
        </form>
      </div>
      <div class="card-footer auth-footer">
        <p>Don't have an account? <router-link to="/register" class="auth-link">Register</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../store/auth'
import BaseInput from '../components/BaseInput.vue'
import BaseButton from '../components/BaseButton.vue'
import AlertMessage from '../components/AlertMessage.vue'

export default {
  name: 'LoginView',
  components: {
    BaseInput,
    BaseButton,
    AlertMessage
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    
    // Form data
    const email = ref('')
    const password = ref('')
    const errors = reactive({
      email: '',
      password: ''
    })
    
    // Computed properties
    const loading = computed(() => authStore.loading)
    const error = computed(() => authStore.error)
    const errorMessage = computed(() => {
      if (!error.value) return ''
      
      if (error.value.status === 401) {
        return 'Invalid email or password. Please try again.'
      } else if (error.value.status === 400) {
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
        
        return 'Please check your input and try again.'
      } else {
        return 'An error occurred. Please try again later.'
      }
    })
    
    // Methods
    const validateForm = () => {
      let isValid = true
      
      // Reset errors
      errors.email = ''
      errors.password = ''
      
      // Validate email
      if (!email.value) {
        errors.email = 'Email is required'
        isValid = false
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        errors.email = 'Please enter a valid email address'
        isValid = false
      }
      
      // Validate password
      if (!password.value) {
        errors.password = 'Password is required'
        isValid = false
      }
      
      return isValid
    }
    
    const handleLogin = async () => {
      if (!validateForm()) return
      
      try {
        await authStore.login(email.value, password.value)
        
        // Redirect to dashboard or the original requested page
        const redirectPath = route.query.redirect || '/dashboard'
        router.push(redirectPath)
      } catch (error) {
        // Error is handled by the store and displayed via the error computed property
        console.error('Login error:', error)
      }
    }
    
    const clearError = () => {
      authStore.clearError()
    }
    
    return {
      email,
      password,
      errors,
      loading,
      error,
      errorMessage,
      handleLogin,
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
