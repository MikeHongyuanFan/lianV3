<template>
  <div class="applications-view">
    <div class="container-fluid py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Applications</h1>
        <router-link to="/applications/create" class="btn btn-primary">
          <i class="bi bi-plus-circle me-2"></i> New Application
        </router-link>
      </div>

      <!-- Search and filters -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-4">
              <div class="input-group">
                <span class="input-group-text">
                  <i class="bi bi-search"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Search by reference or purpose"
                  v-model="filters.search"
                  @input="handleSearchInput"
                />
                <button
                  class="btn btn-outline-secondary"
                  type="button"
                  @click="clearSearch"
                  v-if="filters.search"
                >
                  <i class="bi bi-x"></i>
                </button>
              </div>
            </div>
            <div class="col-md-2">
              <select class="form-select" v-model="filters.stage" @change="applyFilters">
                <option value="">All Stages</option>
                <option value="inquiry">Inquiry</option>
                <option value="pre_approval">Pre-Approval</option>
                <option value="valuation">Valuation</option>
                <option value="formal_approval">Formal Approval</option>
                <option value="settlement">Settlement</option>
                <option value="funded">Funded</option>
                <option value="declined">Declined</option>
                <option value="withdrawn">Withdrawn</option>
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
        <p class="mt-2">Loading applications...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchApplications">
          Try Again
        </button>
      </div>

      <!-- Empty state -->
      <div v-else-if="applications && applications.length === 0" class="text-center py-5">
        <i class="bi bi-file-earmark-text display-1 text-muted"></i>
        <h3 class="mt-3">No applications found</h3>
        <p class="text-muted">
          {{ hasFilters ? 'Try adjusting your filters' : 'Create your first application to get started' }}
        </p>
        <router-link to="/applications/create" class="btn btn-primary mt-3" v-if="!hasFilters">
          <i class="bi bi-plus-circle me-2"></i> Create Application
        </router-link>
      </div>

      <!-- Applications list -->
      <div v-else class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Reference</th>
                      <th>Type</th>
                      <th>Purpose</th>
                      <th>Amount</th>
                      <th>Stage</th>
                      <th>Created</th>
                      <th>Borrowers</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="app in applications" :key="app.id">
                      <td>{{ app.reference_number }}</td>
                      <td>{{ app.application_type }}</td>
                      <td>{{ app.purpose }}</td>
                      <td>${{ formatCurrency(app.loan_amount) }}</td>
                      <td>
                        <span class="badge" :class="getStageClass(app.stage)">
                          {{ app.stage_display || app.stage }}
                        </span>
                      </td>
                      <td>{{ formatDate(app.created_at) }}</td>
                      <td>{{ app.borrower_count || 0 }}</td>
                      <td>
                        <div class="btn-group">
                          <router-link :to="`/applications/${app.id}`" class="btn btn-sm btn-outline-primary">
                            <i class="bi bi-eye"></i>
                          </router-link>
                          <router-link :to="`/applications/${app.id}/edit`" class="btn btn-sm btn-outline-secondary">
                            <i class="bi bi-pencil"></i>
                          </router-link>
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

      <!-- Pagination -->
      <div v-if="applications.length > 0" class="d-flex justify-content-between align-items-center mt-4">
        <div>
          Showing {{ paginationInfo.currentPage * paginationInfo.itemsPerPage - paginationInfo.itemsPerPage + 1 }} to 
          {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }} of 
          {{ paginationInfo.totalItems }} applications
        </div>
        <nav aria-label="Application pagination">
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
import { useApplicationStore } from '@/store/application'

export default {
  name: 'ApplicationsView',
  setup() {
    const applicationStore = useApplicationStore()
    
    // State
    const filters = ref({
      search: '',
      stage: '',
      date_from: '',
      date_to: ''
    })
    
    // Computed properties
    const applications = computed(() => applicationStore.applications || [])
    const loading = computed(() => applicationStore.loading)
    const error = computed(() => applicationStore.error)
    const paginationInfo = computed(() => applicationStore.getPaginationInfo)
    const hasFilters = computed(() => {
      return filters.value.search || filters.value.stage || filters.value.date_from || filters.value.date_to
    })
    
    // Methods
    const fetchApplications = async () => {
      try {
        await applicationStore.fetchApplications()
      } catch (error) {
        console.error('Error fetching applications:', error)
      }
    }
    
    const handleSearchInput = () => {
      applicationStore.setFilters({ search: filters.value.search })
    }
    
    const applyFilters = () => {
      applicationStore.setFilters({
        stage: filters.value.stage,
        date_from: filters.value.date_from,
        date_to: filters.value.date_to
      })
    }
    
    const clearSearch = () => {
      filters.value.search = ''
      applicationStore.setFilters({ search: '' })
    }
    
    const clearFilters = () => {
      filters.value = {
        search: '',
        stage: '',
        date_from: '',
        date_to: ''
      }
      applicationStore.clearFilters()
    }
    
    const goToPage = (page) => {
      if (page < 1 || page > paginationInfo.value.totalPages) return
      applicationStore.setPage(page)
    }
    
    const formatCurrency = (value) => {
      return value ? value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : '0.00'
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
    }
    
    const getStageClass = (stage) => {
      const stageClasses = {
        'inquiry': 'bg-secondary',
        'pre_approval': 'bg-info',
        'valuation': 'bg-primary',
        'formal_approval': 'bg-warning',
        'settlement': 'bg-success',
        'funded': 'bg-success',
        'declined': 'bg-danger',
        'withdrawn': 'bg-dark'
      }
      
      return stageClasses[stage] || 'bg-secondary'
    }
    
    // Fetch applications on component mount
    onMounted(() => {
      fetchApplications()
    })
    
    return {
      applications,
      loading,
      error,
      filters,
      paginationInfo,
      hasFilters,
      fetchApplications,
      handleSearchInput,
      applyFilters,
      clearSearch,
      clearFilters,
      goToPage,
      formatCurrency,
      formatDate,
      getStageClass
    }
  }
}
</script>

<style scoped>
.applications-view {
  min-height: 100vh;
}
</style>
