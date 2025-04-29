// Admin routes
import { RouteRecordRaw } from 'vue-router'

// Lazy-loaded components
const UserListView = () => import('../views/admin/UserListView.vue')
const UserDetailView = () => import('../views/admin/UserDetailView.vue')

const adminRoutes: Array<RouteRecordRaw> = [
  {
    path: '/admin/users',
    name: 'admin-users',
    component: UserListView,
    meta: { 
      requiresAuth: true, 
      requiresAdmin: true,
      title: 'User Management' 
    }
  },
  {
    path: '/admin/users/:id',
    name: 'admin-user-detail',
    component: UserDetailView,
    meta: { 
      requiresAuth: true, 
      requiresAdmin: true,
      title: 'User Details' 
    }
  },
  {
    path: '/admin/users/create',
    name: 'admin-user-create',
    component: UserDetailView,
    meta: { 
      requiresAuth: true, 
      requiresAdmin: true,
      title: 'Create User' 
    }
  }
]

export default adminRoutes