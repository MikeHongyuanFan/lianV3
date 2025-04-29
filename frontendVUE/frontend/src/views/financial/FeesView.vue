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
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useFeeStore } from '@/store/fee'
import { useApplicationStore } from '@/store/application'
import feeService from '@/services/fee.service'

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
      return fees.value.reduce((total, fee) => total + fee.amount, 0)
    })
    
    const paidFees = computed(() => {
      return fees.value.filter(fee => fee.is_paid).reduce((total, fee) => total + fee.amount, 0)
    })
    
    const pendingFees = computed(() => {
      return fees.value.filter(fee => !fee.is_paid).reduce((total, fee) => total + fee.amount, 0)
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
        is_paid: filters.value.is_paid,
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
    
    const showAddFeeModal = () => {
      // In a real implementation, this would open a modal to add a new fee
      console.log('Show add fee modal')
    }
    
    const viewFee = (fee) => {
      // In a real implementation, this would show fee details
      console.log('View fee:', fee.id)
    }
    
    const editFee = (fee) => {
      // In a real implementation, this would open a modal to edit the fee
      console.log('Edit fee:', fee.id)
    }
    
    const markAsPaid = async (fee) => {
      try {
        await feeService.markFeePaid(fee.id)
        // Refresh fees after marking as paid
        fetchFees()
      } catch (error) {
        console.error('Error marking fee as paid:', error)
      }
    }
    
    // Fetch fees and applications on component mount
    onMounted(() => {
      fetchFees()
      fetchApplications()
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
      showAddFeeModal,
      viewFee,
      editFee,
      markAsPaid
    }
  }
}
</script>

<style scoped>
.fees-view {
  min-height: 100vh;
}
</style>
