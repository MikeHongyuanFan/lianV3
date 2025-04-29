// Note routes configuration
const noteRoutes = [
  {
    path: '/notes',
    name: 'note-list',
    component: () => import('../views/notes/NoteListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/notes/create',
    name: 'note-create',
    component: () => import('../views/notes/NoteFormView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/notes/:id',
    name: 'note-detail',
    component: () => import('../views/notes/NoteDetailView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/notes/:id/edit',
    name: 'note-edit',
    component: () => import('../views/notes/NoteFormView.vue'),
    props: route => ({ 
      id: route.params.id,
      isEditing: true 
    }),
    meta: { requiresAuth: true }
  }
]

export default noteRoutes
