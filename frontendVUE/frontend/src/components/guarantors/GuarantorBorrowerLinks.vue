<template>
  <div class="guarantor-borrower-links">
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchBorrowers" class="underline">Try again</button>
    </div>
    
    <!-- Empty state -->
    <div v-else-if="!borrowers.length" class="text-center py-8 bg-gray-50 rounded-lg">
      <p class="text-gray-500 mb-4">No borrowers linked to this guarantor</p>
      <button
        @click="navigateToCreateBorrower"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
      >
        Create New Borrower
      </button>
    </div>
    
    <!-- Borrowers list -->
    <div v-else>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Linked Borrowers</h2>
        <button
          @click="navigateToCreateBorrower"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
        >
          Create New Borrower
        </button>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="borrower in borrowers" 
          :key="borrower.id"
          class="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow"
        >
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-lg font-medium">{{ borrower.first_name }} {{ borrower.last_name }}</h3>
              <p class="text-sm text-gray-500">{{ formatBorrowerType(borrower.borrower_type) }}</p>
            </div>
            <button
              @click="navigateToBorrower(borrower.id)"
              class="text-blue-600 hover:text-blue-800"
            >
              View
            </button>
          </div>
          
          <div class="mt-3 space-y-1">
            <div class="flex items-center">
              <span class="material-icons text-gray-400 mr-2 text-sm">email</span>
              <p class="text-sm">{{ borrower.email }}</p>
            </div>
            <div class="flex items-center">
              <span class="material-icons text-gray-400 mr-2 text-sm">phone</span>
              <p class="text-sm">{{ borrower.phone_number || 'Not provided' }}</p>
            </div>
            <div class="flex items-center">
              <span class="material-icons text-gray-400 mr-2 text-sm">home</span>
              <p class="text-sm truncate">{{ borrower.address || 'Not provided' }}</p>
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
import guarantorService from '@/services/guarantor.service'
import borrowerService from '@/services/borrower.service'

export default {
  name: 'GuarantorBorrowerLinks',
  props: {
    guarantorId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const router = useRouter()
    const borrowers = ref([])
    const loading = ref(false)
    const error = ref(null)
    
    const fetchBorrowers = async () => {
      loading.value = true
      error.value = null
      
      try {
        // First get the applications guaranteed by this guarantor
        const applications = await guarantorService.getGuaranteedApplications(props.guarantorId)
        
        // Then get all borrowers from these applications
        const borrowerIds = new Set()
        const borrowerPromises = []
        
        // For each application, get its borrowers
        for (const application of applications) {
          if (application.id) {
            const promise = borrowerService.getBorrowerApplications(application.id)
              .then(appBorrowers => {
                // Add unique borrowers to our set
                appBorrowers.forEach(borrower => {
                  if (!borrowerIds.has(borrower.id)) {
                    borrowerIds.add(borrower.id)
                    borrowers.value.push(borrower)
                  }
                })
              })
              .catch(err => {
                console.error(`Error fetching borrowers for application ${application.id}:`, err)
              })
            
            borrowerPromises.push(promise)
          }
        }
        
        // Wait for all promises to resolve
        await Promise.all(borrowerPromises)
      } catch (err) {
        console.error('Error fetching borrowers:', err)
        error.value = err.message || 'Failed to load borrowers'
      } finally {
        loading.value = false
      }
    }
    
    const navigateToBorrower = (borrowerId) => {
      router.push({ name: 'borrower-detail', params: { id: borrowerId } })
    }
    
    const navigateToCreateBorrower = () => {
      router.push({ 
        name: 'borrower-create',
        query: { guarantor: props.guarantorId }
      })
    }
    
    const formatBorrowerType = (type) => {
      if (!type) return 'Unknown'
      
      // Convert snake_case to Title Case
      return type
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    onMounted(() => {
      fetchBorrowers()
    })
    
    return {
      borrowers,
      loading,
      error,
      fetchBorrowers,
      navigateToBorrower,
      navigateToCreateBorrower,
      formatBorrowerType
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
