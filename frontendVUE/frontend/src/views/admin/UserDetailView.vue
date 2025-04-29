<template>
  <div class="user-detail-container">
    <header class="bg-gray-800 text-white py-4 mb-6">
      <div class="container mx-auto px-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold">{{ isNewUser ? 'Create User' : 'Edit User' }}</h1>
          <router-link to="/admin/users" class="btn btn-secondary">
            <i class="bi bi-arrow-left mr-2"></i> Back to Users
          </router-link>
        </div>
      </div>
    </header>

    <main class="container mx-auto px-4">
      <!-- Loading state -->
      <div v-if="loading && !isNewUser" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <p class="mt-2 text-gray-600">Loading user details...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="bg-danger-100 border border-danger-300 text-danger-700 px-4 py-3 rounded mb-6">
        <p>{{ error.message }}</p>
        <button @click="loadUser" class="text-danger-800 underline mt-2">Try again</button>
      </div>

      <!-- User form -->
      <div v-else class="bg-white rounded-lg shadow p-6">
        <form @submit.prevent="saveUser">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="form-group">
              <label for="first_name" class="form-label">First Name</label>
              <input
                id="first_name"
                v-model="userData.first_name"
                type="text"
                class="form-input"
                :class="{ 'border-danger-500': errors.first_name }"
                required
              />
              <p v-if="errors.first_name" class="form-error">{{ errors.first_name }}</p>
            </div>

            <div class="form-group">
              <label for="last_name" class="form-label">Last Name</label>
              <input
                id="last_name"
                v-model="userData.last_name"
                type="text"
                class="form-input"
                :class="{ 'border-danger-500': errors.last_name }"
                required
              />
              <p v-if="errors.last_name" class="form-error">{{ errors.last_name }}</p>
            </div>

            <div class="form-group">
              <label for="email" class="form-label">Email</label>
              <input
                id="email"
                v-model="userData.email"
                type="email"
                class="form-input"
                :class="{ 'border-danger-500': errors.email }"
                required
              />
              <p v-if="errors.email" class="form-error">{{ errors.email }}</p>
            </div>

            <div class="form-group">
              <label for="phone" class="form-label">Phone</label>
              <input
                id="phone"
                v-model="userData.phone"
                type="tel"
                class="form-input"
                :class="{ 'border-danger-500': errors.phone }"
              />
              <p v-if="errors.phone" class="form-error">{{ errors.phone }}</p>
            </div>

            <div class="form-group">
              <label for="role" class="form-label">Role</label>
              <select
                id="role"
                v-model="userData.role"
                class="form-input"
                :class="{ 'border-danger-500': errors.role }"
                required
              >
                <option value="" disabled>Select a role</option>
                <option value="admin">Admin</option>
                <option value="broker">Broker</option>
                <option value="bd">Business Development</option>
                <option value="client">Client</option>
              </select>
              <p v-if="errors.role" class="form-error">{{ errors.role }}</p>
            </div>
          </div>

          <!-- Password fields (only for new users) -->
          <div v-if="isNewUser" class="mt-6 border-t border-gray-200 pt-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Set Password</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="form-group">
                <label for="password" class="form-label">Password</label>
                <input
                  id="password"
                  v-model="userData.password"
                  type="password"
                  class="form-input"
                  :class="{ 'border-danger-500': errors.password }"
                  required
                />
                <p v-if="errors.password" class="form-error">{{ errors.password }}</p>
                <p v-else class="text-xs text-gray-500 mt-1">Password must be at least 8 characters</p>
              </div>

              <div class="form-group">
                <label for="password2" class="form-label">Confirm Password</label>
                <input
                  id="password2"
                  v-model="userData.password2"
                  type="password"
                  class="form-input"
                  :class="{ 'border-danger-500': errors.password2 }"
                  required
                />
                <p v-if="errors.password2" class="form-error">{{ errors.password2 }}</p>
              </div>
            </div>
          </div>

          <div class="mt-6 flex justify-end space-x-3">
            <router-link to="/admin/users" class="btn btn-secondary">Cancel</router-link>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              <span v-if="saving" class="inline-block animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></span>
              {{ isNewUser ? 'Create User' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { UserProfile } from '@/types/auth'

export default defineComponent({
  name: 'UserDetailView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    
    // State
    const userId = computed(() => route.params.id as string)
    const isNewUser = computed(() => userId.value === 'create')
    const loading = ref(false)
    const saving = ref(false)
    const error = ref(null)
    
    const userData = ref<any>({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      role: '',
      password: '',
      password2: ''
    })
    
    const errors = ref<Record<string, string>>({})
    
    // Methods
    const loadUser = async () => {
      if (isNewUser.value) return
      
      loading.value = true
      error.value = null
      
      try {
        const user = await authStore.getUserById(parseInt(userId.value))
        userData.value = {
          first_name: user.first_name,
          last_name: user.last_name,
          email: user.email,
          phone: user.phone || '',
          role: user.role
        }
      } catch (err: any) {
        error.value = err
        console.error('Error loading user:', err)
      } finally {
        loading.value = false
      }
    }
    
    const validateForm = () => {
      const newErrors: Record<string, string> = {}
      
      // Validate first name
      if (!userData.value.first_name.trim()) {
        newErrors.first_name = 'First name is required'
      }
      
      // Validate last name
      if (!userData.value.last_name.trim()) {
        newErrors.last_name = 'Last name is required'
      }
      
      // Validate email
      if (!userData.value.email) {
        newErrors.email = 'Email is required'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(userData.value.email)) {
        newErrors.email = 'Please enter a valid email address'
      }
      
      // Validate role
      if (!userData.value.role) {
        newErrors.role = 'Role is required'
      }
      
      // Validate password for new users
      if (isNewUser.value) {
        if (!userData.value.password) {
          newErrors.password = 'Password is required'
        } else if (userData.value.password.length < 8) {
          newErrors.password = 'Password must be at least 8 characters'
        }
        
        if (!userData.value.password2) {
          newErrors.password2 = 'Please confirm your password'
        } else if (userData.value.password !== userData.value.password2) {
          newErrors.password2 = 'Passwords do not match'
        }
      }
      
      errors.value = newErrors
      return Object.keys(newErrors).length === 0
    }
    
    const saveUser = async () => {
      if (!validateForm()) return
      
      saving.value = true
      error.value = null
      
      try {
        if (isNewUser.value) {
          // Create new user
          await authStore.register(userData.value)
        } else {
          // Update existing user
          await authStore.updateUser(parseInt(userId.value), userData.value)
        }
        
        // Redirect to user list on success
        router.push('/admin/users')
      } catch (err: any) {
        error.value = err
        console.error('Error saving user:', err)
        
        // Handle validation errors from API
        if (err.errors) {
          Object.keys(err.errors).forEach(key => {
            if (typeof err.errors[key] === 'string') {
              errors.value[key] = err.errors[key]
            } else if (Array.isArray(err.errors[key]) && err.errors[key].length > 0) {
              errors.value[key] = err.errors[key][0]
            }
          })
        }
      } finally {
        saving.value = false
      }
    }
    
    // Load user data on component mount
    onMounted(loadUser)
    
    return {
      userId,
      isNewUser,
      loading,
      saving,
      error,
      userData,
      errors,
      loadUser,
      saveUser
    }
  }
})
</script>