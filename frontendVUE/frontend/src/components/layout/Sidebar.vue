<template>
  <div class="sidebar bg-dark text-white">
    <div class="sidebar-header p-3 border-bottom border-secondary">
      <h5 class="mb-0">CRM Loan Management</h5>
    </div>
    <div class="sidebar-content">
      <ul class="nav flex-column">
        <li class="nav-item">
          <router-link to="/dashboard" class="nav-link text-white" active-class="active">
            <i class="bi bi-speedometer2 me-2"></i> Dashboard
          </router-link>
        </li>
        
        <li class="nav-item">
          <router-link to="/applications" class="nav-link text-white" active-class="active">
            <i class="bi bi-file-earmark-text me-2"></i> Applications
          </router-link>
        </li>
        
        <li class="nav-item">
          <router-link to="/borrowers" class="nav-link text-white" active-class="active">
            <i class="bi bi-person me-2"></i> Borrowers
          </router-link>
        </li>
        
        <li class="nav-item">
          <router-link to="/guarantors" class="nav-link text-white" active-class="active">
            <i class="bi bi-shield me-2"></i> Guarantors
          </router-link>
        </li>
        
        <!-- Broker Management Dropdown -->
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle text-white" href="#" id="brokerDropdown" 
             @click.prevent="toggleDropdown('broker')">
            <i class="bi bi-briefcase me-2"></i> Broker Management
          </a>
          <ul class="dropdown-menu dropdown-menu-dark" :class="{'show': activeDropdown === 'broker'}" aria-labelledby="brokerDropdown">
            <li>
              <router-link to="/brokers" class="dropdown-item" @click="closeDropdowns">
                <i class="bi bi-people me-2"></i> Brokers
              </router-link>
            </li>
            <li>
              <router-link to="/branches" class="dropdown-item" @click="closeDropdowns">
                <i class="bi bi-building me-2"></i> Branches
              </router-link>
            </li>
            <li>
              <router-link to="/bdms" class="dropdown-item" @click="closeDropdowns">
                <i class="bi bi-person-badge me-2"></i> BDMs
              </router-link>
            </li>
          </ul>
        </li>
        
        <!-- Documents Dropdown -->
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle text-white" href="#" id="documentDropdown" 
             @click.prevent="toggleDropdown('document')">
            <i class="bi bi-folder me-2"></i> Documents
          </a>
          <ul class="dropdown-menu dropdown-menu-dark" :class="{'show': activeDropdown === 'document'}" aria-labelledby="documentDropdown">
            <li>
              <router-link to="/documents" class="dropdown-item" @click="closeDropdowns">
                <i class="bi bi-file-earmark me-2"></i> All Documents
              </router-link>
            </li>
            <li>
              <router-link to="/notes" class="dropdown-item" @click="closeDropdowns">
                <i class="bi bi-journal-text me-2"></i> Notes
              </router-link>
            </li>
          </ul>
        </li>
        
        <!-- Financial Dropdown -->
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle text-white" href="#" id="financialDropdown" 
             @click.prevent="toggleDropdown('financial')">
            <i class="bi bi-cash-coin me-2"></i> Financial
          </a>
          <ul class="dropdown-menu dropdown-menu-dark" :class="{'show': activeDropdown === 'financial'}" aria-labelledby="financialDropdown">
            <li>
              <router-link to="/fees" class="dropdown-item" @click="closeDropdowns">
                <i class="bi bi-receipt me-2"></i> Fees
              </router-link>
            </li>
            <li>
              <router-link to="/repayments" class="dropdown-item" @click="closeDropdowns">
                <i class="bi bi-calendar-check me-2"></i> Repayments
              </router-link>
            </li>
          </ul>
        </li>
        
        <li class="nav-item">
          <router-link to="/notifications" class="nav-link text-white" active-class="active">
            <i class="bi bi-bell me-2"></i> Notifications
            <span v-if="unreadCount > 0" class="badge bg-danger ms-2">{{ unreadCount }}</span>
          </router-link>
        </li>
        
        <li class="nav-item">
          <router-link to="/profile" class="nav-link text-white" active-class="active">
            <i class="bi bi-person-circle me-2"></i> Profile
          </router-link>
        </li>
      </ul>
    </div>
    <div class="sidebar-footer p-3 border-top border-secondary">
      <button class="btn btn-outline-light w-100" @click="logout">
        <i class="bi bi-box-arrow-right me-2"></i> Logout
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useNotificationStore } from '@/store/notification'

export default {
  name: 'Sidebar',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const notificationStore = useNotificationStore()
    
    const unreadCount = computed(() => notificationStore.unreadCount || 0)
    const activeDropdown = ref(null)
    
    // Toggle dropdown function
    const toggleDropdown = (type) => {
      if (activeDropdown.value === type) {
        activeDropdown.value = null
      } else {
        activeDropdown.value = type
      }
    }
    
    // Close all dropdowns
    const closeDropdowns = () => {
      activeDropdown.value = null
    }
    
    // Initialize when component is mounted
    onMounted(() => {
      // Fetch unread notification count
      notificationStore.fetchUnreadCount()
      
      // Add click event listener to document to close dropdowns when clicking outside
      document.addEventListener('click', (event) => {
        const isDropdownClick = event.target.closest('.dropdown-toggle') || event.target.closest('.dropdown-menu')
        if (!isDropdownClick) {
          closeDropdowns()
        }
      })
    })
    
    const logout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    return {
      unreadCount,
      activeDropdown,
      toggleDropdown,
      closeDropdowns,
      logout
    }
  }
}
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 250px;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding-top: 1rem;
}

.nav-link {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  margin: 0.2rem 0.5rem;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
  background-color: rgba(255, 255, 255, 0.2);
}

.dropdown-menu {
  margin-top: 0;
  border-radius: 0;
  border: none;
  background-color: #343a40;
  position: static;
  float: none;
  display: none;
}

.dropdown-menu.show {
  display: block;
}

.dropdown-item {
  padding: 0.5rem 1.5rem;
  color: #fff;
}

.dropdown-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Style dropdown toggle arrow */
.dropdown-toggle::after {
  display: inline-block;
  margin-left: 0.255em;
  vertical-align: 0.255em;
  content: "";
  border-top: 0.3em solid;
  border-right: 0.3em solid transparent;
  border-bottom: 0;
  border-left: 0.3em solid transparent;
}
</style>
