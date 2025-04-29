// Broker routes
export default [
  {
    path: '/brokers',
    name: 'BrokerList',
    component: () => import('@/views/broker/BrokerListView.vue'),
    meta: {
      requiresAuth: true,
      title: 'Brokers'
    }
  },
  {
    path: '/brokers/:id',
    name: 'BrokerDetail',
    component: () => import('@/views/broker/BrokerDetailView.vue'),
    props: true,
    meta: {
      requiresAuth: true,
      title: 'Broker Details'
    }
  },
  {
    path: '/branches',
    name: 'BranchList',
    component: () => import('@/views/broker/BranchListView.vue'),
    meta: {
      requiresAuth: true,
      title: 'Branches'
    }
  },
  {
    path: '/branches/:id',
    name: 'BranchDetail',
    component: () => import('@/views/broker/BranchDetailView.vue'),
    props: true,
    meta: {
      requiresAuth: true,
      title: 'Branch Details'
    }
  },
  {
    path: '/bdms',
    name: 'BDMList',
    component: () => import('@/views/broker/BDMListView.vue'),
    meta: {
      requiresAuth: true,
      title: 'Business Development Managers'
    }
  },
  {
    path: '/bdms/:id',
    name: 'BDMDetail',
    component: () => import('@/views/broker/BDMDetailView.vue'),
    props: true,
    meta: {
      requiresAuth: true,
      title: 'BDM Details'
    }
  }
]
