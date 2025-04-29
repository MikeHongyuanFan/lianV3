<template>
  <div class="guarantor-financial-summary">
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchFinancialData" class="underline">Try again</button>
    </div>
    
    <!-- Financial summary -->
    <div v-else class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4">Financial Summary</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Annual Income -->
        <div class="bg-blue-50 p-4 rounded-lg">
          <h3 class="text-sm font-medium text-gray-500">Annual Income</h3>
          <p class="text-2xl font-bold text-blue-700">{{ formatCurrency(guarantor.annual_income) }}</p>
        </div>
        
        <!-- Credit Score -->
        <div class="bg-green-50 p-4 rounded-lg">
          <h3 class="text-sm font-medium text-gray-500">Credit Score</h3>
          <p class="text-2xl font-bold" :class="getCreditScoreColor(guarantor.credit_score)">
            {{ guarantor.credit_score || 'N/A' }}
          </p>
        </div>
        
        <!-- Employment Status -->
        <div class="bg-purple-50 p-4 rounded-lg">
          <h3 class="text-sm font-medium text-gray-500">Employment Status</h3>
          <p class="text-2xl font-bold text-purple-700">{{ formatEmploymentStatus(guarantor.employment_status) }}</p>
        </div>
        
        <!-- Guaranteed Applications -->
        <div class="bg-amber-50 p-4 rounded-lg">
          <h3 class="text-sm font-medium text-gray-500">Guaranteed Applications</h3>
          <p class="text-2xl font-bold text-amber-700">{{ applicationCount }}</p>
        </div>
      </div>
      
      <div class="mt-6">
        <h3 class="text-lg font-semibold mb-3">Financial Details</h3>
        <div class="bg-gray-50 p-4 rounded-lg">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Date of Birth</p>
              <p class="font-medium">{{ formatDate(guarantor.date_of_birth) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Relationship to Borrower</p>
              <p class="font-medium">{{ formatRelationship(guarantor.relationship_to_borrower) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import guarantorService from '@/services/guarantor.service'

export default {
  name: 'GuarantorFinancialSummary',
  props: {
    guarantor: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const loading = ref(false)
    const error = ref(null)
    const applicationCount = ref(0)
    
    const fetchFinancialData = async () => {
      if (!props.guarantor || !props.guarantor.id) return
      
      loading.value = true
      error.value = null
      
      try {
        // Fetch guaranteed applications to get the count
        const applications = await guarantorService.getGuaranteedApplications(props.guarantor.id)
        applicationCount.value = applications.length
      } catch (err) {
        console.error('Error fetching financial data:', err)
        error.value = err.message || 'Failed to load financial data'
      } finally {
        loading.value = false
      }
    }
    
    const formatCurrency = (amount) => {
      if (amount === null || amount === undefined) return 'Not provided'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Not provided'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
    
    const formatEmploymentStatus = (status) => {
      if (!status) return 'Not provided'
      
      // Convert snake_case to Title Case
      return status
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    const formatRelationship = (relationship) => {
      if (!relationship) return 'Not provided'
      
      // Convert snake_case to Title Case
      return relationship
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    const getCreditScoreColor = (score) => {
      if (!score) return 'text-gray-700'
      
      if (score >= 750) return 'text-green-700'
      if (score >= 650) return 'text-blue-700'
      if (score >= 550) return 'text-amber-700'
      return 'text-red-700'
    }
    
    onMounted(() => {
      fetchFinancialData()
    })
    
    return {
      loading,
      error,
      applicationCount,
      fetchFinancialData,
      formatCurrency,
      formatDate,
      formatEmploymentStatus,
      formatRelationship,
      getCreditScoreColor
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
