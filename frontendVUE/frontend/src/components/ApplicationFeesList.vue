<template>
  <div class="application-fees-container">
    <div class="fees-header">
      <h3>Application Fees</h3>
      <BaseButton @click="showAddFeeModal = true" variant="primary">Add Fee</BaseButton>
    </div>

    <!-- Fee status filter -->
    <div class="filter-container">
      <label for="feeStatusFilter">Filter by status:</label>
      <select 
        id="feeStatusFilter" 
        v-model="feeStatusFilter" 
        class="form-control"
        @change="handleFilterChange"
      >
        <option value="">All fees</option>
        <option value="true">Paid</option>
        <option value="false">Unpaid</option>
      </select>
      
      <label for="feeTypeFilter" class="ml-4">Filter by type:</label>
      <select 
        id="feeTypeFilter" 
        v-model="feeTypeFilter" 
        class="form-control"
        @change="handleFilterChange"
      >
        <option value="">All types</option>
        <option value="application">Application</option>
        <option value="valuation">Valuation</option>
        <option value="legal">Legal</option>
        <option value="broker">Broker</option>
        <option value="settlement">Settlement</option>
        <option value="other">Other</option>
      </select>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-container">
      <p>Loading fees...</p>
    </div>

    <!-- Error display -->
    <AlertMessage v-if="error" :message="error" type="error" />

    <!-- Empty state -->
    <div v-if="!loading && !error && (!fees || fees.length === 0)" class="empty-state">
      <p>No fees found for this application.</p>
    </div>

    <!-- Fees list -->
    <div v-if="!loading && !error && fees && fees.length > 0" class="fees-list">
      <table class="fees-table">
        <thead>
          <tr>
            <th>Fee Type</th>
            <th>Amount</th>
            <th>Due Date</th>
            <th>Status</th>
            <th>Paid Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="fee in fees" :key="fee.id" :class="{ 'paid': fee.is_paid }">
            <td>{{ fee.fee_type_display }}</td>
            <td>${{ fee.amount.toFixed(2) }}</td>
            <td>{{ formatDate(fee.due_date) }}</td>
            <td>
              <span :class="['status-badge', fee.is_paid ? 'status-paid' : 'status-pending']">
                {{ fee.is_paid ? 'Paid' : 'Pending' }}
              </span>
            </td>
            <td>{{ fee.paid_date ? formatDate(fee.paid_date) : '-' }}</td>
            <td>
              <button 
                v-if="!fee.is_paid" 
                @click="openMarkPaidModal(fee)" 
                class="mark-paid-button"
              >
                Mark as Paid
              </button>
              <span v-else>-</span>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div v-if="totalFees > limit" class="pagination">
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

    <!-- Add Fee Modal -->
    <div v-if="showAddFeeModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Add Fee</h3>
          <button @click="showAddFeeModal = false" class="close-button">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="feeType">Fee Type</label>
            <select 
              id="feeType" 
              v-model="newFee.fee_type" 
              class="form-control"
            >
              <option value="">Select fee type</option>
              <option value="application">Application</option>
              <option value="valuation">Valuation</option>
              <option value="legal">Legal</option>
              <option value="broker">Broker</option>
              <option value="settlement">Settlement</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div class="form-group">
            <label for="feeAmount">Amount</label>
            <input 
              id="feeAmount" 
              v-model.number="newFee.amount" 
              type="number" 
              step="0.01" 
              min="0" 
              class="form-control"
              placeholder="Enter fee amount"
            />
          </div>
          <div class="form-group">
            <label for="feeDueDate">Due Date</label>
            <input 
              id="feeDueDate" 
              v-model="newFee.due_date" 
              type="date" 
              class="form-control"
            />
          </div>
          <div v-if="feeError" class="error-message">{{ feeError }}</div>
        </div>
        <div class="modal-footer">
          <BaseButton @click="showAddFeeModal = false" variant="secondary">Cancel</BaseButton>
          <BaseButton @click="addFee" variant="primary" :loading="addingFee">Add Fee</BaseButton>
        </div>
      </div>
    </div>

    <!-- Mark Fee as Paid Modal -->
    <div v-if="showMarkPaidModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Mark Fee as Paid</h3>
          <button @click="showMarkPaidModal = false" class="close-button">&times;</button>
        </div>
        <div class="modal-body">
          <p>
            Are you sure you want to mark this {{ selectedFee?.fee_type_display }} fee of 
            ${{ selectedFee?.amount?.toFixed(2) }} as paid?
          </p>
          <div class="form-group">
            <label for="paidDate">Payment Date</label>
            <input 
              id="paidDate" 
              v-model="paidDate" 
              type="date" 
              class="form-control"
            />
          </div>
          <div v-if="markPaidError" class="error-message">{{ markPaidError }}</div>
        </div>
        <div class="modal-footer">
          <BaseButton @click="showMarkPaidModal = false" variant="secondary">Cancel</BaseButton>
          <BaseButton @click="markFeePaid" variant="primary" :loading="markingPaid">Mark as Paid</BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useApplicationStore } from '@/store/application'
import { useFeeStore } from '@/store/fee'
import BaseButton from '@/components/BaseButton.vue'
import AlertMessage from '@/components/AlertMessage.vue'

export default {
  name: 'ApplicationFeesList',
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
    const feeStore = useFeeStore()
    
    // Fees state
    const fees = ref([])
    const loading = ref(false)
    const error = ref(null)
    const totalFees = ref(0)
    const limit = ref(10)
    const offset = ref(0)
    const feeStatusFilter = ref('')
    const feeTypeFilter = ref('')
    
    // Add fee state
    const showAddFeeModal = ref(false)
    const newFee = ref({
      fee_type: '',
      amount: null,
      due_date: new Date().toISOString().split('T')[0] // Today's date in YYYY-MM-DD format
    })
    const feeError = ref(null)
    const addingFee = ref(false)
    
    // Mark fee as paid state
    const showMarkPaidModal = ref(false)
    const selectedFee = ref(null)
    const paidDate = ref(new Date().toISOString().split('T')[0]) // Today's date in YYYY-MM-DD format
    const markPaidError = ref(null)
    const markingPaid = ref(false)
    
    // Computed properties
    const currentPage = computed(() => Math.floor(offset.value / limit.value) + 1)
    const totalPages = computed(() => Math.ceil(totalFees.value / limit.value))
    
    // Fetch fees
    const fetchFees = async () => {
      try {
        loading.value = true
        error.value = null
        
        const params = {
          limit: limit.value,
          offset: offset.value
        }
        
        if (feeStatusFilter.value !== '') {
          params.is_paid = feeStatusFilter.value === 'true'
        }
        
        if (feeTypeFilter.value !== '') {
          params.fee_type = feeTypeFilter.value
        }
        
        const response = await applicationStore.fetchApplicationFees(
          props.applicationId,
          limit.value,
          offset.value,
          feeStatusFilter.value !== '' ? feeStatusFilter.value === 'true' : null,
          feeTypeFilter.value || null
        )
        
        fees.value = response.results
        totalFees.value = response.count
      } catch (err) {
        error.value = err.message || 'Failed to load fees'
        console.error('Error fetching fees:', err)
      } finally {
        loading.value = false
      }
    }
    
    // Change page
    const changePage = (page) => {
      offset.value = (page - 1) * limit.value
      fetchFees()
    }
    
    // Handle filter change
    const handleFilterChange = () => {
      offset.value = 0 // Reset to first page
      fetchFees()
    }
    
    // Add fee
    const addFee = async () => {
      // Validate input
      if (!newFee.value.fee_type) {
        feeError.value = 'Fee type is required'
        return
      }
      
      if (!newFee.value.amount || newFee.value.amount <= 0) {
        feeError.value = 'Amount must be greater than 0'
        return
      }
      
      if (!newFee.value.due_date) {
        feeError.value = 'Due date is required'
        return
      }
      
      try {
        addingFee.value = true
        feeError.value = null
        
        await applicationStore.addApplicationFee(
          props.applicationId,
          newFee.value
        )
        
        // Reset form and close modal
        newFee.value = {
          fee_type: '',
          amount: null,
          due_date: new Date().toISOString().split('T')[0]
        }
        showAddFeeModal.value = false
        
        // Refresh fees list
        await fetchFees()
      } catch (err) {
        feeError.value = err.message || 'Failed to add fee'
        console.error('Error adding fee:', err)
      } finally {
        addingFee.value = false
      }
    }
    
    // Open mark paid modal
    const openMarkPaidModal = (fee) => {
      selectedFee.value = fee
      paidDate.value = new Date().toISOString().split('T')[0] // Reset to today's date
      markPaidError.value = null
      showMarkPaidModal.value = true
      showMarkPaidModal.value = true
    }
    
    // Mark fee as paid
    const markFeePaid = async () => {
      if (!paidDate.value) {
        markPaidError.value = 'Payment date is required'
        return
      }
      
      try {
        markingPaid.value = true
        markPaidError.value = null
        
        // Call the API to mark the fee as paid
      await applicationStore.markFeePaid(
        selectedFee.value.id,
        { paid_date: paidDate.value }
      )
      
      // Refresh fees list
      await fetchFees()
      
      // Close modal
      showMarkPaidModal.value = false
      selectedFee.value = null
      } catch (err) {
        markPaidError.value = err.message || 'Failed to mark fee as paid'
        console.error('Error marking fee as paid:', err)
      } finally {
        markingPaid.value = false
      }
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
      fetchFees()
    })
    
    return {
      fees,
      loading,
      error,
      totalFees,
      limit,
      currentPage,
      totalPages,
      feeStatusFilter,
      feeTypeFilter,
      showAddFeeModal,
      newFee,
      feeError,
      addingFee,
      selectedFee,
      paidDate,
      markPaidError,
      markingPaid,
      changePage,
      handleFilterChange,
      addFee,
      showMarkPaidModal,
      openMarkPaidModal,
      markFeePaid,
      formatDate
    }
  }
}
</script>

<style scoped>
.application-fees-container {
  margin-bottom: 2rem;
}

.fees-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.fees-header h3 {
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

.fees-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.fees-table th,
.fees-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.fees-table th {
  background-color: #f9fafb;
  font-weight: 600;
}

.fees-table tr.paid {
  background-color: #f0fdf4;
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

.status-pending {
  background-color: #fef3c7;
  color: #92400e;
}

.mark-paid-button {
  padding: 0.375rem 0.75rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  cursor: pointer;
}

.mark-paid-button:hover {
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
