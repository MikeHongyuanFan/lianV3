<template>
  <div class="borrower-guarantors-list">
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchGuarantors" class="underline">Try again</button>
    </div>
    
    <!-- Empty state -->
    <div v-else-if="!guarantors.length" class="text-center py-8 bg-gray-50 rounded-lg">
      <p class="text-gray-500 mb-4">No guarantors found for this borrower</p>
      <button
        @click="navigateToCreateGuarantor"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
      >
        Add Guarantor
      </button>
    </div>
    
    <!-- Guarantors list -->
    <div v-else>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Guarantors</h2>
        <button
          @click="navigateToCreateGuarantor"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
        >
          Add Guarantor
        </button>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="guarantor in guarantors" 
          :key="guarantor.id"
          class="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow"
        >
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-lg font-medium">{{ guarantor.first_name }} {{ guarantor.last_name }}</h3>
              <p class="text-sm text-gray-500">{{ formatRelationship(guarantor.relationship_to_borrower) }}</p>
            </div>
            <button
              @click="navigateToGuarantor(guarantor.id)"
              class="text-blue-600 hover:text-blue-800"
            >
              View
            </button>
          </div>
          
          <div class="mt-3 space-y-1">
            <div class="flex items-center">
              <span class="material-icons text-gray-400 mr-2 text-sm">email</span>
              <p class="text-sm">{{ guarantor.email }}</p>
            </div>
            <div class="flex items-center">
              <span class="material-icons text-gray-400 mr-2 text-sm">phone</span>
              <p class="text-sm">{{ guarantor.phone_number || 'Not provided' }}</p>
            </div>
            <div class="flex items-center">
              <span class="material-icons text-gray-400 mr-2 text-sm">home</span>
              <p class="text-sm truncate">{{ guarantor.address || 'Not provided' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import borrowerService from '@/services/borrower.service'

export default {
  name: 'BorrowerGuarantorsList',
  props: {
    borrowerId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const router = useRouter()
    const guarantors = ref([])
    const loading = ref(false)
    const error = ref(null)
    
    const fetchGuarantors = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await borrowerService.getBorrowerGuarantors(props.borrowerId)
        guarantors.value = response
      } catch (err) {
        console.error('Error fetching guarantors:', err)
        error.value = err.message || 'Failed to load guarantors'
      } finally {
        loading.value = false
      }
    }
    
    const navigateToGuarantor = (guarantorId) => {
      router.push({ name: 'guarantor-detail', params: { id: guarantorId } })
    }
    
    const navigateToCreateGuarantor = () => {
      router.push({ 
        name: 'guarantor-create',
        query: { borrower: props.borrowerId }
      })
    }
    
    const formatRelationship = (relationship) => {
      if (!relationship) return 'Unknown'
      
      // Convert snake_case to Title Case
      return relationship
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    onMounted(() => {
      fetchGuarantors()
    })
    
    return {
      guarantors,
      loading,
      error,
      fetchGuarantors,
      navigateToGuarantor,
      navigateToCreateGuarantor,
      formatRelationship
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
