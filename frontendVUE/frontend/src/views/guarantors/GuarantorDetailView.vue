<template>
  <div class="guarantor-detail-container">
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchGuarantorData" class="underline">Try again</button>
    </div>
    
    <!-- Guarantor details -->
    <div v-else-if="guarantor" class="bg-white rounded-lg shadow-md p-6">
      <div class="flex justify-between items-start mb-6">
        <div>
          <h1 class="text-2xl font-bold">
            {{ guarantor.guarantor_type === 'company' ? guarantor.company_name : `${guarantor.first_name} ${guarantor.last_name}` }}
          </h1>
          <div class="flex flex-wrap gap-2 mt-2">
            <span
              class="guarantor-type-badge px-2 py-1 text-xs rounded-full"
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
            @click="activeTab = 'applications'"
            class="py-4 px-1 border-b-2 font-medium text-sm"
            :class="activeTab === 'applications' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          >
            Guaranteed Applications
          </button>
          <button
            @click="activeTab = 'borrowers'"
            class="py-4 px-1 border-b-2 font-medium text-sm"
            :class="activeTab === 'borrowers' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          >
            Linked Borrowers
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
                <p>{{ guarantor.email }}</p>
              </div>
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">phone</span>
                <p>{{ guarantor.phone_number || guarantor.phone || 'Not provided' }}</p>
              </div>
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">home</span>
                <p>{{ guarantor.address || 'Not provided' }}</p>
              </div>
            </div>
          </div>
          
          <!-- Company Information (if guarantor is a company) -->
          <div v-if="guarantor.guarantor_type === 'company'" class="detail-group">
            <h3 class="text-sm font-medium text-gray-500">Company Information</h3>
            <div class="mt-2 space-y-2">
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">business</span>
                <p>Company Name: {{ guarantor.company_name }}</p>
              </div>
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">badge</span>
                <p>ABN: {{ guarantor.company_abn || 'Not provided' }}</p>
              </div>
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">numbers</span>
                <p>ACN: {{ guarantor.company_acn || 'Not provided' }}</p>
              </div>
            </div>
          </div>
          
          <!-- Personal Information (if guarantor is an individual) -->
          <div v-if="guarantor.guarantor_type === 'individual' || !guarantor.guarantor_type" class="detail-group">
            <h3 class="text-sm font-medium text-gray-500">Personal Information</h3>
            <div class="mt-2 space-y-2">
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">cake</span>
                <p>Date of Birth: {{ formatDate(guarantor.date_of_birth) || 'Not provided' }}</p>
              </div>
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">work</span>
                <p>Employment Status: {{ guarantor.employment_status || 'Not provided' }}</p>
              </div>
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">attach_money</span>
                <p>Annual Income: {{ formatCurrency(guarantor.annual_income) || 'Not provided' }}</p>
              </div>
              <div class="flex items-center">
                <span class="material-icons text-gray-400 mr-2">trending_up</span>
                <p>Credit Score: {{ guarantor.credit_score || 'Not provided' }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Financial Summary Component -->
        <div class="mt-6">
          <GuarantorFinancialSummary :guarantor="guarantor" />
        </div>
        
        <div class="mt-6">
          <h3 class="text-sm font-medium text-gray-500">System Information</h3>
          <div class="mt-2 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <p class="text-xs text-gray-500">Created</p>
              <p>{{ formatDateTime(guarantor.created_at) }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Last Updated</p>
              <p>{{ formatDateTime(guarantor.updated_at) }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">ID</p>
              <p>{{ guarantor.id }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Applications tab -->
      <div v-else-if="activeTab === 'applications'" class="applications-tab">
        <GuarantorApplicationsList :guarantor-id="guarantorId" />
      </div>
      
      <!-- Borrowers tab -->
      <div v-else-if="activeTab === 'borrowers'" class="borrowers-tab">
        <GuarantorBorrowerLinks :guarantor-id="guarantorId" />
      </div>
    </div>
    
    <!-- Delete confirmation modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
        <h3 class="text-lg font-bold mb-4">Confirm Deletion</h3>
        <p class="mb-6">Are you sure you want to delete this guarantor? This action cannot be undone.</p>
        <div class="flex justify-end space-x-3">
          <button
            @click="showDeleteModal = false"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
          >
            Cancel
          </button>
          <button
            @click="deleteGuarantor"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none"
            :disabled="deletingGuarantor"
          >
            {{ deletingGuarantor ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useGuarantorStore } from '@/store/guarantor'
import GuarantorApplicationsList from '@/components/guarantors/GuarantorApplicationsList.vue'
import GuarantorFinancialSummary from '@/components/guarantors/GuarantorFinancialSummary.vue'
import GuarantorBorrowerLinks from '@/components/guarantors/GuarantorBorrowerLinks.vue'

export default {
  name: 'GuarantorDetailView',
  components: {
    GuarantorApplicationsList,
    GuarantorFinancialSummary,
    GuarantorBorrowerLinks
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const guarantorStore = useGuarantorStore()
    
    // Local state
    const guarantorId = ref(parseInt(route.params.id))
    const activeTab = ref('details')
    const showDeleteModal = ref(false)
    const deletingGuarantor = ref(false)
    
    // Computed properties
    const guarantor = computed(() => guarantorStore.currentGuarantor)
    const loading = computed(() => guarantorStore.loading)
    const error = computed(() => guarantorStore.error)
    
    // Methods
    const fetchGuarantorData = async () => {
      try {
        await guarantorStore.fetchGuarantorById(guarantorId.value)
      } catch (error) {
        console.error('Error fetching guarantor:', error)
      }
    }
    
    const navigateToEdit = () => {
      router.push({ name: 'guarantor-edit', params: { id: guarantorId.value } })
    }
    
    const confirmDelete = () => {
      showDeleteModal.value = true
    }
    
    const deleteGuarantor = async () => {
      deletingGuarantor.value = true
      
      try {
        await guarantorStore.deleteGuarantor(guarantorId.value)
        showDeleteModal.value = false
        router.push({ name: 'guarantor-list' })
      } catch (error) {
        console.error('Error deleting guarantor:', error)
      } finally {
        deletingGuarantor.value = false
      }
    }
    
    const formatRelationship = (relationship) => {
      if (!relationship) return 'Unknown'
      
      // Convert snake_case to Title Case
      return relationship
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
    
    // Watch for tab changes to load data
    const handleTabChange = () => {
      // No need to handle tab changes anymore as the GuarantorApplicationsList component
      // will handle loading its own data
    }
    
    // Lifecycle hooks
    onMounted(() => {
      fetchGuarantorData()
    })
    
    return {
      guarantor,
      loading,
      error,
      activeTab,
      showDeleteModal,
      deletingGuarantor,
      guarantorId,
      fetchGuarantorData,
      navigateToEdit,
      confirmDelete,
      deleteGuarantor,
      formatRelationship,
      formatDate,
      formatDateTime,
      formatCurrency,
      handleTabChange
    }
  },
  watch: {
    activeTab: {
      handler(newTab) {
        // No need to handle tab changes anymore
      }
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
