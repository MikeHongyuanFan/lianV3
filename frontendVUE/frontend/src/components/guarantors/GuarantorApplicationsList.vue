<template>
  <div class="guarantor-applications-list">
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchApplications" class="underline">Try again</button>
    </div>
    
    <!-- Empty state -->
    <div v-else-if="!applications.length" class="text-center py-8 bg-gray-50 rounded-lg">
      <p class="text-gray-500 mb-4">No applications found for this guarantor</p>
      <button
        @click="navigateToCreateApplication"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
      >
        Create New Application
      </button>
    </div>
    
    <!-- Applications list -->
    <div v-else>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Guaranteed Applications</h2>
        <button
          @click="navigateToCreateApplication"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
        >
          Create New Application
        </button>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reference</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Purpose</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stage</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="application in applications" :key="application.id">
              <td class="px-6 py-4 whitespace-nowrap">{{ application.reference_number }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ application.application_type }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ application.purpose }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(application.loan_amount) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2 py-1 text-xs rounded-full"
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
              </td>
              <td class="px-6 py-4 whitespace-nowrap">{{ formatDate(application.created_at) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <button
                  @click="navigateToApplication(application.id)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  View
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import guarantorService from '@/services/guarantor.service'

export default {
  name: 'GuarantorApplicationsList',
  props: {
    guarantorId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const router = useRouter()
    const applications = ref([])
    const loading = ref(false)
    const error = ref(null)
    
    const fetchApplications = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await guarantorService.getGuaranteedApplications(props.guarantorId)
        applications.value = response
      } catch (err) {
        console.error('Error fetching applications:', err)
        error.value = err.message || 'Failed to load applications'
      } finally {
        loading.value = false
      }
    }
    
    const navigateToApplication = (applicationId) => {
      router.push({ name: 'application-detail', params: { id: applicationId } })
    }
    
    const navigateToCreateApplication = () => {
      router.push({ 
        name: 'application-create',
        query: { guarantor: props.guarantorId }
      })
    }
    
    const formatCurrency = (amount) => {
      if (amount === null || amount === undefined) return 'Not provided'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Not provided'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
    
    const formatStage = (stage) => {
      if (!stage) return 'Unknown'
      
      // Convert snake_case to Title Case
      return stage
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    onMounted(() => {
      fetchApplications()
    })
    
    return {
      applications,
      loading,
      error,
      fetchApplications,
      navigateToApplication,
      navigateToCreateApplication,
      formatCurrency,
      formatDate,
      formatStage
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
