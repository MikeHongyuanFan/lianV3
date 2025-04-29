<template>
  <div class="application-documents-container">
    <div class="documents-header">
      <h3>Application Documents</h3>
      <BaseButton @click="showUploadModal = true" variant="primary">Upload Document</BaseButton>
    </div>

    <!-- Document type filter -->
    <div class="filter-container">
      <label for="documentTypeFilter">Filter by document type:</label>
      <select 
        id="documentTypeFilter" 
        v-model="documentTypeFilter" 
        class="form-control"
        @change="handleFilterChange"
      >
        <option value="">All document types</option>
        <option value="contract">Contract</option>
        <option value="id_verification">ID Verification</option>
        <option value="income_proof">Income Proof</option>
        <option value="property_valuation">Property Valuation</option>
        <option value="bank_statement">Bank Statement</option>
        <option value="credit_report">Credit Report</option>
        <option value="other">Other</option>
      </select>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-container">
      <p>Loading documents...</p>
    </div>

    <!-- Error display -->
    <AlertMessage v-if="error" :message="error" type="error" />

    <!-- Empty state -->
    <div v-if="!loading && !error && (!documents || documents.length === 0)" class="empty-state">
      <p>No documents found for this application.</p>
    </div>

    <!-- Documents list -->
    <div v-if="!loading && !error && documents && documents.length > 0" class="documents-list">
      <div v-for="document in documents" :key="document.id" class="document-card">
        <div class="document-header">
          <div class="document-title">{{ document.title }}</div>
          <div class="document-type">{{ document.document_type_display }}</div>
        </div>
        <div class="document-meta">
          <div class="document-info">
            <div class="document-size">{{ formatFileSize(document.file_size) }}</div>
            <div class="document-date">Uploaded: {{ formatDate(document.created_at) }}</div>
            <div class="document-uploader">By: {{ document.created_by_name }}</div>
          </div>
          <div class="document-actions">
            <a :href="document.file_url" target="_blank" class="view-button">View</a>
            <a :href="`/api/documents/documents/${document.id}/download/`" class="download-button">Download</a>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalDocuments > limit" class="pagination">
        <button 
          :disabled="currentPage === 1" 
          @click="changePage(currentPage - 1)" 
          class="pagination-button"
        >
          Previous
        </button>
        <span class="pagination-info">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button 
          :disabled="currentPage === totalPages" 
          @click="changePage(currentPage + 1)" 
          class="pagination-button"
        >
          Next
        </button>
      </div>
    </div>

    <!-- Upload Document Modal -->
    <div v-if="showUploadModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Upload Document</h3>
          <button @click="showUploadModal = false" class="close-button">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="documentTitle">Document Title</label>
            <input 
              id="documentTitle" 
              v-model="newDocument.title" 
              type="text" 
              class="form-control"
              placeholder="Enter document title"
            />
          </div>
          <div class="form-group">
            <label for="documentType">Document Type</label>
            <select 
              id="documentType" 
              v-model="newDocument.document_type" 
              class="form-control"
            >
              <option value="">Select document type</option>
              <option value="contract">Contract</option>
              <option value="id_verification">ID Verification</option>
              <option value="income_proof">Income Proof</option>
              <option value="property_valuation">Property Valuation</option>
              <option value="bank_statement">Bank Statement</option>
              <option value="credit_report">Credit Report</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div class="form-group">
            <label for="documentFile">Document File</label>
            <input 
              id="documentFile" 
              type="file" 
              @change="handleFileChange" 
              class="form-control"
            />
          </div>
          <div v-if="uploadError" class="error-message">{{ uploadError }}</div>
        </div>
        <div class="modal-footer">
          <BaseButton @click="showUploadModal = false" variant="secondary">Cancel</BaseButton>
          <BaseButton @click="uploadDocument" variant="primary" :loading="uploading">Upload</BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useApplicationStore } from '@/store/application'
import BaseButton from '@/components/BaseButton.vue'
import AlertMessage from '@/components/AlertMessage.vue'

export default {
  name: 'ApplicationDocumentsList',
  components: {
    BaseButton,
    AlertMessage
  },
  props: {
    applicationId: {
      type: [Number, String],
      required: true
    }
  },
  setup(props) {
    const applicationStore = useApplicationStore()
    
    // Documents state
    const documents = ref([])
    const loading = ref(false)
    const error = ref(null)
    const totalDocuments = ref(0)
    const limit = ref(10)
    const offset = ref(0)
    const documentTypeFilter = ref('')
    
    // Upload document state
    const showUploadModal = ref(false)
    const newDocument = ref({
      title: '',
      document_type: '',
      file: null
    })
    const uploadError = ref(null)
    const uploading = ref(false)
    
    // Computed properties
    const currentPage = computed(() => Math.floor(offset.value / limit.value) + 1)
    const totalPages = computed(() => Math.ceil(totalDocuments.value / limit.value))
    
    // Fetch documents
    const fetchDocuments = async () => {
      try {
        loading.value = true
        error.value = null
        
        const response = await applicationStore.fetchApplicationDocuments(
          props.applicationId,
          limit.value,
          offset.value,
          documentTypeFilter.value || null
        )
        
        documents.value = response.results
        totalDocuments.value = response.count
      } catch (err) {
        error.value = err.message || 'Failed to load documents'
        console.error('Error fetching documents:', err)
      } finally {
        loading.value = false
      }
    }
    
    // Change page
    const changePage = (page) => {
      offset.value = (page - 1) * limit.value
      fetchDocuments()
    }
    
    // Handle filter change
    const handleFilterChange = () => {
      offset.value = 0 // Reset to first page
      fetchDocuments()
    }
    
    // Handle file selection
    const handleFileChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        newDocument.value.file = file
      }
    }
    
    // Upload document
    const uploadDocument = async () => {
      // Validate input
      if (!newDocument.value.title || newDocument.value.title.trim() === '') {
        uploadError.value = 'Document title is required'
        return
      }
      
      if (!newDocument.value.document_type) {
        uploadError.value = 'Document type is required'
        return
      }
      
      if (!newDocument.value.file) {
        uploadError.value = 'Document file is required'
        return
      }
      
      try {
        uploading.value = true
        uploadError.value = null
        
        // Create FormData object for file upload
        const formData = new FormData()
        formData.append('title', newDocument.value.title)
        formData.append('document_type', newDocument.value.document_type)
        formData.append('file', newDocument.value.file)
        
        await applicationStore.uploadApplicationDocument(
          props.applicationId,
          formData
        )
        
        // Reset form and close modal
        newDocument.value = {
          title: '',
          document_type: '',
          file: null
        }
        showUploadModal.value = false
        
        // Refresh documents list
        await fetchDocuments()
      } catch (err) {
        uploadError.value = err.message || 'Failed to upload document'
        console.error('Error uploading document:', err)
      } finally {
        uploading.value = false
      }
    }
    
    // Format file size
    const formatFileSize = (bytes) => {
      if (!bytes) return '0 Bytes'
      
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    // Format date
    const formatDate = (dateString) => {
      if (!dateString) return ''
      
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      }).format(date)
    }
    
    onMounted(() => {
      fetchDocuments()
    })
    
    return {
      documents,
      loading,
      error,
      totalDocuments,
      limit,
      currentPage,
      totalPages,
      documentTypeFilter,
      showUploadModal,
      newDocument,
      uploadError,
      uploading,
      changePage,
      handleFilterChange,
      handleFileChange,
      uploadDocument,
      formatFileSize,
      formatDate
    }
  }
}
</script>

<style scoped>
.application-documents-container {
  margin-bottom: 2rem;
}

.documents-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.documents-header h3 {
  margin: 0;
}

.filter-container {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-container label {
  font-weight: 500;
}

.form-control {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-family: inherit;
  font-size: inherit;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  background-color: #f9fafb;
  border-radius: 0.5rem;
}

.empty-state {
  padding: 2rem;
  text-align: center;
  background-color: #f9fafb;
  border-radius: 0.5rem;
  color: #6b7280;
}

.documents-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.document-card {
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

.document-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.document-title {
  font-weight: 600;
  font-size: 1.125rem;
}

.document-type {
  background-color: #e5e7eb;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.document-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.document-info {
  color: #6b7280;
  font-size: 0.875rem;
}

.document-actions {
  display: flex;
  gap: 0.5rem;
}

.view-button, .download-button {
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  text-decoration: none;
  cursor: pointer;
}

.view-button {
  background-color: #f3f4f6;
  color: #4b5563;
  border: 1px solid #d1d5db;
}

.download-button {
  background-color: #3b82f6;
  color: white;
  border: 1px solid #2563eb;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1.5rem;
  gap: 1rem;
}

.pagination-button {
  padding: 0.5rem 1rem;
  background-color: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  cursor: pointer;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  color: #6b7280;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-container {
  background-color: white;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
}

.modal-body {
  padding: 1rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style>
