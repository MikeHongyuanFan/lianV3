// Guarantor routes configuration
const guarantorRoutes = [
  {
    path: '/guarantors',
    name: 'guarantor-list',
    component: () => import('../views/guarantors/GuarantorListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/guarantors/create',
    name: 'guarantor-create',
    component: () => import('../views/guarantors/GuarantorCreateView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/guarantors/:id',
    name: 'guarantor-detail',
    component: () => import('../views/guarantors/GuarantorDetailView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/guarantors/:id/edit',
    name: 'guarantor-edit',
    component: () => import('../views/guarantors/GuarantorCreateView.vue'),
    props: route => ({ 
      id: route.params.id,
      isEditing: true 
    }),
    meta: { requiresAuth: true }
  }
]

export default guarantorRoutes
