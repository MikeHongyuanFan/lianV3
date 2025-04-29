<template>
  <div class="guarantor-list-container">
    <div class="header-section">
      <h1 class="text-2xl font-bold mb-4">Guarantors</h1>
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
          
          <!-- Relationship filter -->
          <div class="filter-container">
            <select
              v-model="selectedRelationship"
              class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="applyFilters"
            >
              <option value="">All Relationships</option>
              <option value="spouse">Spouse</option>
              <option value="parent">Parent</option>
              <option value="child">Child</option>
              <option value="sibling">Sibling</option>
              <option value="friend">Friend</option>
              <option value="business_partner">Business Partner</option>
              <option value="other">Other</option>
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
        
        <!-- Create new guarantor button -->
        <button
          @click="navigateToCreate"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
        >
          Create New Guarantor
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
      <button @click="fetchGuarantors" class="underline">Try again</button>
    </div>
    
    <!-- Empty state -->
    <div v-else-if="!hasGuarantors" class="text-center py-12">
      <p class="text-gray-500 mb-4">No guarantors found</p>
      <button
        @click="navigateToCreate"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
      >
        Create Your First Guarantor
      </button>
    </div>
    
    <!-- Guarantors list -->
    <div v-else class="guarantors-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="guarantor in guarantors"
        :key="guarantor.id"
        class="guarantor-card bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer"
        @click="navigateToDetail(guarantor.id)"
      >
        <div class="flex justify-between items-start">
          <h3 class="text-lg font-semibold">
            {{ guarantor.guarantor_type === 'company' ? guarantor.company_name : `${guarantor.first_name} ${guarantor.last_name}` }}
          </h3>
          <div class="flex flex-col items-end">
            <span
              class="guarantor-type-badge px-2 py-1 text-xs rounded-full mb-1"
              :class="guarantor.guarantor_type === 'company' ? 'bg-purple-100 text-purple-800' : 'bg-green-100 text-green-800'"
            >
              {{ guarantor.guarantor_type === 'company' ? 'Company' : 'Individual' }}
            </span>
            <span
              v-if="guarantor.relationship_to_borrower"
              class="relationship-badge px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800"
            >
              {{ formatRelationship(guarantor.relationship_to_borrower) }}
            </span>
          </div>
        </div>
        
        <div class="mt-2 text-gray-600">
          <p class="flex items-center">
            <span class="material-icons text-sm mr-2">email</span>
            {{ guarantor.email }}
          </p>
          <p class="flex items-center">
            <span class="material-icons text-sm mr-2">phone</span>
            {{ guarantor.phone_number }}
          </p>
          <p class="flex items-center">
            <span class="material-icons text-sm mr-2">home</span>
            {{ truncateAddress(guarantor.address) }}
          </p>
        </div>
        
        <div class="mt-3 text-sm text-gray-500">
          Created: {{ formatDate(guarantor.created_at) }}
        </div>
      </div>
    </div>
    
    <!-- Pagination -->
    <div v-if="hasGuarantors" class="pagination-container flex justify-between items-center mt-6">
      <div class="text-sm text-gray-500">
        Showing {{ paginationInfo.currentPage * paginationInfo.itemsPerPage - paginationInfo.itemsPerPage + 1 }} 
        to {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }} 
        of {{ paginationInfo.totalItems }} guarantors
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
import { useGuarantorStore } from '@/store/guarantor'

export default {
  name: 'GuarantorListView',
  setup() {
    const router = useRouter()
    const guarantorStore = useGuarantorStore()
    
    // Local state
    const searchQuery = ref('')
    const selectedRelationship = ref('')
    const itemsPerPage = ref(10)
    const searchTimeout = ref(null)
    
    // Computed properties
    const guarantors = computed(() => guarantorStore.guarantors)
    const loading = computed(() => guarantorStore.loading)
    const error = computed(() => guarantorStore.error)
    const hasGuarantors = computed(() => guarantorStore.hasGuarantors)
    const paginationInfo = computed(() => guarantorStore.getPaginationInfo)
    const hasActiveFilters = computed(() => searchQuery.value || selectedRelationship.value)
    
    // Methods
    const fetchGuarantors = async () => {
      try {
        await guarantorStore.fetchGuarantors()
      } catch (error) {
        console.error('Error fetching guarantors:', error)
      }
    }
    
    const navigateToDetail = (id) => {
      router.push({ name: 'guarantor-detail', params: { id } })
    }
    
    const navigateToCreate = () => {
      router.push({ name: 'guarantor-create' })
    }
    
    const debounceSearch = () => {
      clearTimeout(searchTimeout.value)
      searchTimeout.value = setTimeout(() => {
        applyFilters()
      }, 300)
    }
    
    const applyFilters = () => {
      guarantorStore.setFilters({
        search: searchQuery.value,
        relationshipToBorrower: selectedRelationship.value
      })
    }
    
    const clearFilters = () => {
      searchQuery.value = ''
      selectedRelationship.value = ''
      guarantorStore.clearFilters()
    }
    
    const prevPage = () => {
      if (paginationInfo.value.currentPage > 1) {
        guarantorStore.setPage(paginationInfo.value.currentPage - 1)
      }
    }
    
    const nextPage = () => {
      if (paginationInfo.value.currentPage < paginationInfo.value.totalPages) {
        guarantorStore.setPage(paginationInfo.value.currentPage + 1)
      }
    }
    
    const changeItemsPerPage = () => {
      guarantorStore.setLimit(itemsPerPage.value)
    }
    
    const formatRelationship = (relationship) => {
      if (!relationship) return 'Unknown'
      
      // Convert snake_case to Title Case
      return relationship
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
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
      guarantorStore.setLimit(itemsPerPage.value)
      fetchGuarantors()
    })
    
    return {
      guarantors,
      loading,
      error,
      hasGuarantors,
      paginationInfo,
      searchQuery,
      selectedRelationship,
      itemsPerPage,
      hasActiveFilters,
      fetchGuarantors,
      navigateToDetail,
      navigateToCreate,
      debounceSearch,
      applyFilters,
      clearFilters,
      prevPage,
      nextPage,
      changeItemsPerPage,
      formatRelationship,
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
