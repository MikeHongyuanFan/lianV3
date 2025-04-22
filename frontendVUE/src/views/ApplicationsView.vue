<template>
  <div class="applications-view">
    <h1 class="text-2xl font-bold mb-6">Loan Applications</h1>
    
    <div class="mb-6 flex justify-between items-center">
      <div class="flex space-x-4">
        <button 
          @click="createNewApplication" 
          class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded"
        >
          Create New Application
        </button>
        
        <div class="relative">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search applications..." 
            class="border border-gray-300 rounded py-2 px-4 w-64"
          />
          <button 
            v-if="searchQuery" 
            @click="searchQuery = ''" 
            class="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
        </div>
      </div>
      
      <div class="flex items-center space-x-2">
        <label class="text-sm text-gray-600">Filter by status:</label>
        <select 
          v-model="statusFilter" 
          class="border border-gray-300 rounded py-2 px-3"
        >
          <option value="">All Statuses</option>
          <option value="inquiry">Inquiry</option>
          <option value="pre_approval">Pre-Approval</option>
          <option value="processing">Processing</option>
          <option value="approved">Approved</option>
          <option value="settled">Settled</option>
          <option value="declined">Declined</option>
        </select>
      </div>
    </div>
    
    <div v-if="loading" class="flex justify-center my-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>
    
    <div v-else-if="applications.length === 0" class="text-center my-12">
      <p class="text-gray-500 text-lg">No applications found</p>
      <button 
        @click="createNewApplication" 
        class="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded"
      >
        Create Your First Application
      </button>
    </div>
    
    <div v-else class="overflow-x-auto">
      <table class="min-w-full bg-white border border-gray-200">
        <thead>
          <tr>
            <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
              ID
            </th>
            <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
              Borrower
            </th>
            <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
              Loan Amount
            </th>
            <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
              Type
            </th>
            <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
              Status
            </th>
            <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
              Created
            </th>
            <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="application in applications" :key="application.id" class="hover:bg-gray-50">
            <td class="py-4 px-4 border-b border-gray-200">
              {{ application.id }}
            </td>
            <td class="py-4 px-4 border-b border-gray-200">
              {{ getBorrowerNames(application) }}
            </td>
            <td class="py-4 px-4 border-b border-gray-200">
              {{ formatCurrency(application.loan_amount) }}
            </td>
            <td class="py-4 px-4 border-b border-gray-200 capitalize">
              {{ application.application_type }}
            </td>
            <td class="py-4 px-4 border-b border-gray-200">
              <span 
                :class="getStatusClass(application.stage)" 
                class="px-2 py-1 text-xs font-medium rounded-full"
              >
                {{ formatStatus(application.stage) }}
              </span>
            </td>
            <td class="py-4 px-4 border-b border-gray-200">
              {{ formatDate(application.created_at) }}
            </td>
            <td class="py-4 px-4 border-b border-gray-200">
              <button 
                @click="viewApplication(application.id)" 
                class="text-blue-600 hover:text-blue-800 mr-3"
              >
                View
              </button>
              <button 
                v-if="canEdit(application)" 
                @click="editApplication(application.id)" 
                class="text-green-600 hover:text-green-800"
              >
                Edit
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div class="mt-4 flex justify-between items-center">
        <div class="text-sm text-gray-600">
          Showing {{ applications.length }} of {{ totalApplications }} applications
        </div>
        
        <div class="flex space-x-2">
          <button 
            @click="prevPage" 
            :disabled="currentPage === 1" 
            :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
            class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded"
          >
            Previous
          </button>
          <button 
            @click="nextPage" 
            :disabled="!hasMorePages" 
            :class="{ 'opacity-50 cursor-not-allowed': !hasMorePages }"
            class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../store/auth'

const router = useRouter()
const authStore = useAuthStore()

// State
const applications = ref([])
const loading = ref(true)
const searchQuery = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalApplications = ref(0)

// Computed
const hasMorePages = computed(() => {
  return currentPage.value * pageSize.value < totalApplications.value
})

// Methods
const fetchApplications = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    
    if (statusFilter.value) {
      params.stage = statusFilter.value
    }
    
    const response = await axios.get('/api/applications/applications/', { params })
    applications.value = response.data.results
    totalApplications.value = response.data.count
  } catch (error) {
    console.error('Error fetching applications:', error)
  } finally {
    loading.value = false
  }
}

const createNewApplication = () => {
  router.push({ name: 'application-new' })
}

const viewApplication = (id) => {
  router.push({ name: 'application-detail', params: { id } })
}

const editApplication = (id) => {
  router.push({ name: 'application-detail', params: { id }, query: { edit: true } })
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (hasMorePages.value) {
    currentPage.value++
  }
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0
  }).format(amount)
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

const formatStatus = (status) => {
  if (!status) return ''
  return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const getStatusClass = (status) => {
  switch (status) {
    case 'inquiry':
      return 'bg-gray-100 text-gray-800'
    case 'pre_approval':
      return 'bg-blue-100 text-blue-800'
    case 'processing':
      return 'bg-yellow-100 text-yellow-800'
    case 'approved':
      return 'bg-green-100 text-green-800'
    case 'settled':
      return 'bg-purple-100 text-purple-800'
    case 'declined':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const getBorrowerNames = (application) => {
  if (!application.borrowers || application.borrowers.length === 0) {
    return 'No borrowers'
  }
  
  return application.borrowers
    .map(borrower => `${borrower.first_name} ${borrower.last_name}`)
    .join(', ')
}

const canEdit = (application) => {
  // Check if user has permission to edit
  if (authStore.isAdmin) return true
  if (authStore.isBroker && application.broker?.user_id === authStore.userId) return true
  return false
}

// Watchers
watch([searchQuery, statusFilter], () => {
  currentPage.value = 1
  fetchApplications()
})

watch(currentPage, () => {
  fetchApplications()
})

// Lifecycle
onMounted(() => {
  fetchApplications()
})
</script>
