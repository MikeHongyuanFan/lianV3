<template>
  <div class="borrower-financial-summary">
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchFinancialSummary" class="underline">Try again</button>
    </div>
    
    <!-- Financial summary data -->
    <div v-else-if="financialSummary" class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4">Financial Summary</h2>
      
      <!-- Summary cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div class="bg-blue-50 p-4 rounded-lg">
          <p class="text-sm text-blue-600 font-medium">Total Loans</p>
          <p class="text-2xl font-bold">{{ financialSummary.total_loans }}</p>
        </div>
        
        <div class="bg-green-50 p-4 rounded-lg">
          <p class="text-sm text-green-600 font-medium">Active Loans</p>
          <p class="text-2xl font-bold">{{ financialSummary.active_loans }}</p>
        </div>
        
        <div class="bg-purple-50 p-4 rounded-lg">
          <p class="text-sm text-purple-600 font-medium">Total Loan Amount</p>
          <p class="text-2xl font-bold">{{ formatCurrency(financialSummary.total_loan_amount) }}</p>
        </div>
        
        <div class="bg-amber-50 p-4 rounded-lg">
          <p class="text-sm text-amber-600 font-medium">Outstanding Amount</p>
          <p class="text-2xl font-bold">{{ formatCurrency(financialSummary.outstanding_amount) }}</p>
        </div>
      </div>
      
      <!-- Repayment history section -->
      <div v-if="financialSummary.repayment_history" class="mt-8">
        <h3 class="text-lg font-medium mb-3">Repayment History</h3>
        
        <div class="bg-gray-50 p-4 rounded-lg">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <p class="text-sm text-gray-500">On-time Payments</p>
              <p class="text-xl font-semibold">{{ financialSummary.repayment_history.on_time_payments || 0 }}</p>
            </div>
            
            <div>
              <p class="text-sm text-gray-500">Late Payments</p>
              <p class="text-xl font-semibold">{{ financialSummary.repayment_history.late_payments || 0 }}</p>
            </div>
            
            <div>
              <p class="text-sm text-gray-500">Missed Payments</p>
              <p class="text-xl font-semibold">{{ financialSummary.repayment_history.missed_payments || 0 }}</p>
            </div>
          </div>
          
          <div class="mt-4">
            <p class="text-sm text-gray-500">Payment Compliance Rate</p>
            <div class="w-full bg-gray-200 rounded-full h-2.5 mt-2">
              <div 
                class="bg-blue-600 h-2.5 rounded-full" 
                :style="`width: ${calculateComplianceRate()}%`"
              ></div>
            </div>
            <p class="text-sm mt-1">{{ calculateComplianceRate() }}%</p>
          </div>
        </div>
      </div>
      
      <!-- No repayment history -->
      <div v-else class="mt-8 text-center py-4 bg-gray-50 rounded-lg">
        <p class="text-gray-500">No repayment history available</p>
      </div>
    </div>
    
    <!-- No data state -->
    <div v-else class="bg-gray-50 p-6 rounded-lg text-center">
      <p class="text-gray-500">No financial data available for this borrower</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import borrowerService from '@/services/borrower.service'

export default {
  name: 'BorrowerFinancialSummary',
  props: {
    borrowerId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const financialSummary = ref(null)
    const loading = ref(false)
    const error = ref(null)
    
    const fetchFinancialSummary = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await borrowerService.getFinancialSummary(props.borrowerId)
        financialSummary.value = response
      } catch (err) {
        console.error('Error fetching financial summary:', err)
        error.value = err.message || 'Failed to load financial summary'
      } finally {
        loading.value = false
      }
    }
    
    const formatCurrency = (amount) => {
      if (amount === null || amount === undefined) return '$0.00'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }
    
    const calculateComplianceRate = () => {
      if (!financialSummary.value || !financialSummary.value.repayment_history) return 0
      
      const history = financialSummary.value.repayment_history
      const onTime = history.on_time_payments || 0
      const late = history.late_payments || 0
      const missed = history.missed_payments || 0
      
      const total = onTime + late + missed
      if (total === 0) return 0
      
      return Math.round((onTime / total) * 100)
    }
    
    onMounted(() => {
      fetchFinancialSummary()
    })
    
    return {
      financialSummary,
      loading,
      error,
      fetchFinancialSummary,
      formatCurrency,
      calculateComplianceRate
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
