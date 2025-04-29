<template>
  <div class="fee-detail-view">
    <div class="container mx-auto px-4 py-6">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">Fee Details</h1>
        <div class="flex space-x-2">
          <button
            @click="navigateBack"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none flex items-center"
          >
            <span class="material-icons mr-1">arrow_back</span>
            Back
          </button>
          <button
            v-if="!fee.is_paid"
            @click="handleMarkPaid"
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none flex items-center"
          >
            <span class="material-icons mr-1">check_circle</span>
            Mark as Paid
          </button>
          <button
            @click="navigateToEdit"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none flex items-center"
          >
            <span class="material-icons mr-1">edit</span>
            Edit
          </button>
        </div>
      </div>
      
      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="loader"></div>
      </div>
      
      <!-- Error state -->
      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        <p>{{ error }}</p>
        <button @click="loadFee" class="underline">Try again</button>
      </div>
      
      <!-- Fee details -->
      <div v-else-if="fee" class="bg-white rounded-lg shadow overflow-hidden">
        <!-- Header with status -->
        <div class="p-6 border-b flex justify-between items-center">
          <div>
            <h2 class="text-xl font-semibold">{{ formatFeeType(fee.fee_type_display || fee.fee_type) }}</h2>
            <p class="text-gray-500">Fee ID: {{ fee.id }}</p>
          </div>
          <span
            class="px-3 py-1 text-sm rounded-full"
            :class="fee.is_paid ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'"
          >
            {{ fee.is_paid ? 'Paid' : 'Pending' }}
          </span>
        </div>
        
        <!-- Fee information -->
        <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-lg font-semibold mb-4">Fee Information</h3>
            
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600">Amount:</span>
                <span class="font-semibold">{{ formatCurrency(fee.amount) }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-600">Due Date:</span>
                <span>{{ formatDate(fee.due_date) }}</span>
              </div>
              
              <div v-if="fee.is_paid" class="flex justify-between">
                <span class="text-gray-600">Paid Date:</span>
                <span>{{ formatDate(fee.paid_date) }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-600">Status:</span>
                <span>{{ fee.status }}</span>
              </div>
              
              <div v-if="fee.description" class="pt-2">
                <span class="text-gray-600 block mb-1">Description:</span>
                <p class="text-gray-800">{{ fee.description }}</p>
              </div>
            </div>
          </div>
          
          <div>
            <h3 class="text-lg font-semibold mb-4">Related Information</h3>
            
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600">Application:</span>
                <button 
                  @click="navigateToApplication(fee.application)" 
                  class="text-blue-600 hover:underline"
                >
                  View Application
                </button>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-600">Created By:</span>
                <span>{{ fee.created_by_name }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-600">Created At:</span>
                <span>{{ formatDateTime(fee.created_at) }}</span>
              </div>
              
              <div v-if="fee.updated_at" class="flex justify-between">
                <span class="text-gray-600">Last Updated:</span>
                <span>{{ formatDateTime(fee.updated_at) }}</span>
              </div>
              
              <div v-if="fee.invoice_url" class="pt-2">
                <span class="text-gray-600 block mb-1">Invoice:</span>
                <a 
                  :href="fee.invoice_url" 
                  target="_blank" 
                  class="text-blue-600 hover:underline flex items-center"
                >
                  <span class="material-icons mr-1">description</span>
                  View Invoice
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Mark as Paid Modal -->
      <div v-if="showMarkPaidModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
          <h3 class="text-lg font-semibold mb-4">Mark Fee as Paid</h3>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Payment Date</label>
            <input
              v-model="paymentDate"
              type="date"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div class="flex justify-end space-x-3">
            <button
              @click="showMarkPaidModal = false"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
            >
              Cancel
            </button>
            <button
              @click="markFeePaid"
              class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none"
            >
              Mark as Paid
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useFeeStore } from '@/store/fee'

export default {
  name: 'FeeDetailView',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const feeStore = useFeeStore()
    
    // State
    const loading = ref(false)
    const error = ref('')
    const showMarkPaidModal = ref(false)
    const paymentDate = ref(new Date().toISOString().split('T')[0]) // Today's date
    
    // Computed properties
    const fee = computed(() => feeStore.currentFee || {})
    
    // Methods
    const loadFee = async () => {
      loading.value = true
      error.value = ''
      
      try {
        await feeStore.fetchFeeById(route.params.id)
      } catch (err) {
        error.value = 'Failed to load fee details. Please try again.'
        console.error('Error loading fee:', err)
      } finally {
        loading.value = false
      }
    }
    
    const formatFeeType = (type) => {
      if (!type) return 'Unknown'
      
      // If it's already formatted (from fee_type_display), return as is
      if (type.includes(' ')) return type
      
      // Convert snake_case to Title Case
      return type
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    const formatCurrency = (amount) => {
      if (amount === undefined || amount === null) return '$0.00'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Not specified'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
    
    const formatDateTime = (dateString) => {
      if (!dateString) return 'Not specified'
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
    
    const navigateBack = () => {
      router.back()
    }
    
    const navigateToEdit = () => {
      router.push({ name: 'fee-edit', params: { id: route.params.id } })
    }
    
    const navigateToApplication = (id) => {
      router.push({ name: 'application-detail', params: { id } })
    }
    
    const handleMarkPaid = () => {
      showMarkPaidModal.value = true
    }
    
    const markFeePaid = async () => {
      try {
        await feeStore.markFeePaid(route.params.id, { paid_date: paymentDate.value })
        showMarkPaidModal.value = false
      } catch (err) {
        error.value = 'Failed to mark fee as paid. Please try again.'
        console.error('Error marking fee as paid:', err)
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      loadFee()
    })
    
    return {
      fee,
      loading,
      error,
      showMarkPaidModal,
      paymentDate,
      loadFee,
      formatFeeType,
      formatCurrency,
      formatDate,
      formatDateTime,
      navigateBack,
      navigateToEdit,
      navigateToApplication,
      handleMarkPaid,
      markFeePaid
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
