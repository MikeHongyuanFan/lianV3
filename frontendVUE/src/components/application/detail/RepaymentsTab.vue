<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Repayment Schedule</h2>
      <button 
        @click="showAddRepaymentForm = !showAddRepaymentForm" 
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {{ showAddRepaymentForm ? 'Cancel' : 'Add Repayment' }}
      </button>
    </div>
    
    <!-- Add Repayment Form -->
    <div v-if="showAddRepaymentForm" class="bg-gray-50 p-4 rounded-md mb-6">
      <h3 class="text-lg font-medium mb-3">Schedule New Repayment</h3>
      
      <form @submit.prevent="addRepayment" class="space-y-4">
        <div>
          <label for="due_date" class="block text-sm font-medium text-gray-700">Due Date</label>
          <input 
            type="date" 
            id="due_date" 
            v-model="newRepayment.due_date"
            class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            required
          />
        </div>
        
        <div>
          <label for="amount" class="block text-sm font-medium text-gray-700">Amount</label>
          <div class="mt-1 relative rounded-md shadow-sm">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <span class="text-gray-500 sm:text-sm">$</span>
            </div>
            <input 
              type="number" 
              id="amount" 
              v-model="newRepayment.amount"
              class="focus:ring-blue-500 focus:border-blue-500 block w-full pl-7 pr-12 sm:text-sm border-gray-300 rounded-md"
              placeholder="0.00"
              step="0.01"
              min="0"
              required
            />
          </div>
        </div>
        
        <div>
          <label for="repayment_type" class="block text-sm font-medium text-gray-700">Repayment Type</label>
          <select 
            id="repayment_type" 
            v-model="newRepayment.repayment_type"
            class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            required
          >
            <option value="">Select repayment type</option>
            <option value="principal">Principal</option>
            <option value="interest">Interest</option>
            <option value="principal_and_interest">Principal & Interest</option>
          </select>
        </div>
        
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
          <textarea 
            id="description" 
            v-model="newRepayment.description"
            rows="2"
            class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
          ></textarea>
        </div>
        
        <div class="flex justify-end">
          <button 
            type="submit" 
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="submitting"
          >
            <span v-if="submitting">Saving...</span>
            <span v-else>Schedule Repayment</span>
          </button>
        </div>
      </form>
    </div>
    
    <!-- Record Payment Modal -->
    <div v-if="showRecordPaymentModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Record Payment</h3>
        
        <form @submit.prevent="recordPayment" class="space-y-4">
          <div>
            <label for="payment_amount" class="block text-sm font-medium text-gray-700">Payment Amount</label>
            <div class="mt-1 relative rounded-md shadow-sm">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span class="text-gray-500 sm:text-sm">$</span>
              </div>
              <input 
                type="number" 
                id="payment_amount" 
                v-model="paymentDetails.payment_amount"
                class="focus:ring-blue-500 focus:border-blue-500 block w-full pl-7 pr-12 sm:text-sm border-gray-300 rounded-md"
                placeholder="0.00"
                step="0.01"
                min="0"
                :max="selectedRepayment.amount"
                required
              />
            </div>
          </div>
          
          <div>
            <label for="payment_date" class="block text-sm font-medium text-gray-700">Payment Date</label>
            <input 
              type="date" 
              id="payment_date" 
              v-model="paymentDetails.payment_date"
              class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
              required
            />
          </div>
          
          <div class="flex justify-end space-x-3">
            <button 
              type="button" 
              @click="showRecordPaymentModal = false"
              class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              :disabled="recordingPayment"
            >
              <span v-if="recordingPayment">Processing...</span>
              <span v-else>Record Payment</span>
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Repayments Table -->
    <div v-if="repayments && repayments.length > 0">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Due Date
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Amount
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Payment
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="repayment in repayments" :key="repayment.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ formatDate(repayment.due_date) }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">${{ formatCurrency(repayment.amount) }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ formatRepaymentType(repayment.repayment_type) }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="getStatusClass(repayment)">
                  {{ formatStatus(repayment) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div v-if="repayment.status === 'paid'" class="text-sm text-gray-900">
                  ${{ formatCurrency(repayment.payment_amount) }} on {{ formatDate(repayment.paid_date) }}
                </div>
                <div v-else class="text-sm text-gray-500">
                  Not paid
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button 
                  v-if="repayment.status !== 'paid'"
                  @click="openRecordPaymentModal(repayment)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  Record Payment
                </button>
                <span v-else class="text-gray-400">Paid</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else class="bg-gray-50 p-4 rounded-md">
      <p class="text-sm text-gray-500">No repayments scheduled for this application</p>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import axios from 'axios'

const props = defineProps({
  repayments: {
    type: Array,
    default: () => []
  },
  applicationId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['repayment-added'])

const showAddRepaymentForm = ref(false)
const submitting = ref(false)
const newRepayment = ref({
  due_date: '',
  amount: '',
  repayment_type: '',
  description: ''
})

const showRecordPaymentModal = ref(false)
const recordingPayment = ref(false)
const selectedRepayment = ref({})
const paymentDetails = ref({
  repayment_id: null,
  payment_amount: '',
  payment_date: new Date().toISOString().split('T')[0] // Today's date
})

const addRepayment = async () => {
  submitting.value = true
  
  try {
    await axios.post(`/api/applications/${props.applicationId}/add_repayment/`, newRepayment.value)
    
    // Reset form
    newRepayment.value = {
      due_date: '',
      amount: '',
      repayment_type: '',
      description: ''
    }
    showAddRepaymentForm.value = false
    
    // Notify parent to refresh data
    emit('repayment-added')
    
  } catch (error) {
    console.error('Error adding repayment:', error)
    alert('Failed to add repayment. Please try again.')
  } finally {
    submitting.value = false
  }
}

const openRecordPaymentModal = (repayment) => {
  selectedRepayment.value = repayment
  paymentDetails.value = {
    repayment_id: repayment.id,
    payment_amount: repayment.amount,
    payment_date: new Date().toISOString().split('T')[0]
  }
  showRecordPaymentModal.value = true
}

const recordPayment = async () => {
  recordingPayment.value = true
  
  try {
    await axios.post(`/api/applications/${props.applicationId}/record_payment/`, paymentDetails.value)
    
    showRecordPaymentModal.value = false
    
    // Notify parent to refresh data
    emit('repayment-added')
    
  } catch (error) {
    console.error('Error recording payment:', error)
    alert('Failed to record payment. Please try again.')
  } finally {
    recordingPayment.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US').format(value)
}

const formatRepaymentType = (type) => {
  const types = {
    'principal': 'Principal',
    'interest': 'Interest',
    'principal_and_interest': 'Principal & Interest'
  }
  
  return types[type] || type
}

const formatStatus = (repayment) => {
  if (repayment.status === 'paid') {
    return 'Paid'
  }
  
  const dueDate = new Date(repayment.due_date)
  const today = new Date()
  
  // Set time to 00:00:00 for both dates to compare just the date
  dueDate.setHours(0, 0, 0, 0)
  today.setHours(0, 0, 0, 0)
  
  if (dueDate < today) {
    return 'Overdue'
  } else if (dueDate.getTime() === today.getTime()) {
    return 'Due Today'
  } else {
    // Calculate days until due
    const diffTime = Math.abs(dueDate - today)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays <= 7) {
      return 'Due Soon'
    } else {
      return 'Upcoming'
    }
  }
}

const getStatusClass = (repayment) => {
  const status = formatStatus(repayment)
  
  const statusClasses = {
    'Paid': 'bg-green-100 text-green-800',
    'Overdue': 'bg-red-100 text-red-800',
    'Due Today': 'bg-yellow-100 text-yellow-800',
    'Due Soon': 'bg-orange-100 text-orange-800',
    'Upcoming': 'bg-blue-100 text-blue-800'
  }
  
  return statusClasses[status] || 'bg-gray-100 text-gray-800'
}
</script>
