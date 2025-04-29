// Document routes configuration
const documentRoutes = [
  {
    path: '/documents',
    name: 'document-list',
    component: () => import('../views/documents/DocumentListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/documents/create',
    name: 'document-create',
    component: () => import('../views/documents/DocumentUploadView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/documents/:id',
    name: 'document-detail',
    component: () => import('../views/documents/DocumentDetailView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/documents/:id/edit',
    name: 'document-edit',
    component: () => import('../views/documents/DocumentUploadView.vue'),
    props: route => ({ 
      id: route.params.id,
      isEditing: true 
    }),
    meta: { requiresAuth: true }
  }
]

export default documentRoutes
