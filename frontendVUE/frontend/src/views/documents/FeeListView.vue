<template>
  <div class="fee-list-view">
    <div class="container mx-auto px-4 py-6">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">Fees</h1>
        <button
          @click="navigateToCreateFee"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none flex items-center"
        >
          <span class="material-icons mr-1">add</span>
          Create Fee
        </button>
      </div>
      
      <!-- Filters -->
      <div class="bg-white p-4 rounded-lg shadow mb-6">
        <h2 class="text-lg font-semibold mb-4">Filters</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Fee Type</label>
            <select
              v-model="filters.feeType"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Types</option>
              <option value="application">Application</option>
              <option value="valuation">Valuation</option>
              <option value="legal">Legal</option>
              <option value="broker">Broker</option>
              <option value="settlement">Settlement</option>
              <option value="other">Other</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Payment Status</label>
            <select
              v-model="filters.isPaid"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option :value="null">All Statuses</option>
              <option :value="true">Paid</option>
              <option :value="false">Pending</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Application</label>
            <input
              v-model="filters.application"
              type="number"
              placeholder="Application ID"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Date From</label>
            <input
              v-model="filters.dateFrom"
              type="date"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Date To</label>
            <input
              v-model="filters.dateTo"
              type="date"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div class="flex items-end space-x-2">
            <button
              @click="applyFilters"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
            >
              Apply Filters
            </button>
            <button
              @click="clearFilters"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
            >
              Clear
            </button>
          </div>
        </div>
      </div>
      
      <!-- Fee List -->
      <FeeList
        :fees="fees"
        :loading="loading"
        :error="error"
        :show-actions="true"
        :can-edit="true"
        :can-delete="true"
        :show-create-button="true"
        :show-pagination="true"
        :show-summary="true"
        :current-page="paginationInfo.currentPage"
        :total-pages="paginationInfo.totalPages"
        :items-per-page="paginationInfo.itemsPerPage"
        :total-items="paginationInfo.totalItems"
        :total-amount="totalAmount"
        :total-paid-amount="totalPaidAmount"
        :total-unpaid-amount="totalUnpaidAmount"
        @create="navigateToCreateFee"
        @view="navigateToFeeDetail"
        @mark-paid="handleMarkPaid"
        @edit="navigateToEditFee"
        @delete="confirmDeleteFee"
        @view-application="navigateToApplication"
        @prev-page="handlePrevPage"
        @next-page="handleNextPage"
        @fetch="fetchFees"
      />
      
      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
          <h3 class="text-lg font-semibold mb-4">Confirm Delete</h3>
          <p class="mb-6">Are you sure you want to delete this fee? This action cannot be undone.</p>
          <div class="flex justify-end space-x-3">
            <button
              @click="showDeleteModal = false"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
            >
              Cancel
            </button>
            <button
              @click="deleteFee"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
      
      <!-- Mark as Paid Modal -->
      <div v-if="showMarkPaidModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
          <h3 class="text-lg font-semibold mb-4">Mark Fee as Paid</h3>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Payment Date</label>
            <input
              v-model="paymentDate"
              type="date"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div class="flex justify-end space-x-3">
            <button
              @click="showMarkPaidModal = false"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
            >
              Cancel
            </button>
            <button
              @click="markFeePaid"
              class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none"
            >
              Mark as Paid
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useFeeStore } from '@/store/fee'
import FeeList from '@/components/documents/FeeList.vue'

export default {
  name: 'FeeListView',
  components: {
    FeeList
  },
  setup() {
    const router = useRouter()
    const feeStore = useFeeStore()
    
    // State
    const filters = reactive({
      feeType: '',
      isPaid: null,
      application: null,
      dateFrom: '',
      dateTo: ''
    })
    
    const showDeleteModal = ref(false)
    const feeToDelete = ref(null)
    
    const showMarkPaidModal = ref(false)
    const feeToMarkPaid = ref(null)
    const paymentDate = ref(new Date().toISOString().split('T')[0]) // Today's date
    
    // Computed properties
    const fees = computed(() => feeStore.fees)
    const loading = computed(() => feeStore.loading)
    const error = computed(() => feeStore.error)
    const paginationInfo = computed(() => feeStore.getPaginationInfo)
    const totalAmount = computed(() => feeStore.getTotalAmount)
    const totalPaidAmount = computed(() => feeStore.getTotalPaidAmount)
    const totalUnpaidAmount = computed(() => feeStore.getTotalUnpaidAmount)
    
    // Methods
    const fetchFees = async () => {
      try {
        await feeStore.fetchFees()
      } catch (error) {
        console.error('Error fetching fees:', error)
      }
    }
    
    const applyFilters = () => {
      feeStore.setFilters({
        feeType: filters.feeType,
        isPaid: filters.isPaid,
        application: filters.application,
        dateFrom: filters.dateFrom,
        dateTo: filters.dateTo
      })
    }
    
    const clearFilters = () => {
      filters.feeType = ''
      filters.isPaid = null
      filters.application = null
      filters.dateFrom = ''
      filters.dateTo = ''
      feeStore.clearFilters()
    }
    
    const navigateToCreateFee = () => {
      router.push({ name: 'fee-create' })
    }
    
    const navigateToFeeDetail = (id) => {
      router.push({ name: 'fee-detail', params: { id } })
    }
    
    const navigateToEditFee = (id) => {
      router.push({ name: 'fee-edit', params: { id } })
    }
    
    const navigateToApplication = (id) => {
      router.push({ name: 'application-detail', params: { id } })
    }
    
    const confirmDeleteFee = (fee) => {
      feeToDelete.value = fee
      showDeleteModal.value = true
    }
    
    const deleteFee = async () => {
      if (!feeToDelete.value) return
      
      try {
        await feeStore.deleteFee(feeToDelete.value.id)
        showDeleteModal.value = false
        feeToDelete.value = null
      } catch (error) {
        console.error('Error deleting fee:', error)
      }
    }
    
    const handleMarkPaid = (id) => {
      feeToMarkPaid.value = id
      showMarkPaidModal.value = true
    }
    
    const markFeePaid = async () => {
      if (!feeToMarkPaid.value) return
      
      try {
        await feeStore.markFeePaid(feeToMarkPaid.value, { paid_date: paymentDate.value })
        showMarkPaidModal.value = false
        feeToMarkPaid.value = null
      } catch (error) {
        console.error('Error marking fee as paid:', error)
      }
    }
    
    const handlePrevPage = () => {
      if (paginationInfo.value.currentPage > 1) {
        feeStore.setPage(paginationInfo.value.currentPage - 1)
      }
    }
    
    const handleNextPage = () => {
      if (paginationInfo.value.currentPage < paginationInfo.value.totalPages) {
        feeStore.setPage(paginationInfo.value.currentPage + 1)
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      fetchFees()
    })
    
    return {
      fees,
      loading,
      error,
      filters,
      paginationInfo,
      totalAmount,
      totalPaidAmount,
      totalUnpaidAmount,
      showDeleteModal,
      showMarkPaidModal,
      paymentDate,
      fetchFees,
      applyFilters,
      clearFilters,
      navigateToCreateFee,
      navigateToFeeDetail,
      navigateToEditFee,
      navigateToApplication,
      confirmDeleteFee,
      deleteFee,
      handleMarkPaid,
      markFeePaid,
      handlePrevPage,
      handleNextPage
    }
  }
}
</script>

<style scoped>
/* Add any view-specific styles here */
</style>
