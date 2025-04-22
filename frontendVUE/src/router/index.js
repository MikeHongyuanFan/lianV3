import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/broker',
      name: 'broker',
      component: () => import('../views/BrokerView.vue'),
      meta: { requiresAuth: true, requiresBroker: true }
    },
    {
      path: '/bd',
      name: 'bd',
      component: () => import('../views/BDView.vue'),
      meta: { requiresAuth: true, requiresBD: true }
    },
    {
      path: '/applications',
      name: 'applications',
      component: () => import('../views/ApplicationsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/applications/new',
      name: 'application-new',
      component: () => import('../views/ApplicationFormView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/applications/:id',
      name: 'application-detail',
      component: () => import('../views/ApplicationDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/borrowers/new',
      name: 'borrower-new',
      component: () => import('../views/BorrowerFormView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/borrowers',
      name: 'borrowers',
      component: () => import('../views/BorrowersView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/borrowers/:id',
      name: 'borrower-detail',
      component: () => import('../views/BorrowerDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: () => import('../views/NotificationsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/notification-preferences',
      name: 'notification-preferences',
      component: () => import('../views/NotificationPreferencesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reports',
      name: 'reports',
      component: () => import('../views/ReportsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reports/repayment-compliance',
      name: 'repayment-compliance-report',
      component: () => import('../views/reports/RepaymentComplianceReportView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reports/application-volume',
      name: 'application-volume-report',
      component: () => import('../views/reports/ApplicationVolumeReportView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reports/application-status',
      name: 'application-status-report',
      component: () => import('../views/reports/ApplicationStatusReportView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  
  // Check role-based access
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/')
    return
  }
  
  if (to.meta.requiresBroker && !authStore.isBroker) {
    next('/')
    return
  }
  
  if (to.meta.requiresBD && !authStore.isBD) {
    next('/')
    return
  }
  
  next()
})

export default router


