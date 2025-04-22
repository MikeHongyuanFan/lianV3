<template>
  <div class="application-form-view">
    <h1 class="text-2xl font-bold mb-6">New Loan Application</h1>
    
    <div class="bg-white shadow-md rounded-lg p-6">
      <div class="mb-6">
        <div class="flex items-center mb-4">
          <div 
            v-for="(step, index) in steps" 
            :key="index" 
            class="flex items-center"
          >
            <div 
              :class="[
                'w-8 h-8 rounded-full flex items-center justify-center font-medium text-sm',
                currentStep > index 
                  ? 'bg-green-500 text-white' 
                  : currentStep === index 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-200 text-gray-600'
              ]"
            >
              {{ index + 1 }}
            </div>
            <div 
              v-if="index < steps.length - 1" 
              :class="[
                'h-1 w-12', 
                currentStep > index ? 'bg-green-500' : 'bg-gray-200'
              ]"
            ></div>
          </div>
        </div>
        
        <div class="flex justify-between text-sm text-gray-600 px-1">
          <div 
            v-for="(step, index) in steps" 
            :key="index"
            :class="[
              'text-center',
              currentStep >= index ? 'text-blue-600 font-medium' : ''
            ]"
            style="width: 120px"
          >
            {{ step }}
          </div>
        </div>
      </div>
      
      <!-- Step 1: Application Type -->
      <div v-if="currentStep === 0">
        <h2 class="text-xl font-semibold mb-4">Application Type</h2>
        
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Application Type
          </label>
          <div class="flex flex-col space-y-2">
            <label class="inline-flex items-center">
              <input 
                type="radio" 
                v-model="formData.application_type" 
                value="residential" 
                class="form-radio h-5 w-5 text-blue-600"
              />
              <span class="ml-2">Residential</span>
            </label>
            <label class="inline-flex items-center">
              <input 
                type="radio" 
                v-model="formData.application_type" 
                value="commercial" 
                class="form-radio h-5 w-5 text-blue-600"
              />
              <span class="ml-2">Commercial</span>
            </label>
            <label class="inline-flex items-center">
              <input 
                type="radio" 
                v-model="formData.application_type" 
                value="personal" 
                class="form-radio h-5 w-5 text-blue-600"
              />
              <span class="ml-2">Personal</span>
            </label>
          </div>
          <p v-if="errors.application_type" class="text-red-500 text-xs mt-1">
            {{ errors.application_type }}
          </p>
        </div>
        
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Purpose
          </label>
          <select 
            v-model="formData.purpose" 
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          >
            <option value="">Select a purpose</option>
            <option value="Purchase of primary residence">Purchase of primary residence</option>
            <option value="Purchase of investment property">Purchase of investment property</option>
            <option value="Refinance of primary residence">Refinance of primary residence</option>
            <option value="Refinance of investment property">Refinance of investment property</option>
            <option value="Home improvement">Home improvement</option>
            <option value="Debt consolidation">Debt consolidation</option>
            <option value="Business expansion">Business expansion</option>
            <option value="Working capital">Working capital</option>
            <option value="Equipment purchase">Equipment purchase</option>
            <option value="Other">Other</option>
          </select>
          <p v-if="errors.purpose" class="text-red-500 text-xs mt-1">
            {{ errors.purpose }}
          </p>
        </div>
      </div>
      
      <!-- Step 2: Loan Details -->
      <div v-if="currentStep === 1">
        <h2 class="text-xl font-semibold mb-4">Loan Details</h2>
        
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Loan Amount
          </label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-600">$</span>
            <input 
              type="number" 
              v-model="formData.loan_amount" 
              class="shadow appearance-none border rounded w-full py-2 pl-8 pr-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Enter loan amount"
            />
          </div>
          <p v-if="errors.loan_amount" class="text-red-500 text-xs mt-1">
            {{ errors.loan_amount }}
          </p>
        </div>
        
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Loan Term (years)
          </label>
          <input 
            type="number" 
            v-model="formData.loan_term" 
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="Enter loan term in years"
          />
          <p v-if="errors.loan_term" class="text-red-500 text-xs mt-1">
            {{ errors.loan_term }}
          </p>
        </div>
        
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Interest Rate (%)
          </label>
          <input 
            type="number" 
            v-model="formData.interest_rate" 
            step="0.01"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="Enter interest rate"
          />
          <p v-if="errors.interest_rate" class="text-red-500 text-xs mt-1">
            {{ errors.interest_rate }}
          </p>
        </div>
        
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Repayment Frequency
          </label>
          <select 
            v-model="formData.repayment_frequency" 
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          >
            <option value="">Select frequency</option>
            <option value="weekly">Weekly</option>
            <option value="fortnightly">Fortnightly</option>
            <option value="monthly">Monthly</option>
            <option value="quarterly">Quarterly</option>
          </select>
          <p v-if="errors.repayment_frequency" class="text-red-500 text-xs mt-1">
            {{ errors.repayment_frequency }}
          </p>
        </div>
      </div>
      
      <!-- Step 3: Borrower Information -->
      <div v-if="currentStep === 2">
        <h2 class="text-xl font-semibold mb-4">Borrower Information</h2>
        
        <div v-if="loading" class="flex justify-center my-12">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
        
        <div v-else>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">
              Select Existing Borrowers
            </label>
            <div v-if="availableBorrowers.length === 0" class="text-gray-500 text-sm">
              No existing borrowers found. Please add a new borrower below.
            </div>
            <div v-else class="max-h-60 overflow-y-auto border rounded p-2">
              <div 
                v-for="borrower in availableBorrowers" 
                :key="borrower.id"
                class="flex items-center p-2 hover:bg-gray-100"
              >
                <input 
                  type="checkbox" 
                  :value="borrower.id" 
                  v-model="formData.borrower_ids" 
                  class="form-checkbox h-5 w-5 text-blue-600"
                />
                <span class="ml-2">
                  {{ borrower.first_name }} {{ borrower.last_name }} ({{ borrower.email }})
                </span>
              </div>
            </div>
          </div>
          
          <div class="mb-4">
            <div class="flex items-center justify-between">
              <label class="block text-gray-700 text-sm font-bold">
                Add New Borrower
              </label>
              <button 
                type="button" 
                @click="addNewBorrowerForm" 
                class="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                + Add Another Borrower
              </button>
            </div>
            
            <div 
              v-for="(borrower, index) in formData.new_borrowers" 
              :key="index"
              class="border rounded p-4 mt-2"
            >
              <div class="flex justify-between items-center mb-3">
                <h3 class="font-medium">New Borrower #{{ index + 1 }}</h3>
                <button 
                  type="button" 
                  @click="removeBorrowerForm(index)" 
                  class="text-red-600 hover:text-red-800"
                >
                  Remove
                </button>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-2">
                    First Name
                  </label>
                  <input 
                    type="text" 
                    v-model="borrower.first_name" 
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    placeholder="Enter first name"
                  />
                  <p v-if="borrowerErrors[index]?.first_name" class="text-red-500 text-xs mt-1">
                    {{ borrowerErrors[index].first_name }}
                  </p>
                </div>
                
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-2">
                    Last Name
                  </label>
                  <input 
                    type="text" 
                    v-model="borrower.last_name" 
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    placeholder="Enter last name"
                  />
                  <p v-if="borrowerErrors[index]?.last_name" class="text-red-500 text-xs mt-1">
                    {{ borrowerErrors[index].last_name }}
                  </p>
                </div>
                
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-2">
                    Email
                  </label>
                  <input 
                    type="email" 
                    v-model="borrower.email" 
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    placeholder="Enter email"
                  />
                  <p v-if="borrowerErrors[index]?.email" class="text-red-500 text-xs mt-1">
                    {{ borrowerErrors[index].email }}
                  </p>
                </div>
                
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-2">
                    Phone
                  </label>
                  <input 
                    type="tel" 
                    v-model="borrower.phone" 
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    placeholder="Enter phone number"
                  />
                  <p v-if="borrowerErrors[index]?.phone" class="text-red-500 text-xs mt-1">
                    {{ borrowerErrors[index].phone }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <p v-if="errors.borrowers" class="text-red-500 text-sm mt-1">
            {{ errors.borrowers }}
          </p>
        </div>
      </div>
      
      <!-- Step 4: Review & Submit -->
      <div v-if="currentStep === 3">
        <h2 class="text-xl font-semibold mb-4">Review & Submit</h2>
        
        <div class="bg-gray-50 p-4 rounded mb-6">
          <h3 class="font-medium mb-2">Application Type</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600">Type:</p>
              <p class="font-medium capitalize">{{ formData.application_type }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Purpose:</p>
              <p class="font-medium">{{ formData.purpose }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-gray-50 p-4 rounded mb-6">
          <h3 class="font-medium mb-2">Loan Details</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600">Loan Amount:</p>
              <p class="font-medium">{{ formatCurrency(formData.loan_amount) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Loan Term:</p>
              <p class="font-medium">{{ formData.loan_term }} years</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Interest Rate:</p>
              <p class="font-medium">{{ formData.interest_rate }}%</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Repayment Frequency:</p>
              <p class="font-medium capitalize">{{ formData.repayment_frequency }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-gray-50 p-4 rounded mb-6">
          <h3 class="font-medium mb-2">Borrowers</h3>
          
          <div v-if="selectedExistingBorrowers.length > 0">
            <h4 class="text-sm font-medium text-gray-600 mb-2">Existing Borrowers:</h4>
            <ul class="list-disc list-inside mb-4">
              <li v-for="borrower in selectedExistingBorrowers" :key="borrower.id">
                {{ borrower.first_name }} {{ borrower.last_name }} ({{ borrower.email }})
              </li>
            </ul>
          </div>
          
          <div v-if="formData.new_borrowers.length > 0">
            <h4 class="text-sm font-medium text-gray-600 mb-2">New Borrowers:</h4>
            <ul class="list-disc list-inside">
              <li v-for="(borrower, index) in formData.new_borrowers" :key="index">
                {{ borrower.first_name }} {{ borrower.last_name }} ({{ borrower.email }})
              </li>
            </ul>
          </div>
          
          <div v-if="selectedExistingBorrowers.length === 0 && formData.new_borrowers.length === 0">
            <p class="text-red-500">No borrowers selected. Please go back and add at least one borrower.</p>
          </div>
        </div>
        
        <div v-if="submitError" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {{ submitError }}
        </div>
      </div>
      
      <!-- Navigation Buttons -->
      <div class="flex justify-between mt-8">
        <button 
          v-if="currentStep > 0" 
          @click="prevStep" 
          class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-medium py-2 px-4 rounded"
        >
          Back
        </button>
        <div v-else></div>
        
        <button 
          v-if="currentStep < steps.length - 1" 
          @click="nextStep" 
          class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded"
        >
          Next
        </button>
        
        <button 
          v-else 
          @click="submitApplication" 
          :disabled="submitting"
          class="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded flex items-center"
        >
          <span v-if="submitting" class="mr-2">
            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </span>
          Submit Application
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// State
const steps = ['Application Type', 'Loan Details', 'Borrower Information', 'Review & Submit']
const currentStep = ref(0)
const formData = ref({
  application_type: '',
  purpose: '',
  loan_amount: null,
  loan_term: null,
  interest_rate: null,
  repayment_frequency: '',
  borrower_ids: [],
  new_borrowers: []
})
const errors = ref({})
const borrowerErrors = ref([])
const availableBorrowers = ref([])
const loading = ref(false)
const submitting = ref(false)
const submitError = ref('')

// Computed
const selectedExistingBorrowers = computed(() => {
  return availableBorrowers.value.filter(borrower => 
    formData.value.borrower_ids.includes(borrower.id)
  )
})

// Methods
const fetchBorrowers = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/borrowers/borrowers/')
    availableBorrowers.value = response.data.results || response.data
  } catch (error) {
    console.error('Error fetching borrowers:', error)
  } finally {
    loading.value = false
  }
}

const addNewBorrowerForm = () => {
  formData.value.new_borrowers.push({
    first_name: '',
    last_name: '',
    email: '',
    phone: ''
  })
  borrowerErrors.value.push({})
}

const removeBorrowerForm = (index) => {
  formData.value.new_borrowers.splice(index, 1)
  borrowerErrors.value.splice(index, 1)
}

const validateStep = () => {
  errors.value = {}
  
  if (currentStep.value === 0) {
    if (!formData.value.application_type) {
      errors.value.application_type = 'Application type is required'
    }
    if (!formData.value.purpose) {
      errors.value.purpose = 'Purpose is required'
    }
  } else if (currentStep.value === 1) {
    if (!formData.value.loan_amount) {
      errors.value.loan_amount = 'Loan amount is required'
    } else if (formData.value.loan_amount <= 0) {
      errors.value.loan_amount = 'Loan amount must be greater than 0'
    }
    
    if (!formData.value.loan_term) {
      errors.value.loan_term = 'Loan term is required'
    } else if (formData.value.loan_term <= 0) {
      errors.value.loan_term = 'Loan term must be greater than 0'
    }
    
    if (!formData.value.interest_rate) {
      errors.value.interest_rate = 'Interest rate is required'
    } else if (formData.value.interest_rate < 0) {
      errors.value.interest_rate = 'Interest rate cannot be negative'
    }
    
    if (!formData.value.repayment_frequency) {
      errors.value.repayment_frequency = 'Repayment frequency is required'
    }
  } else if (currentStep.value === 2) {
    borrowerErrors.value = formData.value.new_borrowers.map(borrower => {
      const errors = {}
      
      if (!borrower.first_name) {
        errors.first_name = 'First name is required'
      }
      
      if (!borrower.last_name) {
        errors.last_name = 'Last name is required'
      }
      
      if (!borrower.email) {
        errors.email = 'Email is required'
      } else if (!isValidEmail(borrower.email)) {
        errors.email = 'Please enter a valid email'
      }
      
      if (!borrower.phone) {
        errors.phone = 'Phone is required'
      }
      
      return errors
    })
    
    // Check if any borrower is selected or added
    if (formData.value.borrower_ids.length === 0 && formData.value.new_borrowers.length === 0) {
      errors.value.borrowers = 'At least one borrower is required'
      return false
    }
    
    // Check if any new borrower has validation errors
    const hasNewBorrowerErrors = borrowerErrors.value.some(error => Object.keys(error).length > 0)
    if (hasNewBorrowerErrors) {
      return false
    }
  }
  
  return Object.keys(errors.value).length === 0
}

const nextStep = () => {
  if (validateStep()) {
    currentStep.value++
    
    // Fetch borrowers when reaching the borrower step
    if (currentStep.value === 2) {
      fetchBorrowers()
    }
  }
}

const prevStep = () => {
  currentStep.value--
}

const submitApplication = async () => {
  if (!validateStep()) {
    return
  }
  
  submitting.value = true
  submitError.value = ''
  
  try {
    // Prepare data for submission
    const applicationData = {
      application_type: formData.value.application_type,
      purpose: formData.value.purpose,
      loan_amount: formData.value.loan_amount,
      loan_term: formData.value.loan_term,
      interest_rate: formData.value.interest_rate,
      repayment_frequency: formData.value.repayment_frequency,
      borrower_ids: formData.value.borrower_ids,
      new_borrowers: formData.value.new_borrowers
    }
    
    // Submit application
    const response = await axios.post('/api/applications/applications/', applicationData)
    
    // Redirect to application detail page
    router.push({ 
      name: 'application-detail', 
      params: { id: response.data.id },
      query: { created: 'true' }
    })
  } catch (error) {
    console.error('Error submitting application:', error)
    
    if (error.response?.data) {
      if (typeof error.response.data === 'string') {
        submitError.value = error.response.data
      } else if (typeof error.response.data === 'object') {
        submitError.value = 'Please correct the errors in the form'
        errors.value = error.response.data
      } else {
        submitError.value = 'An error occurred while submitting the application'
      }
    } else {
      submitError.value = 'An error occurred while submitting the application'
    }
  } finally {
    submitting.value = false
  }
}

const formatCurrency = (amount) => {
  if (!amount) return '$0'
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0
  }).format(amount)
}

const isValidEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

// Lifecycle
onMounted(() => {
  // Add initial borrower form
  if (formData.value.new_borrowers.length === 0) {
    addNewBorrowerForm()
  }
})
</script>
