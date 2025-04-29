// Notification routes
const NotificationsView = () => import('../views/notifications/NotificationsView.vue')
const NotificationPreferencesView = () => import('../views/notifications/NotificationPreferencesView.vue')

const notificationRoutes = [
  {
    path: '/notifications',
    name: 'notifications',
    component: NotificationsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/notification-preferences',
    name: 'notification-preferences',
    component: NotificationPreferencesView,
    meta: { requiresAuth: true }
  }
]

export default notificationRoutes
