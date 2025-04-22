<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">Ledger</h2>
    
    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <h3 class="text-sm font-medium text-gray-500">Total Fees</h3>
        <p class="mt-1 text-2xl font-semibold text-gray-900">${{ formatCurrency(totalFees) }}</p>
      </div>
      
      <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <h3 class="text-sm font-medium text-gray-500">Total Payments</h3>
        <p class="mt-1 text-2xl font-semibold text-gray-900">${{ formatCurrency(totalPayments) }}</p>
      </div>
      
      <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <h3 class="text-sm font-medium text-gray-500">Balance</h3>
        <p class="mt-1 text-2xl font-semibold" :class="balance < 0 ? 'text-red-600' : 'text-green-600'">
          ${{ formatCurrency(Math.abs(balance)) }}
          <span class="text-sm font-normal">{{ balance < 0 ? '(Owing)' : '(Credit)' }}</span>
        </p>
      </div>
    </div>
    
    <!-- Ledger Entries Table -->
    <div v-if="ledgerEntries && ledgerEntries.length > 0">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Transaction Type
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Description
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Amount
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Related To
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created By
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="entry in ledgerEntries" :key="entry.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ formatDate(entry.transaction_date) }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="getTransactionTypeClass(entry.transaction_type)">
                  {{ formatTransactionType(entry.transaction_type) }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">{{ entry.description }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium" :class="isDebit(entry.transaction_type) ? 'text-red-600' : 'text-green-600'">
                  {{ isDebit(entry.transaction_type) ? '-' : '+' }}${{ formatCurrency(entry.amount) }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div v-if="entry.related_fee" class="text-sm text-gray-900">
                  Fee: {{ formatFeeType(entry.related_fee.fee_type) }}
                </div>
                <div v-else-if="entry.related_repayment" class="text-sm text-gray-900">
                  Repayment: {{ formatDate(entry.related_repayment.due_date) }}
                </div>
                <div v-else class="text-sm text-gray-500">
                  N/A
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ entry.created_by_name }}</div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else class="bg-gray-50 p-4 rounded-md">
      <p class="text-sm text-gray-500">No ledger entries for this application</p>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from 'vue'

const props = defineProps({
  ledgerEntries: {
    type: Array,
    default: () => []
  }
})

const totalFees = computed(() => {
  return props.ledgerEntries
    .filter(entry => isDebit(entry.transaction_type))
    .reduce((sum, entry) => sum + parseFloat(entry.amount), 0)
})

const totalPayments = computed(() => {
  return props.ledgerEntries
    .filter(entry => !isDebit(entry.transaction_type))
    .reduce((sum, entry) => sum + parseFloat(entry.amount), 0)
})

const balance = computed(() => {
  return totalPayments.value - totalFees.value
})

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US').format(value)
}

const formatTransactionType = (type) => {
  const types = {
    'fee_added': 'Fee Added',
    'payment_received': 'Payment Received',
    'fee_waived': 'Fee Waived',
    'refund_issued': 'Refund Issued',
    'adjustment': 'Adjustment'
  }
  
  return types[type] || type
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

const isDebit = (transactionType) => {
  return ['fee_added', 'refund_issued'].includes(transactionType)
}

const getTransactionTypeClass = (type) => {
  const typeClasses = {
    'fee_added': 'bg-red-100 text-red-800',
    'payment_received': 'bg-green-100 text-green-800',
    'fee_waived': 'bg-blue-100 text-blue-800',
    'refund_issued': 'bg-yellow-100 text-yellow-800',
    'adjustment': 'bg-purple-100 text-purple-800'
  }
  
  return typeClasses[type] || 'bg-gray-100 text-gray-800'
}
</script>
