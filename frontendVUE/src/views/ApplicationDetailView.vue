<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>
    
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      <p>{{ error }}</p>
    </div>
    
    <div v-else>
      <!-- Application Header -->
      <div class="bg-white shadow rounded-lg p-6 mb-6">
        <div class="flex justify-between items-center mb-4">
          <h1 class="text-2xl font-bold text-gray-800">
            Application: {{ application.reference_number }}
          </h1>
          <span 
            class="px-3 py-1 rounded-full text-sm font-medium" 
            :class="getStageClass(application.stage)"
          >
            {{ application.stage_display }}
          </span>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div class="border-r border-gray-200 pr-4">
            <h3 class="text-sm font-medium text-gray-500">Loan Details</h3>
            <p class="mt-1 text-lg font-semibold">${{ formatCurrency(application.loan_amount) }}</p>
            <p class="text-sm text-gray-600">{{ application.loan_term }} months @ {{ application.interest_rate }}%</p>
            <p class="text-sm text-gray-600">Purpose: {{ application.purpose }}</p>
          </div>
          
          <div class="border-r border-gray-200 pr-4">
            <h3 class="text-sm font-medium text-gray-500">Key Dates</h3>
            <p class="text-sm text-gray-600">Created: {{ formatDate(application.created_at) }}</p>
            <p class="text-sm text-gray-600">Updated: {{ formatDate(application.updated_at) }}</p>
            <p class="text-sm text-gray-600">Est. Settlement: {{ formatDate(application.estimated_settlement_date) }}</p>
          </div>
          
          <div>
            <h3 class="text-sm font-medium text-gray-500">Assigned To</h3>
            <p class="text-sm text-gray-600">Broker: {{ application.broker?.name || 'N/A' }}</p>
            <p class="text-sm text-gray-600">BD: {{ application.bd?.name || 'N/A' }}</p>
            <p class="text-sm text-gray-600">Branch: {{ application.branch?.name || 'N/A' }}</p>
          </div>
        </div>
      </div>
      
      <!-- Tabs Navigation -->
      <div class="bg-white shadow rounded-lg mb-6">
        <nav class="flex border-b border-gray-200">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            class="px-4 py-3 text-sm font-medium"
            :class="activeTab === tab.id ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'"
          >
            {{ tab.name }}
          </button>
        </nav>
        
        <!-- Tab Content -->
        <div class="p-6">
          <!-- Overview Tab -->
          <div v-if="activeTab === 'overview'">
            <application-overview :application="application" />
          </div>
          
          <!-- Borrowers Tab -->
          <div v-if="activeTab === 'borrowers'">
            <borrowers-tab :borrowers="application.borrowers" :guarantors="application.guarantors" />
          </div>
          
          <!-- Documents Tab -->
          <div v-if="activeTab === 'documents'">
            <documents-tab :documents="application.documents" :application-id="application.id" @document-uploaded="fetchApplicationDetails" />
          </div>
          
          <!-- Notes Tab -->
          <div v-if="activeTab === 'notes'">
            <notes-tab :notes="application.notes" :application-id="application.id" @note-added="fetchApplicationDetails" />
          </div>
          
          <!-- Repayments Tab -->
          <div v-if="activeTab === 'repayments'">
            <repayments-tab :repayments="application.repayments" :application-id="application.id" @repayment-added="fetchApplicationDetails" />
          </div>
          
          <!-- Fees Tab -->
          <div v-if="activeTab === 'fees'">
            <fees-tab :fees="application.fees" :application-id="application.id" @fee-added="fetchApplicationDetails" />
          </div>
          
          <!-- Ledger Tab -->
          <div v-if="activeTab === 'ledger'">
            <ledger-tab :ledger-entries="application.ledger_entries" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import ApplicationOverview from '../components/application/detail/ApplicationOverview.vue'
import BorrowersTab from '../components/application/detail/BorrowersTab.vue'
import DocumentsTab from '../components/application/detail/DocumentsTab.vue'
import NotesTab from '../components/application/detail/NotesTab.vue'
import RepaymentsTab from '../components/application/detail/RepaymentsTab.vue'
import FeesTab from '../components/application/detail/FeesTab.vue'
import LedgerTab from '../components/application/detail/LedgerTab.vue'

const route = useRoute()
const applicationId = route.params.id
const application = ref({})
const loading = ref(true)
const error = ref(null)

const tabs = [
  { id: 'overview', name: 'Overview' },
  { id: 'borrowers', name: 'Borrowers & Guarantors' },
  { id: 'documents', name: 'Documents' },
  { id: 'notes', name: 'Notes' },
  { id: 'repayments', name: 'Repayments' },
  { id: 'fees', name: 'Fees' },
  { id: 'ledger', name: 'Ledger' }
]

const activeTab = ref('overview')

const fetchApplicationDetails = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get(`/api/applications/${applicationId}/`)
    application.value = response.data
  } catch (err) {
    console.error('Error fetching application details:', err)
    error.value = 'Failed to load application details. Please try again.'
  } finally {
    loading.value = false
  }
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US').format(value)
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const getStageClass = (stage) => {
  const stageClasses = {
    'inquiry': 'bg-gray-100 text-gray-800',
    'application': 'bg-blue-100 text-blue-800',
    'processing': 'bg-yellow-100 text-yellow-800',
    'approved': 'bg-green-100 text-green-800',
    'settled': 'bg-purple-100 text-purple-800',
    'declined': 'bg-red-100 text-red-800'
  }
  
  return stageClasses[stage] || 'bg-gray-100 text-gray-800'
}

onMounted(() => {
  fetchApplicationDetails()
})
</script>
