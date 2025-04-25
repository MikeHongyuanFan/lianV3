import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import './assets/main.css'
import { useAuthStore } from './store/auth'
import websocketService from './services/websocket'

// Configure Axios
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create app
const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Setup Axios interceptors after pinia is installed
const authStore = useAuthStore()

// Add token to requests
axios.interceptors.request.use(
  config => {
    const token = authStore.token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Handle token expiration
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Token expired or invalid
      authStore.logout()
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

// Connect to WebSocket when authenticated
router.beforeEach((to, from, next) => {
  if (authStore.isAuthenticated && !websocketService.isConnected) {
    websocketService.connect()
  }
  next()
})

app.mount('#app')
