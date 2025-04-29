import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './store/auth'
import { useNotificationStore } from './store/notification'

// Import Bootstrap CSS and JS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import * as bootstrap from 'bootstrap'

// Create the app
const app = createApp(App)

// Make bootstrap available globally
window.bootstrap = bootstrap

// Create a directive for bootstrap dropdowns
app.directive('dropdown', {
  mounted(el) {
    new bootstrap.Dropdown(el)
  }
})

// Use Pinia for state management
app.use(createPinia())

// Use Vue Router
app.use(router)

// Mount the app
app.mount('#app')

// Initialize WebSocket connection after app is mounted
// This ensures the store is properly initialized
const initializeWebSocket = () => {
  const authStore = useAuthStore()
  const notificationStore = useNotificationStore()
  
  // Connect to WebSocket if user is authenticated
  if (authStore.isAuthenticated) {
    notificationStore.connectToWebSocket().catch(() => {
      // Fall back to polling if WebSocket connection fails
      notificationStore.startPolling()
    })
  }
}

// Initialize WebSocket connection
initializeWebSocket()

// Set up route change handler to reconnect WebSocket if needed
router.afterEach(() => {
  const authStore = useAuthStore()
  const notificationStore = useNotificationStore()
  
  // Reconnect WebSocket if user is authenticated but WebSocket is not connected
  if (authStore.isAuthenticated && !notificationStore.websocketConnected) {
    notificationStore.connectToWebSocket().catch(() => {
      // Fall back to polling if WebSocket connection fails
      notificationStore.startPolling()
    })
  }
})
