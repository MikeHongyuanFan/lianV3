import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useNotificationStore } from '../notifications'
import axios from 'axios'

// Mock axios
vi.mock('axios')

describe('Notification Store', () => {
  beforeEach(() => {
    // Create a fresh pinia instance for each test
    setActivePinia(createPinia())
    
    // Reset all mocks
    vi.resetAllMocks()
  })
  
  it('fetches notifications', async () => {
    // Mock data
    const mockNotifications = [
      { id: 1, title: 'Test 1', message: 'Message 1', read: false },
      { id: 2, title: 'Test 2', message: 'Message 2', read: true }
    ]
    
    // Setup mock response
    axios.get.mockResolvedValue({ data: mockNotifications })
    
    // Get store instance
    const store = useNotificationStore()
    
    // Call the action
    await store.fetchNotifications()
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/api/notifications/')
    
    // Verify state was updated correctly
    expect(store.notifications).toEqual(mockNotifications)
    expect(store.unreadCount).toBe(1)
    expect(store.loading).toBe(false)
    expect(store.error).toBe(null)
  })
  
  it('handles fetch notifications error', async () => {
    // Setup mock error response
    const errorMessage = 'Network Error'
    axios.get.mockRejectedValue({ 
      response: { data: { message: errorMessage } }
    })
    
    // Get store instance
    const store = useNotificationStore()
    
    // Call the action
    await store.fetchNotifications()
    
    // Verify state was updated correctly
    expect(store.notifications).toEqual([])
    expect(store.loading).toBe(false)
    expect(store.error).toBe(errorMessage)
  })
  
  it('marks notification as read', async () => {
    // Mock data
    const mockNotifications = [
      { id: 1, title: 'Test 1', message: 'Message 1', read: false },
      { id: 2, title: 'Test 2', message: 'Message 2', read: true }
    ]
    
    // Setup mock response
    axios.patch.mockResolvedValue({})
    
    // Get store instance
    const store = useNotificationStore()
    store.notifications = [...mockNotifications]
    store.unreadCount = 1
    
    // Call the action
    await store.markAsRead(1)
    
    // Verify axios was called correctly
    expect(axios.patch).toHaveBeenCalledWith('/api/notifications/1/', { read: true })
    
    // Verify state was updated correctly
    expect(store.notifications[0].read).toBe(true)
    expect(store.unreadCount).toBe(0)
  })
  
  it('marks all notifications as read', async () => {
    // Mock data
    const mockNotifications = [
      { id: 1, title: 'Test 1', message: 'Message 1', read: false },
      { id: 2, title: 'Test 2', message: 'Message 2', read: false }
    ]
    
    // Setup mock response
    axios.post.mockResolvedValue({})
    
    // Get store instance
    const store = useNotificationStore()
    store.notifications = [...mockNotifications]
    store.unreadCount = 2
    
    // Call the action
    await store.markAllAsRead()
    
    // Verify axios was called correctly
    expect(axios.post).toHaveBeenCalledWith('/api/notifications/mark-all-read/')
    
    // Verify state was updated correctly
    expect(store.notifications[0].read).toBe(true)
    expect(store.notifications[1].read).toBe(true)
    expect(store.unreadCount).toBe(0)
  })
  
  it('deletes notification', async () => {
    // Mock data
    const mockNotifications = [
      { id: 1, title: 'Test 1', message: 'Message 1', read: false },
      { id: 2, title: 'Test 2', message: 'Message 2', read: true }
    ]
    
    // Setup mock response
    axios.delete.mockResolvedValue({})
    
    // Get store instance
    const store = useNotificationStore()
    store.notifications = [...mockNotifications]
    store.unreadCount = 1
    
    // Call the action
    await store.deleteNotification(1)
    
    // Verify axios was called correctly
    expect(axios.delete).toHaveBeenCalledWith('/api/notifications/1/')
    
    // Verify state was updated correctly
    expect(store.notifications.length).toBe(1)
    expect(store.notifications[0].id).toBe(2)
    expect(store.unreadCount).toBe(0)
  })
  
  it('fetches notification preferences', async () => {
    // Mock data
    const mockPreferences = {
      emailNotifications: true,
      inAppNotifications: true,
      dailyDigest: false,
      weeklyDigest: true
    }
    
    // Setup mock response
    axios.get.mockResolvedValue({ data: mockPreferences })
    
    // Get store instance
    const store = useNotificationStore()
    
    // Call the action
    await store.fetchPreferences()
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/api/notification-preferences/')
    
    // Verify state was updated correctly
    expect(store.preferences).toEqual(mockPreferences)
  })
  
  it('updates notification preferences', async () => {
    // Mock data
    const mockPreferences = {
      emailNotifications: false,
      inAppNotifications: true,
      dailyDigest: true,
      weeklyDigest: false
    }
    
    // Setup mock response
    axios.put.mockResolvedValue({})
    
    // Get store instance
    const store = useNotificationStore()
    
    // Call the action
    await store.updatePreferences(mockPreferences)
    
    // Verify axios was called correctly
    expect(axios.put).toHaveBeenCalledWith('/api/notification-preferences/', mockPreferences)
    
    // Verify state was updated correctly
    expect(store.preferences).toEqual(mockPreferences)
  })
  
  it('adds new notification', () => {
    // Mock data
    const mockNotification = {
      id: 3,
      title: 'New Notification',
      message: 'This is a new notification',
      read: false
    }
    
    // Get store instance
    const store = useNotificationStore()
    store.notifications = [
      { id: 1, title: 'Test 1', message: 'Message 1', read: true },
      { id: 2, title: 'Test 2', message: 'Message 2', read: true }
    ]
    store.unreadCount = 0
    
    // Call the action
    store.addNotification(mockNotification)
    
    // Verify state was updated correctly
    expect(store.notifications.length).toBe(3)
    expect(store.notifications[0]).toEqual(mockNotification)
    expect(store.unreadCount).toBe(1)
  })
  
  it('correctly filters unread notifications', () => {
    // Mock data
    const mockNotifications = [
      { id: 1, title: 'Test 1', message: 'Message 1', read: false },
      { id: 2, title: 'Test 2', message: 'Message 2', read: true },
      { id: 3, title: 'Test 3', message: 'Message 3', read: false }
    ]
    
    // Get store instance
    const store = useNotificationStore()
    store.notifications = mockNotifications
    
    // Get unread notifications
    const unreadNotifications = store.getUnreadNotifications
    
    // Verify correct filtering
    expect(unreadNotifications.length).toBe(2)
    expect(unreadNotifications[0].id).toBe(1)
    expect(unreadNotifications[1].id).toBe(3)
  })
  
  it('correctly filters read notifications', () => {
    // Mock data
    const mockNotifications = [
      { id: 1, title: 'Test 1', message: 'Message 1', read: false },
      { id: 2, title: 'Test 2', message: 'Message 2', read: true },
      { id: 3, title: 'Test 3', message: 'Message 3', read: false }
    ]
    
    // Get store instance
    const store = useNotificationStore()
    store.notifications = mockNotifications
    
    // Get read notifications
    const readNotifications = store.getReadNotifications
    
    // Verify correct filtering
    expect(readNotifications.length).toBe(1)
    expect(readNotifications[0].id).toBe(2)
  })
})