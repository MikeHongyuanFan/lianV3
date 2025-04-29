<template>
  <div 
    class="repayment-card bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow"
    :class="{ 
      'border-l-4 border-red-400': isOverdue && !repayment.is_paid,
      'border-l-4 border-yellow-400': isDueSoon && !repayment.is_paid
    }"
  >
    <div class="flex justify-between items-start">
      <h3 class="text-lg font-semibold">Repayment</h3>
      <span
        class="repayment-status-badge px-2 py-1 text-xs rounded-full"
        :class="statusClass"
      >
        {{ statusText }}
      </span>
    </div>
    
    <div class="mt-2 flex justify-between">
      <div class="text-gray-700">
        <div class="text-2xl font-bold">{{ formatCurrency(repayment.amount) }}</div>
        <div class="text-sm text-gray-500">
          Due: {{ formatDate(repayment.due_date) }}
        </div>
        <div v-if="repayment.is_paid" class="text-sm text-gray-500">
          Paid: {{ formatDate(repayment.paid_date) }}
          <span v-if="repayment.payment_method" class="ml-1">({{ repayment.payment_method }})</span>
        </div>
      </div>
      
      <div v-if="repayment.status" class="text-sm text-gray-600 max-w-xs">
        {{ repayment.status }}
      </div>
    </div>
    
    <div class="mt-3 text-sm text-gray-500">
      <div v-if="repayment.application" class="flex items-center">
        <span class="material-icons text-sm mr-2">description</span>
        Application: 
        <button 
          @click.stop="$emit('view-application', repayment.application)" 
          class="ml-1 text-blue-600 hover:underline"
        >
          View
        </button>
      </div>
      
      <div class="flex items-center">
        <span class="material-icons text-sm mr-2">person</span>
        Created by: {{ repayment.created_by_name || 'System' }}
      </div>
    </div>
    
    <div v-if="showActions" class="mt-3 flex justify-end space-x-2">
      <button 
        v-if="!repayment.is_paid" 
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
        title="Edit repayment"
      >
        <span class="material-icons">edit</span>
      </button>
      <button 
        v-if="canDelete" 
        @click.stop="$emit('delete')" 
        class="text-red-600 hover:text-red-800"
        title="Delete repayment"
      >
        <span class="material-icons">delete</span>
      </button>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'RepaymentCard',
  props: {
    repayment: {
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
      if (!props.repayment.due_date || props.repayment.is_paid) return false
      
      const dueDate = new Date(props.repayment.due_date)
      const today = new Date()
      
      // Reset time part for accurate date comparison
      today.setHours(0, 0, 0, 0)
      dueDate.setHours(0, 0, 0, 0)
      
      return dueDate < today
    })
    
    const isDueSoon = computed(() => {
      if (!props.repayment.due_date || props.repayment.is_paid || isOverdue.value) return false
      
      const dueDate = new Date(props.repayment.due_date)
      const today = new Date()
      const nextWeek = new Date(today)
      nextWeek.setDate(today.getDate() + 7)
      
      // Reset time part for accurate date comparison
      today.setHours(0, 0, 0, 0)
      dueDate.setHours(0, 0, 0, 0)
      nextWeek.setHours(0, 0, 0, 0)
      
      return dueDate >= today && dueDate <= nextWeek
    })
    
    const statusText = computed(() => {
      if (props.repayment.is_paid) return 'Paid'
      if (isOverdue.value) return 'Overdue'
      if (isDueSoon.value) return 'Due Soon'
      return 'Scheduled'
    })
    
    const statusClass = computed(() => {
      if (props.repayment.is_paid) return 'bg-green-100 text-green-800'
      if (isOverdue.value) return 'bg-red-100 text-red-800'
      if (isDueSoon.value) return 'bg-yellow-100 text-yellow-800'
      return 'bg-blue-100 text-blue-800'
    })
    
    return {
      formatCurrency,
      formatDate,
      isOverdue,
      isDueSoon,
      statusText,
      statusClass
    }
  }
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
