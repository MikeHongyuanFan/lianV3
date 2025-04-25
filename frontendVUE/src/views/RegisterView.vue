<template>
  <div class="flex items-center justify-center min-h-[80vh]">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
      <h1 class="text-2xl font-bold mb-6 text-center">Register</h1>
      
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>
      
      <div v-if="success" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
        Registration successful! You can now <router-link to="/login" class="underline">login</router-link>.
      </div>
      
      <form @submit.prevent="handleRegister" v-if="!success">
        <div class="mb-4">
          <label for="email" class="block text-gray-700 text-sm font-bold mb-2">Email</label>
          <input
            type="email"
            id="email"
            v-model="formData.email"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
        </div>
        
        <div class="mb-4">
          <label for="first_name" class="block text-gray-700 text-sm font-bold mb-2">First Name</label>
          <input
            type="text"
            id="first_name"
            v-model="formData.first_name"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
        </div>
        
        <div class="mb-4">
          <label for="last_name" class="block text-gray-700 text-sm font-bold mb-2">Last Name</label>
          <input
            type="text"
            id="last_name"
            v-model="formData.last_name"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
        </div>
        
        <div class="mb-4">
          <label for="phone" class="block text-gray-700 text-sm font-bold mb-2">Phone</label>
          <input
            type="tel"
            id="phone"
            v-model="formData.phone"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
        
        <div class="mb-4">
          <label for="role" class="block text-gray-700 text-sm font-bold mb-2">Role</label>
          <select
            id="role"
            v-model="formData.role"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          >
            <option value="client">Client</option>
            <option value="broker">Broker</option>
            <option value="bd">Business Development</option>
          </select>
        </div>
        
        <div class="mb-4">
          <label for="password" class="block text-gray-700 text-sm font-bold mb-2">Password</label>
          <input
            type="password"
            id="password"
            v-model="formData.password"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
        </div>
        
        <div class="mb-6">
          <label for="confirm_password" class="block text-gray-700 text-sm font-bold mb-2">Confirm Password</label>
          <input
            type="password"
            id="confirm_password"
            v-model="confirmPassword"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
        </div>
        
        <div class="flex items-center justify-between">
          <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Registering...' : 'Register' }}
          </button>
        </div>
        
        <div class="mt-4 text-center">
          Already have an account? 
          <router-link to="/login" class="text-blue-500 hover:text-blue-700">Login</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '../store/auth'

const authStore = useAuthStore()

const formData = reactive({
  email: '',
  first_name: '',
  last_name: '',
  phone: '',
  role: 'client',
  password: ''
})

const confirmPassword = ref('')
const error = ref('')
const success = ref(false)
const isLoading = ref(false)

async function handleRegister() {
  error.value = ''
  isLoading.value = true
  
  // Validate passwords match
  if (formData.password !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    isLoading.value = false
    return
  }
  
  try {
    const result = await authStore.register(formData)
    if (result) {
      success.value = true
      // Reset form
      Object.keys(formData).forEach(key => formData[key] = '')
      confirmPassword.value = ''
    } else {
      error.value = 'Registration failed. Please try again.'
    }
  } catch (err) {
    error.value = err.message || 'An error occurred during registration'
  } finally {
    isLoading.value = false
  }
}
</script>
