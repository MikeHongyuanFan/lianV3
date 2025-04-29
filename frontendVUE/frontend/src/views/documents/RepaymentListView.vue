<template>
  <MainLayout>
    <div class="repayment-list-view">
      <div class="container mx-auto px-4 py-6">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold">Repayments</h1>
          <button
            @click="navigateToCreateRepayment"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none flex items-center"
          >
            <span class="material-icons mr-1">add</span>
            Create Repayment
          </button>
        </div>
        
        <!-- Filters -->
        <div class="bg-white p-4 rounded-lg shadow mb-6">
          <h2 class="text-lg font-semibold mb-4">Filters</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
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
        
        <!-- Repayment List -->
        <RepaymentList
          :repayments="repayments"
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
          @create="navigateToCreateRepayment"
          @view="navigateToRepaymentDetail"
          @mark-paid="handleMarkPaid"
          @edit="navigateToEditRepayment"
          @delete="confirmDeleteRepayment"
          @view-application="navigateToApplication"
          @prev-page="handlePrevPage"
          @next-page="handleNextPage"
          @fetch="fetchRepayments"
        />
        
        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
            <h3 class="text-lg font-semibold mb-4">Confirm Delete</h3>
            <p class="mb-6">Are you sure you want to delete this repayment? This action cannot be undone.</p>
            <div class="flex justify-end space-x-3">
              <button
                @click="showDeleteModal = false"
                class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
              >
                Cancel
              </button>
              <button
                @click="deleteRepayment"
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
            <h3 class="text-lg font-semibold mb-4">Mark Repayment as Paid</h3>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Payment Date</label>
              <input
                v-model="paymentDate"
                type="date"
                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Payment Method</label>
              <select
                v-model="paymentMethod"
                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select Payment Method</option>
                <option value="bank_transfer">Bank Transfer</option>
                <option value="credit_card">Credit Card</option>
                <option value="direct_debit">Direct Debit</option>
                <option value="cash">Cash</option>
                <option value="check">Check</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div class="flex justify-end space-x-3">
              <button
                @click="showMarkPaidModal = false"
                class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
              >
                Cancel
              </button>
              <button
                @click="markRepaymentPaid"
                class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none"
              >
                Mark as Paid
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script>
import { ref, computed, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useRepaymentStore } from '@/store/repayment'
import RepaymentList from '@/components/documents/RepaymentList.vue'
import MainLayout from '@/layouts/MainLayout.vue'

export default {
  name: 'RepaymentListView',
  components: {
    RepaymentList,
    MainLayout
  },
  setup() {
    const router = useRouter()
    const repaymentStore = useRepaymentStore()
    
    // State
    const filters = reactive({
      isPaid: null,
      application: null,
      dateFrom: '',
      dateTo: ''
    })
    
    const showDeleteModal = ref(false)
    const repaymentToDelete = ref(null)
    
    const showMarkPaidModal = ref(false)
    const repaymentToMarkPaid = ref(null)
    const paymentDate = ref(new Date().toISOString().split('T')[0]) // Today's date
    const paymentMethod = ref('')
    
    // Computed properties
    const repayments = computed(() => repaymentStore.repayments)
    const loading = computed(() => repaymentStore.loading)
    const error = computed(() => repaymentStore.error)
    const paginationInfo = computed(() => repaymentStore.getPaginationInfo)
    const totalAmount = computed(() => repaymentStore.getTotalAmount)
    const totalPaidAmount = computed(() => repaymentStore.getTotalPaidAmount)
    const totalUnpaidAmount = computed(() => repaymentStore.getTotalUnpaidAmount)
    
    // Methods
    const fetchRepayments = async () => {
      try {
        await repaymentStore.fetchRepayments()
      } catch (error) {
        console.error('Error fetching repayments:', error)
      }
    }
    
    const applyFilters = () => {
      repaymentStore.setFilters({
        isPaid: filters.isPaid,
        application: filters.application,
        dateFrom: filters.dateFrom,
        dateTo: filters.dateTo
      })
    }
    
    const clearFilters = () => {
      filters.isPaid = null
      filters.application = null
      filters.dateFrom = ''
      filters.dateTo = ''
      repaymentStore.clearFilters()
    }
    
    const navigateToCreateRepayment = () => {
      router.push({ name: 'repayment-create' })
    }
    
    const navigateToRepaymentDetail = (id) => {
      router.push({ name: 'repayment-detail', params: { id } })
    }
    
    const navigateToEditRepayment = (id) => {
      router.push({ name: 'repayment-edit', params: { id } })
    }
    
    const navigateToApplication = (id) => {
      router.push({ name: 'application-detail', params: { id } })
    }
    
    const confirmDeleteRepayment = (repayment) => {
      repaymentToDelete.value = repayment
      showDeleteModal.value = true
    }
    
    const deleteRepayment = async () => {
      if (!repaymentToDelete.value) return
      
      try {
        await repaymentStore.deleteRepayment(repaymentToDelete.value.id)
        showDeleteModal.value = false
        repaymentToDelete.value = null
      } catch (error) {
        console.error('Error deleting repayment:', error)
      }
    }
    
    const handleMarkPaid = (id) => {
      repaymentToMarkPaid.value = id
      showMarkPaidModal.value = true
    }
    
    const markRepaymentPaid = async () => {
      if (!repaymentToMarkPaid.value) return
      
      try {
        await repaymentStore.markRepaymentPaid(repaymentToMarkPaid.value, { 
          paid_date: paymentDate.value,
          payment_method: paymentMethod.value || undefined
        })
        showMarkPaidModal.value = false
        repaymentToMarkPaid.value = null
        paymentMethod.value = ''
      } catch (error) {
        console.error('Error marking repayment as paid:', error)
      }
    }
    
    const handlePrevPage = () => {
      if (paginationInfo.value.currentPage > 1) {
        repaymentStore.setPage(paginationInfo.value.currentPage - 1)
      }
    }
    
    const handleNextPage = () => {
      if (paginationInfo.value.currentPage < paginationInfo.value.totalPages) {
        repaymentStore.setPage(paginationInfo.value.currentPage + 1)
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      fetchRepayments()
    })
    
    return {
      repayments,
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
      paymentMethod,
      fetchRepayments,
      applyFilters,
      clearFilters,
      navigateToCreateRepayment,
      navigateToRepaymentDetail,
      navigateToEditRepayment,
      navigateToApplication,
      confirmDeleteRepayment,
      deleteRepayment,
      handleMarkPaid,
      markRepaymentPaid,
      handlePrevPage,
      handleNextPage
    }
  }
}
</script>

<style scoped>
/* Add any view-specific styles here */
</style>
