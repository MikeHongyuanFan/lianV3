import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'
import applicationRoutes from './applicationRoutes'
import borrowerRoutes from './borrowerRoutes'
import guarantorRoutes from './guarantorRoutes'
import documentRoutes from './documentRoutes'
import noteRoutes from './noteRoutes'
import feeRoutes from './feeRoutes'
import repaymentRoutes from './repaymentRoutes'
import notificationRoutes from './notificationRoutes'
import brokerRoutes from './broker.routes'

// Lazy-loaded components
const LoginView = () => import('../views/LoginView.vue')
const RegisterView = () => import('../views/RegisterView.vue')
const DashboardView = () => import('../views/DashboardView.vue')
const ProfileView = () => import('../views/ProfileView.vue')
const NotFoundView = () => import('../views/NotFoundView.vue')
const ApplicationsView = () => import('../views/applications/ApplicationsView.vue')
const DocumentsView = () => import('../views/documents/DocumentsView.vue')
const FeesView = () => import('../views/financial/FeesView.vue')
const RepaymentsView = () => import('../views/financial/RepaymentsView.vue')

// Routes configuration
const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true, title: 'Dashboard' }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true, title: 'Profile' }
  },
  {
    path: '/applications',
    name: 'ApplicationList',
    component: ApplicationsView,
    meta: { requiresAuth: true, title: 'Applications' }
  },
  {
    path: '/documents',
    name: 'DocumentList',
    component: DocumentsView,
    meta: { requiresAuth: true, title: 'Documents' }
  },
  {
    path: '/fees',
    name: 'FeeList',
    component: FeesView,
    meta: { requiresAuth: true, title: 'Fees' }
  },
  {
    path: '/repayments',
    name: 'RepaymentList',
    component: RepaymentsView,
    meta: { requiresAuth: true, title: 'Repayments' }
  },
  // Include application routes
  ...applicationRoutes,
  // Include borrower routes
  ...borrowerRoutes,
  // Include guarantor routes
  ...guarantorRoutes,
  // Include document routes
  ...documentRoutes,
  // Include note routes
  ...noteRoutes,
  // Include fee routes
  ...feeRoutes,
  // Include repayment routes
  ...repaymentRoutes,
  // Include notification routes
  ...notificationRoutes,
  // Include broker routes
  ...brokerRoutes,
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView
  }
]

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  // If route requires auth and user is not authenticated, redirect to login
  if (requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } 
  // If user is authenticated and tries to access login/register, redirect to dashboard
  else if (isAuthenticated && (to.name === 'login' || to.name === 'register')) {
    next({ name: 'dashboard' })
  } 
  // Otherwise proceed as normal
  else {
    next()
  }
})

export default router
