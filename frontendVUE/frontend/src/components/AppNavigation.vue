<template>
  <nav class="bg-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <router-link to="/" class="text-white font-bold text-xl">CRM Loan System</router-link>
          </div>
          <div class="hidden md:block">
            <div class="ml-10 flex items-baseline space-x-4">
              <router-link 
                to="/dashboard" 
                class="px-3 py-2 rounded-md text-sm font-medium"
                :class="[currentRoute.path.startsWith('/dashboard') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
              >
                Dashboard
              </router-link>
              
              <router-link 
                to="/applications" 
                class="px-3 py-2 rounded-md text-sm font-medium"
                :class="[currentRoute.path.startsWith('/applications') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
              >
                Applications
              </router-link>
              
              <router-link 
                to="/borrowers" 
                class="px-3 py-2 rounded-md text-sm font-medium"
                :class="[currentRoute.path.startsWith('/borrowers') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
              >
                Borrowers
              </router-link>
              
              <router-link 
                to="/guarantors" 
                class="px-3 py-2 rounded-md text-sm font-medium"
                :class="[currentRoute.path.startsWith('/guarantors') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
              >
                Guarantors
              </router-link>
              
              <router-link 
                to="/documents" 
                class="px-3 py-2 rounded-md text-sm font-medium"
                :class="[currentRoute.path.startsWith('/documents') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
              >
                Documents
              </router-link>
              
              <router-link 
                to="/notes" 
                class="px-3 py-2 rounded-md text-sm font-medium"
                :class="[currentRoute.path.startsWith('/notes') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
              >
                Notes
              </router-link>
              
              <router-link 
                to="/fees" 
                class="px-3 py-2 rounded-md text-sm font-medium"
                :class="[currentRoute.path.startsWith('/fees') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
              >
                Fees
              </router-link>
              
              <router-link 
                to="/repayments" 
                class="px-3 py-2 rounded-md text-sm font-medium"
                :class="[currentRoute.path.startsWith('/repayments') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
              >
                Repayments
              </router-link>
            </div>
          </div>
        </div>
        <div class="hidden md:block">
          <div class="ml-4 flex items-center md:ml-6">
            <!-- Notification Badge -->
            <notification-badge class="mr-4" />
            
            <!-- Profile dropdown -->
            <div class="ml-3 relative">
              <div>
                <button 
                  @click="toggleProfileMenu" 
                  class="max-w-xs bg-gray-800 rounded-full flex items-center text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
                >
                  <span class="sr-only">Open user menu</span>
                  <div class="h-8 w-8 rounded-full bg-gray-500 flex items-center justify-center text-white">
                    {{ userInitials }}
                  </div>
                </button>
              </div>
              <div 
                v-if="showProfileMenu" 
                class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
              >
                <router-link 
                  to="/profile" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  @click="showProfileMenu = false"
                >
                  Your Profile
                </router-link>
                <router-link 
                  to="/notification-preferences" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  @click="showProfileMenu = false"
                >
                  Notification Settings
                </router-link>
                <a 
                  href="#" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  @click.prevent="logout"
                >
                  Sign out
                </a>
              </div>
            </div>
          </div>
        </div>
        <div class="-mr-2 flex md:hidden">
          <!-- Mobile menu button -->
          <button 
            @click="toggleMobileMenu" 
            class="bg-gray-800 inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
          >
            <span class="sr-only">Open main menu</span>
            <svg 
              class="h-6 w-6" 
              :class="[showMobileMenu ? 'hidden' : 'block']" 
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor" 
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg 
              class="h-6 w-6" 
              :class="[showMobileMenu ? 'block' : 'hidden']" 
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor" 
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div 
      v-if="showMobileMenu" 
      class="md:hidden"
    >
      <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
        <router-link 
          to="/dashboard" 
          class="block px-3 py-2 rounded-md text-base font-medium"
          :class="[currentRoute.path.startsWith('/dashboard') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
          @click="showMobileMenu = false"
        >
          Dashboard
        </router-link>
        
        <router-link 
          to="/applications" 
          class="block px-3 py-2 rounded-md text-base font-medium"
          :class="[currentRoute.path.startsWith('/applications') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
          @click="showMobileMenu = false"
        >
          Applications
        </router-link>
        
        <router-link 
          to="/borrowers" 
          class="block px-3 py-2 rounded-md text-base font-medium"
          :class="[currentRoute.path.startsWith('/borrowers') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
          @click="showMobileMenu = false"
        >
          Borrowers
        </router-link>
        
        <router-link 
          to="/guarantors" 
          class="block px-3 py-2 rounded-md text-base font-medium"
          :class="[currentRoute.path.startsWith('/guarantors') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
          @click="showMobileMenu = false"
        >
          Guarantors
        </router-link>
        
        <router-link 
          to="/documents" 
          class="block px-3 py-2 rounded-md text-base font-medium"
          :class="[currentRoute.path.startsWith('/documents') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
          @click="showMobileMenu = false"
        >
          Documents
        </router-link>
        
        <router-link 
          to="/notes" 
          class="block px-3 py-2 rounded-md text-base font-medium"
          :class="[currentRoute.path.startsWith('/notes') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
          @click="showMobileMenu = false"
        >
          Notes
        </router-link>
        
        <router-link 
          to="/fees" 
          class="block px-3 py-2 rounded-md text-base font-medium"
          :class="[currentRoute.path.startsWith('/fees') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
          @click="showMobileMenu = false"
        >
          Fees
        </router-link>
        
        <router-link 
          to="/repayments" 
          class="block px-3 py-2 rounded-md text-base font-medium"
          :class="[currentRoute.path.startsWith('/repayments') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white']"
          @click="showMobileMenu = false"
        >
          Repayments
        </router-link>
      </div>
      <div class="pt-4 pb-3 border-t border-gray-700">
        <div class="flex items-center px-5">
          <div class="flex-shrink-0">
            <div class="h-10 w-10 rounded-full bg-gray-500 flex items-center justify-center text-white">
              {{ userInitials }}
            </div>
          </div>
          <div class="ml-3">
            <div class="text-base font-medium leading-none text-white">{{ userName }}</div>
            <div class="text-sm font-medium leading-none text-gray-400">{{ userEmail }}</div>
          </div>
        </div>
        <div class="mt-3 px-2 space-y-1">
          <router-link 
            to="/profile" 
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-400 hover:text-white hover:bg-gray-700"
            @click="showMobileMenu = false"
          >
            Your Profile
          </router-link>
          <router-link 
            to="/notification-preferences" 
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-400 hover:text-white hover:bg-gray-700"
            @click="showMobileMenu = false"
          >
            Notification Settings
          </router-link>
          <router-link 
            to="/notifications" 
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-400 hover:text-white hover:bg-gray-700"
            @click="showMobileMenu = false"
          >
            Notifications
          </router-link>
          <a 
            href="#" 
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-400 hover:text-white hover:bg-gray-700"
            @click.prevent="logout"
          >
            Sign out
          </a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import NotificationBadge from './notifications/NotificationBadge.vue'

export default {
  name: 'AppNavigation',
  components: {
    NotificationBadge
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    
    const showMobileMenu = ref(false)
    const showProfileMenu = ref(false)
    
    const userName = computed(() => {
      const user = authStore.user
      if (!user) return ''
      return `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.email
    })
    
    const userEmail = computed(() => {
      const user = authStore.user
      return user ? user.email : ''
    })
    
    const userInitials = computed(() => {
      const user = authStore.user
      if (!user) return ''
      
      if (user.first_name && user.last_name) {
        return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase()
      } else if (user.first_name) {
        return user.first_name[0].toUpperCase()
      } else if (user.email) {
        return user.email[0].toUpperCase()
      }
      
      return 'U'
    })
    
    const toggleMobileMenu = () => {
      showMobileMenu.value = !showMobileMenu.value
    }
    
    const toggleProfileMenu = () => {
      showProfileMenu.value = !showProfileMenu.value
    }
    
    const logout = async () => {
      await authStore.logout()
      router.push('/login')
    }
    
    // Close profile menu when clicking outside
    const handleClickOutside = (event) => {
      if (showProfileMenu.value && !event.target.closest('.profile-menu')) {
        showProfileMenu.value = false
      }
    }
    
    // Add event listener for clicks outside profile menu
    window.addEventListener('click', handleClickOutside)
    
    return {
      showMobileMenu,
      showProfileMenu,
      userName,
      userEmail,
      userInitials,
      toggleMobileMenu,
      toggleProfileMenu,
      logout,
      currentRoute: route
    }
  }
}
</script>
