<template>
  <div class="application-ledger-container">
    <div class="ledger-header">
      <h3>Application Ledger</h3>
    </div>

    <!-- Ledger filters -->
    <div class="filter-container">
      <label for="entryTypeFilter">Filter by entry type:</label>
      <select 
        id="entryTypeFilter" 
        v-model="entryTypeFilter" 
        class="form-control"
        @change="handleFilterChange"
      >
        <option value="">All entry types</option>
        <option value="fee_added">Fee Added</option>
        <option value="fee_paid">Fee Paid</option>
        <option value="repayment_added">Repayment Added</option>
        <option value="repayment_received">Repayment Received</option>
        <option value="adjustment">Adjustment</option>
      </select>
      
      <label for="dateFromFilter" class="ml-4">From:</label>
      <input 
        id="dateFromFilter" 
        v-model="dateFromFilter" 
        type="date" 
        class="form-control"
        @change="handleFilterChange"
      />
      
      <label for="dateToFilter" class="ml-2">To:</label>
      <input 
        id="dateToFilter" 
        v-model="dateToFilter" 
        type="date" 
        class="form-control"
        @change="handleFilterChange"
      />
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-container">
      <p>Loading ledger entries...</p>
    </div>

    <!-- Error display -->
    <AlertMessage v-if="error" :message="error" type="error" />

    <!-- Empty state -->
    <div v-if="!loading && !error && (!ledgerEntries || ledgerEntries.length === 0)" class="empty-state">
      <p>No ledger entries found for this application.</p>
    </div>

    <!-- Ledger entries -->
    <div v-if="!loading && !error && ledgerEntries && ledgerEntries.length > 0" class="ledger-entries">
      <table class="ledger-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Entry Type</th>
            <th>Description</th>
            <th>Amount</th>
            <th>Balance</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in ledgerEntries" :key="entry.id" :class="getEntryClass(entry)">
            <td>{{ formatDate(entry.date) }}</td>
            <td>{{ entry.entry_type_display || entry.transaction_type_display }}</td>
            <td>{{ entry.description }}</td>
            <td :class="{ 'amount-positive': isPositiveAmount(entry), 'amount-negative': !isPositiveAmount(entry) }">
              {{ formatAmount(entry.amount) }}
            </td>
            <td>{{ formatCurrency(entry.balance) }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div v-if="totalEntries > limit" class="pagination">
        <button 
          :disabled="currentPage === 1" 
          @click="changePage(currentPage - 1)" 
          class="pagination-button"
        >
          Previous
        </button>
        <span class="pagination-info">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button 
          :disabled="currentPage === totalPages" 
          @click="changePage(currentPage + 1)" 
          class="pagination-button"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useApplicationStore } from '@/store/application'
import AlertMessage from '@/components/AlertMessage.vue'

export default {
  name: 'ApplicationLedgerView',
  components: {
    AlertMessage
  },
  props: {
    applicationId: {
      type: [Number, String],
      required: true
    }
  },
  setup(props) {
    const applicationStore = useApplicationStore()
    
    // Ledger state
    const ledgerEntries = ref([])
    const loading = ref(false)
    const error = ref(null)
    const totalEntries = ref(0)
    const limit = ref(10)
    const offset = ref(0)
    const entryTypeFilter = ref('')
    const dateFromFilter = ref('')
    const dateToFilter = ref('')
    
    // Computed properties
    const currentPage = computed(() => Math.floor(offset.value / limit.value) + 1)
    const totalPages = computed(() => Math.ceil(totalEntries.value / limit.value))
    
    // Fetch ledger entries
    const fetchLedgerEntries = async () => {
      try {
        loading.value = true
        error.value = null
        
        const params = {
          limit: limit.value,
          offset: offset.value
        }
        
        if (entryTypeFilter.value) {
          // According to the API documentation, the filter parameter is 'entry_type'
          // for the ledger endpoint
          params.entry_type = entryTypeFilter.value
        }
        
        if (dateFromFilter.value) {
          params.date_from = dateFromFilter.value
        }
        
        if (dateToFilter.value) {
          params.date_to = dateToFilter.value
        }
        
        const response = await applicationStore.fetchApplicationLedger(
          props.applicationId,
          limit.value,
          offset.value,
          params
        )
        
        ledgerEntries.value = response.results
        totalEntries.value = response.count
      } catch (err) {
        error.value = err.message || 'Failed to load ledger entries'
        console.error('Error fetching ledger entries:', err)
      } finally {
        loading.value = false
      }
    }
    
    // Change page
    const changePage = (page) => {
      offset.value = (page - 1) * limit.value
      fetchLedgerEntries()
    }
    
    // Handle filter change
    const handleFilterChange = () => {
      offset.value = 0 // Reset to first page
      fetchLedgerEntries()
    }
    
    // Format date
    const formatDate = (dateString) => {
      if (!dateString) return ''
      
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    }
    
    // Format currency
    const formatCurrency = (amount) => {
      if (amount === null || amount === undefined) return '-'
      
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
      }).format(amount)
    }
    
    // Format amount with sign
    const formatAmount = (amount) => {
      if (amount === null || amount === undefined) return '-'
      
      const prefix = amount >= 0 ? '+' : ''
      return prefix + formatCurrency(amount)
    }
    
    // Check if amount is positive
    const isPositiveAmount = (entry) => {
      const entryType = entry.entry_type || entry.transaction_type
      
      // Fee added and repayment added are negative entries (money out)
      // Fee paid and repayment received are positive entries (money in)
      if (entryType === 'fee_added' || entryType === 'repayment_added') {
        return false
      }
      
      if (entryType === 'fee_paid' || entryType === 'repayment_received') {
        return true
      }
      
      // For adjustments, check the amount
      return entry.amount >= 0
    }
    
    // Get CSS class for entry row
    const getEntryClass = (entry) => {
      const entryType = entry.entry_type || entry.transaction_type
      
      if (entryType === 'fee_added' || entryType === 'repayment_added') {
        return 'entry-negative'
      }
      
      if (entryType === 'fee_paid' || entryType === 'repayment_received') {
        return 'entry-positive'
      }
      
      return entry.amount >= 0 ? 'entry-positive' : 'entry-negative'
    }
    
    onMounted(() => {
      fetchLedgerEntries()
    })
    
    return {
      ledgerEntries,
      loading,
      error,
      totalEntries,
      limit,
      currentPage,
      totalPages,
      entryTypeFilter,
      dateFromFilter,
      dateToFilter,
      changePage,
      handleFilterChange,
      formatDate,
      formatCurrency,
      formatAmount,
      isPositiveAmount,
      getEntryClass
    }
  }
}
</script>

<style scoped>
.application-ledger-container {
  margin-bottom: 2rem;
}

.ledger-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.ledger-header h3 {
  margin: 0;
}

.filter-container {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-container label {
  font-weight: 500;
}

.ml-4 {
  margin-left: 1rem;
}

.ml-2 {
  margin-left: 0.5rem;
}

.form-control {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-family: inherit;
  font-size: inherit;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  background-color: #f9fafb;
  border-radius: 0.5rem;
}

.empty-state {
  padding: 2rem;
  text-align: center;
  background-color: #f9fafb;
  border-radius: 0.5rem;
  color: #6b7280;
}

.ledger-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.ledger-table th,
.ledger-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.ledger-table th {
  background-color: #f9fafb;
  font-weight: 600;
}

.entry-positive {
  background-color: #f0fdf4;
}

.entry-negative {
  background-color: #fef2f2;
}

.amount-positive {
  color: #16a34a;
}

.amount-negative {
  color: #dc2626;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1.5rem;
  gap: 1rem;
}

.pagination-button {
  padding: 0.5rem 1rem;
  background-color: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  cursor: pointer;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  color: #6b7280;
}
</style>
