import { useAuthStore } from '../store/auth'

class WebSocketService {
  constructor() {
    this.socket = null
    this.isConnected = false
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectTimeout = null
    this.listeners = {}
  }

  connect() {
    const authStore = useAuthStore()
    
    if (!authStore.isAuthenticated) {
      console.log('Not authenticated, skipping WebSocket connection')
      return
    }
    
    // Close existing connection if any
    this.disconnect()
    
    // Get the access token
    const token = authStore.token
    
    // Determine WebSocket URL (ws or wss based on http or https)
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = import.meta.env.VITE_API_BASE_URL?.replace(/^https?:\/\//, '') || window.location.host
    
    // Create WebSocket connection with token
    this.socket = new WebSocket(`${protocol}//${host}/ws/notifications/?token=${token}`)
    
    // Connection opened
    this.socket.addEventListener('open', (event) => {
      console.log('WebSocket connection established')
      this.isConnected = true
      this.reconnectAttempts = 0
      
      // Request initial unread count
      this.send({ type: 'get_unread_count' })
    })
    
    // Listen for messages
    this.socket.addEventListener('message', (event) => {
      try {
        const data = JSON.parse(event.data)
        const messageType = data.type
        
        // Notify all listeners for this message type
        if (this.listeners[messageType]) {
          this.listeners[messageType].forEach(callback => {
            callback(data)
          })
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
    })
    
    // Connection closed
    this.socket.addEventListener('close', (event) => {
      console.log('WebSocket connection closed')
      this.isConnected = false
      
      // Attempt to reconnect if not a normal closure
      if (event.code !== 1000) {
        this.attemptReconnect()
      }
    })
    
    // Connection error
    this.socket.addEventListener('error', (error) => {
      console.error('WebSocket error:', error)
      this.isConnected = false
    })
  }
  
  disconnect() {
    if (this.socket) {
      this.socket.close()
      this.socket = null
      this.isConnected = false
    }
    
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout)
      this.reconnectTimeout = null
    }
  }
  
  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000)
      console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`)
      
      this.reconnectTimeout = setTimeout(() => {
        console.log(`Reconnecting... (attempt ${this.reconnectAttempts})`)
        this.connect()
      }, delay)
    } else {
      console.error('Max reconnect attempts reached')
    }
  }
  
  send(data) {
    if (this.isConnected) {
      this.socket.send(JSON.stringify(data))
    } else {
      console.error('Cannot send message, WebSocket not connected')
    }
  }
  
  addListener(messageType, callback) {
    if (!this.listeners[messageType]) {
      this.listeners[messageType] = []
    }
    
    this.listeners[messageType].push(callback)
  }
  
  removeListener(messageType, callback) {
    if (this.listeners[messageType]) {
      this.listeners[messageType] = this.listeners[messageType].filter(cb => cb !== callback)
    }
  }
}

// Create a singleton instance
const websocketService = new WebSocketService()

export default websocketService
