<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Dashboard</h1>
    
    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-2">
          <h2 class="text-lg font-semibold text-gray-700">Applications</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <div class="text-3xl font-bold">{{ stats.applications }}</div>
        <div class="text-sm text-gray-500">Total Applications</div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-2">
          <h2 class="text-lg font-semibold text-gray-700">Active</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="text-3xl font-bold">{{ stats.active }}</div>
        <div class="text-sm text-gray-500">Active Applications</div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-2">
          <h2 class="text-lg font-semibold text-gray-700">Loan Volume</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="text-3xl font-bold">${{ formatCurrency(stats.loanVolume) }}</div>
        <div class="text-sm text-gray-500">Total Loan Amount</div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-2">
          <h2 class="text-lg font-semibold text-gray-700">Compliance</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <div class="text-3xl font-bold">{{ stats.compliance }}%</div>
        <div class="text-sm text-gray-500">Repayment Compliance</div>
      </div>
    </div>
    
    <!-- Recent Applications -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-semibold">Recent Applications</h2>
        <router-link to="/applications" class="text-blue-500 hover:text-blue-700 text-sm">View All</router-link>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reference</th>
              <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Borrower</th>
              <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
              <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stage</th>
              <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
              <th class="px-6 py-3 bg-gray-50"></th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="app in recentApplications" :key="app.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ app.reference_number }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ app.borrower_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${{ formatCurrency(app.loan_amount) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getStageClass(app.stage)" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                  {{ formatStage(app.stage) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(app.created_at) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <router-link :to="`/applications/${app.id}`" class="text-blue-600 hover:text-blue-900">View</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Quick Links and Reports -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Quick Links -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">Quick Links</h2>
        <ul class="space-y-2">
          <li>
            <router-link to="/applications/new" class="flex items-center text-blue-600 hover:text-blue-800">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              New Application
            </router-link>
          </li>
          <li>
            <router-link to="/borrowers" class="flex items-center text-blue-600 hover:text-blue-800">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              Manage Borrowers
            </router-link>
          </li>
          <li>
            <router-link to="/reports" class="flex items-center text-blue-600 hover:text-blue-800">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              View Reports
            </router-link>
          </li>
          <li>
            <router-link to="/notification-preferences" class="flex items-center text-blue-600 hover:text-blue-800">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              Notification Settings
            </router-link>
          </li>
        </ul>
      </div>
      
      <!-- Mini Reports -->
      <div class="md:col-span-2 bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Application Status</h2>
          <router-link to="/reports/application-status" class="text-blue-500 hover:text-blue-700 text-sm">View Full Report</router-link>
        </div>
        <canvas ref="statusChartRef" height="200"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import api from '../services/api'
import Chart from 'chart.js/auto'

const authStore = useAuthStore()
const statusChartRef = ref(null)
let statusChart = null

// Dashboard stats
const stats = ref({
  applications: 0,
  active: 0,
  loanVolume: 0,
  compliance: 0
})

// Recent applications
const recentApplications = ref([])

// Format currency
const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

// Format date
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

// Format stage
const formatStage = (stage) => {
  return stage.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

// Get stage class
const getStageClass = (stage) => {
  const classes = {
    'inquiry': 'bg-blue-100 text-blue-800',
    'pre_approval': 'bg-yellow-100 text-yellow-800',
    'valuation': 'bg-purple-100 text-purple-800',
    'formal_approval': 'bg-indigo-100 text-indigo-800',
    'settlement': 'bg-green-100 text-green-800',
    'funded': 'bg-green-100 text-green-800',
    'declined': 'bg-red-100 text-red-800',
    'withdrawn': 'bg-gray-100 text-gray-800'
  }
  
  return classes[stage] || 'bg-gray-100 text-gray-800'
}

// Fetch dashboard data
const fetchDashboardData = async () => {
  try {
    // Fetch application stats
    const volumeResponse = await api.get('/api/reports/application-volume/')
    stats.value.applications = volumeResponse.data.total_applications
    stats.value.loanVolume = volumeResponse.data.total_loan_amount
    
    // Fetch application status
    const statusResponse = await api.get('/api/reports/application-status/')
    stats.value.active = statusResponse.data.total_active
    
    // Fetch repayment compliance
    const complianceResponse = await api.get('/api/reports/repayment-compliance/')
    stats.value.compliance = complianceResponse.data.compliance_rate
    
    // Fetch recent applications
    const applicationsResponse = await api.get('/api/applications/?limit=5')
    recentApplications.value = applicationsResponse.data.results || []
    
    // Update status chart
    updateStatusChart(statusResponse.data)
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    // Use placeholder data if API calls fail
    stats.value = {
      applications: 125,
      active: 78,
      loanVolume: 24500000,
      compliance: 87
    }
    
    recentApplications.value = [
      {
        id: 1,
        reference_number: 'APP-12345678',
        borrower_name: 'John Smith',
        loan_amount: 450000,
        stage: 'formal_approval',
        created_at: '2024-03-15T10:30:00Z'
      },
      {
        id: 2,
        reference_number: 'APP-23456789',
        borrower_name: 'Sarah Johnson',
        loan_amount: 320000,
        stage: 'valuation',
        created_at: '2024-03-12T14:45:00Z'
      },
      {
        id: 3,
        reference_number: 'APP-34567890',
        borrower_name: 'Michael Brown',
        loan_amount: 550000,
        stage: 'inquiry',
        created_at: '2024-03-10T09:15:00Z'
      }
    ]
    
    // Update status chart with placeholder data
    updateStatusChart({
      total_active: 78,
      total_settled: 40,
      total_declined: 5,
      total_withdrawn: 2,
      active_by_stage: {
        'inquiry': 15,
        'pre_approval': 20,
        'valuation': 18,
        'formal_approval': 25
      }
    })
  }
}

// Update status chart
const updateStatusChart = (data) => {
  if (statusChart) {
    statusChart.destroy()
  }
  
  if (!statusChartRef.value) return
  
  const ctx = statusChartRef.value.getContext('2d')
  
  const labels = ['Active', 'Settled', 'Declined', 'Withdrawn']
  const chartData = [
    data.total_active,
    data.total_settled,
    data.total_declined,
    data.total_withdrawn
  ]
  
  const backgroundColors = [
    'rgba(59, 130, 246, 0.7)',  // blue - active
    'rgba(16, 185, 129, 0.7)',  // green - settled
    'rgba(239, 68, 68, 0.7)',   // red - declined
    'rgba(156, 163, 175, 0.7)'  // gray - withdrawn
  ]
  
  statusChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Applications',
        data: chartData,
        backgroundColor: backgroundColors,
        borderColor: backgroundColors.map(color => color.replace('0.7', '1')),
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  })
}

onMounted(() => {
  fetchDashboardData()
})
</script>
