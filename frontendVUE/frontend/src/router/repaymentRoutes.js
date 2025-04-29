// Repayment routes configuration
const repaymentRoutes = [
  {
    path: '/repayments',
    name: 'repayment-list',
    component: () => import('../views/documents/RepaymentListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/repayments/create',
    name: 'repayment-create',
    component: () => import('../views/documents/RepaymentFormView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/repayments/:id',
    name: 'repayment-detail',
    component: () => import('../views/documents/RepaymentDetailView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/repayments/:id/edit',
    name: 'repayment-edit',
    component: () => import('../views/documents/RepaymentFormView.vue'),
    props: route => ({ 
      id: route.params.id,
      isEditing: true 
    }),
    meta: { requiresAuth: true }
  }
]

export default repaymentRoutes
