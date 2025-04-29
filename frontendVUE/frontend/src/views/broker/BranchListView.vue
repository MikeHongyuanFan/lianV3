<template>
  <div class="branch-list-view">
    <div class="container-fluid py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Branches</h1>
        <button class="btn btn-primary" @click="showCreateModal">
          <i class="bi bi-plus-circle me-2"></i> Add Branch
        </button>
      </div>

      <!-- Search and filters -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-8">
              <div class="input-group">
                <span class="input-group-text">
                  <i class="bi bi-search"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Search by name or address"
                  v-model="searchQuery"
                  @input="handleSearchInput"
                />
                <button
                  class="btn btn-outline-secondary"
                  type="button"
                  @click="clearSearch"
                  v-if="searchQuery"
                >
                  <i class="bi bi-x"></i>
                </button>
              </div>
            </div>
            <div class="col-md-4">
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
        <p class="mt-2">Loading branches...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchBranches">
          Try Again
        </button>
      </div>

      <!-- Empty state -->
      <div v-else-if="!hasBranches" class="text-center py-5">
        <i class="bi bi-building display-1 text-muted"></i>
        <h3 class="mt-3">No branches found</h3>
        <p class="text-muted">
          {{ searchQuery ? 'Try adjusting your search' : 'Add your first branch to get started' }}
        </p>
        <button class="btn btn-primary mt-3" @click="showCreateModal">
          <i class="bi bi-plus-circle me-2"></i> Add Branch
        </button>
      </div>

      <!-- Branch list -->
      <div v-else class="row">
        <div v-for="branch in branches" :key="branch.id" class="col-md-6 col-lg-4">
          <branch-card
            :branch="branch"
            @view="viewBranch"
            @edit="editBranch"
            @delete="deleteBranch"
            @view-brokers="viewBranchBrokers"
            @view-bdms="viewBranchBDMs"
          />
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="hasBranches" class="d-flex justify-content-between align-items-center mt-4">
        <div>
          Showing {{ paginationInfo.currentPage * paginationInfo.itemsPerPage - paginationInfo.itemsPerPage + 1 }} to 
          {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }} of 
          {{ paginationInfo.totalItems }} branches
        </div>
        <nav aria-label="Branch pagination">
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

    <!-- Create/Edit Branch Modal -->
    <div class="modal fade" id="branchModal" tabindex="-1" aria-labelledby="branchModalLabel" aria-hidden="true" ref="branchModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="branchModalLabel">{{ isEditing ? 'Edit Branch' : 'Create Branch' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <branch-form
              :branch="currentBranch"
              :loading="formLoading"
              @submit="handleFormSubmit"
              @cancel="hideModal"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- View Branch Modal -->
    <div class="modal fade" id="viewBranchModal" tabindex="-1" aria-labelledby="viewBranchModalLabel" aria-hidden="true" ref="viewBranchModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="viewBranchModalLabel">Branch Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="currentBranch">
            <div class="row mb-4">
              <div class="col-md-6">
                <h4>{{ currentBranch.name }}</h4>
                <p class="text-muted">Manager: {{ currentBranch.manager }}</p>
              </div>
              <div class="col-md-6 text-md-end">
                <button class="btn btn-outline-primary me-2" @click="showEditModal">
                  <i class="bi bi-pencil me-1"></i> Edit
                </button>
                <button class="btn btn-outline-danger" @click="confirmDelete(currentBranch)">
                  <i class="bi bi-trash me-1"></i> Delete
                </button>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <h5>Contact Information</h5>
                <ul class="list-unstyled">
                  <li class="mb-2">
                    <i class="bi bi-geo-alt me-2"></i>
                    {{ currentBranch.address }}
                  </li>
                  <li class="mb-2">
                    <i class="bi bi-telephone me-2"></i>
                    <a :href="`tel:${currentBranch.phone}`">{{ currentBranch.phone }}</a>
                  </li>
                  <li class="mb-2">
                    <i class="bi bi-envelope me-2"></i>
                    <a :href="`mailto:${currentBranch.email}`">{{ currentBranch.email }}</a>
                  </li>
                </ul>
              </div>

              <div class="col-md-6">
                <h5>Branch Personnel</h5>
                <div class="d-flex justify-content-between mb-3">
                  <span>Brokers:</span>
                  <span>{{ branchBrokers.length }}</span>
                </div>
                <div class="d-flex justify-content-between mb-3">
                  <span>BDMs:</span>
                  <span>{{ branchBDMs.length }}</span>
                </div>
                <div class="mt-3">
                  <button class="btn btn-sm btn-outline-primary me-2" @click="viewBranchBrokers(currentBranch)">
                    View Brokers
                  </button>
                  <button class="btn btn-sm btn-outline-primary" @click="viewBranchBDMs(currentBranch)">
                    View BDMs
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Branch Brokers Modal -->
    <div class="modal fade" id="branchBrokersModal" tabindex="-1" aria-labelledby="branchBrokersModalLabel" aria-hidden="true" ref="branchBrokersModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="branchBrokersModalLabel" v-if="currentBranch">
              Brokers in {{ currentBranch.name }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="loadingBranchData" class="text-center py-4">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="mt-2">Loading brokers...</p>
            </div>
            <div v-else-if="branchBrokers.length === 0" class="text-center py-4">
              <p>No brokers found in this branch</p>
              <button class="btn btn-primary" @click="navigateToBrokers">
                Add Broker to Branch
              </button>
            </div>
            <div v-else>
              <div class="list-group">
                <div v-for="broker in branchBrokers" :key="broker.id" class="list-group-item list-group-item-action">
                  <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">{{ broker.first_name }} {{ broker.last_name }}</h5>
                    <button class="btn btn-sm btn-outline-primary" @click="viewBrokerDetails(broker)">
                      View Details
                    </button>
                  </div>
                  <p class="mb-1">{{ broker.email }} | {{ broker.phone }}</p>
                  <small>License: {{ broker.license_number }}</small>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Branch BDMs Modal -->
    <div class="modal fade" id="branchBDMsModal" tabindex="-1" aria-labelledby="branchBDMsModalLabel" aria-hidden="true" ref="branchBDMsModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="branchBDMsModalLabel" v-if="currentBranch">
              BDMs in {{ currentBranch.name }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="loadingBranchData" class="text-center py-4">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="mt-2">Loading BDMs...</p>
            </div>
            <div v-else-if="branchBDMs.length === 0" class="text-center py-4">
              <p>No BDMs found in this branch</p>
              <button class="btn btn-primary" @click="navigateToBDMs">
                Add BDM to Branch
              </button>
            </div>
            <div v-else>
              <div class="list-group">
                <div v-for="bdm in branchBDMs" :key="bdm.id" class="list-group-item list-group-item-action">
                  <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">{{ bdm.first_name }} {{ bdm.last_name }}</h5>
                    <button class="btn btn-sm btn-outline-primary" @click="viewBDMDetails(bdm)">
                      View Details
                    </button>
                  </div>
                  <p class="mb-1">{{ bdm.email }} | {{ bdm.phone }}</p>
                  <small>Employee ID: {{ bdm.employee_id }}</small>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Modal } from 'bootstrap'
import { useBrokerStore } from '@/store/broker'
import BranchCard from '@/components/broker/BranchCard.vue'
import BranchForm from '@/components/broker/BranchForm.vue'

export default {
  name: 'BranchListView',
  components: {
    BranchCard,
    BranchForm
  },
  setup() {
    const router = useRouter()
    const brokerStore = useBrokerStore()
    
    // Refs for modals
    const branchModal = ref(null)
    const viewBranchModal = ref(null)
    const branchBrokersModal = ref(null)
    const branchBDMsModal = ref(null)
    let bsCreateEditModal = null
    let bsViewModal = null
    let bsBrokersModal = null
    let bsBDMsModal = null
    
    // State
    const searchQuery = ref('')
    const isEditing = ref(false)
    const currentBranch = ref(null)
    const formLoading = ref(false)
    const loadingBranchData = ref(false)
    const branchBrokers = ref([])
    const branchBDMs = ref([])
    
    // Computed properties
    const branches = computed(() => brokerStore.branches)
    const loading = computed(() => brokerStore.loading)
    const error = computed(() => brokerStore.error)
    const hasBranches = computed(() => brokerStore.hasBranches)
    const paginationInfo = computed(() => brokerStore.getBranchPaginationInfo)
    
    // Initialize modals on component mount
    onMounted(() => {
      bsCreateEditModal = new Modal(branchModal.value)
      bsViewModal = new Modal(viewBranchModal.value)
      bsBrokersModal = new Modal(branchBrokersModal.value)
      bsBDMsModal = new Modal(branchBDMsModal.value)
      
      // Fetch branches
      fetchBranches()
    })
    
    // Methods
    const fetchBranches = async () => {
      try {
        await brokerStore.fetchBranches()
      } catch (error) {
        console.error('Error fetching branches:', error)
      }
    }
    
    const handleSearchInput = () => {
      brokerStore.setBranchFilters({ search: searchQuery.value })
    }
    
    const clearSearch = () => {
      searchQuery.value = ''
      brokerStore.setBranchFilters({ search: '' })
    }
    
    const clearFilters = () => {
      searchQuery.value = ''
      brokerStore.setBranchFilters({ search: '' })
    }
    
    const goToPage = (page) => {
      if (page < 1 || page > paginationInfo.value.totalPages) return
      brokerStore.setBranchPage(page)
    }
    
    const showCreateModal = () => {
      isEditing.value = false
      currentBranch.value = null
      bsCreateEditModal.show()
    }
    
    const showEditModal = () => {
      isEditing.value = true
      bsViewModal.hide()
      setTimeout(() => {
        bsCreateEditModal.show()
      }, 500)
    }
    
    const hideModal = () => {
      bsCreateEditModal.hide()
    }
    
    const handleFormSubmit = async (branchData) => {
      formLoading.value = true
      try {
        if (isEditing.value && currentBranch.value) {
          await brokerStore.updateBranch(currentBranch.value.id, branchData)
        } else {
          await brokerStore.createBranch(branchData)
        }
        bsCreateEditModal.hide()
        fetchBranches() // Refresh the list
      } catch (error) {
        console.error('Error saving branch:', error)
      } finally {
        formLoading.value = false
      }
    }
    
    const viewBranch = (branch) => {
      currentBranch.value = branch
      loadBranchData(branch.id)
      bsViewModal.show()
    }
    
    const loadBranchData = async (branchId) => {
      loadingBranchData.value = true
      try {
        const [brokersResponse, bdmsResponse] = await Promise.all([
          brokerStore.fetchBrokersInBranch(branchId),
          brokerStore.fetchBDMsInBranch(branchId)
        ])
        branchBrokers.value = brokersResponse || []
        branchBDMs.value = bdmsResponse || []
      } catch (error) {
        console.error('Error loading branch data:', error)
      } finally {
        loadingBranchData.value = false
      }
    }
    
    const editBranch = (branch) => {
      isEditing.value = true
      currentBranch.value = branch
      bsCreateEditModal.show()
    }
    
    const deleteBranch = async (branch) => {
      try {
        await brokerStore.deleteBranch(branch.id)
        
        // If we're viewing the branch that was deleted, close the modal
        if (currentBranch.value && currentBranch.value.id === branch.id) {
          bsViewModal.hide()
        }
      } catch (error) {
        console.error('Error deleting branch:', error)
      }
    }
    
    const viewBranchBrokers = async (branch) => {
      currentBranch.value = branch
      loadingBranchData.value = true
      
      try {
        const response = await brokerStore.fetchBrokersInBranch(branch.id)
        branchBrokers.value = response || []
      } catch (error) {
        console.error('Error fetching branch brokers:', error)
      } finally {
        loadingBranchData.value = false
      }
      
      bsViewModal.hide()
      setTimeout(() => {
        bsBrokersModal.show()
      }, 500)
    }
    
    const viewBranchBDMs = async (branch) => {
      currentBranch.value = branch
      loadingBranchData.value = true
      
      try {
        const response = await brokerStore.fetchBDMsInBranch(branch.id)
        branchBDMs.value = response || []
      } catch (error) {
        console.error('Error fetching branch BDMs:', error)
      } finally {
        loadingBranchData.value = false
      }
      
      bsViewModal.hide()
      setTimeout(() => {
        bsBDMsModal.show()
      }, 500)
    }
    
    const viewBrokerDetails = (broker) => {
      bsBrokersModal.hide()
      router.push({ name: 'BrokerDetail', params: { id: broker.id } })
    }
    
    const viewBDMDetails = (bdm) => {
      bsBDMsModal.hide()
      router.push({ name: 'BDMDetail', params: { id: bdm.id } })
    }
    
    const navigateToBrokers = () => {
      bsBrokersModal.hide()
      router.push({ name: 'BrokerList', query: { branch: currentBranch.value.id } })
    }
    
    const navigateToBDMs = () => {
      bsBDMsModal.hide()
      router.push({ name: 'BDMList', query: { branch: currentBranch.value.id } })
    }
    
    return {
      branches,
      loading,
      error,
      hasBranches,
      paginationInfo,
      searchQuery,
      isEditing,
      currentBranch,
      formLoading,
      loadingBranchData,
      branchBrokers,
      branchBDMs,
      branchModal,
      viewBranchModal,
      branchBrokersModal,
      branchBDMsModal,
      fetchBranches,
      handleSearchInput,
      clearSearch,
      clearFilters,
      goToPage,
      showCreateModal,
      showEditModal,
      hideModal,
      handleFormSubmit,
      viewBranch,
      editBranch,
      deleteBranch,
      viewBranchBrokers,
      viewBranchBDMs,
      viewBrokerDetails,
      viewBDMDetails,
      navigateToBrokers,
      navigateToBDMs
    }
  }
}
</script>

<style scoped>
.branch-list-view {
  min-height: 100vh;
}

.pagination {
  margin-bottom: 0;
}
</style>
