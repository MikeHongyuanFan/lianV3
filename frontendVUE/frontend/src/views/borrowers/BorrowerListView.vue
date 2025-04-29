<template>
  <div class="borrower-list-container">
    <div class="header-section">
      <h1 class="text-2xl font-bold mb-4">Borrowers</h1>
      <div class="flex justify-between items-center mb-6">
        <div class="search-filter-container flex items-center space-x-4">
          <!-- Search input -->
          <div class="search-container">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by name or email"
              class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              @input="debounceSearch"
            />
          </div>
          
          <!-- Borrower type filter -->
          <div class="filter-container">
            <select
              v-model="selectedBorrowerType"
              class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="applyFilters"
            >
              <option value="">All Borrower Types</option>
              <option value="individual">Individual</option>
              <option value="company">Company</option>
              <option value="trust">Trust</option>
            </select>
          </div>
          
          <!-- Clear filters button -->
          <button
            v-if="hasActiveFilters"
            @click="clearFilters"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
          >
            Clear Filters
          </button>
        </div>
        
        <!-- Create new borrower button -->
        <button
          @click="navigateToCreate"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
        >
          Create New Borrower
        </button>
      </div>
    </div>
    
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchBorrowers" class="underline">Try again</button>
    </div>
    
    <!-- Empty state -->
    <div v-else-if="!hasBorrowers" class="text-center py-12">
      <p class="text-gray-500 mb-4">No borrowers found</p>
      <button
        @click="navigateToCreate"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
      >
        Create Your First Borrower
      </button>
    </div>
    
    <!-- Borrowers list -->
    <div v-else class="borrowers-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="borrower in borrowers"
        :key="borrower.id"
        class="borrower-card bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer"
        @click="navigateToDetail(borrower.id)"
      >
        <div class="flex justify-between items-start">
          <h3 class="text-lg font-semibold">{{ borrower.first_name }} {{ borrower.last_name }}</h3>
          <span
            class="borrower-type px-2 py-1 text-xs rounded-full"
            :class="{
              'bg-blue-100 text-blue-800': borrower.borrower_type === 'individual',
              'bg-green-100 text-green-800': borrower.borrower_type === 'company',
              'bg-purple-100 text-purple-800': borrower.borrower_type === 'trust'
            }"
          >
            {{ formatBorrowerType(borrower.borrower_type) }}
          </span>
        </div>
        
        <div class="mt-2 text-gray-600">
          <p class="flex items-center">
            <span class="material-icons text-sm mr-2">email</span>
            {{ borrower.email }}
          </p>
          <p class="flex items-center">
            <span class="material-icons text-sm mr-2">phone</span>
            {{ borrower.phone_number }}
          </p>
          <p class="flex items-center">
            <span class="material-icons text-sm mr-2">home</span>
            {{ truncateAddress(borrower.address) }}
          </p>
        </div>
        
        <div class="mt-3 text-sm text-gray-500">
          Created: {{ formatDate(borrower.created_at) }}
        </div>
      </div>
    </div>
    
    <!-- Pagination -->
    <div v-if="hasBorrowers" class="pagination-container flex justify-between items-center mt-6">
      <div class="text-sm text-gray-500">
        Showing {{ paginationInfo.currentPage * paginationInfo.itemsPerPage - paginationInfo.itemsPerPage + 1 }} 
        to {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }} 
        of {{ paginationInfo.totalItems }} borrowers
      </div>
      
      <div class="flex items-center space-x-2">
        <button
          @click="prevPage"
          :disabled="paginationInfo.currentPage === 1"
          class="px-3 py-1 border rounded-md"
          :class="paginationInfo.currentPage === 1 ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'"
        >
          Previous
        </button>
        
        <span class="px-3 py-1">
          Page {{ paginationInfo.currentPage }} of {{ paginationInfo.totalPages }}
        </span>
        
        <button
          @click="nextPage"
          :disabled="paginationInfo.currentPage === paginationInfo.totalPages"
          class="px-3 py-1 border rounded-md"
          :class="paginationInfo.currentPage === paginationInfo.totalPages ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'"
        >
          Next
        </button>
        
        <select
          v-model="itemsPerPage"
          class="ml-4 px-2 py-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          @change="changeItemsPerPage"
        >
          <option :value="10">10 per page</option>
          <option :value="25">25 per page</option>
          <option :value="50">50 per page</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBorrowerStore } from '@/store/borrower'

export default {
  name: 'BorrowerListView',
  setup() {
    const router = useRouter()
    const borrowerStore = useBorrowerStore()
    
    // Local state
    const searchQuery = ref('')
    const selectedBorrowerType = ref('')
    const itemsPerPage = ref(10)
    const searchTimeout = ref(null)
    
    // Computed properties
    const borrowers = computed(() => borrowerStore.borrowers)
    const loading = computed(() => borrowerStore.loading)
    const error = computed(() => borrowerStore.error)
    const hasBorrowers = computed(() => borrowerStore.hasBorrowers)
    const paginationInfo = computed(() => borrowerStore.getPaginationInfo)
    const hasActiveFilters = computed(() => searchQuery.value || selectedBorrowerType.value)
    
    // Methods
    const fetchBorrowers = async () => {
      try {
        await borrowerStore.fetchBorrowers()
      } catch (error) {
        console.error('Error fetching borrowers:', error)
      }
    }
    
    const navigateToDetail = (id) => {
      router.push({ name: 'borrower-detail', params: { id } })
    }
    
    const navigateToCreate = () => {
      router.push({ name: 'borrower-create' })
    }
    
    const debounceSearch = () => {
      clearTimeout(searchTimeout.value)
      searchTimeout.value = setTimeout(() => {
        applyFilters()
      }, 300)
    }
    
    const applyFilters = () => {
      borrowerStore.setFilters({
        search: searchQuery.value,
        borrowerType: selectedBorrowerType.value
      })
    }
    
    const clearFilters = () => {
      searchQuery.value = ''
      selectedBorrowerType.value = ''
      borrowerStore.clearFilters()
    }
    
    const prevPage = () => {
      if (paginationInfo.value.currentPage > 1) {
        borrowerStore.setPage(paginationInfo.value.currentPage - 1)
      }
    }
    
    const nextPage = () => {
      if (paginationInfo.value.currentPage < paginationInfo.value.totalPages) {
        borrowerStore.setPage(paginationInfo.value.currentPage + 1)
      }
    }
    
    const changeItemsPerPage = () => {
      borrowerStore.setLimit(itemsPerPage.value)
    }
    
    const formatBorrowerType = (type) => {
      if (!type) return 'Unknown'
      return type.charAt(0).toUpperCase() + type.slice(1)
    }
    
    const truncateAddress = (address) => {
      if (!address) return 'No address'
      return address.length > 30 ? address.substring(0, 30) + '...' : address
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Unknown'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
    
    // Lifecycle hooks
    onMounted(() => {
      // Set initial items per page
      borrowerStore.setLimit(itemsPerPage.value)
      fetchBorrowers()
    })
    
    return {
      borrowers,
      loading,
      error,
      hasBorrowers,
      paginationInfo,
      searchQuery,
      selectedBorrowerType,
      itemsPerPage,
      hasActiveFilters,
      fetchBorrowers,
      navigateToDetail,
      navigateToCreate,
      debounceSearch,
      applyFilters,
      clearFilters,
      prevPage,
      nextPage,
      changeItemsPerPage,
      formatBorrowerType,
      truncateAddress,
      formatDate
    }
  }
}
</script>

<style scoped>
.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
