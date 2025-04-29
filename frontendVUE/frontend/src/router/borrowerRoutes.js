// Borrower routes configuration
const borrowerRoutes = [
  {
    path: '/borrowers',
    name: 'borrower-list',
    component: () => import('../views/borrowers/BorrowerListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/borrowers/create',
    name: 'borrower-create',
    component: () => import('../views/borrowers/BorrowerCreateView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/borrowers/:id',
    name: 'borrower-detail',
    component: () => import('../views/borrowers/BorrowerDetailView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/borrowers/:id/edit',
    name: 'borrower-edit',
    component: () => import('../views/borrowers/BorrowerCreateView.vue'),
    props: route => ({ 
      id: route.params.id,
      isEditing: true 
    }),
    meta: { requiresAuth: true }
  }
]

export default borrowerRoutes
