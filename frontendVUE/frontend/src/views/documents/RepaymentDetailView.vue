<template>
  <MainLayout>
    <div class="repayment-detail-view">
      <div class="container mx-auto px-4 py-6">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold">Repayment Details</h1>
          <div class="flex space-x-2">
            <button
              @click="goBack"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
            >
              Back
            </button>
            <button
              @click="navigateToEdit"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
            >
              Edit
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
          <button @click="fetchRepaymentData" class="underline">Try again</button>
        </div>
        
        <!-- Repayment details -->
        <div v-else-if="repayment" class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Main details -->
          <div class="col-span-2 bg-white p-6 rounded-lg shadow-md">
            <div class="flex justify-between items-start mb-4">
              <div>
                <h2 class="text-xl font-semibold">Repayment #{{ repayment.id }}</h2>
                <p class="text-gray-500">
                  For Application #{{ repayment.application }}
                  <button 
                    @click="navigateToApplication(repayment.application)" 
                    class="text-blue-600 hover:text-blue-800 underline ml-1"
                  >
                    View Application
                  </button>
                </p>
              </div>
              <span
                class="px-3 py-1 text-sm rounded-full"
                :class="{
                  'bg-green-100 text-green-800': repayment.is_paid,
                  'bg-yellow-100 text-yellow-800': !repayment.is_paid && !isOverdue,
                  'bg-red-100 text-red-800': !repayment.is_paid && isOverdue
                }"
              >
                {{ repayment.is_paid ? 'Paid' : (isOverdue ? 'Overdue' : 'Pending') }}
              </span>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div>
                <p class="text-sm text-gray-500">Amount</p>
                <p class="text-xl font-bold">{{ formatCurrency(repayment.amount) }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Due Date</p>
                <p class="text-lg">{{ formatDate(repayment.due_date) }}</p>
              </div>
            </div>
            
            <div v-if="repayment.is_paid" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div>
                <p class="text-sm text-gray-500">Paid Date</p>
                <p class="text-lg">{{ formatDate(repayment.paid_date) }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Payment Method</p>
                <p class="text-lg">{{ formatPaymentMethod(repayment.payment_method) }}</p>
              </div>
            </div>
            
            <div v-if="repayment.invoice_url" class="mb-6">
              <p class="text-sm text-gray-500 mb-2">Invoice</p>
              <a 
                :href="repayment.invoice_url" 
                target="_blank" 
                class="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200"
              >
                <span class="material-icons mr-1">description</span>
                View Invoice
              </a>
            </div>
            
            <div v-if="!repayment.is_paid" class="mt-6">
              <button
                @click="showMarkPaidModal = true"
                class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none"
              >
                Mark as Paid
              </button>
            </div>
          </div>
          
          <!-- Additional information -->
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h3 class="text-lg font-semibold mb-4">Additional Information</h3>
            
            <div class="mb-4">
              <p class="text-sm text-gray-500">Created At</p>
              <p>{{ formatDateTime(repayment.created_at) }}</p>
            </div>
            
            <div class="mb-4">
              <p class="text-sm text-gray-500">Last Updated</p>
              <p>{{ formatDateTime(repayment.updated_at) }}</p>
            </div>
            
            <div class="mb-4">
              <p class="text-sm text-gray-500">Created By</p>
              <p>{{ repayment.created_by_name || 'N/A' }}</p>
            </div>
            
            <div v-if="repayment.status" class="mb-4">
              <p class="text-sm text-gray-500">Status</p>
              <p>{{ repayment.status }}</p>
            </div>
            
            <div v-if="daysUntilDue !== null" class="mt-6">
              <p class="text-sm text-gray-500">Time Until Due</p>
              <p v-if="daysUntilDue > 0" class="text-yellow-600">
                Due in {{ daysUntilDue }} {{ daysUntilDue === 1 ? 'day' : 'days' }}
              </p>
              <p v-else-if="daysUntilDue === 0" class="text-orange-600">
                Due today
              </p>
              <p v-else class="text-red-600">
                Overdue by {{ Math.abs(daysUntilDue) }} {{ Math.abs(daysUntilDue) === 1 ? 'day' : 'days' }}
              </p>
            </div>
          </div>
        </div>
        
        <!-- Mark as Paid Modal -->
        <div v-if="showMarkPaidModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
            <h3 class="text-lg font-semibold mb-4">Mark Repayment as Paid</h3>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Payment Date</label>
              <input
                v-model="paymentDate"
                type="date"
                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Payment Method</label>
              <select
                v-model="paymentMethod"
                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select Payment Method</option>
                <option value="bank_transfer">Bank Transfer</option>
                <option value="credit_card">Credit Card</option>
                <option value="direct_debit">Direct Debit</option>
                <option value="cash">Cash</option>
                <option value="check">Check</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div class="flex justify-end space-x-3">
              <button
                @click="showMarkPaidModal = false"
                class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
              >
                Cancel
              </button>
              <button
                @click="markRepaymentPaid"
                class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none"
              >
                Mark as Paid
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRepaymentStore } from '@/store/repayment'
import MainLayout from '@/layouts/MainLayout.vue'

export default {
  name: 'RepaymentDetailView',
  components: {
    MainLayout
  },
  props: {
    id: {
      type: [Number, String],
      default: null
    }
  },
  setup(props) {
    const route = useRoute()
    const router = useRouter()
    const repaymentStore = useRepaymentStore()
    
    // State
    const loading = ref(false)
    const error = ref(null)
    const showMarkPaidModal = ref(false)
    const paymentDate = ref(new Date().toISOString().split('T')[0]) // Today's date
    const paymentMethod = ref('')
    
    // Computed properties
    const repaymentId = computed(() => {
      return props.id || route.params.id
    })
    
    const repayment = computed(() => {
      return repaymentStore.currentRepayment
    })
    
    const isOverdue = computed(() => {
      if (!repayment.value || repayment.value.is_paid) return false
      
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      
      const dueDate = new Date(repayment.value.due_date)
      dueDate.setHours(0, 0, 0, 0)
      
      return dueDate < today
    })
    
    const daysUntilDue = computed(() => {
      if (!repayment.value) return null
      if (repayment.value.is_paid) return null
      
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      
      const dueDate = new Date(repayment.value.due_date)
      dueDate.setHours(0, 0, 0, 0)
      
      const diffTime = dueDate - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      return diffDays
    })
    
    // Methods
    const fetchRepaymentData = async () => {
      try {
        loading.value = true
        error.value = null
        
        await repaymentStore.fetchRepaymentById(repaymentId.value)
      } catch (err) {
        error.value = err.message || 'Failed to load repayment data'
        console.error('Error fetching repayment:', err)
      } finally {
        loading.value = false
      }
    }
    
    const goBack = () => {
      router.push({ name: 'repayment-list' })
    }
    
    const navigateToEdit = () => {
      router.push({ name: 'repayment-edit', params: { id: repaymentId.value } })
    }
    
    const navigateToApplication = (applicationId) => {
      router.push({ name: 'application-detail', params: { id: applicationId } })
    }
    
    const markRepaymentPaid = async () => {
      try {
        await repaymentStore.markRepaymentPaid(repaymentId.value, {
          paid_date: paymentDate.value,
          payment_method: paymentMethod.value || undefined
        })
        
        showMarkPaidModal.value = false
        
        // Refresh repayment data
        await fetchRepaymentData()
      } catch (err) {
        error.value = err.message || 'Failed to mark repayment as paid'
        console.error('Error marking repayment as paid:', err)
      }
    }
    
    const formatCurrency = (amount) => {
      if (amount === undefined || amount === null) return '$0.00'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(date)
    }
    
    const formatDateTime = (dateString) => {
      if (!dateString) return 'N/A'
      
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    }
    
    const formatPaymentMethod = (method) => {
      if (!method) return 'N/A'
      
      const methodMap = {
        'bank_transfer': 'Bank Transfer',
        'credit_card': 'Credit Card',
        'direct_debit': 'Direct Debit',
        'cash': 'Cash',
        'check': 'Check',
        'other': 'Other'
      }
      
      return methodMap[method] || method
    }
    
    // Lifecycle hooks
    onMounted(() => {
      fetchRepaymentData()
    })
    
    return {
      repayment,
      loading,
      error,
      isOverdue,
      daysUntilDue,
      showMarkPaidModal,
      paymentDate,
      paymentMethod,
      fetchRepaymentData,
      goBack,
      navigateToEdit,
      navigateToApplication,
      markRepaymentPaid,
      formatCurrency,
      formatDate,
      formatDateTime,
      formatPaymentMethod
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
