<template>
  <div class="branch-detail-view">
    <div class="container-fluid py-4">
      <!-- Loading state -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading branch details...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchBranchDetails">
          Try Again
        </button>
      </div>

      <!-- Branch details -->
      <div v-else-if="branch" class="branch-details">
        <!-- Header section -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <div>
            <h1 class="h3">{{ branch.name }}</h1>
            <p class="text-muted mb-0">Manager: {{ branch.manager }}</p>
          </div>
          <div class="branch-actions">
            <button class="btn btn-outline-primary me-2" @click="editBranch">
              <i class="bi bi-pencil me-1"></i> Edit
            </button>
            <button class="btn btn-outline-danger" @click="confirmDelete">
              <i class="bi bi-trash me-1"></i> Delete
            </button>
          </div>
        </div>

        <!-- Main content -->
        <div class="row">
          <!-- Left column - Branch information -->
          <div class="col-lg-8">
            <div class="card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">Branch Information</h5>
              </div>
              <div class="card-body">
                <div class="row">
                  <div class="col-md-6">
                    <h6>Contact Information</h6>
                    <ul class="list-unstyled">
                      <li class="mb-2">
                        <i class="bi bi-geo-alt me-2"></i>
                        {{ branch.address }}
                      </li>
                      <li class="mb-2">
                        <i class="bi bi-telephone me-2"></i>
                        <a :href="`tel:${branch.phone}`">{{ branch.phone }}</a>
                      </li>
                      <li class="mb-2">
                        <i class="bi bi-envelope me-2"></i>
                        <a :href="`mailto:${branch.email}`">{{ branch.email }}</a>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <!-- Brokers section -->
            <div class="card mb-4">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">Brokers</h5>
                <router-link 
                  :to="{ name: 'BrokerList', query: { branch: branch.id }}" 
                  class="btn btn-sm btn-outline-primary"
                >
                  View All
                </router-link>
              </div>
              <div class="card-body">
                <div v-if="loadingBrokers" class="text-center py-3">
                  <div class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <p class="mt-2">Loading brokers...</p>
                </div>
                <div v-else-if="branchBrokers.length === 0" class="text-center py-3">
                  <p class="text-muted mb-0">No brokers found in this branch</p>
                  <router-link 
                    :to="{ name: 'BrokerList', query: { branch: branch.id }}" 
                    class="btn btn-sm btn-primary mt-2"
                  >
                    Add Broker to Branch
                  </router-link>
                </div>
                <div v-else class="table-responsive">
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>License</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="broker in branchBrokers.slice(0, 5)" :key="broker.id">
                        <td>{{ broker.first_name }} {{ broker.last_name }}</td>
                        <td>{{ broker.email }}</td>
                        <td>{{ broker.phone }}</td>
                        <td>{{ broker.license_number }}</td>
                        <td>
                          <router-link 
                            :to="{ name: 'BrokerDetail', params: { id: broker.id }}" 
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

            <!-- BDMs section -->
            <div class="card mb-4">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">Business Development Managers</h5>
                <router-link 
                  :to="{ name: 'BDMList', query: { branch: branch.id }}" 
                  class="btn btn-sm btn-outline-primary"
                >
                  View All
                </router-link>
              </div>
              <div class="card-body">
                <div v-if="loadingBDMs" class="text-center py-3">
                  <div class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <p class="mt-2">Loading BDMs...</p>
                </div>
                <div v-else-if="branchBDMs.length === 0" class="text-center py-3">
                  <p class="text-muted mb-0">No BDMs found in this branch</p>
                  <router-link 
                    :to="{ name: 'BDMList', query: { branch: branch.id }}" 
                    class="btn btn-sm btn-primary mt-2"
                  >
                    Add BDM to Branch
                  </router-link>
                </div>
                <div v-else class="table-responsive">
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Employee ID</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="bdm in branchBDMs.slice(0, 5)" :key="bdm.id">
                        <td>{{ bdm.first_name }} {{ bdm.last_name }}</td>
                        <td>{{ bdm.email }}</td>
                        <td>{{ bdm.phone }}</td>
                        <td>{{ bdm.employee_id }}</td>
                        <td>
                          <router-link 
                            :to="{ name: 'BDMDetail', params: { id: bdm.id }}" 
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
            <!-- Branch stats card -->
            <div class="card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">Branch Statistics</h5>
              </div>
              <div class="card-body">
                <div class="stat-item mb-3">
                  <div class="d-flex justify-content-between">
                    <span>Total Brokers</span>
                    <span class="fw-bold">{{ branchBrokers.length }}</span>
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
                    <span>Total BDMs</span>
                    <span class="fw-bold">{{ branchBDMs.length }}</span>
                  </div>
                  <div class="progress mt-1">
                    <div 
                      class="progress-bar bg-info" 
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
                    <span>Total Applications</span>
                    <span class="fw-bold">{{ totalApplications }}</span>
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
                    :to="{ name: 'BrokerList', query: { branch: branch.id }}" 
                    class="btn btn-outline-primary"
                  >
                    <i class="bi bi-people me-2"></i> Manage Brokers
                  </router-link>
                  <router-link 
                    :to="{ name: 'BDMList', query: { branch: branch.id }}" 
                    class="btn btn-outline-info"
                  >
                    <i class="bi bi-briefcase me-2"></i> Manage BDMs
                  </router-link>
                  <router-link 
                    :to="{ name: 'ApplicationList', query: { branch: branch.id }}" 
                    class="btn btn-outline-secondary"
                  >
                    <i class="bi bi-file-earmark-text me-2"></i> View Applications
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
        <h3 class="mt-3">Branch Not Found</h3>
        <p class="text-muted">The branch you're looking for doesn't exist or you don't have permission to view it.</p>
        <router-link :to="{ name: 'BranchList' }" class="btn btn-primary mt-3">
          Back to Branch List
        </router-link>
      </div>
    </div>

    <!-- Edit Branch Modal -->
    <div class="modal fade" id="editBranchModal" tabindex="-1" aria-labelledby="editBranchModalLabel" aria-hidden="true" ref="editModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editBranchModalLabel">Edit Branch</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <branch-form
              :branch="branch"
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
            <p>Are you sure you want to delete branch {{ branch?.name }}?</p>
            <p class="text-danger fw-bold">This action cannot be undone and may affect associated brokers and BDMs.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteBranch" :disabled="formLoading">
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
import BranchForm from '@/components/broker/BranchForm.vue'

export default {
  name: 'BranchDetailView',
  components: {
    BranchForm
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
    const loadingBrokers = ref(false)
    const loadingBDMs = ref(false)
    const formLoading = ref(false)
    const error = ref(null)
    const branchBrokers = ref([])
    const branchBDMs = ref([])
    
    // Computed properties
    const branch = computed(() => brokerStore.currentBranch)
    const totalApplications = computed(() => {
      // Calculate total applications from brokers in this branch
      let total = 0
      branchBrokers.value.forEach(broker => {
        if (broker.application_count) {
          total += broker.application_count
        }
      })
      return total
    })
    
    // Initialize modals on component mount
    onMounted(() => {
      bsEditModal = new Modal(editModal.value)
      bsDeleteModal = new Modal(deleteModal.value)
      
      // Fetch branch details
      fetchBranchDetails()
    })
    
    // Methods
    const fetchBranchDetails = async () => {
      const branchId = route.params.id
      if (!branchId) return
      
      loading.value = true
      error.value = null
      
      try {
        await brokerStore.fetchBranchById(branchId)
        fetchBranchBrokers(branchId)
        fetchBranchBDMs(branchId)
      } catch (err) {
        error.value = err.message || 'Failed to fetch branch details'
      } finally {
        loading.value = false
      }
    }
    
    const fetchBranchBrokers = async (branchId) => {
      loadingBrokers.value = true
      
      try {
        branchBrokers.value = await brokerStore.fetchBrokersInBranch(branchId) || []
      } catch (err) {
        console.error('Failed to fetch branch brokers:', err)
        branchBrokers.value = []
      } finally {
        loadingBrokers.value = false
      }
    }
    
    const fetchBranchBDMs = async (branchId) => {
      loadingBDMs.value = true
      
      try {
        branchBDMs.value = await brokerStore.fetchBDMsInBranch(branchId) || []
      } catch (err) {
        console.error('Failed to fetch branch BDMs:', err)
        branchBDMs.value = []
      } finally {
        loadingBDMs.value = false
      }
    }
    
    const editBranch = () => {
      bsEditModal.show()
    }
    
    const hideModal = () => {
      bsEditModal.hide()
    }
    
    const handleFormSubmit = async (branchData) => {
      if (!branch.value) return
      
      formLoading.value = true
      
      try {
        await brokerStore.updateBranch(branch.value.id, branchData)
        bsEditModal.hide()
        // Refresh branch details
        await brokerStore.fetchBranchById(branch.value.id)
      } catch (err) {
        console.error('Failed to update branch:', err)
      } finally {
        formLoading.value = false
      }
    }
    
    const confirmDelete = () => {
      bsDeleteModal.show()
    }
    
    const deleteBranch = async () => {
      if (!branch.value) return
      
      formLoading.value = true
      
      try {
        await brokerStore.deleteBranch(branch.value.id)
        bsDeleteModal.hide()
        router.push({ name: 'BranchList' })
      } catch (err) {
        console.error('Failed to delete branch:', err)
      } finally {
        formLoading.value = false
      }
    }
    
    return {
      branch,
      loading,
      loadingBrokers,
      loadingBDMs,
      formLoading,
      error,
      branchBrokers,
      branchBDMs,
      totalApplications,
      editModal,
      deleteModal,
      fetchBranchDetails,
      editBranch,
      hideModal,
      handleFormSubmit,
      confirmDelete,
      deleteBranch
    }
  }
}
</script>

<style scoped>
.branch-detail-view {
  min-height: 100vh;
}

.stat-item {
  margin-bottom: 1rem;
}

.progress {
  height: 0.5rem;
}
</style>
