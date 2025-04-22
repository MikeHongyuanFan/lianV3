import api from './api'

export default {
  login(credentials) {
    return api.post('/api/users/auth/login/', credentials)
  },
  
  register(userData) {
    return api.post('/api/users/auth/register/', userData)
  },
  
  refreshToken(refreshToken) {
    return api.post('/api/users/auth/refresh/', refreshToken)
  },
  
  getUserInfo() {
    return api.get('/api/users/profile/')
  },
  
  getUserProfile() {
    return api.get('/api/users/profile/')
  },
  
  updateProfile(userData) {
    return api.patch('/api/users/profile/update/', userData)
  }
}


