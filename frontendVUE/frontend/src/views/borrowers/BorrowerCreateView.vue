<template>
  <div class="borrower-create-container">
    <h1 class="text-2xl font-bold mb-6">{{ isEditing ? 'Edit Borrower' : 'Create New Borrower' }}</h1>
    
    <!-- Error alert -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p class="font-bold">Error</p>
      <p>{{ error }}</p>
    </div>
    
    <!-- Borrower form -->
    <form @submit.prevent="submitForm" class="bg-white rounded-lg shadow-md p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Basic Information -->
        <div class="col-span-2">
          <h2 class="text-lg font-semibold mb-4">Basic Information</h2>
        </div>
        
        <!-- First Name -->
        <div class="form-group">
          <label for="first_name" class="block text-sm font-medium text-gray-700 mb-1">First Name *</label>
          <input
            id="first_name"
            v-model="borrowerForm.first_name"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.first_name }"
            required
          />
          <p v-if="validationErrors.first_name" class="mt-1 text-sm text-red-600">{{ validationErrors.first_name }}</p>
        </div>
        
        <!-- Last Name -->
        <div class="form-group">
          <label for="last_name" class="block text-sm font-medium text-gray-700 mb-1">Last Name *</label>
          <input
            id="last_name"
            v-model="borrowerForm.last_name"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.last_name }"
            required
          />
          <p v-if="validationErrors.last_name" class="mt-1 text-sm text-red-600">{{ validationErrors.last_name }}</p>
        </div>
        
        <!-- Email -->
        <div class="form-group">
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email *</label>
          <input
            id="email"
            v-model="borrowerForm.email"
            type="email"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.email }"
            required
          />
          <p v-if="validationErrors.email" class="mt-1 text-sm text-red-600">{{ validationErrors.email }}</p>
        </div>
        
        <!-- Phone Number -->
        <div class="form-group">
          <label for="phone_number" class="block text-sm font-medium text-gray-700 mb-1">Phone Number *</label>
          <input
            id="phone_number"
            v-model="borrowerForm.phone_number"
            type="tel"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.phone_number }"
            required
          />
          <p v-if="validationErrors.phone_number" class="mt-1 text-sm text-red-600">{{ validationErrors.phone_number }}</p>
        </div>
        
        <!-- Address -->
        <div class="form-group col-span-2">
          <label for="address" class="block text-sm font-medium text-gray-700 mb-1">Address *</label>
          <input
            id="address"
            v-model="borrowerForm.address"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.address }"
            required
          />
          <p v-if="validationErrors.address" class="mt-1 text-sm text-red-600">{{ validationErrors.address }}</p>
        </div>
        
        <!-- Borrower Type -->
        <div class="form-group">
          <label for="borrower_type" class="block text-sm font-medium text-gray-700 mb-1">Borrower Type *</label>
          <select
            id="borrower_type"
            v-model="borrowerForm.borrower_type"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.borrower_type }"
            required
          >
            <option value="">Select Type</option>
            <option value="individual">Individual</option>
            <option value="company">Company</option>
            <option value="trust">Trust</option>
          </select>
          <p v-if="validationErrors.borrower_type" class="mt-1 text-sm text-red-600">{{ validationErrors.borrower_type }}</p>
        </div>
        
        <!-- Date of Birth -->
        <div class="form-group">
          <label for="date_of_birth" class="block text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
          <input
            id="date_of_birth"
            v-model="borrowerForm.date_of_birth"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.date_of_birth }"
          />
          <p v-if="validationErrors.date_of_birth" class="mt-1 text-sm text-red-600">{{ validationErrors.date_of_birth }}</p>
        </div>
        
        <!-- Additional Information -->
        <div class="col-span-2 mt-4">
          <h2 class="text-lg font-semibold mb-4">Additional Information</h2>
        </div>
        
        <!-- Employment Status -->
        <div class="form-group">
          <label for="employment_status" class="block text-sm font-medium text-gray-700 mb-1">Employment Status</label>
          <select
            id="employment_status"
            v-model="borrowerForm.employment_status"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.employment_status }"
          >
            <option value="">Select Status</option>
            <option value="employed">Employed</option>
            <option value="self_employed">Self-Employed</option>
            <option value="unemployed">Unemployed</option>
            <option value="retired">Retired</option>
            <option value="student">Student</option>
          </select>
          <p v-if="validationErrors.employment_status" class="mt-1 text-sm text-red-600">{{ validationErrors.employment_status }}</p>
        </div>
        
        <!-- Annual Income -->
        <div class="form-group">
          <label for="annual_income" class="block text-sm font-medium text-gray-700 mb-1">Annual Income</label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">$</span>
            <input
              id="annual_income"
              v-model="borrowerForm.annual_income"
              type="number"
              step="0.01"
              min="0"
              class="w-full pl-8 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="{ 'border-red-500': validationErrors.annual_income }"
            />
          </div>
          <p v-if="validationErrors.annual_income" class="mt-1 text-sm text-red-600">{{ validationErrors.annual_income }}</p>
        </div>
        
        <!-- Credit Score -->
        <div class="form-group">
          <label for="credit_score" class="block text-sm font-medium text-gray-700 mb-1">Credit Score</label>
          <input
            id="credit_score"
            v-model="borrowerForm.credit_score"
            type="number"
            min="300"
            max="850"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.credit_score }"
          />
          <p v-if="validationErrors.credit_score" class="mt-1 text-sm text-red-600">{{ validationErrors.credit_score }}</p>
        </div>
      </div>
      
      <!-- Form actions -->
      <div class="mt-8 flex justify-end space-x-3">
        <button
          type="button"
          @click="navigateBack"
          class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
        >
          Cancel
        </button>
        <button
          type="submit"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
          :disabled="loading"
        >
          {{ loading ? (isEditing ? 'Updating...' : 'Creating...') : (isEditing ? 'Update Borrower' : 'Create Borrower') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBorrowerStore } from '@/store/borrower'

export default {
  name: 'BorrowerCreateView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const borrowerStore = useBorrowerStore()
    
    // Determine if we're editing or creating
    const isEditing = computed(() => !!route.params.id)
    const borrowerId = ref(isEditing.value ? parseInt(route.params.id) : null)
    
    // Form state
    const borrowerForm = ref({
      first_name: '',
      last_name: '',
      email: '',
      phone_number: '',
      address: '',
      borrower_type: '',
      date_of_birth: '',
      employment_status: '',
      annual_income: '',
      credit_score: ''
    })
    
    const validationErrors = ref({})
    const loading = computed(() => borrowerStore.loading)
    const error = computed(() => borrowerStore.error)
    
    // Methods
    const fetchBorrowerData = async () => {
      if (isEditing.value) {
        try {
          const borrower = await borrowerStore.fetchBorrowerById(borrowerId.value)
          
          // Populate form with borrower data
          borrowerForm.value = {
            first_name: borrower.first_name || '',
            last_name: borrower.last_name || '',
            email: borrower.email || '',
            phone_number: borrower.phone_number || '',
            address: borrower.address || '',
            borrower_type: borrower.borrower_type || '',
            date_of_birth: borrower.date_of_birth || '',
            employment_status: borrower.employment_status || '',
            annual_income: borrower.annual_income || '',
            credit_score: borrower.credit_score || ''
          }
        } catch (error) {
          console.error('Error fetching borrower:', error)
        }
      }
    }
    
    const validateForm = () => {
      const errors = {}
      
      // Required fields
      if (!borrowerForm.value.first_name) errors.first_name = 'First name is required'
      if (!borrowerForm.value.last_name) errors.last_name = 'Last name is required'
      if (!borrowerForm.value.email) errors.email = 'Email is required'
      if (!borrowerForm.value.phone_number) errors.phone_number = 'Phone number is required'
      if (!borrowerForm.value.address) errors.address = 'Address is required'
      if (!borrowerForm.value.borrower_type) errors.borrower_type = 'Borrower type is required'
      
      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (borrowerForm.value.email && !emailRegex.test(borrowerForm.value.email)) {
        errors.email = 'Please enter a valid email address'
      }
      
      // Phone validation
      const phoneRegex = /^\+?[0-9]{10,15}$/
      if (borrowerForm.value.phone_number && !phoneRegex.test(borrowerForm.value.phone_number)) {
        errors.phone_number = 'Please enter a valid phone number (10-15 digits)'
      }
      
      // Date validation
      if (borrowerForm.value.date_of_birth) {
        const birthDate = new Date(borrowerForm.value.date_of_birth)
        const today = new Date()
        if (birthDate > today) {
          errors.date_of_birth = 'Date of birth cannot be in the future'
        }
      }
      
      // Number validation
      if (borrowerForm.value.annual_income && (isNaN(borrowerForm.value.annual_income) || borrowerForm.value.annual_income < 0)) {
        errors.annual_income = 'Annual income must be a positive number'
      }
      
      if (borrowerForm.value.credit_score) {
        const score = parseInt(borrowerForm.value.credit_score)
        if (isNaN(score) || score < 300 || score > 850) {
          errors.credit_score = 'Credit score must be between 300 and 850'
        }
      }
      
      validationErrors.value = errors
      return Object.keys(errors).length === 0
    }
    
    const submitForm = async () => {
      if (!validateForm()) return
      
      try {
        // Prepare form data
        const formData = {
          first_name: borrowerForm.value.first_name,
          last_name: borrowerForm.value.last_name,
          email: borrowerForm.value.email,
          phone_number: borrowerForm.value.phone_number,
          address: borrowerForm.value.address,
          borrower_type: borrowerForm.value.borrower_type
        }
        
        // Add optional fields if they have values
        if (borrowerForm.value.date_of_birth) formData.date_of_birth = borrowerForm.value.date_of_birth
        if (borrowerForm.value.employment_status) formData.employment_status = borrowerForm.value.employment_status
        if (borrowerForm.value.annual_income) formData.annual_income = parseFloat(borrowerForm.value.annual_income)
        if (borrowerForm.value.credit_score) formData.credit_score = parseInt(borrowerForm.value.credit_score)
        
        let response
        if (isEditing.value) {
          response = await borrowerStore.updateBorrower(borrowerId.value, formData)
        } else {
          response = await borrowerStore.createBorrower(formData)
        }
        
        // Navigate to the borrower detail page
        router.push({ 
          name: 'borrower-detail', 
          params: { id: isEditing.value ? borrowerId.value : response.id }
        })
      } catch (error) {
        console.error('Error saving borrower:', error)
        
        // Handle validation errors from the API
        if (error.errors) {
          validationErrors.value = error.errors
        }
      }
    }
    
    const navigateBack = () => {
      if (isEditing.value) {
        router.push({ name: 'borrower-detail', params: { id: borrowerId.value } })
      } else {
        router.push({ name: 'borrower-list' })
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      fetchBorrowerData()
    })
    
    return {
      isEditing,
      borrowerForm,
      validationErrors,
      loading,
      error,
      submitForm,
      navigateBack
    }
  }
}
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}
</style>
