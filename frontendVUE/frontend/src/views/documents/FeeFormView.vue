<template>
  <div class="fee-form-view">
    <div class="container mx-auto px-4 py-6">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">{{ isEditing ? 'Edit Fee' : 'Create Fee' }}</h1>
        <button
          @click="navigateBack"
          class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none flex items-center"
        >
          <span class="material-icons mr-1">arrow_back</span>
          Back
        </button>
      </div>
      
      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="loader"></div>
      </div>
      
      <!-- Error state -->
      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        <p>{{ error }}</p>
      </div>
      
      <!-- Form -->
      <form v-else @submit.prevent="submitForm" class="bg-white p-6 rounded-lg shadow">
        <!-- Fee Type -->
        <div class="mb-4">
          <label for="fee_type" class="block text-sm font-medium text-gray-700 mb-1">Fee Type *</label>
          <select
            id="fee_type"
            v-model="form.fee_type"
            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{'border-red-500': validationErrors.fee_type}"
            required
          >
            <option value="" disabled>Select Fee Type</option>
            <option value="application">Application</option>
            <option value="valuation">Valuation</option>
            <option value="legal">Legal</option>
            <option value="broker">Broker</option>
            <option value="settlement">Settlement</option>
            <option value="other">Other</option>
          </select>
          <p v-if="validationErrors.fee_type" class="text-red-500 text-sm mt-1">{{ validationErrors.fee_type }}</p>
        </div>
        
        <!-- Amount -->
        <div class="mb-4">
          <label for="amount" class="block text-sm font-medium text-gray-700 mb-1">Amount *</label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">$</span>
            <input
              id="amount"
              v-model="form.amount"
              type="number"
              step="0.01"
              min="0"
              class="w-full pl-8 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="{'border-red-500': validationErrors.amount}"
              required
            />
          </div>
          <p v-if="validationErrors.amount" class="text-red-500 text-sm mt-1">{{ validationErrors.amount }}</p>
        </div>
        
        <!-- Application -->
        <div class="mb-4">
          <label for="application" class="block text-sm font-medium text-gray-700 mb-1">Application ID *</label>
          <div class="flex space-x-2">
            <input
              id="application"
              v-model="form.application"
              type="number"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="{'border-red-500': validationErrors.application}"
              @blur="checkApplicationExists"
              required
            />
            <button 
              type="button"
              @click="$router.push({ name: 'application-list', query: { selectFor: 'fee' } })"
              class="px-3 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
              title="Browse applications"
            >
              <span class="material-icons">search</span>
            </button>
          </div>
          <p v-if="validationErrors.application" class="text-red-500 text-sm mt-1">{{ validationErrors.application }}</p>
        </div>
        
        <!-- Due Date -->
        <div class="mb-4">
          <label for="due_date" class="block text-sm font-medium text-gray-700 mb-1">Due Date *</label>
          <input
            id="due_date"
            v-model="form.due_date"
            type="date"
            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{'border-red-500': validationErrors.due_date}"
            required
          />
          <p v-if="validationErrors.due_date" class="text-red-500 text-sm mt-1">{{ validationErrors.due_date }}</p>
        </div>
        
        <!-- Description -->
        <div class="mb-4">
          <label for="description" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            id="description"
            v-model="form.description"
            rows="3"
            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{'border-red-500': validationErrors.description}"
          ></textarea>
          <p v-if="validationErrors.description" class="text-red-500 text-sm mt-1">{{ validationErrors.description }}</p>
        </div>
        
        <!-- Invoice Upload -->
        <div class="mb-6">
          <label for="invoice" class="block text-sm font-medium text-gray-700 mb-1">Invoice (Optional)</label>
          <input
            id="invoice"
            type="file"
            @change="handleFileUpload"
            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{'border-red-500': validationErrors.invoice}"
          />
          <p v-if="validationErrors.invoice" class="text-red-500 text-sm mt-1">{{ validationErrors.invoice }}</p>
        </div>
        
        <!-- Submit Button -->
        <div class="flex justify-end">
          <button
            type="submit"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
            :disabled="submitting"
          >
            <span v-if="submitting">Saving...</span>
            <span v-else>{{ isEditing ? 'Update Fee' : 'Create Fee' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useFeeStore } from '@/store/fee'

export default {
  name: 'FeeFormView',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const feeStore = useFeeStore()
    
    // State
    const form = reactive({
      fee_type: '',
      amount: '',
      application: '',
      due_date: new Date().toISOString().split('T')[0], // Today's date
      description: '',
      invoice: null
    })
    
    const validationErrors = reactive({})
    const submitting = ref(false)
    const loading = ref(false)
    const error = ref('')
    
    // Computed properties
    const isEditing = computed(() => !!route.params.id)
    
    // Methods
    // Fetch application details to verify it exists
    const verifyApplication = async (applicationId) => {
      if (!applicationId) return false
      
      try {
        // This would typically call an API endpoint to verify the application exists
        // For now, we'll just simulate a check
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/applications/${applicationId}/`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        
        if (response.ok) {
          return true
        } else if (response.status === 404) {
          validationErrors.application = 'Application not found'
          return false
        } else {
          console.error('Error verifying application:', response.statusText)
          return false
        }
      } catch (err) {
        console.error('Error verifying application:', err)
        return false
      }
    }
    
    const loadFee = async () => {
      if (!isEditing.value) return
      
      loading.value = true
      error.value = ''
      
      try {
        const fee = await feeStore.fetchFeeById(route.params.id)
        
        // Populate form with fee data
        form.fee_type = fee.fee_type
        form.amount = fee.amount
        form.application = fee.application
        form.due_date = fee.due_date
        form.description = fee.description || ''
        
      } catch (err) {
        error.value = 'Failed to load fee details. Please try again.'
        console.error('Error loading fee:', err)
      } finally {
        loading.value = false
      }
    }
    
    const validateForm = () => {
      const errors = {}
      
      if (!form.fee_type) {
        errors.fee_type = 'Fee type is required'
      }
      
      if (!form.amount || isNaN(form.amount) || parseFloat(form.amount) <= 0) {
        errors.amount = 'Amount must be a positive number'
      }
      
      if (!form.application || isNaN(form.application) || parseInt(form.application) <= 0) {
        errors.application = 'Valid application ID is required'
      }
      
      if (!form.due_date) {
        errors.due_date = 'Due date is required'
      } else {
        // Validate date format and ensure it's not in the past
        const dueDate = new Date(form.due_date)
        const today = new Date()
        today.setHours(0, 0, 0, 0)
        
        if (isNaN(dueDate.getTime())) {
          errors.due_date = 'Invalid date format'
        }
      }
      
      // Validate file type if provided
      if (form.invoice) {
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
        if (!allowedTypes.includes(form.invoice.type)) {
          errors.invoice = 'Only PDF, JPEG, and PNG files are allowed'
        }
        
        // Check file size (max 5MB)
        const maxSize = 5 * 1024 * 1024 // 5MB in bytes
        if (form.invoice.size > maxSize) {
          errors.invoice = 'File size must be less than 5MB'
        }
      }
      
      return errors
    }
    
    const submitForm = async () => {
      // Validate form
      const errors = validateForm()
      Object.assign(validationErrors, errors)
      
      if (Object.keys(errors).length > 0) {
        // Scroll to the first error
        const firstErrorField = Object.keys(errors)[0]
        const element = document.getElementById(firstErrorField)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'center' })
          element.focus()
        }
        return
      }
      
      submitting.value = true
      error.value = ''
      
      try {
        // Create FormData if we have a file to upload
        let feeData
        
        if (form.invoice) {
          feeData = new FormData()
          feeData.append('fee_type', form.fee_type)
          feeData.append('amount', form.amount)
          feeData.append('application', form.application)
          feeData.append('due_date', form.due_date)
          
          if (form.description) {
            feeData.append('description', form.description)
          }
          
          feeData.append('invoice', form.invoice)
        } else {
          // Regular JSON data if no file
          feeData = {
            fee_type: form.fee_type,
            amount: parseFloat(form.amount),
            application: parseInt(form.application),
            due_date: form.due_date,
            description: form.description || undefined
          }
        }
        
        if (isEditing.value) {
          await feeStore.updateFee(route.params.id, feeData)
        } else {
          await feeStore.createFee(feeData)
        }
        
        // Navigate back to fee list
        router.push({ name: 'fee-list' })
        
      } catch (err) {
        if (err.errors) {
          // API validation errors
          Object.assign(validationErrors, err.errors)
          
          // Scroll to the first error
          const firstErrorField = Object.keys(validationErrors)[0]
          const element = document.getElementById(firstErrorField)
          if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'center' })
            element.focus()
          }
        } else {
          error.value = err.message || 'Failed to save fee. Please try again.'
        }
        console.error('Error saving fee:', err)
      } finally {
        submitting.value = false
      }
    }
    
    const handleFileUpload = (event) => {
      const file = event.target.files[0] || null
      form.invoice = file
      
      // Clear any previous file validation errors
      if (validationErrors.invoice) {
        validationErrors.invoice = ''
      }
      
      // Validate file if selected
      if (file) {
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
        if (!allowedTypes.includes(file.type)) {
          validationErrors.invoice = 'Only PDF, JPEG, and PNG files are allowed'
        }
        
        // Check file size (max 5MB)
        const maxSize = 5 * 1024 * 1024 // 5MB in bytes
        if (file.size > maxSize) {
          validationErrors.invoice = 'File size must be less than 5MB'
        }
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      if (isEditing.value) {
        loadFee()
      }
    })
    
    return {
      form,
      validationErrors,
      submitting,
      loading,
      error,
      isEditing,
      handleFileUpload,
      submitForm,
      navigateBack,
      verifyApplication,
      checkApplicationExists
    }
  }
}
</script>

<style scoped>
.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
