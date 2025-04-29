<template>
  <div 
    class="fee-card bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow"
    :class="{ 'border-l-4 border-red-400': isOverdue && !fee.is_paid }"
  >
    <div class="flex justify-between items-start">
      <h3 class="text-lg font-semibold">{{ formatFeeType(fee.fee_type_display || fee.fee_type) }}</h3>
      <span
        class="fee-status-badge px-2 py-1 text-xs rounded-full"
        :class="fee.is_paid ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'"
      >
        {{ fee.is_paid ? 'Paid' : 'Pending' }}
      </span>
    </div>
    
    <div class="mt-2 flex justify-between">
      <div class="text-gray-700">
        <div class="text-2xl font-bold">{{ formatCurrency(fee.amount) }}</div>
        <div class="text-sm text-gray-500">
          Due: {{ formatDate(fee.due_date) }}
        </div>
        <div v-if="fee.is_paid" class="text-sm text-gray-500">
          Paid: {{ formatDate(fee.paid_date) }}
        </div>
      </div>
      
      <div v-if="fee.description" class="text-sm text-gray-600 max-w-xs">
        {{ fee.description }}
      </div>
    </div>
    
    <div class="mt-3 text-sm text-gray-500">
      <div v-if="fee.application" class="flex items-center">
        <span class="material-icons text-sm mr-2">description</span>
        Application: 
        <button 
          @click.stop="$emit('view-application', fee.application)" 
          class="ml-1 text-blue-600 hover:underline"
        >
          View
        </button>
      </div>
      
      <div class="flex items-center">
        <span class="material-icons text-sm mr-2">person</span>
        Created by: {{ fee.created_by_name }}
      </div>
    </div>
    
    <div v-if="showActions" class="mt-3 flex justify-end space-x-2">
      <button 
        v-if="!fee.is_paid" 
        @click.stop="$emit('mark-paid')" 
        class="px-3 py-1 bg-green-600 text-white rounded-md hover:bg-green-700"
        title="Mark as paid"
      >
        Mark Paid
      </button>
      <button 
        v-if="canEdit" 
        @click.stop="$emit('edit')" 
        class="text-blue-600 hover:text-blue-800"
        title="Edit fee"
      >
        <span class="material-icons">edit</span>
      </button>
      <button 
        v-if="canDelete" 
        @click.stop="$emit('delete')" 
        class="text-red-600 hover:text-red-800"
        title="Delete fee"
      >
        <span class="material-icons">delete</span>
      </button>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'FeeCard',
  props: {
    fee: {
      type: Object,
      required: true
    },
    showActions: {
      type: Boolean,
      default: false
    },
    canEdit: {
      type: Boolean,
      default: false
    },
    canDelete: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click', 'mark-paid', 'edit', 'delete', 'view-application'],
  setup(props) {
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
    
    const isOverdue = computed(() => {
      if (!props.fee.due_date || props.fee.is_paid) return false
      
      const dueDate = new Date(props.fee.due_date)
      const today = new Date()
      
      // Reset time part for accurate date comparison
      today.setHours(0, 0, 0, 0)
      dueDate.setHours(0, 0, 0, 0)
      
      return dueDate < today
    })
    
    return {
      formatFeeType,
      formatCurrency,
      formatDate,
      isOverdue
    }
  }
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
