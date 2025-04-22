import { useAuthStore } from '../store/auth'

class WebSocketService {
  constructor() {
    this.socket = null
    this.isConnected = false
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 10 // Increased from 5 to 10
    this.reconnectTimeout = null
    this.listeners = {}
    this.connectionError = null
    this.lastMessageTime = null
    this.heartbeatInterval = null
    this.heartbeatTimeout = null
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
    
    try {
      console.log(`Attempting WebSocket connection to ${protocol}//${host}/ws/notifications/`)
      
      // Create WebSocket connection with token
      this.socket = new WebSocket(`${protocol}//${host}/ws/notifications/?token=${token}`)
      
      // Connection opened
      this.socket.addEventListener('open', (event) => {
        console.log('WebSocket connection established')
        this.isConnected = true
        this.reconnectAttempts = 0
        this.connectionError = null
        this.lastMessageTime = Date.now()
        
        // Request initial unread count
        this.send({ type: 'get_unread_count' })
        
        // Start heartbeat to keep connection alive
        this.startHeartbeat()
      })
      
      // Listen for messages
      this.socket.addEventListener('message', (event) => {
        try {
          // Update last message time for connection health monitoring
          this.lastMessageTime = Date.now()
          
          const data = JSON.parse(event.data)
          const messageType = data.type
          
          // Handle heartbeat response
          if (messageType === 'heartbeat_response') {
            console.debug('Received heartbeat response')
            return
          }
          
          // Notify all listeners for this message type
          if (this.listeners[messageType]) {
            this.listeners[messageType].forEach(callback => {
              try {
                callback(data)
              } catch (error) {
                console.error(`Error in listener callback for ${messageType}:`, error)
              }
            })
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      })
      
      // Connection closed
      this.socket.addEventListener('close', (event) => {
        console.log(`WebSocket connection closed: ${event.code} - ${event.reason}`)
        this.isConnected = false
        this.stopHeartbeat()
        
        // Attempt to reconnect if not a normal closure
        if (event.code !== 1000) {
          this.attemptReconnect()
        }
      })
      
      // Connection error
      this.socket.addEventListener('error', (error) => {
        console.error('WebSocket error:', error)
        this.isConnected = false
        this.connectionError = error
      })
    } catch (error) {
      console.error('Error creating WebSocket connection:', error)
      this.connectionError = error
    }
  }
  
  disconnect() {
    this.stopHeartbeat()
    
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
      
      // Exponential backoff with jitter to prevent thundering herd
      const baseDelay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000)
      const jitter = Math.random() * 1000
      const delay = baseDelay + jitter
      
      console.log(`Attempting to reconnect in ${Math.round(delay/1000)}s (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      
      this.reconnectTimeout = setTimeout(() => {
        console.log(`Reconnecting... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
        this.connect()
      }, delay)
    } else {
      console.error('Max reconnect attempts reached')
      // Don't try to reconnect anymore, but don't crash the application
      this.connectionError = new Error('Max reconnect attempts reached')
      
      // Try one final reconnect after a longer delay (5 minutes)
      setTimeout(() => {
        console.log('Attempting final reconnect after cooling period')
        this.reconnectAttempts = 0
        this.connect()
      }, 5 * 60 * 1000)
    }
  }
  
  startHeartbeat() {
    // Clear any existing intervals
    this.stopHeartbeat()
    
    // Send heartbeat every 30 seconds
    this.heartbeatInterval = setInterval(() => {
      if (this.isConnected) {
        console.debug('Sending heartbeat')
        this.send({ type: 'heartbeat' })
        
        // Set timeout to check for response
        this.heartbeatTimeout = setTimeout(() => {
          // If no message received in 10 seconds, connection might be dead
          const timeSinceLastMessage = Date.now() - this.lastMessageTime
          if (timeSinceLastMessage > 10000) {
            console.warn('No heartbeat response received, connection may be dead')
            this.socket.close(4000, 'Heartbeat timeout')
          }
        }, 10000)
      }
    }, 30000)
  }
  
  stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval)
      this.heartbeatInterval = null
    }
    
    if (this.heartbeatTimeout) {
      clearTimeout(this.heartbeatTimeout)
      this.heartbeatTimeout = null
    }
  }
  
  send(data) {
    if (this.isConnected) {
      try {
        this.socket.send(JSON.stringify(data))
        return true
      } catch (error) {
        console.error('Error sending WebSocket message:', error)
        return false
      }
    } else {
      console.error('Cannot send message, WebSocket not connected')
      return false
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
  
  getConnectionStatus() {
    return {
      isConnected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
      maxReconnectAttempts: this.maxReconnectAttempts,
      error: this.connectionError ? this.connectionError.message : null,
      lastMessageTime: this.lastMessageTime ? new Date(this.lastMessageTime).toISOString() : null
    }
  }
}

// Create a singleton instance
const websocketService = new WebSocketService()

export default websocketService

