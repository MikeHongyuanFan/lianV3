<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold">Reports & Analytics</h1>
      <div class="text-sm text-gray-500">
        Last updated: {{ formatDate(new Date()) }}
      </div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Repayment Compliance Report Card -->
      <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Repayment Compliance</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <p class="text-gray-600 mb-4">Track repayment compliance rates, late payments, and payment trends over time.</p>
        <router-link :to="{ name: 'repayment-compliance-report' }" class="block w-full text-center bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded transition-colors">
          View Report
        </router-link>
      </div>
      
      <!-- Application Volume Report Card -->
      <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Application Volume</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
          </svg>
        </div>
        <p class="text-gray-600 mb-4">Analyze application volume by stage, time period, BD, and application type.</p>
        <router-link :to="{ name: 'application-volume-report' }" class="block w-full text-center bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-4 rounded transition-colors">
          View Report
        </router-link>
      </div>
      
      <!-- Application Status Report Card -->
      <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Application Status</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <p class="text-gray-600 mb-4">Monitor active, settled, declined, and withdrawn applications with conversion rates.</p>
        <router-link :to="{ name: 'application-status-report' }" class="block w-full text-center bg-purple-500 hover:bg-purple-600 text-white font-medium py-2 px-4 rounded transition-colors">
          View Report
        </router-link>
      </div>
    </div>
    
    <div class="mt-12">
      <h2 class="text-2xl font-bold mb-4">Quick Stats</h2>
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="text-center">
            <div class="text-3xl font-bold text-blue-500">{{ quickStats.totalApplications }}</div>
            <div class="text-gray-600">Total Applications</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-green-500">${{ formatCurrency(quickStats.totalLoanAmount) }}</div>
            <div class="text-gray-600">Total Loan Amount</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-purple-500">{{ quickStats.activeApplications }}</div>
            <div class="text-gray-600">Active Applications</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-red-500">{{ quickStats.complianceRate }}%</div>
            <div class="text-gray-600">Repayment Compliance</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

// Quick stats data
const quickStats = ref({
  totalApplications: 0,
  totalLoanAmount: 0,
  activeApplications: 0,
  complianceRate: 0
})

// Format currency
const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

// Format date
const formatDate = (date) => {
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Fetch quick stats data
const fetchQuickStats = async () => {
  try {
    // Fetch application volume data
    const volumeResponse = await api.get('/api/reports/application-volume/')
    quickStats.value.totalApplications = volumeResponse.data.total_applications
    quickStats.value.totalLoanAmount = volumeResponse.data.total_loan_amount
    
    // Fetch application status data
    const statusResponse = await api.get('/api/reports/application-status/')
    quickStats.value.activeApplications = statusResponse.data.total_active
    
    // Fetch repayment compliance data
    const complianceResponse = await api.get('/api/reports/repayment-compliance/')
    quickStats.value.complianceRate = complianceResponse.data.compliance_rate
  } catch (error) {
    console.error('Error fetching quick stats:', error)
    // Use placeholder data if API calls fail
    quickStats.value = {
      totalApplications: 125,
      totalLoanAmount: 24500000,
      activeApplications: 42,
      complianceRate: 94
    }
  }
}

onMounted(() => {
  fetchQuickStats()
})
</script>
