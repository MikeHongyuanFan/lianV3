import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import websocketService from '../websocket'
import { useAuthStore } from '../../store/auth'

// Mock WebSocket
class MockWebSocket {
  constructor(url) {
    this.url = url
    this.listeners = {}
    this.readyState = 1 // OPEN
    
    // Simulate connection open after creation
    setTimeout(() => {
      if (this.listeners.open) {
        this.listeners.open.forEach(callback => callback())
      }
    }, 0)
  }
  
  addEventListener(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = []
    }
    this.listeners[event].push(callback)
  }
  
  removeEventListener(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event] = this.listeners[event].filter(cb => cb !== callback)
    }
  }
  
  send(data) {
    // Store sent data for testing
    this.lastSentData = data
  }
  
  close() {
    // Simulate close event
    if (this.listeners.close) {
      this.listeners.close.forEach(callback => callback({ code: 1000 }))
    }
  }
  
  // Helper method to simulate receiving a message
  simulateMessage(data) {
    if (this.listeners.message) {
      this.listeners.message.forEach(callback => callback({ data }))
    }
  }
  
  // Helper method to simulate an error
  simulateError(error) {
    if (this.listeners.error) {
      this.listeners.error.forEach(callback => callback(error))
    }
  }
}

// Mock auth store
vi.mock('../../store/auth', () => ({
  useAuthStore: vi.fn()
}))

// Replace global WebSocket with mock
const originalWebSocket = global.WebSocket
beforeEach(() => {
  global.WebSocket = MockWebSocket
  
  // Mock auth store
  useAuthStore.mockReturnValue({
    isAuthenticated: true,
    token: 'fake-token'
  })
})

afterEach(() => {
  global.WebSocket = originalWebSocket
  
  // Disconnect websocket to clean up
  websocketService.disconnect()
})

describe('WebSocket Service', () => {
  it('connects to WebSocket with authentication token', () => {
    // Setup spy on WebSocket constructor
    const webSocketSpy = vi.spyOn(global, 'WebSocket')
    
    // Connect to WebSocket
    websocketService.connect()
    
    // Verify WebSocket was created with correct URL including token
    expect(webSocketSpy).toHaveBeenCalledWith(expect.stringContaining('token=fake-token'))
  })
  
  it('does not connect when user is not authenticated', () => {
    // Setup auth store to return not authenticated
    useAuthStore.mockReturnValue({
      isAuthenticated: false,
      token: null
    })
    
    // Setup spy on WebSocket constructor
    const webSocketSpy = vi.spyOn(global, 'WebSocket')
    
    // Try to connect
    websocketService.connect()
    
    // Verify WebSocket was not created
    expect(webSocketSpy).not.toHaveBeenCalled()
  })
  
  it('sends messages when connected', () => {
    // Connect to WebSocket
    websocketService.connect()
    
    // Get the WebSocket instance
    const socket = websocketService.socket
    
    // Send a message
    const message = { type: 'test_message', data: 'test_data' }
    websocketService.send(message)
    
    // Verify message was sent with correct data
    expect(socket.lastSentData).toBe(JSON.stringify(message))
  })
  
  it('notifies listeners when message is received', () => {
    // Setup listener
    const listener = vi.fn()
    websocketService.addListener('notification', listener)
    
    // Connect to WebSocket
    websocketService.connect()
    
    // Simulate receiving a message
    const message = {
      type: 'notification',
      notification: {
        id: 1,
        title: 'Test Notification',
        message: 'This is a test notification'
      }
    }
    websocketService.socket.simulateMessage(JSON.stringify(message))
    
    // Verify listener was called with correct data
    expect(listener).toHaveBeenCalledWith(message)
  })
  
  it('attempts to reconnect when connection is closed abnormally', () => {
    // Mock setTimeout
    const originalSetTimeout = global.setTimeout
    global.setTimeout = vi.fn((callback) => {
      // Call the callback immediately for testing
      callback()
      return 123 // Return a timeout ID
    })
    
    // Setup spy on WebSocket constructor
    const webSocketSpy = vi.spyOn(global, 'WebSocket')
    
    // Connect to WebSocket
    websocketService.connect()
    
    // Clear the spy to reset call count
    webSocketSpy.mockClear()
    
    // Simulate abnormal close
    websocketService.socket.listeners.close.forEach(callback => callback({ code: 1006 }))
    
    // Verify reconnect was attempted
    expect(webSocketSpy).toHaveBeenCalled()
    
    // Restore setTimeout
    global.setTimeout = originalSetTimeout
  })
  
  it('does not attempt to reconnect when connection is closed normally', () => {
    // Setup spy on WebSocket constructor
    const webSocketSpy = vi.spyOn(global, 'WebSocket')
    
    // Connect to WebSocket
    websocketService.connect()
    
    // Clear the spy to reset call count
    webSocketSpy.mockClear()
    
    // Simulate normal close
    websocketService.socket.listeners.close.forEach(callback => callback({ code: 1000 }))
    
    // Verify reconnect was not attempted
    expect(webSocketSpy).not.toHaveBeenCalled()
  })
  
  it('removes listeners correctly', () => {
    // Setup listener
    const listener = vi.fn()
    websocketService.addListener('notification', listener)
    
    // Connect to WebSocket
    websocketService.connect()
    
    // Remove the listener
    websocketService.removeListener('notification', listener)
    
    // Simulate receiving a message
    const message = {
      type: 'notification',
      notification: {
        id: 1,
        title: 'Test Notification',
        message: 'This is a test notification'
      }
    }
    websocketService.socket.simulateMessage(JSON.stringify(message))
    
    // Verify listener was not called
    expect(listener).not.toHaveBeenCalled()
  })
})