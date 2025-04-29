<template>
  <MainLayout>
    <div class="repayment-form-view">
      <div class="container mx-auto px-4 py-6">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold">{{ isEditing ? 'Edit Repayment' : 'Create Repayment' }}</h1>
          <button
            @click="goBack"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
          >
            Back
          </button>
        </div>
        
        <!-- Loading state -->
        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="loader"></div>
        </div>
        
        <!-- Error state -->
        <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p>{{ error }}</p>
        </div>
        
        <!-- Form -->
        <form v-else @submit.prevent="submitForm" class="bg-white p-6 rounded-lg shadow-md">
          <!-- Application ID -->
          <div class="mb-4">
            <label for="application" class="block text-sm font-medium text-gray-700 mb-1">Application ID *</label>
            <input
              id="application"
              v-model="formData.application"
              type="number"
              required
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              :disabled="isEditing"
            />
            <p v-if="validationErrors.application" class="mt-1 text-sm text-red-600">{{ validationErrors.application }}</p>
          </div>
          
          <!-- Amount -->
          <div class="mb-4">
            <label for="amount" class="block text-sm font-medium text-gray-700 mb-1">Amount *</label>
            <div class="relative">
              <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">$</span>
              <input
                id="amount"
                v-model="formData.amount"
                type="number"
                step="0.01"
                required
                class="w-full pl-8 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <p v-if="validationErrors.amount" class="mt-1 text-sm text-red-600">{{ validationErrors.amount }}</p>
          </div>
          
          <!-- Due Date -->
          <div class="mb-4">
            <label for="due_date" class="block text-sm font-medium text-gray-700 mb-1">Due Date *</label>
            <input
              id="due_date"
              v-model="formData.due_date"
              type="date"
              required
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p v-if="validationErrors.due_date" class="mt-1 text-sm text-red-600">{{ validationErrors.due_date }}</p>
          </div>
          
          <!-- Invoice (optional) -->
          <div class="mb-6">
            <label for="invoice" class="block text-sm font-medium text-gray-700 mb-1">Invoice (optional)</label>
            <input
              id="invoice"
              type="file"
              @change="handleFileUpload"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p class="mt-1 text-sm text-gray-500">Upload an invoice file (PDF, PNG, JPEG)</p>
          </div>
          
          <!-- Submit Button -->
          <div class="flex justify-end">
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? 'Saving...' : (isEditing ? 'Update Repayment' : 'Create Repayment') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </MainLayout>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRepaymentStore } from '@/store/repayment'
import MainLayout from '@/layouts/MainLayout.vue'

export default {
  name: 'RepaymentFormView',
  components: {
    MainLayout
  },
  props: {
    id: {
      type: [Number, String],
      default: null
    },
    isEditing: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const route = useRoute()
    const router = useRouter()
    const repaymentStore = useRepaymentStore()
    
    // Form state
    const formData = ref({
      application: '',
      amount: '',
      due_date: new Date().toISOString().split('T')[0], // Default to today
      invoice: null
    })
    
    const validationErrors = ref({})
    const isSubmitting = ref(false)
    const loading = ref(false)
    const error = ref(null)
    
    // Get application ID from query params if available
    if (route.query.application) {
      formData.value.application = route.query.application
    }
    
    // Computed properties
    const repaymentId = computed(() => {
      return props.id || route.params.id
    })
    
    // Methods
    const fetchRepaymentData = async () => {
      if (!repaymentId.value) return
      
      try {
        loading.value = true
        error.value = null
        
        const repayment = await repaymentStore.fetchRepaymentById(repaymentId.value)
        
        // Populate form data
        formData.value = {
          application: repayment.application,
          amount: repayment.amount,
          due_date: repayment.due_date,
          invoice: null // Can't pre-populate file input
        }
      } catch (err) {
        error.value = err.message || 'Failed to load repayment data'
        console.error('Error fetching repayment:', err)
      } finally {
        loading.value = false
      }
    }
    
    const handleFileUpload = (event) => {
      formData.value.invoice = event.target.files[0] || null
    }
    
    const validateForm = () => {
      const errors = {}
      
      if (!formData.value.application) {
        errors.application = 'Application ID is required'
      }
      
      if (!formData.value.amount || parseFloat(formData.value.amount) <= 0) {
        errors.amount = 'Amount must be greater than zero'
      }
      
      if (!formData.value.due_date) {
        errors.due_date = 'Due date is required'
      }
      
      validationErrors.value = errors
      return Object.keys(errors).length === 0
    }
    
    const submitForm = async () => {
      if (!validateForm()) return
      
      try {
        isSubmitting.value = true
        error.value = null
        
        // Create FormData object for file upload
        const formDataObj = new FormData()
        formDataObj.append('application', formData.value.application)
        formDataObj.append('amount', formData.value.amount)
        formDataObj.append('due_date', formData.value.due_date)
        
        if (formData.value.invoice) {
          formDataObj.append('invoice', formData.value.invoice)
        }
        
        if (props.isEditing) {
          await repaymentStore.updateRepayment(repaymentId.value, formDataObj)
        } else {
          await repaymentStore.createRepayment(formDataObj)
        }
        
        // Navigate back to repayments list
        router.push({ name: 'repayment-list' })
      } catch (err) {
        error.value = err.message || 'Failed to save repayment'
        console.error('Error saving repayment:', err)
        
        // Handle validation errors from API
        if (err.errors) {
          validationErrors.value = err.errors
        }
      } finally {
        isSubmitting.value = false
      }
    }
    
    const goBack = () => {
      router.back()
    }
    
    // Lifecycle hooks
    onMounted(() => {
      if (props.isEditing) {
        fetchRepaymentData()
      }
    })
    
    return {
      formData,
      validationErrors,
      isSubmitting,
      loading,
      error,
      handleFileUpload,
      submitForm,
      goBack
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
