<template>
  <div class="repayments-view">
    <div class="container-fluid py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Repayments</h1>
        <button class="btn btn-primary" @click="showAddRepaymentModal">
          <i class="bi bi-plus-circle me-2"></i> Add Repayment
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
            <div class="col-md-2">
              <button class="btn btn-outline-secondary w-100" @click="clearFilters">
                Clear Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading repayments...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchRepayments">
          Try Again
        </button>
      </div>

      <!-- Empty state -->
      <div v-else-if="repayments.length === 0" class="text-center py-5">
        <i class="bi bi-calendar-check display-1 text-muted"></i>
        <h3 class="mt-3">No repayments found</h3>
        <p class="text-muted">
          {{ hasFilters ? 'Try adjusting your filters' : 'Add your first repayment to get started' }}
        </p>
        <button class="btn btn-primary mt-3" @click="showAddRepaymentModal" v-if="!hasFilters">
          <i class="bi bi-plus-circle me-2"></i> Add Repayment
        </button>
      </div>

      <!-- Repayments list -->
      <div v-else class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Application</th>
                      <th>Amount</th>
                      <th>Due Date</th>
                      <th>Status</th>
                      <th>Paid Date</th>
                      <th>Payment Method</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="repayment in repayments" :key="repayment.id">
                      <td>{{ getApplicationReference(repayment.application) }}</td>
                      <td>${{ formatCurrency(repayment.amount) }}</td>
                      <td>{{ formatDate(repayment.due_date) }}</td>
                      <td>
                        <span class="badge" :class="getStatusClass(repayment.status)">
                          {{ formatStatus(repayment.status) }}
                        </span>
                      </td>
                      <td>{{ repayment.is_paid ? formatDate(repayment.paid_date) : 'N/A' }}</td>
                      <td>{{ repayment.payment_method || 'N/A' }}</td>
                      <td>
                        <div class="btn-group">
                          <button class="btn btn-sm btn-outline-primary" @click="viewRepayment(repayment)">
                            <i class="bi bi-eye"></i>
                          </button>
                          <button class="btn btn-sm btn-outline-success" v-if="!repayment.is_paid" @click="recordPayment(repayment)">
                            <i class="bi bi-check-circle"></i> Record Payment
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

      <!-- Summary cards -->
      <div v-if="repayments.length > 0" class="row mt-4">
        <div class="col-md-3">
          <div class="card bg-light">
            <div class="card-body text-center">
              <h5 class="card-title">Total Repayments</h5>
              <h2 class="display-6">${{ formatCurrency(totalAmount) }}</h2>
              <p class="text-muted mb-0">{{ repayments.length }} repayments</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-success text-white">
            <div class="card-body text-center">
              <h5 class="card-title">Paid</h5>
              <h2 class="display-6">${{ formatCurrency(paidAmount) }}</h2>
              <p class="mb-0">{{ paidCount }} repayments</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-warning text-dark">
            <div class="card-body text-center">
              <h5 class="card-title">Due Soon</h5>
              <h2 class="display-6">${{ formatCurrency(dueSoonAmount) }}</h2>
              <p class="mb-0">{{ dueSoonCount }} repayments</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-danger text-white">
            <div class="card-body text-center">
              <h5 class="card-title">Overdue</h5>
              <h2 class="display-6">${{ formatCurrency(overdueAmount) }}</h2>
              <p class="mb-0">{{ overdueCount }} repayments</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="repayments.length > 0" class="d-flex justify-content-between align-items-center mt-4">
        <div>
          Showing {{ paginationInfo.currentPage * paginationInfo.itemsPerPage - paginationInfo.itemsPerPage + 1 }} to 
          {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }} of 
          {{ paginationInfo.totalItems }} repayments
        </div>
        <nav aria-label="Repayment pagination">
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

    <!-- Add Repayment Modal -->
    <div class="modal fade" id="addRepaymentModal" tabindex="-1" aria-labelledby="addRepaymentModalLabel" aria-hidden="true" ref="addRepaymentModalRef">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addRepaymentModalLabel">Add New Repayment</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeAddRepaymentModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="repaymentApplication" class="form-label">Application</label>
              <select class="form-select" id="repaymentApplication" v-model="newRepayment.application" required>
                <option value="">Select Application</option>
                <option v-for="app in applications" :key="app.id" :value="app.id">
                  {{ app.reference_number }}
                </option>
              </select>
              <div class="invalid-feedback" v-if="repaymentErrors.application">{{ repaymentErrors.application }}</div>
            </div>
            <div class="mb-3">
              <label for="repaymentAmount" class="form-label">Amount</label>
              <div class="input-group">
                <span class="input-group-text">$</span>
                <input type="number" class="form-control" id="repaymentAmount" v-model.number="newRepayment.amount" step="0.01" min="0" required>
              </div>
              <div class="invalid-feedback" v-if="repaymentErrors.amount">{{ repaymentErrors.amount }}</div>
            </div>
            <div class="mb-3">
              <label for="repaymentDueDate" class="form-label">Due Date</label>
              <input type="date" class="form-control" id="repaymentDueDate" v-model="newRepayment.due_date" required>
              <div class="invalid-feedback" v-if="repaymentErrors.due_date">{{ repaymentErrors.due_date }}</div>
            </div>
            <div class="alert alert-danger" v-if="repaymentErrors.general">{{ repaymentErrors.general }}</div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeAddRepaymentModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="submitRepayment" :disabled="submittingRepayment">
              <span v-if="submittingRepayment" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Save Repayment
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Record Payment Modal -->
    <div class="modal fade" id="recordPaymentModal" tabindex="-1" aria-labelledby="recordPaymentModalLabel" aria-hidden="true" ref="recordPaymentModalRef">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="recordPaymentModalLabel">Record Payment</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeRecordPaymentModal"></button>
          </div>
          <div class="modal-body">
            <p>Record payment for repayment due on <strong>{{ selectedRepayment ? formatDate(selectedRepayment.due_date) : '' }}</strong> 
               for <strong>${{ selectedRepayment ? formatCurrency(selectedRepayment.amount) : '0.00' }}</strong>.</p>
            <div class="mb-3">
              <label for="paymentDate" class="form-label">Payment Date</label>
              <input type="date" class="form-control" id="paymentDate" v-model="paymentData.paid_date" required>
              <div class="invalid-feedback" v-if="recordPaymentErrors.paid_date">{{ recordPaymentErrors.paid_date }}</div>
            </div>
            <div class="mb-3">
              <label for="paymentMethod" class="form-label">Payment Method</label>
              <select class="form-select" id="paymentMethod" v-model="paymentData.payment_method" required>
                <option value="">Select Payment Method</option>
                <option value="bank_transfer">Bank Transfer</option>
                <option value="credit_card">Credit Card</option>
                <option value="debit_card">Debit Card</option>
                <option value="cash">Cash</option>
                <option value="check">Check</option>
                <option value="other">Other</option>
              </select>
              <div class="invalid-feedback" v-if="recordPaymentErrors.payment_method">{{ recordPaymentErrors.payment_method }}</div>
            </div>
            <div class="alert alert-danger" v-if="recordPaymentErrors.general">{{ recordPaymentErrors.general }}</div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeRecordPaymentModal">Cancel</button>
            <button type="button" class="btn btn-success" @click="confirmRecordPayment" :disabled="recordingPayment">
              <span v-if="recordingPayment" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
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
import { useRepaymentStore } from '@/store/repayment'
import { useApplicationStore } from '@/store/application'
import { Modal } from 'bootstrap'

export default {
  name: 'RepaymentsView',
  setup() {
    const repaymentStore = useRepaymentStore()
    const applicationStore = useApplicationStore()
    
    // State
    const filters = ref({
      application: '',
      is_paid: '',
      date_from: '',
      date_to: ''
    })
    
    // Modal references
    const addRepaymentModalRef = ref(null)
    const recordPaymentModalRef = ref(null)
    let addRepaymentModal = null
    let recordPaymentModal = null
    
    // New repayment form
    const newRepayment = ref({
      application: '',
      amount: null,
      due_date: new Date().toISOString().split('T')[0]
    })
    const repaymentErrors = ref({
      application: '',
      amount: '',
      due_date: '',
      general: ''
    })
    const submittingRepayment = ref(false)
    
    // Record payment form
    const selectedRepayment = ref(null)
    const paymentData = ref({
      paid_date: new Date().toISOString().split('T')[0],
      payment_method: ''
    })
    const recordPaymentErrors = ref({
      paid_date: '',
      payment_method: '',
      general: ''
    })
    const recordingPayment = ref(false)
    
    // Computed properties
    const repayments = computed(() => repaymentStore.repayments)
    const applications = computed(() => applicationStore.applications)
    const loading = computed(() => repaymentStore.loading)
    const error = computed(() => repaymentStore.error)
    const paginationInfo = computed(() => repaymentStore.getPaginationInfo)
    const hasFilters = computed(() => {
      return filters.value.application || filters.value.is_paid || 
             filters.value.date_from || filters.value.date_to
    })
    
    const totalAmount = computed(() => {
      return repayments.value.reduce((total, repayment) => total + parseFloat(repayment.amount), 0)
    })
    
    const paidAmount = computed(() => {
      return repayments.value.filter(repayment => repayment.is_paid).reduce((total, repayment) => total + parseFloat(repayment.amount), 0)
    })
    
    const paidCount = computed(() => {
      return repayments.value.filter(repayment => repayment.is_paid).length
    })
    
    const dueSoonAmount = computed(() => {
      return repayments.value.filter(repayment => repayment.status && repayment.status.includes('due_soon')).reduce((total, repayment) => total + parseFloat(repayment.amount), 0)
    })
    
    const dueSoonCount = computed(() => {
      return repayments.value.filter(repayment => repayment.status && repayment.status.includes('due_soon')).length
    })
    
    const overdueAmount = computed(() => {
      return repayments.value.filter(repayment => repayment.status && repayment.status.includes('overdue')).reduce((total, repayment) => total + parseFloat(repayment.amount), 0)
    })
    
    const overdueCount = computed(() => {
      return repayments.value.filter(repayment => repayment.status && repayment.status.includes('overdue')).length
    })
    
    // Methods
    const fetchRepayments = async () => {
      try {
        await repaymentStore.fetchRepayments()
      } catch (error) {
        console.error('Error fetching repayments:', error)
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
      repaymentStore.setFilters({
        application: filters.value.application,
        is_paid: filters.value.is_paid === '' ? null : filters.value.is_paid === 'true',
        date_from: filters.value.date_from,
        date_to: filters.value.date_to
      })
    }
    
    const clearFilters = () => {
      filters.value = {
        application: '',
        is_paid: '',
        date_from: '',
        date_to: ''
      }
      repaymentStore.clearFilters()
    }
    
    const goToPage = (page) => {
      if (page < 1 || page > paginationInfo.value.totalPages) return
      repaymentStore.setPage(page)
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
    
    const getStatusClass = (status) => {
      if (!status) return 'bg-secondary'
      
      if (status === 'paid') {
        return 'bg-success'
      } else if (status.includes('overdue')) {
        return 'bg-danger'
      } else if (status.includes('due_soon')) {
        return 'bg-warning'
      } else {
        return 'bg-info'
      }
    }
    
    const formatStatus = (status) => {
      if (!status) return 'Unknown'
      
      if (status === 'paid') {
        return 'Paid'
      } else if (status === 'scheduled') {
        return 'Scheduled'
      } else if (status.includes('overdue')) {
        const days = status.split('_').pop()
        return `Overdue (${days} days)`
      } else if (status.includes('due_soon')) {
        const days = status.split('_').pop()
        return `Due Soon (${days} days)`
      } else {
        return status
      }
    }
    
    // Initialize modals
    const initModals = () => {
      if (addRepaymentModalRef.value) {
        addRepaymentModal = new Modal(addRepaymentModalRef.value)
      }
      if (recordPaymentModalRef.value) {
        recordPaymentModal = new Modal(recordPaymentModalRef.value)
      }
    }
    
    // Add repayment modal
    const showAddRepaymentModal = () => {
      // Reset form
      newRepayment.value = {
        application: '',
        amount: null,
        due_date: new Date().toISOString().split('T')[0]
      }
      repaymentErrors.value = {
        application: '',
        amount: '',
        due_date: '',
        general: ''
      }
      
      // Show modal
      if (addRepaymentModal) {
        addRepaymentModal.show()
      }
    }
    
    const closeAddRepaymentModal = () => {
      if (addRepaymentModal) {
        addRepaymentModal.hide()
      }
    }
    
    const validateRepaymentForm = () => {
      let isValid = true
      repaymentErrors.value = {
        application: '',
        amount: '',
        due_date: '',
        general: ''
      }
      
      if (!newRepayment.value.application) {
        repaymentErrors.value.application = 'Application is required'
        isValid = false
      }
      
      if (!newRepayment.value.amount || newRepayment.value.amount <= 0) {
        repaymentErrors.value.amount = 'Amount must be greater than 0'
        isValid = false
      }
      
      if (!newRepayment.value.due_date) {
        repaymentErrors.value.due_date = 'Due date is required'
        isValid = false
      }
      
      return isValid
    }
    
    const submitRepayment = async () => {
      if (!validateRepaymentForm()) {
        return
      }
      
      submittingRepayment.value = true
      
      try {
        await repaymentStore.createRepayment(newRepayment.value)
        closeAddRepaymentModal()
        fetchRepayments()
      } catch (error) {
        repaymentErrors.value.general = error.message || 'Failed to create repayment'
        console.error('Error creating repayment:', error)
      } finally {
        submittingRepayment.value = false
      }
    }
    
    // View repayment
    const viewRepayment = (repayment) => {
      // In a real implementation, this would navigate to repayment detail page
      console.log('View repayment:', repayment.id)
    }
    
    // Record payment modal
    const recordPayment = (repayment) => {
      selectedRepayment.value = repayment
      paymentData.value = {
        paid_date: new Date().toISOString().split('T')[0],
        payment_method: ''
      }
      recordPaymentErrors.value = {
        paid_date: '',
        payment_method: '',
        general: ''
      }
      
      if (recordPaymentModal) {
        recordPaymentModal.show()
      }
    }
    
    const closeRecordPaymentModal = () => {
      if (recordPaymentModal) {
        recordPaymentModal.hide()
      }
    }
    
    const validateRecordPaymentForm = () => {
      let isValid = true
      recordPaymentErrors.value = {
        paid_date: '',
        payment_method: '',
        general: ''
      }
      
      if (!paymentData.value.paid_date) {
        recordPaymentErrors.value.paid_date = 'Payment date is required'
        isValid = false
      }
      
      if (!paymentData.value.payment_method) {
        recordPaymentErrors.value.payment_method = 'Payment method is required'
        isValid = false
      }
      
      return isValid
    }
    
    const confirmRecordPayment = async () => {
      if (!validateRecordPaymentForm()) {
        return
      }
      
      recordingPayment.value = true
      
      try {
        await repaymentStore.markRepaymentPaid(selectedRepayment.value.id, paymentData.value)
        closeRecordPaymentModal()
        fetchRepayments()
      } catch (error) {
        recordPaymentErrors.value.general = error.message || 'Failed to record payment'
        console.error('Error recording payment:', error)
      } finally {
        recordingPayment.value = false
      }
    }
    
    // Fetch repayments and applications on component mount
    onMounted(() => {
      fetchRepayments()
      fetchApplications()
      
      // Initialize modals after DOM is ready
      setTimeout(() => {
        initModals()
      }, 100)
    })
    
    return {
      repayments,
      applications,
      loading,
      error,
      filters,
      paginationInfo,
      hasFilters,
      totalAmount,
      paidAmount,
      paidCount,
      dueSoonAmount,
      dueSoonCount,
      overdueAmount,
      overdueCount,
      fetchRepayments,
      applyFilters,
      clearFilters,
      goToPage,
      formatCurrency,
      formatDate,
      getApplicationReference,
      getStatusClass,
      formatStatus,
      
      // Add repayment modal
      addRepaymentModalRef,
      newRepayment,
      repaymentErrors,
      submittingRepayment,
      showAddRepaymentModal,
      closeAddRepaymentModal,
      submitRepayment,
      
      // View repayment
      viewRepayment,
      
      // Record payment modal
      recordPaymentModalRef,
      selectedRepayment,
      paymentData,
      recordPaymentErrors,
      recordingPayment,
      recordPayment,
      closeRecordPaymentModal,
      confirmRecordPayment
    }
  }
}
</script>

<style scoped>
.repayments-view {
  min-height: 100vh;
}

.invalid-feedback {
  display: block;
}
</style>
