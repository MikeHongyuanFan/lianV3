<template>
  <div class="main-layout d-flex">
    <Sidebar />
    <div class="content-wrapper">
      <header class="header bg-white border-bottom">
        <div class="container-fluid py-2">
          <div class="d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center">
              <button class="btn btn-sm btn-outline-secondary d-md-none me-2" @click="toggleSidebar">
                <i class="bi bi-list"></i>
              </button>
              <h4 class="mb-0">{{ pageTitle }}</h4>
            </div>
            <div class="d-flex align-items-center">
              <NotificationDropdown class="me-3" />
              <div class="dropdown">
                <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" id="userDropdown" @click="toggleUserDropdown">
                  <i class="bi bi-person-circle me-1"></i>
                  {{ userName }}
                </button>
                <ul class="dropdown-menu dropdown-menu-end" :class="{'show': isUserDropdownOpen}" aria-labelledby="userDropdown">
                  <li>
                    <router-link to="/profile" class="dropdown-item" @click="closeUserDropdown">
                      <i class="bi bi-person me-2"></i> Profile
                    </router-link>
                  </li>
                  <li>
                    <router-link to="/notifications" class="dropdown-item" @click="closeUserDropdown">
                      <i class="bi bi-bell me-2"></i> Notifications
                      <span v-if="unreadCount > 0" class="badge bg-danger ms-2">{{ unreadCount }}</span>
                    </router-link>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li>
                    <a class="dropdown-item" href="#" @click.prevent="logout">
                      <i class="bi bi-box-arrow-right me-2"></i> Logout
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </header>
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useNotificationStore } from '@/store/notification'
import Sidebar from '@/components/layout/Sidebar.vue'
import NotificationDropdown from '@/components/notification/NotificationDropdown.vue'

export default {
  name: 'MainLayout',
  components: {
    Sidebar,
    NotificationDropdown
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    const notificationStore = useNotificationStore()
    
    const sidebarVisible = ref(true)
    const isUserDropdownOpen = ref(false)
    
    const pageTitle = computed(() => {
      return route.meta.title || 'Dashboard'
    })
    
    const userName = computed(() => {
      const user = authStore.user
      return user ? `${user.first_name} ${user.last_name}` : 'User'
    })
    
    const unreadCount = computed(() => notificationStore.unreadCount || 0)
    
    const toggleSidebar = () => {
      sidebarVisible.value = !sidebarVisible.value
      document.body.classList.toggle('sidebar-collapsed', !sidebarVisible.value)
    }
    
    const toggleUserDropdown = () => {
      isUserDropdownOpen.value = !isUserDropdownOpen.value
    }
    
    const closeUserDropdown = () => {
      isUserDropdownOpen.value = false
    }
    
    const logout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    // Handle clicks outside to close dropdown
    const handleClickOutside = (event) => {
      const dropdown = document.querySelector('#userDropdown')
      if (dropdown && !dropdown.contains(event.target) && !event.target.closest('.dropdown-menu') && isUserDropdownOpen.value) {
        closeUserDropdown()
      }
    }
    
    onMounted(() => {
      // Fetch unread notification count when component mounts
      notificationStore.fetchUnreadCount()
      document.addEventListener('click', handleClickOutside)
    })
    
    onBeforeUnmount(() => {
      document.removeEventListener('click', handleClickOutside)
    })
    
    return {
      pageTitle,
      userName,
      unreadCount,
      sidebarVisible,
      isUserDropdownOpen,
      toggleSidebar,
      toggleUserDropdown,
      closeUserDropdown,
      logout
    }
  }
}
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
}

.content-wrapper {
  flex: 1;
  margin-left: 250px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  position: sticky;
  top: 0;
  z-index: 99;
}

.main-content {
  flex: 1;
  background-color: #f8f9fa;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.dropdown-menu.show {
  display: block;
}

@media (max-width: 768px) {
  .content-wrapper {
    margin-left: 0;
  }
  
  body.sidebar-collapsed .sidebar {
    transform: translateX(-100%);
  }
  
  .sidebar {
    transform: translateX(0);
    transition: transform 0.3s ease;
  }
}
</style>
