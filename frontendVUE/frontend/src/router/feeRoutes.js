// Fee routes configuration
const feeRoutes = [
  {
    path: '/fees',
    name: 'fee-list',
    component: () => import('../views/documents/FeeListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/fees/create',
    name: 'fee-create',
    component: () => import('../views/documents/FeeFormView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/fees/:id',
    name: 'fee-detail',
    component: () => import('../views/documents/FeeDetailView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/fees/:id/edit',
    name: 'fee-edit',
    component: () => import('../views/documents/FeeFormView.vue'),
    props: route => ({ 
      id: route.params.id,
      isEditing: true 
    }),
    meta: { requiresAuth: true }
  }
]

export default feeRoutes
