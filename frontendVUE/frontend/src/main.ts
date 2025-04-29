import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './store/auth'
import { useNotificationStore } from './store/notification'

// Import TailwindCSS
import './assets/tailwind.css'

// Import Bootstrap Icons (keeping for compatibility)
import 'bootstrap-icons/font/bootstrap-icons.css'

// Create the app
const app = createApp(App)

// Use Pinia for state management
app.use(createPinia())

// Use Vue Router
app.use(router)

// Mount the app
app.mount('#app')

// Initialize WebSocket connection after app is mounted
// This ensures the store is properly initialized
const initializeWebSocket = (): void => {
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