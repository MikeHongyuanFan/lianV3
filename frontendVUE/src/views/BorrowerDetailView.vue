<template>
  <div class="borrower-detail-view">
    <div v-if="loading" class="flex justify-center my-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>
    
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>
    
    <div v-else>
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">
          {{ borrower.first_name }} {{ borrower.last_name }}
        </h1>
        
        <div class="flex space-x-2">
          <button 
            v-if="canEdit" 
            @click="toggleEditMode" 
            class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded"
          >
            {{ isEditing ? 'Cancel' : 'Edit' }}
          </button>
          
          <button 
            v-if="isEditing" 
            @click="saveBorrower" 
            :disabled="saving"
            class="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded flex items-center"
          >
            <span v-if="saving" class="mr-2">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            Save
          </button>
        </div>
      </div>
      
      <div class="bg-white shadow-md rounded-lg overflow-hidden">
        <!-- Borrower Information -->
        <div class="p-6">
          <h2 class="text-xl font-semibold mb-4">Borrower Information</h2>
          
          <div v-if="isEditing">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div>
                <label class="block text-gray-700 text-sm font-bold mb-2">
                  First Name
                </label>
                <input 
                  type="text" 
                  v-model="editForm.first_name" 
                  class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                />
                <p v-if="errors.first_name" class="text-red-500 text-xs mt-1">
                  {{ errors.first_name }}
                </p>
              </div>
              
              <div>
                <label class="block text-gray-700 text-sm font-bold mb-2">
                  Last Name
                </label>
                <input 
                  type="text" 
                  v-model="editForm.last_name" 
                  class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                />
                <p v-if="errors.last_name" class="text-red-500 text-xs mt-1">
                  {{ errors.last_name }}
                </p>
              </div>
              
              <div>
                <label class="block text-gray-700 text-sm font-bold mb-2">
                  Email
                </label>
                <input 
                  type="email" 
                  v-model="editForm.email" 
                  class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                />
                <p v-if="errors.email" class="text-red-500 text-xs mt-1">
                  {{ errors.email }}
                </p>
              </div>
              
              <div>
                <label class="block text-gray-700 text-sm font-bold mb-2">
                  Phone
                </label>
                <input 
                  type="tel" 
                  v-model="editForm.phone" 
                  class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                />
                <p v-if="errors.phone" class="text-red-500 text-xs mt-1">
                  {{ errors.phone }}
                </p>
              </div>
              
              <div>
                <label class="block text-gray-700 text-sm font-bold mb-2">
                  Date of Birth
                </label>
                <input 
                  type="date" 
                  v-model="editForm.date_of_birth" 
                  class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                />
                <p v-if="errors.date_of_birth" class="text-red-500 text-xs mt-1">
                  {{ errors.date_of_birth }}
                </p>
              </div>
              
              <div>
                <label class="block text-gray-700 text-sm font-bold mb-2">
                  Address
                </label>
                <input 
                  type="text" 
                  v-model="editForm.address" 
                  class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                />
                <p v-if="errors.address" class="text-red-500 text-xs mt-1">
                  {{ errors.address }}
                </p>
              </div>
            </div>
          </div>
          
          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600">First Name:</p>
              <p class="font-medium">{{ borrower.first_name }}</p>
            </div>
            
            <div>
              <p class="text-sm text-gray-600">Last Name:</p>
              <p class="font-medium">{{ borrower.last_name }}</p>
            </div>
            
            <div>
              <p class="text-sm text-gray-600">Email:</p>
              <p class="font-medium">{{ borrower.email }}</p>
            </div>
            
            <div>
              <p class="text-sm text-gray-600">Phone:</p>
              <p class="font-medium">{{ borrower.phone }}</p>
            </div>
            
            <div>
              <p class="text-sm text-gray-600">Date of Birth:</p>
              <p class="font-medium">{{ formatDate(borrower.date_of_birth) }}</p>
            </div>
            
            <div>
              <p class="text-sm text-gray-600">Address:</p>
              <p class="font-medium">{{ borrower.address || 'Not provided' }}</p>
            </div>
          </div>
        </div>
        
        <!-- Applications -->
        <div class="border-t border-gray-200 p-6">
          <h2 class="text-xl font-semibold mb-4">Applications</h2>
          
          <div v-if="loadingApplications" class="flex justify-center my-6">
            <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
          </div>
          
          <div v-else-if="applications.length === 0" class="text-center my-6">
            <p class="text-gray-500">No applications found for this borrower</p>
            <button 
              @click="createNewApplication" 
              class="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded"
            >
              Create New Application
            </button>
          </div>
          
          <div v-else class="overflow-x-auto">
            <table class="min-w-full bg-white">
              <thead>
                <tr>
                  <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
                    ID
                  </th>
                  <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
                    Type
                  </th>
                  <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
                    Loan Amount
                  </th>
                  <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
                    Status
                  </th>
                  <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
                    Created
                  </th>
                  <th class="py-3 px-4 bg-gray-100 text-left text-xs font-medium text-gray-600 uppercase tracking-wider border-b">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="application in applications" :key="application.id" class="hover:bg-gray-50">
                  <td class="py-4 px-4 border-b border-gray-200">
                    {{ application.id }}
                  </td>
                  <td class="py-4 px-4 border-b border-gray-200 capitalize">
                    {{ application.application_type }}
                  </td>
                  <td class="py-4 px-4 border-b border-gray-200">
                    {{ formatCurrency(application.loan_amount) }}
                  </td>
                  <td class="py-4 px-4 border-b border-gray-200">
                    <span 
                      :class="getStatusClass(application.stage)" 
                      class="px-2 py-1 text-xs font-medium rounded-full"
                    >
                      {{ formatStatus(application.stage) }}
                    </span>
                  </td>
                  <td class="py-4 px-4 border-b border-gray-200">
                    {{ formatDate(application.created_at) }}
                  </td>
                  <td class="py-4 px-4 border-b border-gray-200">
                    <button 
                      @click="viewApplication(application.id)" 
                      class="text-blue-600 hover:text-blue-800"
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../store/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// State
const borrower = ref({})
const applications = ref([])
const loading = ref(true)
const loadingApplications = ref(true)
const error = ref('')
const isEditing = ref(false)
const editForm = ref({})
const errors = ref({})
const saving = ref(false)

// Computed
const canEdit = computed(() => {
  if (authStore.isAdmin) return true
  if (authStore.isBroker && borrower.value.created_by === authStore.userId) return true
  return false
})

// Methods
const fetchBorrower = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await axios.get(`/api/borrowers/borrowers/${route.params.id}/`)
    borrower.value = response.data
    
    // Initialize edit form with borrower data
    editForm.value = {
      first_name: borrower.value.first_name,
      last_name: borrower.value.last_name,
      email: borrower.value.email,
      phone: borrower.value.phone,
      date_of_birth: borrower.value.date_of_birth,
      address: borrower.value.address
    }
    
    // Check if edit mode should be enabled from query param
    if (route.query.edit === 'true' && canEdit.value) {
      isEditing.value = true
    }
  } catch (error) {
    console.error('Error fetching borrower:', error)
    error.value = 'Failed to load borrower details'
  } finally {
    loading.value = false
  }
}

const fetchApplications = async () => {
  loadingApplications.value = true
  
  try {
    const response = await axios.get(`/api/borrowers/borrowers/${route.params.id}/applications/`)
    applications.value = response.data
  } catch (error) {
    console.error('Error fetching applications:', error)
  } finally {
    loadingApplications.value = false
  }
}

const toggleEditMode = () => {
  if (isEditing.value) {
    // Reset form to original values
    editForm.value = {
      first_name: borrower.value.first_name,
      last_name: borrower.value.last_name,
      email: borrower.value.email,
      phone: borrower.value.phone,
      date_of_birth: borrower.value.date_of_birth,
      address: borrower.value.address
    }
    errors.value = {}
  }
  
  isEditing.value = !isEditing.value
}

const saveBorrower = async () => {
  saving.value = true
  errors.value = {}
  
  try {
    const response = await axios.patch(`/api/borrowers/borrowers/${route.params.id}/`, editForm.value)
    borrower.value = response.data
    isEditing.value = false
  } catch (error) {
    console.error('Error updating borrower:', error)
    
    if (error.response?.data) {
      errors.value = error.response.data
    } else {
      errors.value = { general: 'An error occurred while saving' }
    }
  } finally {
    saving.value = false
  }
}

const createNewApplication = () => {
  router.push({ 
    name: 'application-new',
    query: { borrower_id: borrower.value.id }
  })
}

const viewApplication = (id) => {
  router.push({ name: 'application-detail', params: { id } })
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0
  }).format(amount)
}

const formatDate = (dateString) => {
  if (!dateString) return 'Not provided'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

const formatStatus = (status) => {
  if (!status) return ''
  return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const getStatusClass = (status) => {
  switch (status) {
    case 'inquiry':
      return 'bg-gray-100 text-gray-800'
    case 'pre_approval':
      return 'bg-blue-100 text-blue-800'
    case 'processing':
      return 'bg-yellow-100 text-yellow-800'
    case 'approved':
      return 'bg-green-100 text-green-800'
    case 'settled':
      return 'bg-purple-100 text-purple-800'
    case 'declined':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

// Lifecycle
onMounted(() => {
  fetchBorrower()
  fetchApplications()
})
</script>
