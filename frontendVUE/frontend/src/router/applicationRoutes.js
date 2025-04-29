// Application routes configuration
const applicationRoutes = [
  {
    path: '/applications',
    name: 'applications',
    component: () => import('../views/applications/ApplicationListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/applications/create',
    name: 'application-create',
    component: () => import('../views/applications/ApplicationCreateView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/applications/:id',
    name: 'application-detail',
    component: () => import('../views/applications/ApplicationDetailView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/applications/:id/edit',
    name: 'application-edit',
    component: () => import('../views/applications/ApplicationCreateView.vue'),
    props: route => ({ 
      id: route.params.id,
      isEditing: true 
    }),
    meta: { requiresAuth: true }
  },
  {
    path: '/applications/:id/ledger',
    name: 'application-ledger',
    component: () => import('../views/documents/LedgerView.vue'),
    props: true,
    meta: { requiresAuth: true }
  }
]

export default applicationRoutes
