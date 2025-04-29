<template>
  <div id="app">
    <component :is="layout">
      <router-view />
    </component>
    <notification-toast />
  </div>
</template>

<script>
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from './store/auth'
import MainLayout from './layouts/MainLayout.vue'
import AuthLayout from './layouts/AuthLayout.vue'
import NotificationToast from './components/notifications/NotificationToast.vue'

export default {
  name: 'App',
  components: {
    MainLayout,
    AuthLayout,
    NotificationToast
  },
  setup() {
    const route = useRoute()
    const authStore = useAuthStore()
    
    // Determine which layout to use based on the route
    const layout = computed(() => {
      // Use AuthLayout for login and register pages
      if (route.path === '/login' || route.path === '/register') {
        return 'AuthLayout'
      }
      
      // Use MainLayout for authenticated pages
      return 'MainLayout'
    })
    
    // Update page title when route changes
    watch(
      () => route.meta.title,
      (title) => {
        document.title = title ? `${title} | CRM Loan Management` : 'CRM Loan Management'
      },
      { immediate: true }
    )
    
    return {
      layout
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
@import 'bootstrap/dist/css/bootstrap.min.css';
@import 'bootstrap-icons/font/bootstrap-icons.css';

body {
  font-family: 'Inter', sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f8f9fa;
}

#app {
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
}

/* Global styles */
.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
