<template>
  <div class="document-detail-container">
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchDocumentData" class="underline">Try again</button>
    </div>
    
    <!-- Document details -->
    <div v-else-if="document" class="bg-white rounded-lg shadow-md p-6">
      <div class="flex justify-between items-start mb-6">
        <div>
          <h1 class="text-2xl font-bold">{{ document.title }}</h1>
          <span
            v-if="document.document_type"
            class="document-type-badge px-2 py-1 text-xs rounded-full mt-2 inline-block bg-blue-100 text-blue-800"
          >
            {{ formatDocumentType(document.document_type_display || document.document_type) }}
          </span>
        </div>
        
        <div class="flex space-x-2">
          <button
            @click="downloadDocument"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
          >
            Download
          </button>
          <button
            @click="navigateToEdit"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
          >
            Edit
          </button>
          <button
            @click="confirmDelete"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none"
          >
            Delete
          </button>
        </div>
      </div>
      
      <!-- Document preview -->
      <div class="document-preview mb-6">
        <div v-if="isImage" class="flex justify-center">
          <img :src="document.file_url" :alt="document.title" class="max-h-96 object-contain" />
        </div>
        <div v-else-if="isPdf" class="flex justify-center">
          <div class="bg-gray-100 p-4 rounded-lg text-center">
            <span class="material-icons text-6xl text-gray-500">picture_as_pdf</span>
            <p class="mt-2">PDF Document</p>
            <button
              @click="downloadDocument"
              class="mt-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
            >
              Download to View
            </button>
          </div>
        </div>
        <div v-else class="flex justify-center">
          <div class="bg-gray-100 p-4 rounded-lg text-center">
            <span class="material-icons text-6xl text-gray-500">description</span>
            <p class="mt-2">{{ document.file_type || 'Document' }}</p>
            <button
              @click="downloadDocument"
              class="mt-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
            >
              Download to View
            </button>
          </div>
        </div>
      </div>
      
      <!-- Document details -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="detail-group">
          <h3 class="text-sm font-medium text-gray-500">Document Information</h3>
          <div class="mt-2 space-y-2">
            <div v-if="document.description" class="mb-4">
              <p class="text-gray-700">{{ document.description }}</p>
            </div>
            <div class="flex items-center">
              <span class="material-icons text-gray-400 mr-2">description</span>
              <p>{{ document.file_name }}</p>
            </div>
            <div class="flex items-center">
              <span class="material-icons text-gray-400 mr-2">straighten</span>
              <p>{{ formatFileSize(document.file_size) }}</p>
            </div>
            <div class="flex items-center">
              <span class="material-icons text-gray-400 mr-2">insert_drive_file</span>
              <p>{{ document.file_type || 'Unknown type' }}</p>
            </div>
            <div class="flex items-center">
              <span class="material-icons text-gray-400 mr-2">tag</span>
              <p>Version {{ document.version || 1 }}</p>
            </div>
          </div>
        </div>
        
        <div class="detail-group">
          <h3 class="text-sm font-medium text-gray-500">Related Information</h3>
          <div class="mt-2 space-y-2">
            <div v-if="document.application" class="flex items-center">
              <span class="material-icons text-gray-400 mr-2">assignment</span>
              <p>
                Application: 
                <button 
                  @click="navigateToApplication(document.application)" 
                  class="text-blue-600 hover:underline"
                >
                  View Application
                </button>
              </p>
            </div>
            <div v-if="document.borrower" class="flex items-center">
              <span class="material-icons text-gray-400 mr-2">person</span>
              <p>
                Borrower: 
                <button 
                  @click="navigateToBorrower(document.borrower)" 
                  class="text-blue-600 hover:underline"
                >
                  View Borrower
                </button>
              </p>
            </div>
            <div class="flex items-center">
              <span class="material-icons text-gray-400 mr-2">person</span>
              <p>Uploaded by: {{ document.created_by_name }}</p>
            </div>
            <div class="flex items-center">
              <span class="material-icons text-gray-400 mr-2">event</span>
              <p>Uploaded on: {{ formatDateTime(document.created_at) }}</p>
            </div>
            <div v-if="document.updated_at" class="flex items-center">
              <span class="material-icons text-gray-400 mr-2">update</span>
              <p>Last updated: {{ formatDateTime(document.updated_at) }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Version history -->
      <div v-if="document.version > 1" class="mt-6">
        <h3 class="text-lg font-semibold mb-3">Version History</h3>
        <p class="text-gray-500 mb-4">This document has been updated {{ document.version - 1 }} times.</p>
        
        <div class="mt-4">
          <h4 class="text-md font-medium mb-2">Upload New Version</h4>
          <div class="flex items-center">
            <input
              type="file"
              ref="fileInput"
              class="hidden"
              @change="handleFileSelected"
            />
            <button
              @click="$refs.fileInput.click()"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
            >
              Select File
            </button>
            <span v-if="selectedFile" class="ml-2">{{ selectedFile.name }}</span>
          </div>
          <div v-if="selectedFile" class="mt-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Description of changes (optional)</label>
            <textarea
              v-model="versionDescription"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows="2"
            ></textarea>
            <div class="mt-2 flex justify-end">
              <button
                @click="uploadNewVersion"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
                :disabled="uploadingVersion"
              >
                {{ uploadingVersion ? 'Uploading...' : 'Upload New Version' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Delete confirmation modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
        <h3 class="text-lg font-bold mb-4">Confirm Deletion</h3>
        <p class="mb-6">Are you sure you want to delete this document? This action cannot be undone.</p>
        <div class="flex justify-end space-x-3">
          <button
            @click="showDeleteModal = false"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
          >
            Cancel
          </button>
          <button
            @click="deleteDocument"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none"
            :disabled="deletingDocument"
          >
            {{ deletingDocument ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDocumentStore } from '@/store/document'

export default {
  name: 'DocumentDetailView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const documentStore = useDocumentStore()
    
    // Local state
    const documentId = ref(parseInt(route.params.id))
    const showDeleteModal = ref(false)
    const deletingDocument = ref(false)
    const fileInput = ref(null)
    const selectedFile = ref(null)
    const versionDescription = ref('')
    const uploadingVersion = ref(false)
    
    // Computed properties
    const document = computed(() => documentStore.currentDocument)
    const loading = computed(() => documentStore.loading)
    const error = computed(() => documentStore.error)
    
    const isImage = computed(() => {
      if (!document.value?.file_type) return false
      return document.value.file_type.startsWith('image/')
    })
    
    const isPdf = computed(() => {
      if (!document.value?.file_type) return false
      return document.value.file_type === 'application/pdf'
    })
    
    // Methods
    const fetchDocumentData = async () => {
      try {
        await documentStore.fetchDocumentById(documentId.value)
      } catch (error) {
        console.error('Error fetching document:', error)
      }
    }
    
    const downloadDocument = async () => {
      try {
        await documentStore.downloadDocument(documentId.value)
      } catch (error) {
        console.error('Error downloading document:', error)
      }
    }
    
    const navigateToEdit = () => {
      router.push({ name: 'document-edit', params: { id: documentId.value } })
    }
    
    const confirmDelete = () => {
      showDeleteModal.value = true
    }
    
    const deleteDocument = async () => {
      deletingDocument.value = true
      
      try {
        await documentStore.deleteDocument(documentId.value)
        showDeleteModal.value = false
        router.push({ name: 'document-list' })
      } catch (error) {
        console.error('Error deleting document:', error)
      } finally {
        deletingDocument.value = false
      }
    }
    
    const navigateToApplication = (applicationId) => {
      router.push({ name: 'application-detail', params: { id: applicationId } })
    }
    
    const navigateToBorrower = (borrowerId) => {
      router.push({ name: 'borrower-detail', params: { id: borrowerId } })
    }
    
    const handleFileSelected = (event) => {
      const files = event.target.files
      if (files && files.length > 0) {
        selectedFile.value = files[0]
      }
    }
    
    const uploadNewVersion = async () => {
      if (!selectedFile.value) return
      
      uploadingVersion.value = true
      
      try {
        const formData = new FormData()
        formData.append('file', selectedFile.value)
        
        if (versionDescription.value) {
          formData.append('description', versionDescription.value)
        }
        
        await documentStore.createDocumentVersion(documentId.value, formData)
        
        // Reset form
        selectedFile.value = null
        versionDescription.value = ''
        if (fileInput.value) {
          fileInput.value.value = ''
        }
      } catch (error) {
        console.error('Error uploading new version:', error)
      } finally {
        uploadingVersion.value = false
      }
    }
    
    const formatDocumentType = (type) => {
      if (!type) return 'Unknown'
      
      // If it's already formatted (from document_type_display), return as is
      if (type.includes(' ')) return type
      
      // Convert snake_case to Title Case
      return type
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    const formatFileSize = (bytes) => {
      if (!bytes) return 'Unknown size'
      
      const units = ['B', 'KB', 'MB', 'GB']
      let size = bytes
      let unitIndex = 0
      
      while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024
        unitIndex++
      }
      
      return `${size.toFixed(1)} ${units[unitIndex]}`
    }
    
    const formatDateTime = (dateString) => {
      if (!dateString) return 'Not provided'
      const date = new Date(dateString)
      return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`
    }
    
    // Lifecycle hooks
    onMounted(() => {
      fetchDocumentData()
    })
    
    return {
      document,
      loading,
      error,
      documentId,
      showDeleteModal,
      deletingDocument,
      fileInput,
      selectedFile,
      versionDescription,
      uploadingVersion,
      isImage,
      isPdf,
      fetchDocumentData,
      downloadDocument,
      navigateToEdit,
      confirmDelete,
      deleteDocument,
      navigateToApplication,
      navigateToBorrower,
      handleFileSelected,
      uploadNewVersion,
      formatDocumentType,
      formatFileSize,
      formatDateTime
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
