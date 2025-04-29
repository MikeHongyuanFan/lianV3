<template>
  <div class="bdm-detail-view">
    <div class="container-fluid py-4">
      <!-- Loading state -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading BDM details...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchBDMDetails">
          Try Again
        </button>
      </div>

      <!-- BDM details -->
      <div v-else-if="bdm" class="bdm-details">
        <!-- Header section -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <div>
            <h1 class="h3">{{ bdm.first_name }} {{ bdm.last_name }}</h1>
            <p class="text-muted mb-0">Business Development Manager</p>
          </div>
          <div class="bdm-actions">
            <button class="btn btn-outline-primary me-2" @click="editBDM">
              <i class="bi bi-pencil me-1"></i> Edit
            </button>
            <button class="btn btn-outline-danger" @click="confirmDelete">
              <i class="bi bi-trash me-1"></i> Delete
            </button>
          </div>
        </div>

        <!-- Main content -->
        <div class="row">
          <!-- Left column - BDM information -->
          <div class="col-lg-8">
            <div class="card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">BDM Information</h5>
              </div>
              <div class="card-body">
                <div class="row">
                  <div class="col-md-6">
                    <h6>Contact Information</h6>
                    <ul class="list-unstyled">
                      <li class="mb-2">
                        <i class="bi bi-envelope me-2"></i>
                        <a :href="`mailto:${bdm.email}`">{{ bdm.email }}</a>
                      </li>
                      <li class="mb-2">
                        <i class="bi bi-telephone me-2"></i>
                        <a :href="`tel:${bdm.phone}`">{{ bdm.phone }}</a>
                      </li>
                    </ul>

                    <h6 class="mt-4">Professional Details</h6>
                    <ul class="list-unstyled">
                      <li class="mb-2">
                        <i class="bi bi-person-badge me-2"></i>
                        Employee ID: {{ bdm.employee_id }}
                      </li>
                      <li class="mb-2">
                        <i class="bi bi-house-door me-2"></i>
                        Branch: 
                        <router-link 
                          v-if="bdm.branch" 
                          :to="{ name: 'BranchDetail', params: { id: bdm.branch.id }}"
                        >
                          {{ bdm.branch.name }}
                        </router-link>
                        <span v-else>N/A</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <!-- Applications section -->
            <div class="card mb-4">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">Applications</h5>
                <router-link 
                  :to="{ name: 'ApplicationList', query: { bdm: bdm.id }}" 
                  class="btn btn-sm btn-outline-primary"
                >
                  View All
                </router-link>
              </div>
              <div class="card-body">
                <div v-if="loadingApplications" class="text-center py-3">
                  <div class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <p class="mt-2">Loading applications...</p>
                </div>
                <div v-else-if="applications.length === 0" class="text-center py-3">
                  <p class="text-muted mb-0">No applications found for this BDM</p>
                </div>
                <div v-else class="table-responsive">
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th>Reference</th>
                        <th>Type</th>
                        <th>Amount</th>
                        <th>Stage</th>
                        <th>Created</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="app in applications.slice(0, 5)" :key="app.id">
                        <td>{{ app.reference_number }}</td>
                        <td>{{ app.application_type }}</td>
                        <td>${{ formatCurrency(app.loan_amount) }}</td>
                        <td>
                          <span class="badge" :class="getStageClass(app.stage)">
                            {{ app.stage_display }}
                          </span>
                        </td>
                        <td>{{ formatDate(app.created_at) }}</td>
                        <td>
                          <router-link 
                            :to="{ name: 'ApplicationDetail', params: { id: app.id }}" 
                            class="btn btn-sm btn-outline-primary"
                          >
                            View
                          </router-link>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <!-- Right column - Stats and metrics -->
          <div class="col-lg-4">
            <!-- Stats card -->
            <div class="card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">Performance Statistics</h5>
              </div>
              <div class="card-body">
                <div class="stat-item mb-3">
                  <div class="d-flex justify-content-between">
                    <span>Total Applications</span>
                    <span class="fw-bold">{{ applications.length }}</span>
                  </div>
                  <div class="progress mt-1">
                    <div 
                      class="progress-bar bg-primary" 
                      role="progressbar" 
                      :style="`width: 100%`" 
                      aria-valuenow="100" 
                      aria-valuemin="0" 
                      aria-valuemax="100"
                    ></div>
                  </div>
                </div>

                <div class="stat-item mb-3">
                  <div class="d-flex justify-content-between">
                    <span>Total Loan Amount</span>
                    <span class="fw-bold">${{ formatCurrency(totalLoanAmount) }}</span>
                  </div>
                </div>

                <h6 class="mt-4">Applications by Stage</h6>
                <div v-if="applicationsByStage" class="mt-3">
                  <div v-for="(count, stage) in applicationsByStage" :key="stage" class="stat-item mb-2">
                    <div class="d-flex justify-content-between">
                      <span>{{ formatStage(stage) }}</span>
                      <span class="fw-bold">{{ count }}</span>
                    </div>
                    <div class="progress mt-1">
                      <div 
                        class="progress-bar" 
                        :class="getStageClass(stage)"
                        role="progressbar" 
                        :style="`width: ${(count / applications.length) * 100}%`" 
                        :aria-valuenow="(count / applications.length) * 100" 
                        aria-valuemin="0" 
                        aria-valuemax="100"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Quick actions card -->
            <div class="card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">Quick Actions</h5>
              </div>
              <div class="card-body">
                <div class="d-grid gap-2">
                  <router-link 
                    :to="{ name: 'ApplicationList', query: { bdm: bdm.id }}" 
                    class="btn btn-outline-primary"
                  >
                    <i class="bi bi-file-earmark-text me-2"></i> View All Applications
                  </router-link>
                  <router-link 
                    :to="{ name: 'ApplicationCreate', query: { bdm: bdm.id }}" 
                    class="btn btn-outline-success"
                  >
                    <i class="bi bi-plus-circle me-2"></i> Create New Application
                  </router-link>
                  <router-link 
                    v-if="bdm.branch"
                    :to="{ name: 'BranchDetail', params: { id: bdm.branch.id }}" 
                    class="btn btn-outline-secondary"
                  >
                    <i class="bi bi-building me-2"></i> View Branch
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Not found state -->
      <div v-else class="text-center py-5">
        <i class="bi bi-question-circle display-1 text-muted"></i>
        <h3 class="mt-3">BDM Not Found</h3>
        <p class="text-muted">The BDM you're looking for doesn't exist or you don't have permission to view it.</p>
        <router-link :to="{ name: 'BDMList' }" class="btn btn-primary mt-3">
          Back to BDM List
        </router-link>
      </div>
    </div>

    <!-- Edit BDM Modal -->
    <div class="modal fade" id="editBDMModal" tabindex="-1" aria-labelledby="editBDMModalLabel" aria-hidden="true" ref="editModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editBDMModalLabel">Edit BDM</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <bdm-form
              :bdm="bdm"
              :loading="formLoading"
              @submit="handleFormSubmit"
              @cancel="hideModal"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true" ref="deleteModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="deleteModalLabel">Confirm Delete</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to delete BDM {{ bdm?.first_name }} {{ bdm?.last_name }}?
            This action cannot be undone.
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteBDM" :disabled="formLoading">
              <span v-if="formLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Modal } from 'bootstrap'
import { useBrokerStore } from '@/store/broker'
import BDMForm from '@/components/broker/BDMForm.vue'

export default {
  name: 'BDMDetailView',
  components: {
    BDMForm
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const brokerStore = useBrokerStore()
    
    // Refs for modals
    const editModal = ref(null)
    const deleteModal = ref(null)
    let bsEditModal = null
    let bsDeleteModal = null
    
    // State
    const loading = ref(false)
    const loadingApplications = ref(false)
    const formLoading = ref(false)
    const error = ref(null)
    const applications = ref([])
    
    // Computed properties
    const bdm = computed(() => brokerStore.currentBDM)
    
    const totalLoanAmount = computed(() => {
      return applications.value.reduce((total, app) => {
        return total + (app.loan_amount || 0)
      }, 0)
    })
    
    const applicationsByStage = computed(() => {
      const stages = {}
      applications.value.forEach(app => {
        if (!stages[app.stage]) {
          stages[app.stage] = 0
        }
        stages[app.stage]++
      })
      return stages
    })
    
    // Initialize modals on component mount
    onMounted(() => {
      bsEditModal = new Modal(editModal.value)
      bsDeleteModal = new Modal(deleteModal.value)
      
      // Fetch BDM details
      fetchBDMDetails()
    })
    
    // Methods
    const fetchBDMDetails = async () => {
      const bdmId = route.params.id
      if (!bdmId) return
      
      loading.value = true
      error.value = null
      
      try {
        await brokerStore.fetchBDMById(bdmId)
        fetchBDMApplications(bdmId)
      } catch (err) {
        error.value = err.message || 'Failed to fetch BDM details'
      } finally {
        loading.value = false
      }
    }
    
    const fetchBDMApplications = async (bdmId) => {
      loadingApplications.value = true
      
      try {
        applications.value = await brokerStore.fetchBDMApplications(bdmId) || []
      } catch (err) {
        console.error('Failed to fetch BDM applications:', err)
        applications.value = []
      } finally {
        loadingApplications.value = false
      }
    }
    
    const editBDM = () => {
      bsEditModal.show()
    }
    
    const hideModal = () => {
      bsEditModal.hide()
    }
    
    const handleFormSubmit = async (bdmData) => {
      if (!bdm.value) return
      
      formLoading.value = true
      
      try {
        await brokerStore.updateBDM(bdm.value.id, bdmData)
        bsEditModal.hide()
        // Refresh BDM details
        await brokerStore.fetchBDMById(bdm.value.id)
      } catch (err) {
        console.error('Failed to update BDM:', err)
      } finally {
        formLoading.value = false
      }
    }
    
    const confirmDelete = () => {
      bsDeleteModal.show()
    }
    
    const deleteBDM = async () => {
      if (!bdm.value) return
      
      formLoading.value = true
      
      try {
        await brokerStore.deleteBDM(bdm.value.id)
        bsDeleteModal.hide()
        router.push({ name: 'BDMList' })
      } catch (err) {
        console.error('Failed to delete BDM:', err)
      } finally {
        formLoading.value = false
      }
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
    
    const formatStage = (stage) => {
      const stageNames = {
        'inquiry': 'Inquiry',
        'pre_approval': 'Pre-Approval',
        'valuation': 'Valuation',
        'formal_approval': 'Formal Approval',
        'settlement': 'Settlement',
        'funded': 'Funded',
        'declined': 'Declined',
        'withdrawn': 'Withdrawn'
      }
      
      return stageNames[stage] || stage
    }
    
    return {
      bdm,
      loading,
      loadingApplications,
      formLoading,
      error,
      applications,
      totalLoanAmount,
      applicationsByStage,
      editModal,
      deleteModal,
      fetchBDMDetails,
      editBDM,
      hideModal,
      handleFormSubmit,
      confirmDelete,
      deleteBDM,
      formatCurrency,
      formatDate,
      getStageClass,
      formatStage
    }
  }
}
</script>

<style scoped>
.bdm-detail-view {
  min-height: 100vh;
}

.stat-item {
  margin-bottom: 1rem;
}

.progress {
  height: 0.5rem;
}
</style>
