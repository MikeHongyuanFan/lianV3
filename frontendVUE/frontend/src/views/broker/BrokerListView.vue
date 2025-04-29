<template>
  <div class="broker-list-view">
    <div class="container-fluid py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Brokers</h1>
        <button class="btn btn-primary" @click="showCreateModal">
          <i class="bi bi-plus-circle me-2"></i> Add Broker
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
        <p class="mt-2">Loading brokers...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchBrokers">
          Try Again
        </button>
      </div>

      <!-- Empty state -->
      <div v-else-if="!hasBrokers" class="text-center py-5">
        <i class="bi bi-people display-1 text-muted"></i>
        <h3 class="mt-3">No brokers found</h3>
        <p class="text-muted">
          {{ searchQuery || selectedBranch ? 'Try adjusting your filters' : 'Add your first broker to get started' }}
        </p>
        <button class="btn btn-primary mt-3" @click="showCreateModal">
          <i class="bi bi-plus-circle me-2"></i> Add Broker
        </button>
      </div>

      <!-- Broker list -->
      <div v-else class="row">
        <div v-for="broker in brokers" :key="broker.id" class="col-md-6 col-lg-4">
          <broker-card
            :broker="broker"
            @view="viewBroker"
            @edit="editBroker"
            @delete="deleteBroker"
          />
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="hasBrokers" class="d-flex justify-content-between align-items-center mt-4">
        <div>
          Showing {{ paginationInfo.currentPage * paginationInfo.itemsPerPage - paginationInfo.itemsPerPage + 1 }} to 
          {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }} of 
          {{ paginationInfo.totalItems }} brokers
        </div>
        <nav aria-label="Broker pagination">
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

    <!-- Create/Edit Broker Modal -->
    <div class="modal fade" id="brokerModal" tabindex="-1" aria-labelledby="brokerModalLabel" aria-hidden="true" ref="brokerModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="brokerModalLabel">{{ isEditing ? 'Edit Broker' : 'Create Broker' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <broker-form
              :broker="currentBroker"
              :loading="formLoading"
              @submit="handleFormSubmit"
              @cancel="hideModal"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- View Broker Modal -->
    <div class="modal fade" id="viewBrokerModal" tabindex="-1" aria-labelledby="viewBrokerModalLabel" aria-hidden="true" ref="viewBrokerModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="viewBrokerModalLabel">Broker Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="currentBroker">
            <div class="row mb-4">
              <div class="col-md-6">
                <h4>{{ currentBroker.name }}</h4>
                <p class="text-muted">{{ currentBroker.company || 'Independent' }}</p>
              </div>
              <div class="col-md-6 text-md-end">
                <button class="btn btn-outline-primary me-2" @click="showEditModal">
                  <i class="bi bi-pencil me-1"></i> Edit
                </button>
                <button class="btn btn-outline-danger" @click="confirmDelete(currentBroker)">
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
                    <a :href="`mailto:${currentBroker.email}`">{{ currentBroker.email }}</a>
                  </li>
                  <li class="mb-2">
                    <i class="bi bi-telephone me-2"></i>
                    <a :href="`tel:${currentBroker.phone}`">{{ currentBroker.phone }}</a>
                  </li>
                  <li class="mb-2">
                    <i class="bi bi-geo-alt me-2"></i>
                    {{ currentBroker.address || 'No address provided' }}
                  </li>
                </ul>

                <h5 class="mt-4">Professional Details</h5>
                <ul class="list-unstyled">
                  <li class="mb-2">
                    <i class="bi bi-building me-2"></i>
                    Company: {{ currentBroker.company || 'N/A' }}
                  </li>
                  <li class="mb-2">
                    <i class="bi bi-house-door me-2"></i>
                    Branch: {{ currentBroker.branch_name || 'N/A' }}
                  </li>
                </ul>
              </div>

              <div class="col-md-6">
                <h5>Commission Details</h5>
                <ul class="list-unstyled">
                  <li class="mb-2">
                    <i class="bi bi-bank me-2"></i>
                    Bank: {{ currentBroker.commission_bank_name || 'Not provided' }}
                  </li>
                  <li class="mb-2">
                    <i class="bi bi-person me-2"></i>
                    Account Name: {{ currentBroker.commission_account_name || 'Not provided' }}
                  </li>
                  <li class="mb-2">
                    <i class="bi bi-credit-card me-2"></i>
                    Account Number: {{ currentBroker.commission_account_number || 'Not provided' }}
                  </li>
                  <li class="mb-2">
                    <i class="bi bi-upc me-2"></i>
                    BSB: {{ currentBroker.commission_bsb || 'Not provided' }}
                  </li>
                </ul>

                <h5 class="mt-4">Applications</h5>
                <div v-if="brokerApplications.length > 0">
                  <p>Total Applications: {{ brokerApplications.length }}</p>
                  <button class="btn btn-sm btn-outline-primary" @click="viewBrokerApplications">
                    View Applications
                  </button>
                </div>
                <p v-else class="text-muted">No applications found for this broker</p>
              </div>
            </div>

            <div class="mt-4" v-if="brokerStats">
              <h5>Performance Statistics</h5>
              <div class="row">
                <div class="col-md-4">
                  <div class="card bg-light">
                    <div class="card-body text-center">
                      <h6 class="card-title">Total Applications</h6>
                      <p class="display-6">{{ brokerStats.total_applications }}</p>
                    </div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="card bg-light">
                    <div class="card-body text-center">
                      <h6 class="card-title">Total Loan Amount</h6>
                      <p class="display-6">${{ formatCurrency(brokerStats.total_loan_amount) }}</p>
                    </div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="card bg-light">
                    <div class="card-body text-center">
                      <h6 class="card-title">Success Rate</h6>
                      <p class="display-6">{{ brokerStats.success_rate || 0 }}%</p>
                    </div>
                  </div>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Modal } from 'bootstrap'
import { useBrokerStore } from '@/store/broker'
import BrokerCard from '@/components/broker/BrokerCard.vue'
import BrokerForm from '@/components/broker/BrokerForm.vue'

export default {
  name: 'BrokerListView',
  components: {
    BrokerCard,
    BrokerForm
  },
  setup() {
    const router = useRouter()
    const brokerStore = useBrokerStore()
    
    // Refs for modals
    const brokerModal = ref(null)
    const viewBrokerModal = ref(null)
    let bsCreateEditModal = null
    let bsViewModal = null
    
    // State
    const searchQuery = ref('')
    const selectedBranch = ref('')
    const isEditing = ref(false)
    const currentBroker = ref(null)
    const formLoading = ref(false)
    const brokerApplications = ref([])
    const brokerStats = ref(null)
    
    // Computed properties
    const brokers = computed(() => brokerStore.brokers)
    const branches = computed(() => brokerStore.branches)
    const loading = computed(() => brokerStore.loading)
    const error = computed(() => brokerStore.error)
    const hasBrokers = computed(() => brokerStore.hasBrokers)
    const paginationInfo = computed(() => brokerStore.getPaginationInfo)
    
    // Initialize modals on component mount
    onMounted(() => {
      bsCreateEditModal = new Modal(brokerModal.value)
      bsViewModal = new Modal(viewBrokerModal.value)
      
      // Fetch brokers and branches
      fetchBrokers()
      fetchBranches()
    })
    
    // Methods
    const fetchBrokers = async () => {
      try {
        await brokerStore.fetchBrokers()
      } catch (error) {
        console.error('Error fetching brokers:', error)
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
      brokerStore.setFilters({ search: searchQuery.value })
    }
    
    const filterByBranch = () => {
      brokerStore.setFilters({ branch: selectedBranch.value || undefined })
    }
    
    const clearSearch = () => {
      searchQuery.value = ''
      brokerStore.setFilters({ search: '' })
    }
    
    const clearFilters = () => {
      searchQuery.value = ''
      selectedBranch.value = ''
      brokerStore.clearFilters()
    }
    
    const goToPage = (page) => {
      if (page < 1 || page > paginationInfo.value.totalPages) return
      brokerStore.setPage(page)
    }
    
    const showCreateModal = () => {
      isEditing.value = false
      currentBroker.value = null
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
    
    const handleFormSubmit = async (brokerData) => {
      formLoading.value = true
      try {
        if (isEditing.value && currentBroker.value) {
          await brokerStore.updateBroker(currentBroker.value.id, brokerData)
        } else {
          await brokerStore.createBroker(brokerData)
        }
        bsCreateEditModal.hide()
        fetchBrokers() // Refresh the list
      } catch (error) {
        console.error('Error saving broker:', error)
      } finally {
        formLoading.value = false
      }
    }
    
    const viewBroker = async (broker) => {
      currentBroker.value = broker
      
      // Fetch broker applications and stats
      try {
        brokerApplications.value = await brokerStore.fetchBrokerApplications(broker.id)
        brokerStats.value = await brokerStore.fetchBrokerStats(broker.id)
      } catch (error) {
        console.error('Error fetching broker details:', error)
      }
      
      bsViewModal.show()
    }
    
    const editBroker = (broker) => {
      isEditing.value = true
      currentBroker.value = broker
      bsCreateEditModal.show()
    }
    
    const deleteBroker = async (broker) => {
      try {
        await brokerStore.deleteBroker(broker.id)
        
        // If we're viewing the broker that was deleted, close the modal
        if (currentBroker.value && currentBroker.value.id === broker.id) {
          bsViewModal.hide()
        }
      } catch (error) {
        console.error('Error deleting broker:', error)
      }
    }
    
    const viewBrokerApplications = () => {
      if (currentBroker.value) {
        bsViewModal.hide()
        router.push({ name: 'ApplicationList', query: { broker: currentBroker.value.id } })
      }
    }
    
    const formatCurrency = (value) => {
      return value ? value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : '0.00'
    }
    
    return {
      brokers,
      branches,
      loading,
      error,
      hasBrokers,
      paginationInfo,
      searchQuery,
      selectedBranch,
      isEditing,
      currentBroker,
      formLoading,
      brokerApplications,
      brokerStats,
      brokerModal,
      viewBrokerModal,
      fetchBrokers,
      handleSearchInput,
      filterByBranch,
      clearSearch,
      clearFilters,
      goToPage,
      showCreateModal,
      showEditModal,
      hideModal,
      handleFormSubmit,
      viewBroker,
      editBroker,
      deleteBroker,
      viewBrokerApplications,
      formatCurrency
    }
  }
}
</script>

<style scoped>
.broker-list-view {
  min-height: 100vh;
}

.pagination {
  margin-bottom: 0;
}
</style>
