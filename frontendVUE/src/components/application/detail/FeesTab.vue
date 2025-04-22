<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Fees</h2>
      <button 
        @click="showAddFeeForm = !showAddFeeForm" 
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {{ showAddFeeForm ? 'Cancel' : 'Add Fee' }}
      </button>
    </div>
    
    <!-- Add Fee Form -->
    <div v-if="showAddFeeForm" class="bg-gray-50 p-4 rounded-md mb-6">
      <h3 class="text-lg font-medium mb-3">Add New Fee</h3>
      
      <form @submit.prevent="addFee" class="space-y-4">
        <div>
          <label for="fee_type" class="block text-sm font-medium text-gray-700">Fee Type</label>
          <select 
            id="fee_type" 
            v-model="newFee.fee_type"
            class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            required
          >
            <option value="">Select fee type</option>
            <option value="application">Application Fee</option>
            <option value="valuation">Valuation Fee</option>
            <option value="legal">Legal Fee</option>
            <option value="broker">Broker Commission</option>
            <option value="settlement">Settlement Fee</option>
            <option value="other">Other Fee</option>
          </select>
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
              v-model="newFee.amount"
              class="focus:ring-blue-500 focus:border-blue-500 block w-full pl-7 pr-12 sm:text-sm border-gray-300 rounded-md"
              placeholder="0.00"
              step="0.01"
              min="0"
              required
            />
          </div>
        </div>
        
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
          <textarea 
            id="description" 
            v-model="newFee.description"
            rows="2"
            class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
          ></textarea>
        </div>
        
        <div>
          <label for="due_date" class="block text-sm font-medium text-gray-700">Due Date (Optional)</label>
          <input 
            type="date" 
            id="due_date" 
            v-model="newFee.due_date"
            class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
          />
        </div>
        
        <div class="flex justify-end">
          <button 
            type="submit" 
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="submitting"
          >
            <span v-if="submitting">Saving...</span>
            <span v-else>Add Fee</span>
          </button>
        </div>
      </form>
    </div>
    
    <!-- Fees Table -->
    <div v-if="fees && fees.length > 0">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Fee Type
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Amount
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Description
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Due Date
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created By
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="fee in fees" :key="fee.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="getFeeTypeClass(fee.fee_type)">
                  {{ formatFeeType(fee.fee_type) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">${{ formatCurrency(fee.amount) }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">{{ fee.description }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ formatDate(fee.due_date) }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="getStatusClass(fee.status)">
                  {{ formatStatus(fee.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ fee.created_by_name }}</div>
                <div class="text-xs text-gray-500">{{ formatDate(fee.created_at) }}</div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else class="bg-gray-50 p-4 rounded-md">
      <p class="text-sm text-gray-500">No fees added for this application</p>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import axios from 'axios'

const props = defineProps({
  fees: {
    type: Array,
    default: () => []
  },
  applicationId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['fee-added'])

const showAddFeeForm = ref(false)
const submitting = ref(false)
const newFee = ref({
  fee_type: '',
  amount: '',
  description: '',
  due_date: null
})

const addFee = async () => {
  submitting.value = true
  
  try {
    await axios.post(`/api/applications/${props.applicationId}/add_fee/`, newFee.value)
    
    // Reset form
    newFee.value = {
      fee_type: '',
      amount: '',
      description: '',
      due_date: null
    }
    showAddFeeForm.value = false
    
    // Notify parent to refresh data
    emit('fee-added')
    
  } catch (error) {
    console.error('Error adding fee:', error)
    alert('Failed to add fee. Please try again.')
  } finally {
    submitting.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US').format(value)
}

const formatFeeType = (type) => {
  const types = {
    'application': 'Application Fee',
    'valuation': 'Valuation Fee',
    'legal': 'Legal Fee',
    'broker': 'Broker Commission',
    'settlement': 'Settlement Fee',
    'other': 'Other Fee'
  }
  
  return types[type] || type
}

const formatStatus = (status) => {
  const statuses = {
    'waiting': 'Waiting',
    'paid': 'Paid',
    'waived': 'Waived',
    'overdue': 'Overdue'
  }
  
  return statuses[status] || status
}

const getFeeTypeClass = (type) => {
  const typeClasses = {
    'application': 'bg-blue-100 text-blue-800',
    'valuation': 'bg-green-100 text-green-800',
    'legal': 'bg-purple-100 text-purple-800',
    'broker': 'bg-yellow-100 text-yellow-800',
    'settlement': 'bg-indigo-100 text-indigo-800',
    'other': 'bg-gray-100 text-gray-800'
  }
  
  return typeClasses[type] || 'bg-gray-100 text-gray-800'
}

const getStatusClass = (status) => {
  const statusClasses = {
    'waiting': 'bg-yellow-100 text-yellow-800',
    'paid': 'bg-green-100 text-green-800',
    'waived': 'bg-gray-100 text-gray-800',
    'overdue': 'bg-red-100 text-red-800'
  }
  
  return statusClasses[status] || 'bg-gray-100 text-gray-800'
}
</script>
