<template>
  <div class="document-list-container">
    <div class="header-section">
      <h1 class="text-2xl font-bold mb-4">Documents</h1>
      <div class="flex justify-between items-center mb-6">
        <div class="search-filter-container flex items-center space-x-4">
          <!-- Search input -->
          <div class="search-container">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by title, description or filename"
              class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              @input="debounceSearch"
            />
          </div>
          
          <!-- Document type filter -->
          <div class="filter-container">
            <select
              v-model="selectedDocumentType"
              class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="applyFilters"
            >
              <option value="">All Document Types</option>
              <option value="contract">Contract</option>
              <option value="application_form">Application Form</option>
              <option value="id_verification">ID Verification</option>
              <option value="income_proof">Income Proof</option>
              <option value="property_valuation">Property Valuation</option>
              <option value="credit_report">Credit Report</option>
              <option value="bank_statement">Bank Statement</option>
              <option value="insurance">Insurance</option>
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
        
        <!-- Create new document button -->
        <button
          @click="navigateToCreate"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
        >
          Upload New Document
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
      <button @click="fetchDocuments" class="underline">Try again</button>
    </div>
    
    <!-- Empty state -->
    <div v-else-if="!hasDocuments" class="text-center py-12">
      <p class="text-gray-500 mb-4">No documents found</p>
      <button
        @click="navigateToCreate"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
      >
        Upload Your First Document
      </button>
    </div>
    
    <!-- Documents list -->
    <div v-else class="documents-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="document in documents"
        :key="document.id"
        class="document-card bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer"
        @click="navigateToDetail(document.id)"
      >
        <div class="flex justify-between items-start">
          <h3 class="text-lg font-semibold">{{ document.title }}</h3>
          <span
            v-if="document.document_type"
            class="document-type-badge px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800"
          >
            {{ formatDocumentType(document.document_type_display || document.document_type) }}
          </span>
        </div>
        
        <p v-if="document.description" class="mt-2 text-gray-600 line-clamp-2">
          {{ document.description }}
        </p>
        
        <div class="mt-3 text-sm text-gray-500">
          <div class="flex items-center">
            <span class="material-icons text-sm mr-2">description</span>
            {{ document.file_name }}
          </div>
          <div class="flex items-center">
            <span class="material-icons text-sm mr-2">straighten</span>
            {{ formatFileSize(document.file_size) }}
          </div>
          <div class="flex items-center">
            <span class="material-icons text-sm mr-2">person</span>
            {{ document.created_by_name }}
          </div>
        </div>
        
        <div class="mt-3 text-xs text-gray-500">
          Uploaded: {{ formatDate(document.created_at) }}
          <span v-if="document.version > 1" class="ml-2 px-2 py-0.5 bg-gray-100 rounded-full">
            Version {{ document.version }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- Pagination -->
    <div v-if="hasDocuments" class="pagination-container flex justify-between items-center mt-6">
      <div class="text-sm text-gray-500">
        Showing {{ paginationInfo.currentPage * paginationInfo.itemsPerPage - paginationInfo.itemsPerPage + 1 }} 
        to {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }} 
        of {{ paginationInfo.totalItems }} documents
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
import { useRouter, useRoute } from 'vue-router'
import { useDocumentStore } from '@/store/document'

export default {
  name: 'DocumentListView',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const documentStore = useDocumentStore()
    
    // Local state
    const searchQuery = ref('')
    const selectedDocumentType = ref('')
    const itemsPerPage = ref(10)
    const searchTimeout = ref(null)
    
    // Computed properties
    const documents = computed(() => documentStore.documents)
    const loading = computed(() => documentStore.loading)
    const error = computed(() => documentStore.error)
    const hasDocuments = computed(() => documentStore.hasDocuments)
    const paginationInfo = computed(() => documentStore.getPaginationInfo)
    const hasActiveFilters = computed(() => searchQuery.value || selectedDocumentType.value)
    
    // Methods
    const fetchDocuments = async () => {
      try {
        await documentStore.fetchDocuments()
      } catch (error) {
        console.error('Error fetching documents:', error)
      }
    }
    
    const navigateToDetail = (id) => {
      router.push({ name: 'document-detail', params: { id } })
    }
    
    const navigateToCreate = () => {
      router.push({ name: 'document-create' })
    }
    
    const debounceSearch = () => {
      clearTimeout(searchTimeout.value)
      searchTimeout.value = setTimeout(() => {
        applyFilters()
      }, 300)
    }
    
    const applyFilters = () => {
      documentStore.setFilters({
        search: searchQuery.value,
        documentType: selectedDocumentType.value
      })
    }
    
    const clearFilters = () => {
      searchQuery.value = ''
      selectedDocumentType.value = ''
      documentStore.clearFilters()
    }
    
    const prevPage = () => {
      if (paginationInfo.value.currentPage > 1) {
        documentStore.setPage(paginationInfo.value.currentPage - 1)
      }
    }
    
    const nextPage = () => {
      if (paginationInfo.value.currentPage < paginationInfo.value.totalPages) {
        documentStore.setPage(paginationInfo.value.currentPage + 1)
      }
    }
    
    const changeItemsPerPage = () => {
      documentStore.setLimit(itemsPerPage.value)
    }
    
    const formatDocumentType = (type) => {
      if (!type) return 'Unknown'
      
      // If it's already formatted (from document_type_display), return as is
      if (type.includes(' ')) return type
      
      // Convert snake_case to Title Case
      return type
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    const formatFileSize = (bytes) => {
      if (!bytes) return 'Unknown size'
      
      const units = ['B', 'KB', 'MB', 'GB']
      let size = bytes
      let unitIndex = 0
      
      while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024
        unitIndex++
      }
      
      return `${size.toFixed(1)} ${units[unitIndex]}`
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Unknown'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
    
    // Initialize with query parameters if present
    const initializeFromQuery = () => {
      if (route.query.search) {
        searchQuery.value = route.query.search
      }
      
      if (route.query.document_type) {
        selectedDocumentType.value = route.query.document_type
      }
      
      // Apply filters if any query parameters were set
      if (searchQuery.value || selectedDocumentType.value) {
        applyFilters()
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      // Set initial items per page
      documentStore.setLimit(itemsPerPage.value)
      
      // Initialize from query parameters
      initializeFromQuery()
      
      // Fetch documents
      fetchDocuments()
    })
    
    return {
      documents,
      loading,
      error,
      hasDocuments,
      paginationInfo,
      searchQuery,
      selectedDocumentType,
      itemsPerPage,
      hasActiveFilters,
      fetchDocuments,
      navigateToDetail,
      navigateToCreate,
      debounceSearch,
      applyFilters,
      clearFilters,
      prevPage,
      nextPage,
      changeItemsPerPage,
      formatDocumentType,
      formatFileSize,
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

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
