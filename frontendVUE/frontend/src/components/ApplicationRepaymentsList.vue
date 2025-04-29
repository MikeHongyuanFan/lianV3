<template>
  <div class="application-repayments-container">
    <div class="repayments-header">
      <h3>Application Repayments</h3>
      <BaseButton @click="showAddRepaymentModal = true" variant="primary">Add Repayment</BaseButton>
    </div>

    <!-- Repayment status filter -->
    <div class="filter-container">
      <label for="repaymentStatusFilter">Filter by status:</label>
      <select 
        id="repaymentStatusFilter" 
        v-model="repaymentStatusFilter" 
        class="form-control"
        @change="handleFilterChange"
      >
        <option value="">All repayments</option>
        <option value="true">Paid</option>
        <option value="false">Unpaid</option>
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
      <p>Loading repayments...</p>
    </div>

    <!-- Error display -->
    <AlertMessage v-if="error" :message="error" type="error" />

    <!-- Empty state -->
    <div v-if="!loading && !error && (!repayments || repayments.length === 0)" class="empty-state">
      <p>No repayments found for this application.</p>
    </div>

    <!-- Repayments list -->
    <div v-if="!loading && !error && repayments && repayments.length > 0" class="repayments-list">
      <table class="repayments-table">
        <thead>
          <tr>
            <th>Amount</th>
            <th>Due Date</th>
            <th>Status</th>
            <th>Paid Date</th>
            <th>Payment Method</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="repayment in repayments" :key="repayment.id" :class="{ 'paid': repayment.is_paid, 'overdue': isOverdue(repayment) }">
            <td>${{ repayment.amount.toFixed(2) }}</td>
            <td>{{ formatDate(repayment.due_date) }}</td>
            <td>
              <span :class="['status-badge', getStatusClass(repayment)]">
                {{ getStatusText(repayment) }}
              </span>
            </td>
            <td>{{ repayment.paid_date ? formatDate(repayment.paid_date) : '-' }}</td>
            <td>{{ repayment.payment_method || '-' }}</td>
            <td>
              <button 
                v-if="!repayment.is_paid" 
                @click="openRecordPaymentModal(repayment)" 
                class="record-payment-button"
              >
                Record Payment
              </button>
              <span v-else>-</span>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div v-if="totalRepayments > limit" class="pagination">
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

    <!-- Add Repayment Modal -->
    <div v-if="showAddRepaymentModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Add Repayment</h3>
          <button @click="showAddRepaymentModal = false" class="close-button">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="repaymentAmount">Amount</label>
            <input 
              id="repaymentAmount" 
              v-model.number="newRepayment.amount" 
              type="number" 
              step="0.01" 
              min="0" 
              class="form-control"
              placeholder="Enter repayment amount"
            />
          </div>
          <div class="form-group">
            <label for="repaymentDueDate">Due Date</label>
            <input 
              id="repaymentDueDate" 
              v-model="newRepayment.due_date" 
              type="date" 
              class="form-control"
            />
          </div>
          <div v-if="repaymentError" class="error-message">{{ repaymentError }}</div>
        </div>
        <div class="modal-footer">
          <BaseButton @click="showAddRepaymentModal = false" variant="secondary">Cancel</BaseButton>
          <BaseButton @click="addRepayment" variant="primary" :loading="addingRepayment">Add Repayment</BaseButton>
        </div>
      </div>
    </div>

    <!-- Record Payment Modal -->
    <div v-if="showRecordPaymentModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Record Payment</h3>
          <button @click="showRecordPaymentModal = false" class="close-button">&times;</button>
        </div>
        <div class="modal-body">
          <p>
            Record payment for repayment of ${{ selectedRepayment?.amount?.toFixed(2) }} 
            due on {{ formatDate(selectedRepayment?.due_date) }}
          </p>
          <div class="form-group">
            <label for="paymentMethod">Payment Method</label>
            <select 
              id="paymentMethod" 
              v-model="paymentData.payment_method" 
              class="form-control"
            >
              <option value="">Select payment method</option>
              <option value="bank_transfer">Bank Transfer</option>
              <option value="credit_card">Credit Card</option>
              <option value="direct_debit">Direct Debit</option>
              <option value="cash">Cash</option>
              <option value="check">Check</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div class="form-group">
            <label for="paymentDate">Payment Date</label>
            <input 
              id="paymentDate" 
              v-model="paymentData.payment_date" 
              type="date" 
              class="form-control"
            />
          </div>
          <div v-if="recordPaymentError" class="error-message">{{ recordPaymentError }}</div>
        </div>
        <div class="modal-footer">
          <BaseButton @click="showRecordPaymentModal = false" variant="secondary">Cancel</BaseButton>
          <BaseButton @click="recordPayment" variant="primary" :loading="recordingPayment">Record Payment</BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useApplicationStore } from '@/store/application'
import BaseButton from '@/components/BaseButton.vue'
import AlertMessage from '@/components/AlertMessage.vue'

export default {
  name: 'ApplicationRepaymentsList',
  components: {
    BaseButton,
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
    
    // Repayments state
    const repayments = ref([])
    const loading = ref(false)
    const error = ref(null)
    const totalRepayments = ref(0)
    const limit = ref(10)
    const offset = ref(0)
    const repaymentStatusFilter = ref('')
    const dateFromFilter = ref('')
    const dateToFilter = ref('')
    
    // Add repayment state
    const showAddRepaymentModal = ref(false)
    const newRepayment = ref({
      amount: null,
      due_date: new Date().toISOString().split('T')[0] // Today's date in YYYY-MM-DD format
    })
    const repaymentError = ref(null)
    const addingRepayment = ref(false)
    
    // Record payment state
    const showRecordPaymentModal = ref(false)
    const selectedRepayment = ref(null)
    const paymentData = ref({
      repayment_id: null,
      payment_method: '',
      payment_date: new Date().toISOString().split('T')[0] // Today's date in YYYY-MM-DD format
    })
    const recordPaymentError = ref(null)
    const recordingPayment = ref(false)
    
    // Computed properties
    const currentPage = computed(() => Math.floor(offset.value / limit.value) + 1)
    const totalPages = computed(() => Math.ceil(totalRepayments.value / limit.value))
    
    // Fetch repayments
    const fetchRepayments = async () => {
      try {
        loading.value = true
        error.value = null
        
        const params = {
          limit: limit.value,
          offset: offset.value
        }
        
        if (repaymentStatusFilter.value !== '') {
          params.is_paid = repaymentStatusFilter.value === 'true'
        }
        
        if (dateFromFilter.value) {
          params.date_from = dateFromFilter.value
        }
        
        if (dateToFilter.value) {
          params.date_to = dateToFilter.value
        }
        
        const response = await applicationStore.fetchApplicationRepayments(
          props.applicationId,
          limit.value,
          offset.value,
          repaymentStatusFilter.value !== '' ? repaymentStatusFilter.value === 'true' : null
        )
        
        repayments.value = response.results
        totalRepayments.value = response.count
      } catch (err) {
        error.value = err.message || 'Failed to load repayments'
        console.error('Error fetching repayments:', err)
      } finally {
        loading.value = false
      }
    }
    
    // Change page
    const changePage = (page) => {
      offset.value = (page - 1) * limit.value
      fetchRepayments()
    }
    
    // Handle filter change
    const handleFilterChange = () => {
      offset.value = 0 // Reset to first page
      fetchRepayments()
    }
    
    // Add repayment
    const addRepayment = async () => {
      // Validate input
      if (!newRepayment.value.amount || newRepayment.value.amount <= 0) {
        repaymentError.value = 'Amount must be greater than 0'
        return
      }
      
      if (!newRepayment.value.due_date) {
        repaymentError.value = 'Due date is required'
        return
      }
      
      try {
        addingRepayment.value = true
        repaymentError.value = null
        
        await applicationStore.addApplicationRepayment(
          props.applicationId,
          newRepayment.value
        )
        
        // Reset form and close modal
        newRepayment.value = {
          amount: null,
          due_date: new Date().toISOString().split('T')[0]
        }
        showAddRepaymentModal.value = false
        
        // Refresh repayments list
        await fetchRepayments()
      } catch (err) {
        repaymentError.value = err.message || 'Failed to add repayment'
        console.error('Error adding repayment:', err)
      } finally {
        addingRepayment.value = false
      }
    }
    
    // Open record payment modal
    const openRecordPaymentModal = (repayment) => {
      selectedRepayment.value = repayment
      paymentData.value = {
        repayment_id: repayment.id,
        payment_method: '',
        payment_date: new Date().toISOString().split('T')[0] // Reset to today's date
      }
      recordPaymentError.value = null
      showRecordPaymentModal.value = true
    }
    
    // Record payment
    const recordPayment = async () => {
      // Validate input
      if (!paymentData.value.payment_method) {
        recordPaymentError.value = 'Payment method is required'
        return
      }
      
      if (!paymentData.value.payment_date) {
        recordPaymentError.value = 'Payment date is required'
        return
      }
      
      try {
        recordingPayment.value = true
        recordPaymentError.value = null
        
        // Prepare the payment data according to the API requirements
        const paymentRequest = {
          repayment_id: paymentData.value.repayment_id,
          payment_method: paymentData.value.payment_method,
          payment_date: paymentData.value.payment_date
        }
        
        await applicationStore.recordApplicationPayment(
          props.applicationId,
          paymentRequest
        )
        
        // Close modal
        showRecordPaymentModal.value = false
        selectedRepayment.value = null
        
        // Refresh repayments list
        await fetchRepayments()
      } catch (err) {
        recordPaymentError.value = err.message || 'Failed to record payment'
        console.error('Error recording payment:', err)
      } finally {
        recordingPayment.value = false
      }
    }
    
    // Check if repayment is overdue
    const isOverdue = (repayment) => {
      if (repayment.is_paid) return false
      
      const today = new Date()
      const dueDate = new Date(repayment.due_date)
      return dueDate < today
    }
    
    // Get status class for repayment
    const getStatusClass = (repayment) => {
      if (repayment.is_paid) return 'status-paid'
      if (isOverdue(repayment)) return 'status-overdue'
      
      // Check if due soon (within 7 days)
      const today = new Date()
      const dueDate = new Date(repayment.due_date)
      const diffTime = dueDate - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays <= 7) return 'status-due-soon'
      return 'status-scheduled'
    }
    
    // Get status text for repayment
    const getStatusText = (repayment) => {
      if (repayment.is_paid) return 'Paid'
      if (isOverdue(repayment)) return 'Overdue'
      
      // Check if due soon (within 7 days)
      const today = new Date()
      const dueDate = new Date(repayment.due_date)
      const diffTime = dueDate - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays <= 7) return `Due in ${diffDays} day${diffDays === 1 ? '' : 's'}`
      return 'Scheduled'
    }
    
    // Format date
    const formatDate = (dateString) => {
      if (!dateString) return ''
      
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      }).format(date)
    }
    
    onMounted(() => {
      fetchRepayments()
    })
    
    return {
      repayments,
      loading,
      error,
      totalRepayments,
      limit,
      currentPage,
      totalPages,
      repaymentStatusFilter,
      dateFromFilter,
      dateToFilter,
      showAddRepaymentModal,
      newRepayment,
      repaymentError,
      addingRepayment,
      showRecordPaymentModal,
      selectedRepayment,
      paymentData,
      recordPaymentError,
      recordingPayment,
      changePage,
      handleFilterChange,
      addRepayment,
      openRecordPaymentModal,
      recordPayment,
      isOverdue,
      getStatusClass,
      getStatusText,
      formatDate
    }
  }
}
</script>

<style scoped>
.application-repayments-container {
  margin-bottom: 2rem;
}

.repayments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.repayments-header h3 {
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

.repayments-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.repayments-table th,
.repayments-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.repayments-table th {
  background-color: #f9fafb;
  font-weight: 600;
}

.repayments-table tr.paid {
  background-color: #f0fdf4;
}

.repayments-table tr.overdue {
  background-color: #fef2f2;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-paid {
  background-color: #dcfce7;
  color: #166534;
}

.status-overdue {
  background-color: #fee2e2;
  color: #b91c1c;
}

.status-due-soon {
  background-color: #fef3c7;
  color: #92400e;
}

.status-scheduled {
  background-color: #e0f2fe;
  color: #0369a1;
}

.record-payment-button {
  padding: 0.375rem 0.75rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  cursor: pointer;
}

.record-payment-button:hover {
  background-color: #2563eb;
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

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-container {
  background-color: white;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
}

.modal-body {
  padding: 1rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style>
