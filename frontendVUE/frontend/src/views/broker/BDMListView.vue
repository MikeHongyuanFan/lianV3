<template>
  <div class="bdm-list-view">
    <div class="container-fluid py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Business Development Managers</h1>
        <button class="btn btn-primary" @click="showCreateModal">
          <i class="bi bi-plus-circle me-2"></i> Add BDM
        </button>
      </div>

      <!-- Search and filters -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-6">
              <div class="input-group">
                <span class="input-group-text">
                  <i class="bi bi-search"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Search by name, email, or phone"
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
              <select class="form-select" v-model="selectedBranch" @change="filterByBranch">
                <option value="">All Branches</option>
                <option v-for="branch in branches" :key="branch.id" :value="branch.id">
                  {{ branch.name }}
                </option>
              </select>
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
        <p class="mt-2">Loading BDMs...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchBDMs">
          Try Again
        </button>
      </div>

      <!-- Empty state -->
      <div v-else-if="!hasBDMs" class="text-center py-5">
        <i class="bi bi-briefcase display-1 text-muted"></i>
        <h3 class="mt-3">No BDMs found</h3>
        <p class="text-muted">
          {{ searchQuery || selectedBranch ? 'Try adjusting your filters' : 'Add your first BDM to get started' }}
        </p>
        <button class="btn btn-primary mt-3" @click="showCreateModal">
          <i class="bi bi-plus-circle me-2"></i> Add BDM
        </button>
      </div>

      <!-- BDM list -->
      <div v-else class="row">
        <div v-for="bdm in bdms" :key="bdm.id" class="col-md-6 col-lg-4">
          <bdm-card
            :bdm="bdm"
            @view="viewBDM"
            @edit="editBDM"
            @delete="deleteBDM"
            @view-applications="viewBDMApplications"
          />
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="hasBDMs" class="d-flex justify-content-between align-items-center mt-4">
        <div>
          Showing {{ paginationInfo.currentPage * paginationInfo.itemsPerPage - paginationInfo.itemsPerPage + 1 }} to 
          {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }} of 
          {{ paginationInfo.totalItems }} BDMs
        </div>
        <nav aria-label="BDM pagination">
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

    <!-- Create/Edit BDM Modal -->
    <div class="modal fade" id="bdmModal" tabindex="-1" aria-labelledby="bdmModalLabel" aria-hidden="true" ref="bdmModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="bdmModalLabel">{{ isEditing ? 'Edit BDM' : 'Create BDM' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <bdm-form
              :bdm="currentBDM"
              :loading="formLoading"
              @submit="handleFormSubmit"
              @cancel="hideModal"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- View BDM Modal -->
    <div class="modal fade" id="viewBDMModal" tabindex="-1" aria-labelledby="viewBDMModalLabel" aria-hidden="true" ref="viewBDMModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="viewBDMModalLabel">BDM Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="currentBDM">
            <div class="row mb-4">
              <div class="col-md-6">
                <h4>{{ currentBDM.first_name }} {{ currentBDM.last_name }}</h4>
                <p class="text-muted">Employee ID: {{ currentBDM.employee_id }}</p>
              </div>
              <div class="col-md-6 text-md-end">
                <button class="btn btn-outline-primary me-2" @click="showEditModal">
                  <i class="bi bi-pencil me-1"></i> Edit
                </button>
                <button class="btn btn-outline-danger" @click="confirmDelete(currentBDM)">
                  <i class="bi bi-trash me-1"></i> Delete
                </button>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <h5>Contact Information</h5>
                <ul class="list-unstyled">
                  <li class="mb-2">
                    <i class="bi bi-envelope me-2"></i>
                    <a :href="`mailto:${currentBDM.email}`">{{ currentBDM.email }}</a>
                  </li>
                  <li class="mb-2">
                    <i class="bi bi-telephone me-2"></i>
                    <a :href="`tel:${currentBDM.phone}`">{{ currentBDM.phone }}</a>
                  </li>
                </ul>

                <h5 class="mt-4">Branch Information</h5>
                <ul class="list-unstyled">
                  <li class="mb-2">
                    <i class="bi bi-house-door me-2"></i>
                    Branch: {{ currentBDM.branch?.name || 'N/A' }}
                  </li>
                </ul>
              </div>

              <div class="col-md-6">
                <h5>Applications</h5>
                <div v-if="bdmApplications.length > 0">
                  <p>Total Applications: {{ bdmApplications.length }}</p>
                  <button class="btn btn-sm btn-outline-primary" @click="viewBDMApplications(currentBDM)">
                    View Applications
                  </button>
                </div>
                <p v-else class="text-muted">No applications found for this BDM</p>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Modal } from 'bootstrap'
import { useBrokerStore } from '@/store/broker'
import BDMCard from '@/components/broker/BDMCard.vue'
import BDMForm from '@/components/broker/BDMForm.vue'

export default {
  name: 'BDMListView',
  components: {
    BDMCard,
    BDMForm
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const brokerStore = useBrokerStore()
    
    // Refs for modals
    const bdmModal = ref(null)
    const viewBDMModal = ref(null)
    let bsCreateEditModal = null
    let bsViewModal = null
    
    // State
    const searchQuery = ref('')
    const selectedBranch = ref('')
    const isEditing = ref(false)
    const currentBDM = ref(null)
    const formLoading = ref(false)
    const bdmApplications = ref([])
    
    // Computed properties
    const bdms = computed(() => brokerStore.bdms)
    const branches = computed(() => brokerStore.branches)
    const loading = computed(() => brokerStore.loading)
    const error = computed(() => brokerStore.error)
    const hasBDMs = computed(() => brokerStore.hasBDMs)
    const paginationInfo = computed(() => brokerStore.getBDMPaginationInfo)
    
    // Initialize modals on component mount
    onMounted(() => {
      bsCreateEditModal = new Modal(bdmModal.value)
      bsViewModal = new Modal(viewBDMModal.value)
      
      // Fetch BDMs and branches
      fetchBDMs()
      fetchBranches()
      
      // Check if we have a branch filter from the route
      if (route.query.branch) {
        selectedBranch.value = route.query.branch
        filterByBranch()
      }
    })
    
    // Methods
    const fetchBDMs = async () => {
      try {
        await brokerStore.fetchBDMs()
      } catch (error) {
        console.error('Error fetching BDMs:', error)
      }
    }
    
    const fetchBranches = async () => {
      try {
        await brokerStore.fetchBranches()
      } catch (error) {
        console.error('Error fetching branches:', error)
      }
    }
    
    const handleSearchInput = () => {
      brokerStore.setBDMFilters({ search: searchQuery.value })
    }
    
    const filterByBranch = () => {
      brokerStore.setBDMFilters({ branch: selectedBranch.value || undefined })
    }
    
    const clearSearch = () => {
      searchQuery.value = ''
      brokerStore.setBDMFilters({ search: '' })
    }
    
    const clearFilters = () => {
      searchQuery.value = ''
      selectedBranch.value = ''
      brokerStore.setBDMFilters({ search: '', branch: undefined })
    }
    
    const goToPage = (page) => {
      if (page < 1 || page > paginationInfo.value.totalPages) return
      brokerStore.setBDMPage(page)
    }
    
    const showCreateModal = () => {
      isEditing.value = false
      currentBDM.value = null
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
    
    const handleFormSubmit = async (bdmData) => {
      formLoading.value = true
      try {
        if (isEditing.value && currentBDM.value) {
          await brokerStore.updateBDM(currentBDM.value.id, bdmData)
        } else {
          await brokerStore.createBDM(bdmData)
        }
        bsCreateEditModal.hide()
        fetchBDMs() // Refresh the list
      } catch (error) {
        console.error('Error saving BDM:', error)
      } finally {
        formLoading.value = false
      }
    }
    
    const viewBDM = async (bdm) => {
      currentBDM.value = bdm
      
      // Fetch BDM applications
      try {
        bdmApplications.value = await brokerStore.fetchBDMApplications(bdm.id)
      } catch (error) {
        console.error('Error fetching BDM applications:', error)
        bdmApplications.value = []
      }
      
      bsViewModal.show()
    }
    
    const editBDM = (bdm) => {
      isEditing.value = true
      currentBDM.value = bdm
      bsCreateEditModal.show()
    }
    
    const deleteBDM = async (bdm) => {
      try {
        await brokerStore.deleteBDM(bdm.id)
        
        // If we're viewing the BDM that was deleted, close the modal
        if (currentBDM.value && currentBDM.value.id === bdm.id) {
          bsViewModal.hide()
        }
      } catch (error) {
        console.error('Error deleting BDM:', error)
      }
    }
    
    const viewBDMApplications = (bdm) => {
      if (bdm) {
        bsViewModal.hide()
        router.push({ name: 'ApplicationList', query: { bdm: bdm.id } })
      }
    }
    
    return {
      bdms,
      branches,
      loading,
      error,
      hasBDMs,
      paginationInfo,
      searchQuery,
      selectedBranch,
      isEditing,
      currentBDM,
      formLoading,
      bdmApplications,
      bdmModal,
      viewBDMModal,
      fetchBDMs,
      handleSearchInput,
      filterByBranch,
      clearSearch,
      clearFilters,
      goToPage,
      showCreateModal,
      showEditModal,
      hideModal,
      handleFormSubmit,
      viewBDM,
      editBDM,
      deleteBDM,
      viewBDMApplications
    }
  }
}
</script>

<style scoped>
.bdm-list-view {
  min-height: 100vh;
}

.pagination {
  margin-bottom: 0;
}
</style>
