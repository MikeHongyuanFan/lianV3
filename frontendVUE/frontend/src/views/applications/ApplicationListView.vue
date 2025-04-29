<template>
  <MainLayout>
    <div class="application-list-container">
      <div class="page-header">
        <h1 class="text-2xl font-bold mb-4">Applications</h1>
        <div class="flex justify-between items-center mb-6">
          <div class="search-filter-container flex items-center space-x-4">
            <!-- Search input -->
            <div class="search-container">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by reference or purpose"
                class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                @input="debounceSearch"
              />
            </div>
            
            <!-- Status filter -->
            <div class="filter-container">
              <select
                v-model="selectedStage"
                class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                @change="applyFilters"
              >
                <option value="">All Stages</option>
                <option value="inquiry">Inquiry</option>
                <option value="pre_approval">Pre-Approval</option>
                <option value="valuation">Valuation</option>
                <option value="formal_approval">Formal Approval</option>
                <option value="settlement">Settlement</option>
                <option value="funded">Funded</option>
                <option value="declined">Declined</option>
                <option value="withdrawn">Withdrawn</option>
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
          
          <!-- Create new application button -->
          <button
            @click="navigateToCreate"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
          >
            Create New Application
          </button>
        </div>
      </div>
      
      <!-- Borrower/Guarantor Quick Links -->
      <BorrowerGuarantorLinks class="mb-6" />
      
      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="loader"></div>
      </div>
      
      <!-- Error state -->
      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        <p>{{ error }}</p>
        <button @click="fetchApplications" class="underline">Try again</button>
      </div>
      
      <!-- Empty state -->
      <div v-else-if="!hasApplications" class="text-center py-12">
        <p class="text-gray-500 mb-4">No applications found</p>
        <button
          @click="navigateToCreate"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
        >
          Create Your First Application
        </button>
      </div>
      
      <!-- Applications list -->
      <div v-else class="applications-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="application in applications"
          :key="application.id"
          class="application-card bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer"
          @click="navigateToDetail(application.id)"
        >
          <div class="flex justify-between items-start">
            <h3 class="text-lg font-semibold">{{ application.reference_number }}</h3>
            <span
              class="application-stage px-2 py-1 text-xs rounded-full"
              :class="{
                'bg-yellow-100 text-yellow-800': application.stage === 'inquiry',
                'bg-blue-100 text-blue-800': application.stage === 'pre_approval',
                'bg-purple-100 text-purple-800': application.stage === 'valuation',
                'bg-indigo-100 text-indigo-800': application.stage === 'formal_approval',
                'bg-green-100 text-green-800': application.stage === 'settlement',
                'bg-teal-100 text-teal-800': application.stage === 'funded',
                'bg-red-100 text-red-800': application.stage === 'declined',
                'bg-gray-100 text-gray-800': application.stage === 'withdrawn'
              }"
            >
              {{ application.stage_display || formatStage(application.stage) }}
            </span>
          </div>
          
          <div class="mt-2">
            <p class="text-gray-600">{{ application.purpose }}</p>
            <p class="font-medium mt-1">{{ formatCurrency(application.loan_amount) }}</p>
          </div>
          
          <div class="mt-3 flex justify-between text-sm text-gray-500">
            <span>{{ application.borrower_count }} borrower(s)</span>
            <span>{{ formatDate(application.created_at) }}</span>
          </div>
        </div>
      </div>
      
      <!-- Pagination -->
      <div v-if="hasApplications" class="pagination-container flex justify-between items-center mt-6">
        <div class="text-sm text-gray-500">
          Showing {{ paginationInfo.currentPage * paginationInfo.itemsPerPage - paginationInfo.itemsPerPage + 1 }} 
          to {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }} 
          of {{ paginationInfo.totalItems }} applications
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
  </MainLayout>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useApplicationStore } from '@/store/application'
import MainLayout from '@/layouts/MainLayout.vue'
import BorrowerGuarantorLinks from '@/components/BorrowerGuarantorLinks.vue'

export default {
  name: 'ApplicationListView',
  components: {
    MainLayout,
    BorrowerGuarantorLinks
  },
  setup() {
    const router = useRouter()
    const applicationStore = useApplicationStore()
    
    // Local state
    const searchQuery = ref('')
    const selectedStage = ref('')
    const itemsPerPage = ref(10)
    const searchTimeout = ref(null)
    
    // Computed properties
    const applications = computed(() => applicationStore.applications)
    const loading = computed(() => applicationStore.loading)
    const error = computed(() => applicationStore.error)
    const hasApplications = computed(() => applicationStore.hasApplications)
    const paginationInfo = computed(() => applicationStore.getPaginationInfo)
    const hasActiveFilters = computed(() => searchQuery.value || selectedStage.value)
    
    // Methods
    const fetchApplications = async () => {
      try {
        await applicationStore.fetchApplications()
      } catch (error) {
        console.error('Error fetching applications:', error)
      }
    }
    
    const navigateToDetail = (id) => {
      router.push({ name: 'application-detail', params: { id } })
    }
    
    const navigateToCreate = () => {
      router.push({ name: 'application-create' })
    }
    
    const debounceSearch = () => {
      clearTimeout(searchTimeout.value)
      searchTimeout.value = setTimeout(() => {
        applyFilters()
      }, 300)
    }
    
    const applyFilters = () => {
      applicationStore.setFilters({
        search: searchQuery.value,
        stage: selectedStage.value
      })
    }
    
    const clearFilters = () => {
      searchQuery.value = ''
      selectedStage.value = ''
      applicationStore.clearFilters()
    }
    
    const prevPage = () => {
      if (paginationInfo.value.currentPage > 1) {
        applicationStore.setPage(paginationInfo.value.currentPage - 1)
      }
    }
    
    const nextPage = () => {
      if (paginationInfo.value.currentPage < paginationInfo.value.totalPages) {
        applicationStore.setPage(paginationInfo.value.currentPage + 1)
      }
    }
    
    const changeItemsPerPage = () => {
      applicationStore.setLimit(itemsPerPage.value)
    }
    
    const formatStage = (stage) => {
      if (!stage) return 'Unknown'
      return stage
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    const formatCurrency = (amount) => {
      if (amount === null || amount === undefined) return 'N/A'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Unknown'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
    
    // Lifecycle hooks
    onMounted(() => {
      // Set initial items per page
      applicationStore.setLimit(itemsPerPage.value)
      fetchApplications()
    })
    
    return {
      applications,
      loading,
      error,
      hasApplications,
      paginationInfo,
      searchQuery,
      selectedStage,
      itemsPerPage,
      hasActiveFilters,
      fetchApplications,
      navigateToDetail,
      navigateToCreate,
      debounceSearch,
      applyFilters,
      clearFilters,
      prevPage,
      nextPage,
      changeItemsPerPage,
      formatStage,
      formatCurrency,
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
