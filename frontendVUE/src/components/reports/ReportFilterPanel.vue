<template>
  <div class="bg-white rounded-lg shadow-md p-6 mb-6">
    <h2 class="text-xl font-semibold mb-4">Report Filters</h2>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <!-- Date Range -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
        <input 
          type="date" 
          v-model="localFilters.startDate"
          class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">End Date</label>
        <input 
          type="date" 
          v-model="localFilters.endDate"
          class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      
      <!-- Time Grouping (if applicable) -->
      <div v-if="showTimeGrouping">
        <label class="block text-sm font-medium text-gray-700 mb-1">Time Grouping</label>
        <select 
          v-model="localFilters.timeGrouping"
          class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="day">Daily</option>
          <option value="week">Weekly</option>
          <option value="month">Monthly</option>
        </select>
      </div>
      
      <!-- BD Filter (if applicable) -->
      <div v-if="showBdFilter">
        <label class="block text-sm font-medium text-gray-700 mb-1">BD</label>
        <select 
          v-model="localFilters.bdId"
          class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All BDs</option>
          <option v-for="bd in bdOptions" :key="bd.id" :value="bd.id">{{ bd.name }}</option>
        </select>
      </div>
      
      <!-- Broker Filter (if applicable) -->
      <div v-if="showBrokerFilter">
        <label class="block text-sm font-medium text-gray-700 mb-1">Broker</label>
        <select 
          v-model="localFilters.brokerId"
          class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Brokers</option>
          <option v-for="broker in brokerOptions" :key="broker.id" :value="broker.id">{{ broker.name }}</option>
        </select>
      </div>
      
      <!-- Application Type Filter (if applicable) -->
      <div v-if="showApplicationTypeFilter">
        <label class="block text-sm font-medium text-gray-700 mb-1">Application Type</label>
        <select 
          v-model="localFilters.applicationType"
          class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Types</option>
          <option value="residential">Residential</option>
          <option value="commercial">Commercial</option>
          <option value="construction">Construction</option>
          <option value="refinance">Refinance</option>
          <option value="investment">Investment</option>
          <option value="smsf">SMSF</option>
        </select>
      </div>
      
      <!-- Apply Filters Button -->
      <div class="flex items-end">
        <button 
          @click="applyFilters"
          class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded transition-colors"
        >
          Apply Filters
        </button>
      </div>
      
      <!-- Reset Filters Button -->
      <div class="flex items-end">
        <button 
          @click="resetFilters"
          class="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded transition-colors"
        >
          Reset
        </button>
      </div>
    </div>
    
    <!-- Date Presets -->
    <div class="mt-4 flex flex-wrap gap-2">
      <button 
        @click="setDateRange('last7days')"
        class="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-3 rounded transition-colors"
      >
        Last 7 Days
      </button>
      <button 
        @click="setDateRange('last30days')"
        class="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-3 rounded transition-colors"
      >
        Last 30 Days
      </button>
      <button 
        @click="setDateRange('thisMonth')"
        class="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-3 rounded transition-colors"
      >
        This Month
      </button>
      <button 
        @click="setDateRange('lastMonth')"
        class="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-3 rounded transition-colors"
      >
        Last Month
      </button>
      <button 
        @click="setDateRange('thisQuarter')"
        class="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-3 rounded transition-colors"
      >
        This Quarter
      </button>
      <button 
        @click="setDateRange('thisYear')"
        class="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-3 rounded transition-colors"
      >
        This Year
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, onMounted, watch } from 'vue'
import api from '../../services/api'

const props = defineProps({
  filters: {
    type: Object,
    required: true
  },
  showTimeGrouping: {
    type: Boolean,
    default: false
  },
  showBdFilter: {
    type: Boolean,
    default: false
  },
  showBrokerFilter: {
    type: Boolean,
    default: false
  },
  showApplicationTypeFilter: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:filters', 'apply-filters'])

// Local copy of filters
const localFilters = ref({...props.filters})

// Options for dropdowns
const bdOptions = ref([])
const brokerOptions = ref([])

// Watch for changes in props.filters
watch(() => props.filters, (newFilters) => {
  localFilters.value = {...newFilters}
}, { deep: true })

// Apply filters
const applyFilters = () => {
  emit('update:filters', {...localFilters.value})
  emit('apply-filters')
}

// Reset filters
const resetFilters = () => {
  // Set default date range to last 6 months
  const today = new Date()
  const sixMonthsAgo = new Date()
  sixMonthsAgo.setMonth(today.getMonth() - 6)
  
  localFilters.value = {
    startDate: sixMonthsAgo.toISOString().split('T')[0],
    endDate: today.toISOString().split('T')[0],
    timeGrouping: 'month',
    bdId: '',
    brokerId: '',
    applicationType: ''
  }
  
  applyFilters()
}

// Set date range based on preset
const setDateRange = (preset) => {
  const today = new Date()
  let startDate = new Date()
  
  switch (preset) {
    case 'last7days':
      startDate.setDate(today.getDate() - 7)
      break
    case 'last30days':
      startDate.setDate(today.getDate() - 30)
      break
    case 'thisMonth':
      startDate = new Date(today.getFullYear(), today.getMonth(), 1)
      break
    case 'lastMonth':
      startDate = new Date(today.getFullYear(), today.getMonth() - 1, 1)
      today.setDate(0) // Last day of previous month
      break
    case 'thisQuarter':
      const quarter = Math.floor(today.getMonth() / 3)
      startDate = new Date(today.getFullYear(), quarter * 3, 1)
      break
    case 'thisYear':
      startDate = new Date(today.getFullYear(), 0, 1)
      break
    default:
      startDate.setMonth(today.getMonth() - 6)
  }
  
  localFilters.value.startDate = startDate.toISOString().split('T')[0]
  localFilters.value.endDate = today.toISOString().split('T')[0]
}

// Fetch BD options
const fetchBdOptions = async () => {
  if (!props.showBdFilter) return
  
  try {
    const response = await api.get('/api/brokers/bdm/')
    bdOptions.value = response.data.results || []
  } catch (error) {
    console.error('Error fetching BD options:', error)
    // Use placeholder data if API call fails
    bdOptions.value = [
      { id: 1, name: 'John Smith' },
      { id: 2, name: 'Sarah Johnson' },
      { id: 3, name: 'Michael Brown' }
    ]
  }
}

// Fetch broker options
const fetchBrokerOptions = async () => {
  if (!props.showBrokerFilter) return
  
  try {
    const response = await api.get('/api/brokers/')
    brokerOptions.value = response.data.results || []
  } catch (error) {
    console.error('Error fetching broker options:', error)
    // Use placeholder data if API call fails
    brokerOptions.value = [
      { id: 1, name: 'ABC Brokers' },
      { id: 2, name: 'XYZ Financial' },
      { id: 3, name: 'City Loans' }
    ]
  }
}

onMounted(() => {
  fetchBdOptions()
  fetchBrokerOptions()
})
</script>
