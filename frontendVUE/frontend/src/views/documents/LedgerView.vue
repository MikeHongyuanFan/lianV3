<template>
  <MainLayout>
    <div class="ledger-view-container">
      <div class="page-header flex justify-between items-start mb-6">
        <div>
          <h1 class="text-2xl font-bold">Application Ledger</h1>
          <div v-if="application" class="text-gray-600 mt-1">
            Reference: <span class="font-medium">{{ application.reference_number }}</span>
          </div>
        </div>
        <div class="flex space-x-2">
          <button
            @click="goBack"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
          >
            Back to Application
          </button>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="loader"></div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        <p>{{ error }}</p>
        <button @click="fetchApplicationData" class="underline">Try again</button>
      </div>

      <!-- Application details -->
      <div v-else-if="application" class="application-details">
        <!-- Application summary -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold">Application Summary</h2>
            <span
              class="px-3 py-1 text-sm rounded-full"
              :class="{
                'bg-yellow-100 text-yellow-800': application.stage === 'inquiry',
                'bg-blue-100 text-blue-800': application.stage === 'pre_approval',
                'bg-purple-100 text-purple-800': application.stage === 'valuation',
                'bg-indigo-100 text-indigo-800': application.stage === 'formal_approval',
                'bg-green-100 text-green-800': application.stage === 'settlement',
                'bg-teal-100 text-teal-800': application.stage === 'funded',
                'bg-red-100 text-red-800': application.stage === 'declined',
                'bg-gray-100 text-gray-800': application.stage === 'withdrawn'
              }"
            >
              {{ application.stage_display || formatStage(application.stage) }}
            </span>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-4">
            <div>
              <p><strong>Loan Amount:</strong> {{ formatCurrency(application.loan_amount) }}</p>
              <p><strong>Loan Term:</strong> {{ application.loan_term }} months</p>
            </div>
            <div>
              <p><strong>Interest Rate:</strong> {{ application.interest_rate }}%</p>
              <p><strong>Repayment Frequency:</strong> {{ formatRepaymentFrequency(application.repayment_frequency) }}</p>
            </div>
            <div>
              <p><strong>Created:</strong> {{ formatDate(application.created_at) }}</p>
              <p><strong>Estimated Settlement:</strong> {{ formatDate(application.estimated_settlement_date) }}</p>
            </div>
          </div>
        </div>
        
        <!-- Ledger component -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <ApplicationLedgerView :applicationId="applicationId" />
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApplicationStore } from '@/store/application'
import MainLayout from '@/layouts/MainLayout.vue'
import ApplicationLedgerView from '@/components/ApplicationLedgerView.vue'

export default {
  name: 'LedgerView',
  components: {
    MainLayout,
    ApplicationLedgerView
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const applicationStore = useApplicationStore()
    
    // Local state
    const applicationId = ref(parseInt(route.params.id))
    
    // Computed properties
    const application = computed(() => applicationStore.currentApplication)
    const loading = computed(() => applicationStore.loading)
    const error = computed(() => applicationStore.error)
    
    // Methods
    const fetchApplicationData = async () => {
      try {
        await applicationStore.fetchApplication(applicationId.value)
      } catch (error) {
        console.error('Error fetching application:', error)
      }
    }
    
    const goBack = () => {
      router.push({ name: 'application-detail', params: { id: applicationId.value } })
    }
    
    const formatStage = (stage) => {
      if (!stage) return 'Unknown'
      return stage
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    const formatRepaymentFrequency = (frequency) => {
      if (!frequency) return 'Unknown'
      return frequency.charAt(0).toUpperCase() + frequency.slice(1)
    }
    
    const formatCurrency = (amount) => {
      if (amount === null || amount === undefined) return 'N/A'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
    
    // Lifecycle hooks
    onMounted(() => {
      fetchApplicationData()
    })
    
    return {
      applicationId,
      application,
      loading,
      error,
      fetchApplicationData,
      goBack,
      formatStage,
      formatRepaymentFrequency,
      formatCurrency,
      formatDate
    }
  }
}
</script>

<style scoped>
.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
