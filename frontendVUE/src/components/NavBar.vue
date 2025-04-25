<template>
  <nav class="bg-gray-800 text-white p-4">
    <div class="container mx-auto flex justify-between items-center">
      <div class="flex items-center">
        <router-link to="/" class="text-xl font-bold">CRM Loan System</router-link>
      </div>
      
      <div v-if="authStore.isAuthenticated" class="flex items-center space-x-4">
        <!-- Navigation links based on user role -->
        <template v-if="authStore.isAdmin">
          <router-link to="/admin" class="hover:text-gray-300">Admin Dashboard</router-link>
        </template>
        
        <template v-if="authStore.isBroker">
          <router-link to="/broker" class="hover:text-gray-300">Broker Dashboard</router-link>
        </template>
        
        <template v-if="authStore.isBD">
          <router-link to="/bd" class="hover:text-gray-300">BD Dashboard</router-link>
        </template>
        
        <!-- Common links for all authenticated users -->
        <router-link to="/" class="hover:text-gray-300">Home</router-link>
        <router-link to="/reports" class="hover:text-gray-300">Reports</router-link>
        
        <!-- Notification Center -->
        <notification-center />
        
        <!-- User dropdown -->
        <div class="relative" ref="userMenuContainer">
          <button 
            @click="toggleUserMenu" 
            class="flex items-center focus:outline-none"
          >
            <span class="mr-2">{{ authStore.user.name || authStore.user.email }}</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </button>
          
          <div 
            v-show="userMenuOpen" 
            class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 text-gray-700 z-50"
          >
            <div class="px-4 py-2 text-sm text-gray-500">
              Signed in as <span class="font-medium">{{ authStore.user.email }}</span>
            </div>
            <div class="border-t border-gray-200"></div>
            <router-link to="/profile" class="block px-4 py-2 text-sm hover:bg-gray-100">Your Profile</router-link>
            <router-link to="/notifications" class="block px-4 py-2 text-sm hover:bg-gray-100">Notifications</router-link>
            <button @click="logout" class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 text-red-500">
              Sign out
            </button>
          </div>
        </div>
      </div>
      
      <div v-else class="flex items-center space-x-4">
        <router-link to="/login" class="hover:text-gray-300">Login</router-link>
        <router-link to="/register" class="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded">Register</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'
import NotificationCenter from './notifications/NotificationCenter.vue'

const router = useRouter()
const authStore = useAuthStore()
const userMenuOpen = ref(false)
const userMenuContainer = ref(null)

function toggleUserMenu() {
  userMenuOpen.value = !userMenuOpen.value
}

function handleClickOutside(event) {
  if (userMenuContainer.value && !userMenuContainer.value.contains(event.target)) {
    userMenuOpen.value = false
  }
}

function logout() {
  authStore.logout()
  userMenuOpen.value = false
  router.push('/login')
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
