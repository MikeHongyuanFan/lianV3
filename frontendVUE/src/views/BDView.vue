<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Business Development Dashboard</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium mb-2">Active Applications</h3>
        <p class="text-3xl font-bold">{{ stats.active || 0 }}</p>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium mb-2">Pending Approvals</h3>
        <p class="text-3xl font-bold">{{ stats.pending || 0 }}</p>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium mb-2">Settled This Month</h3>
        <p class="text-3xl font-bold">{{ stats.settled || 0 }}</p>
      </div>
    </div>
    
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold mb-4">Applications Requiring Attention</h2>
      
      <div v-if="loading" class="py-4 text-center">
        Loading applications...
      </div>
      
      <div v-else-if="applications.length === 0" class="py-4 text-center">
        No applications require attention at this time.
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full bg-white">
          <thead>
            <tr>
              <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Reference
              </th>
              <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Borrower
              </th>
              <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Broker
              </th>
              <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Amount
              </th>
              <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Stage
              </th>
              <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in applications" :key="app.id" class="hover:bg-gray-50">
              <td class="py-2 px-4 border-b border-gray-200">
                {{ app.reference_number }}
              </td>
              <td class="py-2 px-4 border-b border-gray-200">
                {{ app.borrower_name || 'N/A' }}
              </td>
              <td class="py-2 px-4 border-b border-gray-200">
                {{ app.broker_name || 'N/A' }}
              </td>
              <td class="py-2 px-4 border-b border-gray-200">
                ${{ app.loan_amount }}
              </td>
              <td class="py-2 px-4 border-b border-gray-200">
                <span 
                  :class="{
                    'px-2 py-1 text-xs rounded-full': true,
                    'bg-yellow-100 text-yellow-800': app.stage === 'inquiry',
                    'bg-blue-100 text-blue-800': app.stage === 'application',
                    'bg-purple-100 text-purple-800': app.stage === 'assessment',
                    'bg-green-100 text-green-800': app.stage === 'approved',
                    'bg-red-100 text-red-800': app.stage === 'declined'
                  }"
                >
                  {{ app.stage }}
                </span>
              </td>
              <td class="py-2 px-4 border-b border-gray-200">
                <button 
                  class="text-blue-600 hover:text-blue-900"
                  @click="viewApplication(app.id)"
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

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const applications = ref([])
const loading = ref(true)
const stats = ref({
  active: 0,
  pending: 0,
  settled: 0
})

onMounted(async () => {
  try {
    // In a real app, these would be filtered by the BD's ID
    const response = await api.get('/applications/')
    applications.value = response
    
    // Calculate stats
    if (applications.value.length) {
      stats.value = {
        active: applications.value.filter(app => ['application', 'assessment', 'approved'].includes(app.stage)).length,
        pending: applications.value.filter(app => app.stage === 'assessment').length,
        settled: applications.value.filter(app => app.stage === 'settlement').length
      }
    }
  } catch (error) {
    console.error('Error fetching applications:', error)
  } finally {
    loading.value = false
  }
})

function viewApplication(id) {
  // Navigate to application detail page
  console.log('View application:', id)
}
</script>
