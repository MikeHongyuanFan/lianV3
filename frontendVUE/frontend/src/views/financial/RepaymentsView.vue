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
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRepaymentStore } from '@/store/repayment'
import { useApplicationStore } from '@/store/application'
import repaymentService from '@/services/repayment.service'

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
      return repayments.value.reduce((total, repayment) => total + repayment.amount, 0)
    })
    
    const paidAmount = computed(() => {
      return repayments.value.filter(repayment => repayment.is_paid).reduce((total, repayment) => total + repayment.amount, 0)
    })
    
    const paidCount = computed(() => {
      return repayments.value.filter(repayment => repayment.is_paid).length
    })
    
    const dueSoonAmount = computed(() => {
      return repayments.value.filter(repayment => repayment.status && repayment.status.includes('due_soon')).reduce((total, repayment) => total + repayment.amount, 0)
    })
    
    const dueSoonCount = computed(() => {
      return repayments.value.filter(repayment => repayment.status && repayment.status.includes('due_soon')).length
    })
    
    const overdueAmount = computed(() => {
      return repayments.value.filter(repayment => repayment.status && repayment.status.includes('overdue')).reduce((total, repayment) => total + repayment.amount, 0)
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
        is_paid: filters.value.is_paid,
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
      return value ? value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : '0.00'
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
    
    const showAddRepaymentModal = () => {
      // In a real implementation, this would open a modal to add a new repayment
      console.log('Show add repayment modal')
    }
    
    const viewRepayment = (repayment) => {
      // In a real implementation, this would show repayment details
      console.log('View repayment:', repayment.id)
    }
    
    const recordPayment = async (repayment) => {
      try {
        // In a real implementation, this would open a modal to record payment
        console.log('Record payment for repayment:', repayment.id)
      } catch (error) {
        console.error('Error recording payment:', error)
      }
    }
    
    // Fetch repayments and applications on component mount
    onMounted(() => {
      fetchRepayments()
      fetchApplications()
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
      showAddRepaymentModal,
      viewRepayment,
      recordPayment
    }
  }
}
</script>

<style scoped>
.repayments-view {
  min-height: 100vh;
}
</style>
