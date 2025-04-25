<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Documents</h2>
      <button 
        @click="showUploadForm = !showUploadForm" 
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {{ showUploadForm ? 'Cancel' : 'Upload Document' }}
      </button>
    </div>
    
    <!-- Upload Form -->
    <div v-if="showUploadForm" class="bg-gray-50 p-4 rounded-md mb-6">
      <h3 class="text-lg font-medium mb-3">Upload New Document</h3>
      
      <form @submit.prevent="uploadDocument" class="space-y-4">
        <div>
          <label for="document_type" class="block text-sm font-medium text-gray-700">Document Type</label>
          <select 
            id="document_type" 
            v-model="newDocument.document_type"
            class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            required
          >
            <option value="">Select document type</option>
            <option value="application_form">Application Form</option>
            <option value="id_verification">ID Verification</option>
            <option value="income_proof">Income Proof</option>
            <option value="bank_statement">Bank Statement</option>
            <option value="property_valuation">Property Valuation</option>
            <option value="contract_of_sale">Contract of Sale</option>
            <option value="loan_agreement">Loan Agreement</option>
            <option value="settlement_letter">Settlement Letter</option>
            <option value="other">Other</option>
          </select>
        </div>
        
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700">Title</label>
          <input 
            type="text" 
            id="title" 
            v-model="newDocument.title"
            class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            required
          />
        </div>
        
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
          <textarea 
            id="description" 
            v-model="newDocument.description"
            rows="3"
            class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
          ></textarea>
        </div>
        
        <div>
          <label for="file" class="block text-sm font-medium text-gray-700">File</label>
          <input 
            type="file" 
            id="file" 
            ref="fileInput"
            class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            required
          />
        </div>
        
        <div class="flex justify-end">
          <button 
            type="submit" 
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="uploading"
          >
            <span v-if="uploading">Uploading...</span>
            <span v-else>Upload</span>
          </button>
        </div>
      </form>
    </div>
    
    <!-- Documents List -->
    <div v-if="documents && documents.length > 0">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Title
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Uploaded By
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="document in documents" :key="document.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="getDocumentTypeClass(document.document_type)">
                  {{ formatDocumentType(document.document_type) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ document.title }}</div>
                <div class="text-sm text-gray-500">{{ document.description }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ document.uploaded_by_name }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ formatDate(document.uploaded_at) }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <a :href="document.file_url" target="_blank" class="text-blue-600 hover:text-blue-900 mr-3">View</a>
                <a :href="document.file_url" download class="text-green-600 hover:text-green-900">Download</a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else class="bg-gray-50 p-4 rounded-md">
      <p class="text-sm text-gray-500">No documents uploaded for this application</p>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import axios from 'axios'

const props = defineProps({
  documents: {
    type: Array,
    default: () => []
  },
  applicationId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['document-uploaded'])

const showUploadForm = ref(false)
const uploading = ref(false)
const fileInput = ref(null)
const newDocument = ref({
  document_type: '',
  title: '',
  description: ''
})

const uploadDocument = async () => {
  if (!fileInput.value.files[0]) {
    alert('Please select a file to upload')
    return
  }
  
  uploading.value = true
  
  try {
    const formData = new FormData()
    formData.append('document_type', newDocument.value.document_type)
    formData.append('title', newDocument.value.title)
    formData.append('description', newDocument.value.description)
    formData.append('file', fileInput.value.files[0])
    
    await axios.post(`/api/applications/${props.applicationId}/upload_document/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    // Reset form
    newDocument.value = {
      document_type: '',
      title: '',
      description: ''
    }
    fileInput.value.value = ''
    showUploadForm.value = false
    
    // Notify parent to refresh data
    emit('document-uploaded')
    
  } catch (error) {
    console.error('Error uploading document:', error)
    alert('Failed to upload document. Please try again.')
  } finally {
    uploading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const formatDocumentType = (type) => {
  const types = {
    'application_form': 'Application Form',
    'id_verification': 'ID Verification',
    'income_proof': 'Income Proof',
    'bank_statement': 'Bank Statement',
    'property_valuation': 'Property Valuation',
    'contract_of_sale': 'Contract of Sale',
    'loan_agreement': 'Loan Agreement',
    'settlement_letter': 'Settlement Letter',
    'other': 'Other'
  }
  
  return types[type] || type
}

const getDocumentTypeClass = (type) => {
  const typeClasses = {
    'application_form': 'bg-blue-100 text-blue-800',
    'id_verification': 'bg-green-100 text-green-800',
    'income_proof': 'bg-yellow-100 text-yellow-800',
    'bank_statement': 'bg-purple-100 text-purple-800',
    'property_valuation': 'bg-indigo-100 text-indigo-800',
    'contract_of_sale': 'bg-pink-100 text-pink-800',
    'loan_agreement': 'bg-red-100 text-red-800',
    'settlement_letter': 'bg-green-100 text-green-800',
    'other': 'bg-gray-100 text-gray-800'
  }
  
  return typeClasses[type] || 'bg-gray-100 text-gray-800'
}
</script>
