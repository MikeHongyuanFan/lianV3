<template>
  <div class="borrower-detail-container">
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchBorrowerData" class="underline">Try again</button>
    </div>
    
    <!-- Borrower details -->
    <div v-else-if="borrower" class="bg-white rounded-lg shadow-md p-6">
      <div class="flex justify-between items-start mb-6">
        <div>
          <h1 class="text-2xl font-bold">{{ borrower.first_name }} {{ borrower.last_name }}</h1>
          <span
            v-if="borrower.borrower_type"
            class="borrower-type-badge px-2 py-1 text-xs rounded-full mt-2 inline-block bg-blue-100 text-blue-800"
          >
            {{ formatBorrowerType(borrower.borrower_type) }}
          </span>
        </div>
        
        <div class="flex space-x-2">
          <button
            @click="navigateToEdit"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
          >
            Edit
          </button>
          <button
            @click="confirmDelete"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none"
          >
            Delete
          </button>
        </div>
      </div>
      
      <!-- Tabs navigation -->
      <div class="border-b mb-6">
        <nav class="flex space-x-8">
          <button
            @click="activeTab = 'details'"
            class="py-4 px-1 border-b-2 font-medium text-sm"
            :class="activeTab === 'details' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          >
            Details
          </button>
          <button
            @click="activeTab = 'financial'"
            class="py-4 px-1 border-b-2 font-medium text-sm"
            :class="activeTab === 'financial' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          >
            Financial Summary
          </button>
          <button
            @click="activeTab = 'applications'"
            class="py-4 px-1 border-b-2 font-medium text-sm"
            :class="activeTab === 'applications' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          >
            Applications
          </button>
          <button
            @click="activeTab = 'guarantors'"
            class="py-4 px-1 border-b-2 font-medium text-sm"
            :class="activeTab === 'guarantors' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          >
            Guarantors
          </button>
        </nav>
      </div>
      
      <!-- Details tab -->
      <div v-if="activeTab === 'details'" class="details-tab">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="detail-group">
            <h3 class="text-sm font-medium text-gray-500">Contact Information</h3>
            <div class="mt-2 space-y-2">
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">email</span>
                <p>{{ borrower.email }}</p>
              </div>
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">phone</span>
                <p>{{ borrower.phone_number || 'Not provided' }}</p>
              </div>
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">home</span>
                <p>{{ borrower.address || 'Not provided' }}</p>
              </div>
            </div>
          </div>
          
          <div class="detail-group">
            <h3 class="text-sm font-medium text-gray-500">Personal Information</h3>
            <div class="mt-2 space-y-2">
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">cake</span>
                <p>Date of Birth: {{ formatDate(borrower.date_of_birth) || 'Not provided' }}</p>
              </div>
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">work</span>
                <p>Employment Status: {{ borrower.employment_status || 'Not provided' }}</p>
              </div>
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">attach_money</span>
                <p>Annual Income: {{ formatCurrency(borrower.annual_income) || 'Not provided' }}</p>
              </div>
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">trending_up</span>
                <p>Credit Score: {{ borrower.credit_score || 'Not provided' }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-6">
          <h3 class="text-sm font-medium text-gray-500">System Information</h3>
          <div class="mt-2 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <p class="text-xs text-gray-500">Created</p>
              <p>{{ formatDateTime(borrower.created_at) }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Last Updated</p>
              <p>{{ formatDateTime(borrower.updated_at) }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">ID</p>
              <p>{{ borrower.id }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Financial Summary tab -->
      <div v-else-if="activeTab === 'financial'" class="financial-tab">
        <BorrowerFinancialSummary :borrower-id="borrowerId" />
      </div>
      
      <!-- Applications tab -->
      <div v-else-if="activeTab === 'applications'" class="applications-tab">
        <BorrowerApplicationsList :borrower-id="borrowerId" />
      </div>
      
      <!-- Guarantors tab -->
      <div v-else-if="activeTab === 'guarantors'" class="guarantors-tab">
        <BorrowerGuarantorsList :borrower-id="borrowerId" />
      </div>
    </div>
    
    <!-- Delete confirmation modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
        <h3 class="text-lg font-bold mb-4">Confirm Deletion</h3>
        <p class="mb-6">Are you sure you want to delete this borrower? This action cannot be undone.</p>
        <div class="flex justify-end space-x-3">
          <button
            @click="showDeleteModal = false"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
          >
            Cancel
          </button>
          <button
            @click="deleteBorrower"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none"
            :disabled="deletingBorrower"
          >
            {{ deletingBorrower ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBorrowerStore } from '@/store/borrower'
import BorrowerFinancialSummary from '@/components/borrowers/BorrowerFinancialSummary.vue'
import BorrowerApplicationsList from '@/components/borrowers/BorrowerApplicationsList.vue'
import BorrowerGuarantorsList from '@/components/borrowers/BorrowerGuarantorsList.vue'

export default {
  name: 'BorrowerDetailView',
  components: {
    BorrowerFinancialSummary,
    BorrowerApplicationsList,
    BorrowerGuarantorsList
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const borrowerStore = useBorrowerStore()
    
    // Local state
    const borrowerId = ref(parseInt(route.params.id))
    const activeTab = ref('details')
    const showDeleteModal = ref(false)
    const deletingBorrower = ref(false)
    
    // Computed properties
    const borrower = computed(() => borrowerStore.currentBorrower)
    const loading = computed(() => borrowerStore.loading)
    const error = computed(() => borrowerStore.error)
    
    // Methods
    const fetchBorrowerData = async () => {
      try {
        await borrowerStore.fetchBorrowerById(borrowerId.value)
      } catch (error) {
        console.error('Error fetching borrower:', error)
      }
    }
    
    const navigateToEdit = () => {
      router.push({ name: 'borrower-edit', params: { id: borrowerId.value } })
    }
    
    const confirmDelete = () => {
      showDeleteModal.value = true
    }
    
    const deleteBorrower = async () => {
      deletingBorrower.value = true
      
      try {
        await borrowerStore.deleteBorrower(borrowerId.value)
        showDeleteModal.value = false
        router.push({ name: 'borrower-list' })
      } catch (error) {
        console.error('Error deleting borrower:', error)
      } finally {
        deletingBorrower.value = false
      }
    }
    
    const formatBorrowerType = (type) => {
      if (!type) return 'Unknown'
      
      // Convert snake_case to Title Case
      return type
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Not provided'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
    
    const formatDateTime = (dateString) => {
      if (!dateString) return 'Not provided'
      const date = new Date(dateString)
      return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`
    }
    
    const formatCurrency = (amount) => {
      if (amount === null || amount === undefined) return 'Not provided'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }
    
    // Lifecycle hooks
    onMounted(() => {
      fetchBorrowerData()
    })
    
    return {
      borrower,
      borrowerId,
      loading,
      error,
      activeTab,
      showDeleteModal,
      deletingBorrower,
      fetchBorrowerData,
      navigateToEdit,
      confirmDelete,
      deleteBorrower,
      formatBorrowerType,
      formatDate,
      formatDateTime,
      formatCurrency
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
