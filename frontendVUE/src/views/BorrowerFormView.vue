<template>
  <div class="borrower-form-view">
    <h1 class="text-2xl font-bold mb-6">{{ isEditing ? 'Edit Borrower' : 'Add New Borrower' }}</h1>
    
    <div class="bg-white shadow-md rounded-lg p-6">
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>
      
      <form @submit.prevent="saveBorrower">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Borrower Type
          </label>
          <div class="flex flex-col space-y-2">
            <label class="inline-flex items-center">
              <input 
                type="radio" 
                v-model="formData.borrower_type" 
                value="individual" 
                class="form-radio h-5 w-5 text-blue-600"
              />
              <span class="ml-2">Individual</span>
            </label>
            <label class="inline-flex items-center">
              <input 
                type="radio" 
                v-model="formData.borrower_type" 
                value="company" 
                class="form-radio h-5 w-5 text-blue-600"
              />
              <span class="ml-2">Company</span>
            </label>
          </div>
          <p v-if="errors.borrower_type" class="text-red-500 text-xs mt-1">
            {{ errors.borrower_type }}
          </p>
        </div>
        
        <div v-if="formData.borrower_type === 'individual'">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-gray-700 text-sm font-bold mb-2">
                First Name
              </label>
              <input 
                type="text" 
                v-model="formData.first_name" 
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter first name"
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
                v-model="formData.last_name" 
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter last name"
              />
              <p v-if="errors.last_name" class="text-red-500 text-xs mt-1">
                {{ errors.last_name }}
              </p>
            </div>
            
            <div>
              <label class="block text-gray-700 text-sm font-bold mb-2">
                Date of Birth
              </label>
              <input 
                type="date" 
                v-model="formData.date_of_birth" 
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              />
              <p v-if="errors.date_of_birth" class="text-red-500 text-xs mt-1">
                {{ errors.date_of_birth }}
              </p>
            </div>
          </div>
        </div>
        
        <div v-else-if="formData.borrower_type === 'company'">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">
              Company Name
            </label>
            <input 
              type="text" 
              v-model="formData.company_name" 
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Enter company name"
            />
            <p v-if="errors.company_name" class="text-red-500 text-xs mt-1">
              {{ errors.company_name }}
            </p>
          </div>
          
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">
              ABN/ACN
            </label>
            <input 
              type="text" 
              v-model="formData.abn_acn" 
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Enter ABN or ACN"
            />
            <p v-if="errors.abn_acn" class="text-red-500 text-xs mt-1">
              {{ errors.abn_acn }}
            </p>
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2">
              Email
            </label>
            <input 
              type="email" 
              v-model="formData.email" 
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Enter email"
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
              v-model="formData.phone" 
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Enter phone number"
            />
            <p v-if="errors.phone" class="text-red-500 text-xs mt-1">
              {{ errors.phone }}
            </p>
          </div>
        </div>
        
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Address
          </label>
          <input 
            type="text" 
            v-model="formData.address" 
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="Enter address"
          />
          <p v-if="errors.address" class="text-red-500 text-xs mt-1">
            {{ errors.address }}
          </p>
        </div>
        
        <div class="flex justify-between">
          <button 
            type="button" 
            @click="goBack" 
            class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-medium py-2 px-4 rounded"
          >
            Cancel
          </button>
          
          <button 
            type="submit" 
            :disabled="saving"
            class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded flex items-center"
          >
            <span v-if="saving" class="mr-2">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ isEditing ? 'Update Borrower' : 'Create Borrower' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

// State
const formData = ref({
  borrower_type: 'individual',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  date_of_birth: '',
  address: '',
  company_name: '',
  abn_acn: ''
})
const errors = ref({})
const error = ref('')
const saving = ref(false)
const borrowerId = ref(null)

// Computed
const isEditing = computed(() => {
  return !!borrowerId.value
})

// Methods
const fetchBorrower = async (id) => {
  try {
    const response = await axios.get(`/api/borrowers/borrowers/${id}/`)
    
    formData.value = {
      borrower_type: response.data.borrower_type || 'individual',
      first_name: response.data.first_name || '',
      last_name: response.data.last_name || '',
      email: response.data.email || '',
      phone: response.data.phone || '',
      date_of_birth: response.data.date_of_birth || '',
      address: response.data.address || '',
      company_name: response.data.company_name || '',
      abn_acn: response.data.abn_acn || ''
    }
  } catch (err) {
    console.error('Error fetching borrower:', err)
    error.value = 'Failed to load borrower details'
  }
}

const saveBorrower = async () => {
  saving.value = true
  errors.value = {}
  error.value = ''
  
  try {
    let response
    
    if (isEditing.value) {
      response = await axios.patch(`/api/borrowers/borrowers/${borrowerId.value}/`, formData.value)
    } else {
      response = await axios.post('/api/borrowers/borrowers/', formData.value)
    }
    
    // Redirect to borrower detail page
    router.push({ 
      name: 'borrower-detail', 
      params: { id: response.data.id },
      query: { created: !isEditing.value }
    })
  } catch (err) {
    console.error('Error saving borrower:', err)
    
    if (err.response?.data) {
      if (typeof err.response.data === 'string') {
        error.value = err.response.data
      } else if (typeof err.response.data === 'object') {
        errors.value = err.response.data
      } else {
        error.value = 'An error occurred while saving the borrower'
      }
    } else {
      error.value = 'An error occurred while saving the borrower'
    }
  } finally {
    saving.value = false
  }
}

const goBack = () => {
  router.back()
}

// Lifecycle
onMounted(() => {
  // Check if we're editing an existing borrower
  if (route.params.id) {
    borrowerId.value = route.params.id
    fetchBorrower(borrowerId.value)
  }
})
</script>
