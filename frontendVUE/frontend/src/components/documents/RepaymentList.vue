<template>
  <div class="repayment-list">
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchRepayments" class="underline">Try again</button>
    </div>
    
    <!-- Empty state -->
    <div v-else-if="!repayments.length" class="text-center py-8 bg-gray-50 rounded-lg">
      <p class="text-gray-500 mb-4">No repayments found</p>
      <button
        v-if="showCreateButton"
        @click="$emit('create')"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
      >
        Create Repayment
      </button>
    </div>
    
    <!-- Repayment summary -->
    <div v-else-if="showSummary" class="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-white p-4 rounded-lg shadow">
        <h4 class="text-sm text-gray-500">Total Repayments</h4>
        <p class="text-xl font-bold">{{ formatCurrency(totalAmount) }}</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <h4 class="text-sm text-gray-500">Paid</h4>
        <p class="text-xl font-bold text-green-600">{{ formatCurrency(totalPaidAmount) }}</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <h4 class="text-sm text-gray-500">Pending</h4>
        <p class="text-xl font-bold text-yellow-600">{{ formatCurrency(totalUnpaidAmount) }}</p>
      </div>
    </div>
    
    <!-- Repayments list -->
    <div v-if="repayments.length" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <RepaymentCard
        v-for="repayment in repayments"
        :key="repayment.id"
        :repayment="repayment"
        :show-actions="showActions"
        :can-edit="canEdit"
        :can-delete="canDelete"
        @click="$emit('view', repayment.id)"
        @mark-paid="$emit('mark-paid', repayment.id)"
        @edit="$emit('edit', repayment.id)"
        @delete="$emit('delete', repayment)"
        @view-application="$emit('view-application', $event)"
      />
    </div>
    
    <!-- Pagination -->
    <div v-if="repayments.length && showPagination" class="pagination-container flex justify-between items-center mt-6">
      <div class="text-sm text-gray-500">
        Showing {{ currentPage * itemsPerPage - itemsPerPage + 1 }} 
        to {{ Math.min(currentPage * itemsPerPage, totalItems) }} 
        of {{ totalItems }} repayments
      </div>
      
      <div class="flex items-center space-x-2">
        <button
          @click="$emit('prev-page')"
          :disabled="currentPage === 1"
          class="px-3 py-1 border rounded-md"
          :class="currentPage === 1 ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'"
        >
          Previous
        </button>
        
        <span class="px-3 py-1">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        
        <button
          @click="$emit('next-page')"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 border rounded-md"
          :class="currentPage === totalPages ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import RepaymentCard from '@/components/documents/RepaymentCard.vue'

export default {
  name: 'RepaymentList',
  components: {
    RepaymentCard
  },
  props: {
    repayments: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    },
    showActions: {
      type: Boolean,
      default: true
    },
    canEdit: {
      type: Boolean,
      default: true
    },
    canDelete: {
      type: Boolean,
      default: true
    },
    showCreateButton: {
      type: Boolean,
      default: true
    },
    showPagination: {
      type: Boolean,
      default: true
    },
    showSummary: {
      type: Boolean,
      default: true
    },
    currentPage: {
      type: Number,
      default: 1
    },
    totalPages: {
      type: Number,
      default: 1
    },
    itemsPerPage: {
      type: Number,
      default: 10
    },
    totalItems: {
      type: Number,
      default: 0
    },
    totalAmount: {
      type: [Number, String],
      default: 0
    },
    totalPaidAmount: {
      type: [Number, String],
      default: 0
    },
    totalUnpaidAmount: {
      type: [Number, String],
      default: 0
    }
  },
  emits: [
    'create', 
    'view',
    'mark-paid', 
    'edit', 
    'delete', 
    'view-application', 
    'prev-page', 
    'next-page',
    'fetch'
  ],
  setup(props, { emit }) {
    const fetchRepayments = () => {
      emit('fetch')
    }
    
    const formatCurrency = (amount) => {
      if (amount === undefined || amount === null) return '$0.00'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }
    
    return {
      fetchRepayments,
      formatCurrency
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
