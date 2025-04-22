<template>
  <div class="borrowers-view">
    <h1 class="text-2xl font-bold mb-6">Borrowers</h1>
    
    <div class="mb-6 flex justify-between items-center">
      <div class="flex space-x-4">
        <button 
          @click="createNewBorrower" 
          class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded"
        >
          Add New Borrower
        </button>
        
        <div class="relative">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search borrowers..." 
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
        <label class="text-sm text-gray-600">Filter by type:</label>
        <select 
          v-model="typeFilter" 
          class="border border-gray-300 rounded py-2 px-3"
        >
          <option value="">All Types</option>
          <option value="individual">Individual</option>
          <option value="company">Company</option>
        </select>
      </div>
    </div>
    
    <div v-if="loading" class="flex justify-center my-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>
    
    <div v-else-if="borrowers.length === 0" class="text-center my-12">
      <p class="text-gray-500 text-lg">No borrowers found</p>
      <button 
        @click="createNewBorrower" 
        class="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded"
      >
        Add Your First Borrower
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
              Name
            </th>
            <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
              Email
            </th>
            <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
              Phone
            </th>
            <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
              Type
            </th>
            <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
              Applications
            </th>
            <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="borrower in borrowers" :key="borrower.id" class="hover:bg-gray-50">
            <td class="py-4 px-4 border-b border-gray-200">
              {{ borrower.id }}
            </td>
            <td class="py-4 px-4 border-b border-gray-200">
              {{ getBorrowerName(borrower) }}
            </td>
            <td class="py-4 px-4 border-b border-gray-200">
              {{ borrower.email }}
            </td>
            <td class="py-4 px-4 border-b border-gray-200">
              {{ borrower.phone }}
            </td>
            <td class="py-4 px-4 border-b border-gray-200 capitalize">
              {{ borrower.borrower_type || 'Individual' }}
            </td>
            <td class="py-4 px-4 border-b border-gray-200">
              {{ borrower.application_count || 0 }}
            </td>
            <td class="py-4 px-4 border-b border-gray-200">
              <button 
                @click="viewBorrower(borrower.id)" 
                class="text-blue-600 hover:text-blue-800 mr-3"
              >
                View
              </button>
              <button 
                v-if="canEdit(borrower)" 
                @click="editBorrower(borrower.id)" 
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
          Showing {{ borrowers.length }} of {{ totalBorrowers }} borrowers
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
const borrowers = ref([])
const loading = ref(true)
const searchQuery = ref('')
const typeFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalBorrowers = ref(0)

// Computed
const hasMorePages = computed(() => {
  return currentPage.value * pageSize.value < totalBorrowers.value
})

// Methods
const fetchBorrowers = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    
    if (typeFilter.value) {
      params.borrower_type = typeFilter.value
    }
    
    const response = await axios.get('/api/borrowers/borrowers/', { params })
    borrowers.value = response.data.results
    totalBorrowers.value = response.data.count
  } catch (error) {
    console.error('Error fetching borrowers:', error)
  } finally {
    loading.value = false
  }
}

const createNewBorrower = () => {
  router.push({ name: 'borrower-new' })
}

const viewBorrower = (id) => {
  router.push({ name: 'borrower-detail', params: { id } })
}

const editBorrower = (id) => {
  router.push({ name: 'borrower-detail', params: { id }, query: { edit: true } })
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

const getBorrowerName = (borrower) => {
  if (borrower.borrower_type === 'company') {
    return borrower.company_name
  }
  return `${borrower.first_name} ${borrower.last_name}`
}

const canEdit = (borrower) => {
  // Check if user has permission to edit
  if (authStore.isAdmin) return true
  if (authStore.isBroker && borrower.created_by === authStore.userId) return true
  return false
}

// Watchers
watch([searchQuery, typeFilter], () => {
  currentPage.value = 1
  fetchBorrowers()
})

watch(currentPage, () => {
  fetchBorrowers()
})

// Lifecycle
onMounted(() => {
  fetchBorrowers()
})
</script>
