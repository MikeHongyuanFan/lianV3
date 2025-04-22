import api from './api'

export default {
  login(credentials) {
    return api.post('/users/auth/login/', credentials)
  },
  
  register(userData) {
    return api.post('/users/auth/register/', userData)
  },
  
  refreshToken(refreshToken) {
    return api.post('/users/auth/refresh/', refreshToken)
  },
  
  getUserInfo() {
    return api.get('/users/me/')
  }
}
