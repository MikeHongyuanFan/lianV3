<template>
  <div class="fees-view">
    <div class="container-fluid py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Fees</h1>
        <button class="btn btn-primary" @click="showAddFeeModal">
          <i class="bi bi-plus-circle me-2"></i> Add Fee
        </button>
      </div>

      <!-- Search and filters -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-3">
              <select class="form-select" v-model="filters.application" @change="applyFilters">
                <option value="">All Applications</option>
                <option v-for="app in applications" :key="app.id" :value="app.id">
                  {{ app.reference_number }}
                </option>
              </select>
            </div>
            <div class="col-md-3">
              <select class="form-select" v-model="filters.fee_type" @change="applyFilters">
                <option value="">All Fee Types</option>
                <option value="application">Application</option>
                <option value="valuation">Valuation</option>
                <option value="legal">Legal</option>
                <option value="broker">Broker</option>
                <option value="settlement">Settlement</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div class="col-md-2">
              <select class="form-select" v-model="filters.is_paid" @change="applyFilters">
                <option value="">Payment Status</option>
                <option value="true">Paid</option>
                <option value="false">Unpaid</option>
              </select>
            </div>
            <div class="col-md-2">
              <input type="date" class="form-control" placeholder="From Date" v-model="filters.date_from" @change="applyFilters" />
            </div>
            <div class="col-md-2">
              <input type="date" class="form-control" placeholder="To Date" v-model="filters.date_to" @change="applyFilters" />
            </div>
          </div>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading fees...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchFees">
          Try Again
        </button>
      </div>

      <!-- Empty state -->
      <div v-else-if="fees.length === 0" class="text-center py-5">
        <i class="bi bi-receipt display-1 text-muted"></i>
        <h3 class="mt-3">No fees found</h3>
        <p class="text-muted">
          {{ hasFilters ? 'Try adjusting your filters' : 'Add your first fee to get started' }}
        </p>
        <button class="btn btn-primary mt-3" @click="showAddFeeModal" v-if="!hasFilters">
          <i class="bi bi-plus-circle me-2"></i> Add Fee
        </button>
      </div>

      <!-- Fees list -->
      <div v-else class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Application</th>
                      <th>Fee Type</th>
                      <th>Amount</th>
                      <th>Due Date</th>
                      <th>Status</th>
                      <th>Paid Date</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="fee in fees" :key="fee.id">
                      <td>{{ getApplicationReference(fee.application) }}</td>
                      <td>{{ fee.fee_type_display || fee.fee_type }}</td>
                      <td>${{ formatCurrency(fee.amount) }}</td>
                      <td>{{ formatDate(fee.due_date) }}</td>
                      <td>
                        <span class="badge" :class="fee.is_paid ? 'bg-success' : 'bg-warning'">
                          {{ fee.is_paid ? 'Paid' : 'Pending' }}
                        </span>
                      </td>
                      <td>{{ fee.is_paid ? formatDate(fee.paid_date) : 'N/A' }}</td>
                      <td>
                        <div class="btn-group">
                          <button class="btn btn-sm btn-outline-primary" @click="viewFee(fee)">
                            <i class="bi bi-eye"></i>
                          </button>
                          <button class="btn btn-sm btn-outline-secondary" v-if="!fee.is_paid" @click="editFee(fee)">
                            <i class="bi bi-pencil"></i>
                          </button>
                          <button class="btn btn-sm btn-outline-success" v-if="!fee.is_paid" @click="markAsPaid(fee)">
                            <i class="bi bi-check-circle"></i>
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Summary card -->
      <div v-if="fees.length > 0" class="row mt-4">
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Fee Summary</h5>
              <div class="d-flex justify-content-between mb-2">
                <span>Total Fees:</span>
                <span>${{ formatCurrency(totalFees) }}</span>
              </div>
              <div class="d-flex justify-content-between mb-2">
                <span>Paid Fees:</span>
                <span>${{ formatCurrency(paidFees) }}</span>
              </div>
              <div class="d-flex justify-content-between mb-2">
                <span>Pending Fees:</span>
                <span>${{ formatCurrency(pendingFees) }}</span>
              </div>
              <div class="progress mt-3">
                <div class="progress-bar bg-success" role="progressbar" :style="`width: ${paidPercentage}%`" :aria-valuenow="paidPercentage" aria-valuemin="0" aria-valuemax="100">{{ paidPercentage }}%</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="fees.length > 0" class="d-flex justify-content-between align-items-center mt-4">
        <div>
          Showing {{ paginationInfo.currentPage * paginationInfo.itemsPerPage - paginationInfo.itemsPerPage + 1 }} to 
          {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }} of 
          {{ paginationInfo.totalItems }} fees
        </div>
        <nav aria-label="Fee pagination">
          <ul class="pagination mb-0">
            <li class="page-item" :class="{ disabled: paginationInfo.currentPage === 1 }">
              <button class="page-link" @click="goToPage(paginationInfo.currentPage - 1)" :disabled="paginationInfo.currentPage === 1">
                Previous
              </button>
            </li>
            <li v-for="page in paginationInfo.totalPages" :key="page" class="page-item" :class="{ active: page === paginationInfo.currentPage }">
              <button class="page-link" @click="goToPage(page)">{{ page }}</button>
            </li>
            <li class="page-item" :class="{ disabled: paginationInfo.currentPage === paginationInfo.totalPages }">
              <button class="page-link" @click="goToPage(paginationInfo.currentPage + 1)" :disabled="paginationInfo.currentPage === paginationInfo.totalPages">
                Next
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- Add Fee Modal -->
    <div class="modal fade" id="addFeeModal" tabindex="-1" aria-labelledby="addFeeModalLabel" aria-hidden="true" ref="addFeeModalRef">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addFeeModalLabel">Add New Fee</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeAddFeeModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="feeApplication" class="form-label">Application</label>
              <select class="form-select" id="feeApplication" v-model="newFee.application" required>
                <option value="">Select Application</option>
                <option v-for="app in applications" :key="app.id" :value="app.id">
                  {{ app.reference_number }}
                </option>
              </select>
              <div class="invalid-feedback" v-if="feeErrors.application">{{ feeErrors.application }}</div>
            </div>
            <div class="mb-3">
              <label for="feeType" class="form-label">Fee Type</label>
              <select class="form-select" id="feeType" v-model="newFee.fee_type" required>
                <option value="">Select Fee Type</option>
                <option value="application">Application</option>
                <option value="valuation">Valuation</option>
                <option value="legal">Legal</option>
                <option value="broker">Broker</option>
                <option value="settlement">Settlement</option>
                <option value="other">Other</option>
              </select>
              <div class="invalid-feedback" v-if="feeErrors.fee_type">{{ feeErrors.fee_type }}</div>
            </div>
            <div class="mb-3">
              <label for="feeAmount" class="form-label">Amount</label>
              <div class="input-group">
                <span class="input-group-text">$</span>
                <input type="number" class="form-control" id="feeAmount" v-model.number="newFee.amount" step="0.01" min="0" required>
              </div>
              <div class="invalid-feedback" v-if="feeErrors.amount">{{ feeErrors.amount }}</div>
            </div>
            <div class="mb-3">
              <label for="feeDueDate" class="form-label">Due Date</label>
              <input type="date" class="form-control" id="feeDueDate" v-model="newFee.due_date" required>
              <div class="invalid-feedback" v-if="feeErrors.due_date">{{ feeErrors.due_date }}</div>
            </div>
            <div class="mb-3">
              <label for="feeDescription" class="form-label">Description (Optional)</label>
              <textarea class="form-control" id="feeDescription" v-model="newFee.description" rows="3"></textarea>
            </div>
            <div class="alert alert-danger" v-if="feeErrors.general">{{ feeErrors.general }}</div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeAddFeeModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="submitFee" :disabled="submittingFee">
              <span v-if="submittingFee" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Save Fee
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Mark as Paid Modal -->
    <div class="modal fade" id="markAsPaidModal" tabindex="-1" aria-labelledby="markAsPaidModalLabel" aria-hidden="true" ref="markAsPaidModalRef">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="markAsPaidModalLabel">Mark Fee as Paid</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeMarkAsPaidModal"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to mark this fee as paid?</p>
            <div class="mb-3">
              <label for="paidDate" class="form-label">Payment Date</label>
              <input type="date" class="form-control" id="paidDate" v-model="paymentDate" required>
              <div class="invalid-feedback" v-if="markAsPaidError">{{ markAsPaidError }}</div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeMarkAsPaidModal">Cancel</button>
            <button type="button" class="btn btn-success" @click="confirmMarkAsPaid" :disabled="markingAsPaid">
              <span v-if="markingAsPaid" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Confirm Payment
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useFeeStore } from '@/store/fee'
import { useApplicationStore } from '@/store/application'
import feeService from '@/services/fee.service'
import { Modal } from 'bootstrap'

export default {
  name: 'FeesView',
  setup() {
    const feeStore = useFeeStore()
    const applicationStore = useApplicationStore()
    
    // State
    const filters = ref({
      application: '',
      fee_type: '',
      is_paid: '',
      date_from: '',
      date_to: ''
    })
    
    // Modal references
    const addFeeModalRef = ref(null)
    const markAsPaidModalRef = ref(null)
    let addFeeModal = null
    let markAsPaidModal = null
    
    // New fee form
    const newFee = ref({
      application: '',
      fee_type: '',
      amount: null,
      due_date: new Date().toISOString().split('T')[0],
      description: ''
    })
    const feeErrors = ref({
      application: '',
      fee_type: '',
      amount: '',
      due_date: '',
      general: ''
    })
    const submittingFee = ref(false)
    
    // Mark as paid form
    const selectedFee = ref(null)
    const paymentDate = ref(new Date().toISOString().split('T')[0])
    const markAsPaidError = ref('')
    const markingAsPaid = ref(false)
    
    // Computed properties
    const fees = computed(() => feeStore.fees)
    const applications = computed(() => applicationStore.applications)
    const loading = computed(() => feeStore.loading)
    const error = computed(() => feeStore.error)
    const paginationInfo = computed(() => feeStore.getPaginationInfo)
    const hasFilters = computed(() => {
      return filters.value.application || filters.value.fee_type || 
             filters.value.is_paid || filters.value.date_from || filters.value.date_to
    })
    
    const totalFees = computed(() => {
      return fees.value.reduce((total, fee) => total + parseFloat(fee.amount), 0)
    })
    
    const paidFees = computed(() => {
      return fees.value.filter(fee => fee.is_paid).reduce((total, fee) => total + parseFloat(fee.amount), 0)
    })
    
    const pendingFees = computed(() => {
      return fees.value.filter(fee => !fee.is_paid).reduce((total, fee) => total + parseFloat(fee.amount), 0)
    })
    
    const paidPercentage = computed(() => {
      return totalFees.value > 0 ? Math.round((paidFees.value / totalFees.value) * 100) : 0
    })
    
    // Methods
    const fetchFees = async () => {
      try {
        await feeStore.fetchFees()
      } catch (error) {
        console.error('Error fetching fees:', error)
      }
    }
    
    const fetchApplications = async () => {
      try {
        await applicationStore.fetchApplications()
      } catch (error) {
        console.error('Error fetching applications:', error)
      }
    }
    
    const applyFilters = () => {
      feeStore.setFilters({
        application: filters.value.application,
        fee_type: filters.value.fee_type,
        is_paid: filters.value.is_paid === '' ? null : filters.value.is_paid === 'true',
        date_from: filters.value.date_from,
        date_to: filters.value.date_to
      })
    }
    
    const clearFilters = () => {
      filters.value = {
        application: '',
        fee_type: '',
        is_paid: '',
        date_from: '',
        date_to: ''
      }
      feeStore.clearFilters()
    }
    
    const goToPage = (page) => {
      if (page < 1 || page > paginationInfo.value.totalPages) return
      feeStore.setPage(page)
    }
    
    const formatCurrency = (value) => {
      return value ? parseFloat(value).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : '0.00'
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
    }
    
    const getApplicationReference = (applicationId) => {
      if (!applicationId) return 'N/A'
      const app = applications.value.find(app => app.id === applicationId)
      return app ? app.reference_number : `App #${applicationId}`
    }
    
    // Initialize modals
    const initModals = () => {
      if (addFeeModalRef.value) {
        addFeeModal = new Modal(addFeeModalRef.value)
      }
      if (markAsPaidModalRef.value) {
        markAsPaidModal = new Modal(markAsPaidModalRef.value)
      }
    }
    
    // Add fee modal
    const showAddFeeModal = () => {
      // Reset form
      newFee.value = {
        application: '',
        fee_type: '',
        amount: null,
        due_date: new Date().toISOString().split('T')[0],
        description: ''
      }
      feeErrors.value = {
        application: '',
        fee_type: '',
        amount: '',
        due_date: '',
        general: ''
      }
      
      // Show modal
      if (addFeeModal) {
        addFeeModal.show()
      }
    }
    
    const closeAddFeeModal = () => {
      if (addFeeModal) {
        addFeeModal.hide()
      }
    }
    
    const validateFeeForm = () => {
      let isValid = true
      feeErrors.value = {
        application: '',
        fee_type: '',
        amount: '',
        due_date: '',
        general: ''
      }
      
      if (!newFee.value.application) {
        feeErrors.value.application = 'Application is required'
        isValid = false
      }
      
      if (!newFee.value.fee_type) {
        feeErrors.value.fee_type = 'Fee type is required'
        isValid = false
      }
      
      if (!newFee.value.amount || newFee.value.amount <= 0) {
        feeErrors.value.amount = 'Amount must be greater than 0'
        isValid = false
      }
      
      if (!newFee.value.due_date) {
        feeErrors.value.due_date = 'Due date is required'
        isValid = false
      }
      
      return isValid
    }
    
    const submitFee = async () => {
      if (!validateFeeForm()) {
        return
      }
      
      submittingFee.value = true
      
      try {
        await feeStore.createFee(newFee.value)
        closeAddFeeModal()
        fetchFees()
      } catch (error) {
        feeErrors.value.general = error.message || 'Failed to create fee'
        console.error('Error creating fee:', error)
      } finally {
        submittingFee.value = false
      }
    }
    
    // View fee
    const viewFee = (fee) => {
      // In a real implementation, this would navigate to fee detail page
      console.log('View fee:', fee.id)
    }
    
    // Edit fee
    const editFee = (fee) => {
      // In a real implementation, this would open a modal to edit the fee
      console.log('Edit fee:', fee.id)
    }
    
    // Mark as paid modal
    const markAsPaid = (fee) => {
      selectedFee.value = fee
      paymentDate.value = new Date().toISOString().split('T')[0]
      markAsPaidError.value = ''
      
      if (markAsPaidModal) {
        markAsPaidModal.show()
      }
    }
    
    const closeMarkAsPaidModal = () => {
      if (markAsPaidModal) {
        markAsPaidModal.hide()
      }
    }
    
    const confirmMarkAsPaid = async () => {
      if (!paymentDate.value) {
        markAsPaidError.value = 'Payment date is required'
        return
      }
      
      markingAsPaid.value = true
      
      try {
        await feeStore.markFeePaid(selectedFee.value.id, { paid_date: paymentDate.value })
        closeMarkAsPaidModal()
        fetchFees()
      } catch (error) {
        markAsPaidError.value = error.message || 'Failed to mark fee as paid'
        console.error('Error marking fee as paid:', error)
      } finally {
        markingAsPaid.value = false
      }
    }
    
    // Fetch fees and applications on component mount
    onMounted(() => {
      fetchFees()
      fetchApplications()
      
      // Initialize modals after DOM is ready
      setTimeout(() => {
        initModals()
      }, 100)
    })
    
    return {
      fees,
      applications,
      loading,
      error,
      filters,
      paginationInfo,
      hasFilters,
      totalFees,
      paidFees,
      pendingFees,
      paidPercentage,
      fetchFees,
      applyFilters,
      clearFilters,
      goToPage,
      formatCurrency,
      formatDate,
      getApplicationReference,
      
      // Add fee modal
      addFeeModalRef,
      newFee,
      feeErrors,
      submittingFee,
      showAddFeeModal,
      closeAddFeeModal,
      submitFee,
      
      // View and edit fee
      viewFee,
      editFee,
      
      // Mark as paid modal
      markAsPaidModalRef,
      selectedFee,
      paymentDate,
      markAsPaidError,
      markingAsPaid,
      markAsPaid,
      closeMarkAsPaidModal,
      confirmMarkAsPaid
    }
  }
}
</script>

<style scoped>
.fees-view {
  min-height: 100vh;
}

.invalid-feedback {
  display: block;
}
</style>
