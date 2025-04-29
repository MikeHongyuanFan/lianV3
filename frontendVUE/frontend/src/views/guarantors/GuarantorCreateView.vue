<template>
  <div class="guarantor-create-container">
    <h1 class="text-2xl font-bold mb-6">{{ isEditing ? 'Edit Guarantor' : 'Create New Guarantor' }}</h1>
    
    <!-- Error alert -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p class="font-bold">Error</p>
      <p>{{ error }}</p>
    </div>
    
    <!-- Guarantor form -->
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
            v-model="guarantorForm.first_name"
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
            v-model="guarantorForm.last_name"
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
            v-model="guarantorForm.email"
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
            v-model="guarantorForm.phone_number"
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
            v-model="guarantorForm.address"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.address }"
            required
          />
          <p v-if="validationErrors.address" class="mt-1 text-sm text-red-600">{{ validationErrors.address }}</p>
        </div>
        
        <!-- Relationship to Borrower -->
        <div class="form-group">
          <label for="relationship_to_borrower" class="block text-sm font-medium text-gray-700 mb-1">Relationship to Borrower *</label>
          <select
            id="relationship_to_borrower"
            v-model="guarantorForm.relationship_to_borrower"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.relationship_to_borrower }"
            required
          >
            <option value="">Select Relationship</option>
            <option value="spouse">Spouse</option>
            <option value="parent">Parent</option>
            <option value="child">Child</option>
            <option value="sibling">Sibling</option>
            <option value="friend">Friend</option>
            <option value="business_partner">Business Partner</option>
            <option value="other">Other</option>
          </select>
          <p v-if="validationErrors.relationship_to_borrower" class="mt-1 text-sm text-red-600">{{ validationErrors.relationship_to_borrower }}</p>
        </div>
        
        <!-- Date of Birth -->
        <div class="form-group">
          <label for="date_of_birth" class="block text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
          <input
            id="date_of_birth"
            v-model="guarantorForm.date_of_birth"
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
            v-model="guarantorForm.employment_status"
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
              v-model="guarantorForm.annual_income"
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
            v-model="guarantorForm.credit_score"
            type="number"
            min="300"
            max="850"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.credit_score }"
          />
          <p v-if="validationErrors.credit_score" class="mt-1 text-sm text-red-600">{{ validationErrors.credit_score }}</p>
        </div>
        
        <!-- Related Entities -->
        <div class="col-span-2 mt-4">
          <h2 class="text-lg font-semibold mb-4">Related Entities</h2>
        </div>
        
        <!-- Borrower (optional) -->
        <div class="form-group">
          <label for="borrower" class="block text-sm font-medium text-gray-700 mb-1">Related Borrower (Optional)</label>
          <select
            id="borrower"
            v-model="guarantorForm.borrower"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.borrower }"
          >
            <option value="">Select Borrower</option>
            <option v-for="borrower in borrowers" :key="borrower.id" :value="borrower.id">
              {{ borrower.first_name }} {{ borrower.last_name }}
            </option>
          </select>
          <p v-if="validationErrors.borrower" class="mt-1 text-sm text-red-600">{{ validationErrors.borrower }}</p>
        </div>
        
        <!-- Application (optional) -->
        <div class="form-group">
          <label for="application" class="block text-sm font-medium text-gray-700 mb-1">Related Application (Optional)</label>
          <select
            id="application"
            v-model="guarantorForm.application"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.application }"
          >
            <option value="">Select Application</option>
            <option v-for="application in applications" :key="application.id" :value="application.id">
              {{ application.reference_number }} - {{ application.purpose }}
            </option>
          </select>
          <p v-if="validationErrors.application" class="mt-1 text-sm text-red-600">{{ validationErrors.application }}</p>
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
          {{ loading ? (isEditing ? 'Updating...' : 'Creating...') : (isEditing ? 'Update Guarantor' : 'Create Guarantor') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useGuarantorStore } from '@/store/guarantor'
import { useBorrowerStore } from '@/store/borrower'
import { useApplicationStore } from '@/store/application'

export default {
  name: 'GuarantorCreateView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const guarantorStore = useGuarantorStore()
    const borrowerStore = useBorrowerStore()
    const applicationStore = useApplicationStore()
    
    // Determine if we're editing or creating
    const isEditing = computed(() => !!route.params.id)
    const guarantorId = ref(isEditing.value ? parseInt(route.params.id) : null)
    
    // Form state
    const guarantorForm = ref({
      first_name: '',
      last_name: '',
      email: '',
      phone_number: '',
      address: '',
      relationship_to_borrower: '',
      date_of_birth: '',
      employment_status: '',
      annual_income: '',
      credit_score: '',
      borrower: route.query.borrower || '',
      application: route.query.application || ''
    })
    
    const validationErrors = ref({})
    const loading = computed(() => guarantorStore.loading)
    const error = computed(() => guarantorStore.error)
    
    // Related entities
    const borrowers = ref([])
    const applications = ref([])
    const loadingBorrowers = ref(false)
    const loadingApplications = ref(false)
    
    // Methods
    const fetchGuarantorData = async () => {
      if (isEditing.value) {
        try {
          const guarantor = await guarantorStore.fetchGuarantorById(guarantorId.value)
          
          // Populate form with guarantor data
          guarantorForm.value = {
            first_name: guarantor.first_name || '',
            last_name: guarantor.last_name || '',
            email: guarantor.email || '',
            phone_number: guarantor.phone_number || '',
            address: guarantor.address || '',
            relationship_to_borrower: guarantor.relationship_to_borrower || '',
            date_of_birth: guarantor.date_of_birth || '',
            employment_status: guarantor.employment_status || '',
            annual_income: guarantor.annual_income || '',
            credit_score: guarantor.credit_score || '',
            borrower: guarantor.borrower || '',
            application: guarantor.application || ''
          }
        } catch (error) {
          console.error('Error fetching guarantor:', error)
        }
      }
    }
    
    const fetchBorrowers = async () => {
      loadingBorrowers.value = true
      try {
        // Set a large limit to get all borrowers (in a real app, you might want to implement search/select)
        borrowerStore.setLimit(100)
        await borrowerStore.fetchBorrowers()
        borrowers.value = borrowerStore.borrowers
      } catch (error) {
        console.error('Error fetching borrowers:', error)
      } finally {
        loadingBorrowers.value = false
      }
    }
    
    const fetchApplications = async () => {
      loadingApplications.value = true
      try {
        // Set a large limit to get all applications (in a real app, you might want to implement search/select)
        applicationStore.setLimit(100)
        await applicationStore.fetchApplications()
        applications.value = applicationStore.applications
      } catch (error) {
        console.error('Error fetching applications:', error)
      } finally {
        loadingApplications.value = false
      }
    }
    
    const validateForm = () => {
      const errors = {}
      
      // Required fields
      if (!guarantorForm.value.first_name) errors.first_name = 'First name is required'
      if (!guarantorForm.value.last_name) errors.last_name = 'Last name is required'
      if (!guarantorForm.value.email) errors.email = 'Email is required'
      if (!guarantorForm.value.phone_number) errors.phone_number = 'Phone number is required'
      if (!guarantorForm.value.address) errors.address = 'Address is required'
      if (!guarantorForm.value.relationship_to_borrower) errors.relationship_to_borrower = 'Relationship to borrower is required'
      
      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (guarantorForm.value.email && !emailRegex.test(guarantorForm.value.email)) {
        errors.email = 'Please enter a valid email address'
      }
      
      // Phone validation
      const phoneRegex = /^\+?[0-9]{10,15}$/
      if (guarantorForm.value.phone_number && !phoneRegex.test(guarantorForm.value.phone_number)) {
        errors.phone_number = 'Please enter a valid phone number (10-15 digits)'
      }
      
      // Date validation
      if (guarantorForm.value.date_of_birth) {
        const birthDate = new Date(guarantorForm.value.date_of_birth)
        const today = new Date()
        if (birthDate > today) {
          errors.date_of_birth = 'Date of birth cannot be in the future'
        }
      }
      
      // Number validation
      if (guarantorForm.value.annual_income && (isNaN(guarantorForm.value.annual_income) || guarantorForm.value.annual_income < 0)) {
        errors.annual_income = 'Annual income must be a positive number'
      }
      
      if (guarantorForm.value.credit_score) {
        const score = parseInt(guarantorForm.value.credit_score)
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
          first_name: guarantorForm.value.first_name,
          last_name: guarantorForm.value.last_name,
          email: guarantorForm.value.email,
          phone_number: guarantorForm.value.phone_number,
          address: guarantorForm.value.address,
          relationship_to_borrower: guarantorForm.value.relationship_to_borrower
        }
        
        // Add optional fields if they have values
        if (guarantorForm.value.date_of_birth) formData.date_of_birth = guarantorForm.value.date_of_birth
        if (guarantorForm.value.employment_status) formData.employment_status = guarantorForm.value.employment_status
        if (guarantorForm.value.annual_income) formData.annual_income = parseFloat(guarantorForm.value.annual_income)
        if (guarantorForm.value.credit_score) formData.credit_score = parseInt(guarantorForm.value.credit_score)
        if (guarantorForm.value.borrower) formData.borrower = parseInt(guarantorForm.value.borrower)
        if (guarantorForm.value.application) formData.application = parseInt(guarantorForm.value.application)
        
        let response
        if (isEditing.value) {
          response = await guarantorStore.updateGuarantor(guarantorId.value, formData)
        } else {
          response = await guarantorStore.createGuarantor(formData)
        }
        
        // Navigate to the guarantor detail page
        router.push({ 
          name: 'guarantor-detail', 
          params: { id: isEditing.value ? guarantorId.value : response.id }
        })
      } catch (error) {
        console.error('Error saving guarantor:', error)
        
        // Handle validation errors from the API
        if (error.errors) {
          validationErrors.value = error.errors
        }
      }
    }
    
    const navigateBack = () => {
      if (isEditing.value) {
        router.push({ name: 'guarantor-detail', params: { id: guarantorId.value } })
      } else {
        router.push({ name: 'guarantor-list' })
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      fetchGuarantorData()
      fetchBorrowers()
      fetchApplications()
    })
    
    return {
      isEditing,
      guarantorForm,
      validationErrors,
      loading,
      error,
      borrowers,
      applications,
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
