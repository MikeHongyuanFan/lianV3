import { defineStore } from 'pinia'
import api from '../services/api'
import authService from '../services/auth'
import { ref, computed } from 'vue'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref(localStorage.getItem('token') || '')
  const refreshToken = ref(localStorage.getItem('refreshToken') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))
  
  // Getters
  const isAuthenticated = computed(() => !!token.value)
  
  const userRole = computed(() => user.value?.role || '')
  
  const isAdmin = computed(() => userRole.value === 'admin')
  
  const isBroker = computed(() => userRole.value === 'broker')
  
  const isBD = computed(() => userRole.value === 'bd')
  
  const isClient = computed(() => userRole.value === 'client')
  
  // Actions
  async function login(credentials) {
    try {
      const response = await authService.login(credentials)
      
      // Store tokens and user data
      token.value = response.data.access
      refreshToken.value = response.data.refresh
      user.value = {
        id: response.data.user_id,
        email: response.data.email,
        role: response.data.role,
        name: response.data.name
      }
      
      // Save to localStorage
      localStorage.setItem('token', token.value)
      localStorage.setItem('refreshToken', refreshToken.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      
      return true
    } catch (error) {
      console.error('Login error:', error)
      return false
    }
  }
  
  async function register(userData) {
    try {
      const response = await authService.register(userData)
      
      // Store tokens and user data
      token.value = response.data.access
      refreshToken.value = response.data.refresh
      user.value = {
        id: response.data.user_id,
        email: response.data.email,
        role: response.data.role,
        name: response.data.name
      }
      
      // Save to localStorage
      localStorage.setItem('token', token.value)
      localStorage.setItem('refreshToken', refreshToken.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      
      return true
    } catch (error) {
      console.error('Registration error:', error)
      throw error
    }
  }
  
  async function refreshAccessToken() {
    try {
      const response = await authService.refreshToken({
        refresh: refreshToken.value
      })
      
      token.value = response.data.access
      localStorage.setItem('token', token.value)
      
      return true
    } catch (error) {
      console.error('Token refresh error:', error)
      logout()
      return false
    }
  }
  
  function logout() {
    // Clear state
    token.value = ''
    refreshToken.value = ''
    user.value = {}
    
    // Clear localStorage
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
    
    // Redirect to login
    router.push('/login')
  }
  
  function setTokens(accessToken, refreshTokenValue) {
    token.value = accessToken
    if (refreshTokenValue) {
      refreshToken.value = refreshTokenValue
      localStorage.setItem('refreshToken', refreshToken.value)
    }
    localStorage.setItem('token', token.value)
  }
  
  return {
    // State
    token,
    refreshToken,
    user,
    
    // Getters
    isAuthenticated,
    userRole,
    isAdmin,
    isBroker,
    isBD,
    isClient,
    
    // Actions
    login,
    register,
    refreshAccessToken,
    logout,
    setTokens
  }
})




