<template>
  <div class="document-upload-container">
    <h1 class="text-2xl font-bold mb-6">{{ isEditing ? 'Edit Document' : 'Upload New Document' }}</h1>
    
    <!-- Error alert -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p class="font-bold">Error</p>
      <p>{{ error }}</p>
    </div>
    
    <!-- Document form -->
    <form @submit.prevent="submitForm" class="bg-white rounded-lg shadow-md p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Basic Information -->
        <div class="col-span-2">
          <h2 class="text-lg font-semibold mb-4">Document Information</h2>
        </div>
        
        <!-- Title -->
        <div class="form-group">
          <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Title *</label>
          <input
            id="title"
            v-model="documentForm.title"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.title }"
            required
          />
          <p v-if="validationErrors.title" class="mt-1 text-sm text-red-600">{{ validationErrors.title }}</p>
        </div>
        
        <!-- Document Type -->
        <div class="form-group">
          <label for="document_type" class="block text-sm font-medium text-gray-700 mb-1">Document Type *</label>
          <select
            id="document_type"
            v-model="documentForm.document_type"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.document_type }"
            required
          >
            <option value="">Select Document Type</option>
            <option value="contract">Contract</option>
            <option value="application_form">Application Form</option>
            <option value="id_verification">ID Verification</option>
            <option value="income_proof">Income Proof</option>
            <option value="property_valuation">Property Valuation</option>
            <option value="credit_report">Credit Report</option>
            <option value="bank_statement">Bank Statement</option>
            <option value="insurance">Insurance</option>
            <option value="other">Other</option>
          </select>
          <p v-if="validationErrors.document_type" class="mt-1 text-sm text-red-600">{{ validationErrors.document_type }}</p>
        </div>
        
        <!-- Description -->
        <div class="col-span-2">
          <label for="description" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            id="description"
            v-model="documentForm.description"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.description }"
          ></textarea>
          <p v-if="validationErrors.description" class="mt-1 text-sm text-red-600">{{ validationErrors.description }}</p>
        </div>
        
        <!-- Related Entities -->
        <div class="col-span-2">
          <h2 class="text-lg font-semibold mb-4">Related Information</h2>
        </div>
        
        <!-- Application -->
        <div class="form-group">
          <label for="application" class="block text-sm font-medium text-gray-700 mb-1">Related Application</label>
          <select
            id="application"
            v-model="documentForm.application"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.application }"
          >
            <option value="">None</option>
            <option v-for="app in applications" :key="app.id" :value="app.id">
              {{ app.reference_number }} - {{ app.purpose }}
            </option>
          </select>
          <p v-if="validationErrors.application" class="mt-1 text-sm text-red-600">{{ validationErrors.application }}</p>
        </div>
        
        <!-- Borrower -->
        <div class="form-group">
          <label for="borrower" class="block text-sm font-medium text-gray-700 mb-1">Related Borrower</label>
          <select
            id="borrower"
            v-model="documentForm.borrower"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.borrower }"
          >
            <option value="">None</option>
            <option v-for="borrower in borrowers" :key="borrower.id" :value="borrower.id">
              {{ borrower.first_name }} {{ borrower.last_name }}
            </option>
          </select>
          <p v-if="validationErrors.borrower" class="mt-1 text-sm text-red-600">{{ validationErrors.borrower }}</p>
        </div>
        
        <!-- File Upload -->
        <div v-if="!isEditing || showFileUpload" class="col-span-2">
          <h2 class="text-lg font-semibold mb-4">Document File</h2>
          <div class="form-group">
            <label for="file" class="block text-sm font-medium text-gray-700 mb-1">
              {{ isEditing ? 'Replace File' : 'Upload File' }} *
            </label>
            <input
              type="file"
              ref="fileInput"
              class="hidden"
              @change="handleFileSelected"
            />
            <div class="flex items-center">
              <button
                type="button"
                @click="$refs.fileInput.click()"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
              >
                Select File
              </button>
              <span v-if="selectedFile" class="ml-2">{{ selectedFile.name }}</span>
              <span v-else-if="isEditing && document?.file_name" class="ml-2">
                Current file: {{ document.file_name }}
              </span>
            </div>
            <p v-if="validationErrors.file" class="mt-1 text-sm text-red-600">{{ validationErrors.file }}</p>
          </div>
        </div>
        
        <!-- Toggle file upload for editing -->
        <div v-if="isEditing" class="col-span-2">
          <div class="flex items-center">
            <input
              id="replace_file"
              type="checkbox"
              v-model="showFileUpload"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label for="replace_file" class="ml-2 block text-sm text-gray-900">
              Replace existing file
            </label>
          </div>
        </div>
      </div>
      
      <!-- Form Actions -->
      <div class="mt-6 flex justify-end space-x-3">
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
          {{ loading ? 'Saving...' : (isEditing ? 'Update Document' : 'Upload Document') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDocumentStore } from '@/store/document'
import { useApplicationStore } from '@/store/application'
import { useBorrowerStore } from '@/store/borrower'

export default {
  name: 'DocumentUploadView',
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
    const documentStore = useDocumentStore()
    const applicationStore = useApplicationStore()
    const borrowerStore = useBorrowerStore()
    
    // Local state
    const documentId = ref(props.id ? parseInt(props.id) : null)
    const fileInput = ref(null)
    const selectedFile = ref(null)
    const showFileUpload = ref(false)
    const validationErrors = ref({})
    const applications = ref([])
    const borrowers = ref([])
    
    // Form data
    const documentForm = reactive({
      title: '',
      document_type: '',
      description: '',
      application: '',
      borrower: ''
    })
    
    // Computed properties
    const document = computed(() => documentStore.currentDocument)
    const loading = computed(() => documentStore.loading)
    const error = computed(() => documentStore.error)
    
    // Methods
    const fetchDocumentData = async () => {
      if (!documentId.value) return
      
      try {
        await documentStore.fetchDocumentById(documentId.value)
        
        // Populate form with document data
        documentForm.title = document.value.title || ''
        documentForm.document_type = document.value.document_type || ''
        documentForm.description = document.value.description || ''
        documentForm.application = document.value.application || ''
        documentForm.borrower = document.value.borrower || ''
      } catch (error) {
        console.error('Error fetching document:', error)
      }
    }
    
    const fetchRelatedData = async () => {
      try {
        // Fetch applications for dropdown
        const appResponse = await applicationStore.fetchApplications()
        applications.value = appResponse.results || []
        
        // Fetch borrowers for dropdown
        const borrowerResponse = await borrowerStore.fetchBorrowers()
        borrowers.value = borrowerResponse.results || []
      } catch (error) {
        console.error('Error fetching related data:', error)
      }
    }
    
    const handleFileSelected = (event) => {
      const files = event.target.files
      if (files && files.length > 0) {
        selectedFile.value = files[0]
      }
    }
    
    const validateForm = () => {
      const errors = {}
      
      if (!documentForm.title) {
        errors.title = 'Title is required'
      }
      
      if (!documentForm.document_type) {
        errors.document_type = 'Document type is required'
      }
      
      if (!props.isEditing && !selectedFile.value) {
        errors.file = 'File is required'
      }
      
      if (props.isEditing && showFileUpload.value && !selectedFile.value) {
        errors.file = 'Please select a file to replace the current one'
      }
      
      validationErrors.value = errors
      return Object.keys(errors).length === 0
    }
    
    const submitForm = async () => {
      if (!validateForm()) return
      
      try {
        const formData = new FormData()
        
        // Add form fields to FormData
        formData.append('title', documentForm.title)
        formData.append('document_type', documentForm.document_type)
        
        if (documentForm.description) {
          formData.append('description', documentForm.description)
        }
        
        if (documentForm.application) {
          formData.append('application', documentForm.application)
        }
        
        if (documentForm.borrower) {
          formData.append('borrower', documentForm.borrower)
        }
        
        // Add file if selected
        if (selectedFile.value) {
          formData.append('file', selectedFile.value)
        }
        
        if (props.isEditing) {
          // If editing and not replacing file, use regular object instead of FormData
          if (!showFileUpload.value) {
            const documentData = {
              title: documentForm.title,
              document_type: documentForm.document_type,
              description: documentForm.description || '',
              application: documentForm.application || null,
              borrower: documentForm.borrower || null
            }
            await documentStore.updateDocument(documentId.value, documentData)
          } else {
            await documentStore.updateDocument(documentId.value, formData)
          }
        } else {
          await documentStore.createDocument(formData)
        }
        
        // Navigate back to document list or detail
        if (props.isEditing) {
          router.push({ name: 'document-detail', params: { id: documentId.value } })
        } else {
          router.push({ name: 'document-list' })
        }
      } catch (error) {
        console.error('Error saving document:', error)
      }
    }
    
    const navigateBack = () => {
      if (props.isEditing && documentId.value) {
        router.push({ name: 'document-detail', params: { id: documentId.value } })
      } else {
        router.push({ name: 'document-list' })
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      // If editing, fetch document data
      if (props.isEditing && documentId.value) {
        fetchDocumentData()
      }
      
      // Fetch related data for dropdowns
      fetchRelatedData()
      
      // Check for query parameters
      if (route.query.application) {
        documentForm.application = parseInt(route.query.application)
      }
      
      if (route.query.borrower) {
        documentForm.borrower = parseInt(route.query.borrower)
      }
    })
    
    return {
      document,
      loading,
      error,
      documentForm,
      fileInput,
      selectedFile,
      showFileUpload,
      validationErrors,
      applications,
      borrowers,
      handleFileSelected,
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
