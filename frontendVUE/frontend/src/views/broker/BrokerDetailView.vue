<template>
  <div class="broker-detail-view">
    <div class="container-fluid py-4">
      <!-- Loading state -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading broker details...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchBrokerDetails">
          Try Again
        </button>
      </div>

      <!-- Broker details -->
      <div v-else-if="broker" class="broker-details">
        <!-- Header section -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <div>
            <h1 class="h3">{{ broker.name }}</h1>
            <p class="text-muted mb-0">{{ broker.company || 'Independent Broker' }}</p>
          </div>
          <div class="broker-actions">
            <button class="btn btn-outline-primary me-2" @click="editBroker">
              <i class="bi bi-pencil me-1"></i> Edit
            </button>
            <button class="btn btn-outline-danger" @click="confirmDelete">
              <i class="bi bi-trash me-1"></i> Delete
            </button>
          </div>
        </div>

        <!-- Main content -->
        <div class="row">
          <!-- Left column - Broker information -->
          <div class="col-lg-8">
            <div class="card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">Broker Information</h5>
              </div>
              <div class="card-body">
                <div class="row">
                  <div class="col-md-6">
                    <h6>Contact Information</h6>
                    <ul class="list-unstyled">
                      <li class="mb-2">
                        <i class="bi bi-envelope me-2"></i>
                        <a :href="`mailto:${broker.email}`">{{ broker.email }}</a>
                      </li>
                      <li class="mb-2">
                        <i class="bi bi-telephone me-2"></i>
                        <a :href="`tel:${broker.phone}`">{{ broker.phone }}</a>
                      </li>
                      <li class="mb-2">
                        <i class="bi bi-geo-alt me-2"></i>
                        {{ broker.address || 'No address provided' }}
                      </li>
                    </ul>

                    <h6 class="mt-4">Professional Details</h6>
                    <ul class="list-unstyled">
                      <li class="mb-2">
                        <i class="bi bi-building me-2"></i>
                        Company: {{ broker.company || 'N/A' }}
                      </li>
                      <li class="mb-2">
                        <i class="bi bi-house-door me-2"></i>
                        Branch: 
                        <router-link 
                          v-if="broker.branch" 
                          :to="{ name: 'BranchDetail', params: { id: broker.branch.id }}"
                        >
                          {{ broker.branch.name }}
                        </router-link>
                        <span v-else>N/A</span>
                      </li>
                    </ul>
                  </div>

                  <div class="col-md-6">
                    <h6>Commission Details</h6>
                    <ul class="list-unstyled">
                      <li class="mb-2">
                        <i class="bi bi-bank me-2"></i>
                        Bank: {{ broker.commission_bank_name || 'Not provided' }}
                      </li>
                      <li class="mb-2">
                        <i class="bi bi-person me-2"></i>
                        Account Name: {{ broker.commission_account_name || 'Not provided' }}
                      </li>
                      <li class="mb-2">
                        <i class="bi bi-credit-card me-2"></i>
                        Account Number: {{ broker.commission_account_number || 'Not provided' }}
                      </li>
                      <li class="mb-2">
                        <i class="bi bi-upc me-2"></i>
                        BSB: {{ broker.commission_bsb || 'Not provided' }}
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
                  :to="{ name: 'ApplicationList', query: { broker: broker.id }}" 
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
                  <p class="text-muted mb-0">No applications found for this broker</p>
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
                <div v-if="loadingStats" class="text-center py-3">
                  <div class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <p class="mt-2">Loading statistics...</p>
                </div>
                <div v-else-if="!stats" class="text-center py-3">
                  <p class="text-muted mb-0">No statistics available</p>
                </div>
                <div v-else>
                  <div class="stat-item mb-3">
                    <div class="d-flex justify-content-between">
                      <span>Total Applications</span>
                      <span class="fw-bold">{{ stats.total_applications }}</span>
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
                      <span class="fw-bold">${{ formatCurrency(stats.total_loan_amount) }}</span>
                    </div>
                  </div>

                  <div class="stat-item mb-3">
                    <div class="d-flex justify-content-between">
                      <span>Success Rate</span>
                      <span class="fw-bold">{{ stats.success_rate || 0 }}%</span>
                    </div>
                    <div class="progress mt-1">
                      <div 
                        class="progress-bar bg-success" 
                        role="progressbar" 
                        :style="`width: ${stats.success_rate || 0}%`" 
                        :aria-valuenow="stats.success_rate || 0" 
                        aria-valuemin="0" 
                        aria-valuemax="100"
                      ></div>
                    </div>
                  </div>

                  <h6 class="mt-4">Applications by Stage</h6>
                  <div v-if="stats.applications_by_stage" class="mt-3">
                    <div v-for="(count, stage) in stats.applications_by_stage" :key="stage" class="stat-item mb-2">
                      <div class="d-flex justify-content-between">
                        <span>{{ formatStage(stage) }}</span>
                        <span class="fw-bold">{{ count }}</span>
                      </div>
                      <div class="progress mt-1">
                        <div 
                          class="progress-bar" 
                          :class="getStageClass(stage)"
                          role="progressbar" 
                          :style="`width: ${(count / stats.total_applications) * 100}%`" 
                          :aria-valuenow="(count / stats.total_applications) * 100" 
                          aria-valuemin="0" 
                          aria-valuemax="100"
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Not found state -->
      <div v-else class="text-center py-5">
        <i class="bi bi-question-circle display-1 text-muted"></i>
        <h3 class="mt-3">Broker Not Found</h3>
        <p class="text-muted">The broker you're looking for doesn't exist or you don't have permission to view it.</p>
        <router-link :to="{ name: 'BrokerList' }" class="btn btn-primary mt-3">
          Back to Broker List
        </router-link>
      </div>
    </div>

    <!-- Edit Broker Modal -->
    <div class="modal fade" id="editBrokerModal" tabindex="-1" aria-labelledby="editBrokerModalLabel" aria-hidden="true" ref="editModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editBrokerModalLabel">Edit Broker</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <broker-form
              :broker="broker"
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
            Are you sure you want to delete broker {{ broker?.first_name }} {{ broker?.last_name }}?
            This action cannot be undone.
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteBroker" :disabled="formLoading">
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
import BrokerForm from '@/components/broker/BrokerForm.vue'

export default {
  name: 'BrokerDetailView',
  components: {
    BrokerForm
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
    const loadingStats = ref(false)
    const formLoading = ref(false)
    const error = ref(null)
    const applications = ref([])
    const stats = ref(null)
    
    // Computed properties
    const broker = computed(() => brokerStore.currentBroker)
    
    // Initialize modals on component mount
    onMounted(() => {
      bsEditModal = new Modal(editModal.value)
      bsDeleteModal = new Modal(deleteModal.value)
      
      // Fetch broker details
      fetchBrokerDetails()
    })
    
    // Methods
    const fetchBrokerDetails = async () => {
      const brokerId = route.params.id
      if (!brokerId) return
      
      loading.value = true
      error.value = null
      
      try {
        await brokerStore.fetchBrokerById(brokerId)
        fetchBrokerApplications(brokerId)
        fetchBrokerStats(brokerId)
      } catch (err) {
        error.value = err.message || 'Failed to fetch broker details'
      } finally {
        loading.value = false
      }
    }
    
    const fetchBrokerApplications = async (brokerId) => {
      loadingApplications.value = true
      
      try {
        applications.value = await brokerStore.fetchBrokerApplications(brokerId)
      } catch (err) {
        console.error('Failed to fetch broker applications:', err)
        applications.value = []
      } finally {
        loadingApplications.value = false
      }
    }
    
    const fetchBrokerStats = async (brokerId) => {
      loadingStats.value = true
      
      try {
        stats.value = await brokerStore.fetchBrokerStats(brokerId)
      } catch (err) {
        console.error('Failed to fetch broker stats:', err)
        stats.value = null
      } finally {
        loadingStats.value = false
      }
    }
    
    const editBroker = () => {
      bsEditModal.show()
    }
    
    const hideModal = () => {
      bsEditModal.hide()
    }
    
    const handleFormSubmit = async (brokerData) => {
      if (!broker.value) return
      
      formLoading.value = true
      
      try {
        await brokerStore.updateBroker(broker.value.id, brokerData)
        bsEditModal.hide()
        // Refresh broker details
        await brokerStore.fetchBrokerById(broker.value.id)
      } catch (err) {
        console.error('Failed to update broker:', err)
      } finally {
        formLoading.value = false
      }
    }
    
    const confirmDelete = () => {
      bsDeleteModal.show()
    }
    
    const deleteBroker = async () => {
      if (!broker.value) return
      
      formLoading.value = true
      
      try {
        await brokerStore.deleteBroker(broker.value.id)
        bsDeleteModal.hide()
        router.push({ name: 'BrokerList' })
      } catch (err) {
        console.error('Failed to delete broker:', err)
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
      broker,
      loading,
      loadingApplications,
      loadingStats,
      formLoading,
      error,
      applications,
      stats,
      editModal,
      deleteModal,
      fetchBrokerDetails,
      editBroker,
      hideModal,
      handleFormSubmit,
      confirmDelete,
      deleteBroker,
      formatCurrency,
      formatDate,
      getStageClass,
      formatStage
    }
  }
}
</script>

<style scoped>
.broker-detail-view {
  min-height: 100vh;
}

.stat-item {
  margin-bottom: 1rem;
}

.progress {
  height: 0.5rem;
}
</style>
