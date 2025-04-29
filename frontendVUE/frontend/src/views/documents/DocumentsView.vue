<template>
  <div class="documents-view">
    <div class="container-fluid py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Documents</h1>
        <button class="btn btn-primary" @click="showUploadDocumentModal">
          <i class="bi bi-upload me-2"></i> Upload Document
        </button>
      </div>

      <!-- Search and filters -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-4">
              <div class="input-group">
                <span class="input-group-text">
                  <i class="bi bi-search"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Search by title or description"
                  v-model="filters.search"
                  @input="handleSearchInput"
                />
                <button
                  class="btn btn-outline-secondary"
                  type="button"
                  @click="clearSearch"
                  v-if="filters.search"
                >
                  <i class="bi bi-x"></i>
                </button>
              </div>
            </div>
            <div class="col-md-3">
              <select class="form-select" v-model="filters.document_type" @change="applyFilters">
                <option value="">All Document Types</option>
                <option value="contract">Contract</option>
                <option value="application">Application</option>
                <option value="id">Identification</option>
                <option value="financial">Financial</option>
                <option value="property">Property</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div class="col-md-3">
              <select class="form-select" v-model="filters.application" @change="applyFilters">
                <option value="">All Applications</option>
                <option v-for="app in applications" :key="app.id" :value="app.id">
                  {{ app.reference_number }}
                </option>
              </select>
            </div>
            <div class="col-md-2">
              <button class="btn btn-outline-secondary w-100" @click="clearFilters">
                Clear Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading documents...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchDocuments">
          Try Again
        </button>
      </div>

      <!-- Empty state -->
      <div v-else-if="documents.length === 0" class="text-center py-5">
        <i class="bi bi-file-earmark display-1 text-muted"></i>
        <h3 class="mt-3">No documents found</h3>
        <p class="text-muted">
          {{ hasFilters ? 'Try adjusting your filters' : 'Upload your first document to get started' }}
        </p>
        <button class="btn btn-primary mt-3" @click="showUploadDocumentModal" v-if="!hasFilters">
          <i class="bi bi-upload me-2"></i> Upload Document
        </button>
      </div>

      <!-- Documents list -->
      <div v-else class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Title</th>
                      <th>Type</th>
                      <th>Application</th>
                      <th>Uploaded By</th>
                      <th>Uploaded At</th>
                      <th>Version</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="doc in documents" :key="doc.id">
                      <td>{{ doc.title }}</td>
                      <td>{{ doc.document_type_display || doc.document_type }}</td>
                      <td>{{ getApplicationReference(doc.application) }}</td>
                      <td>{{ doc.created_by_name }}</td>
                      <td>{{ formatDate(doc.created_at) }}</td>
                      <td>{{ doc.version }}</td>
                      <td>
                        <div class="btn-group">
                          <button class="btn btn-sm btn-outline-primary" @click="viewDocument(doc)">
                            <i class="bi bi-eye"></i>
                          </button>
                          <button class="btn btn-sm btn-outline-secondary" @click="downloadDocument(doc)">
                            <i class="bi bi-download"></i>
                          </button>
                          <button class="btn btn-sm btn-outline-info" @click="showCreateVersionModal(doc)" v-if="canCreateVersion(doc)">
                            <i class="bi bi-arrow-up-circle"></i>
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="documents.length > 0" class="d-flex justify-content-between align-items-center mt-4">
        <div>
          Showing {{ paginationInfo.currentPage * paginationInfo.itemsPerPage - paginationInfo.itemsPerPage + 1 }} to 
          {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }} of 
          {{ paginationInfo.totalItems }} documents
        </div>
        <nav aria-label="Document pagination">
          <ul class="pagination mb-0">
            <li class="page-item" :class="{ disabled: paginationInfo.currentPage === 1 }">
              <button class="page-link" @click="goToPage(paginationInfo.currentPage - 1)" :disabled="paginationInfo.currentPage === 1">
                Previous
              </button>
            </li>
            <li v-for="page in paginationInfo.totalPages" :key="page" class="page-item" :class="{ active: page === paginationInfo.currentPage }">
              <button class="page-link" @click="goToPage(page)">{{ page }}</button>
            </li>
            <li class="page-item" :class="{ disabled: paginationInfo.currentPage === paginationInfo.totalPages }">
              <button class="page-link" @click="goToPage(paginationInfo.currentPage + 1)" :disabled="paginationInfo.currentPage === paginationInfo.totalPages">
                Next
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- Upload Document Modal -->
    <div class="modal fade" id="uploadDocumentModal" tabindex="-1" aria-labelledby="uploadDocumentModalLabel" aria-hidden="true" ref="uploadDocumentModalRef">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="uploadDocumentModalLabel">Upload Document</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeUploadDocumentModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="documentTitle" class="form-label">Title*</label>
              <input type="text" class="form-control" id="documentTitle" v-model="newDocument.title" required>
              <div class="invalid-feedback" v-if="documentErrors.title">{{ documentErrors.title }}</div>
            </div>
            <div class="mb-3">
              <label for="documentType" class="form-label">Document Type*</label>
              <select class="form-select" id="documentType" v-model="newDocument.document_type" required>
                <option value="">Select Document Type</option>
                <option value="contract">Contract</option>
                <option value="application">Application</option>
                <option value="id">Identification</option>
                <option value="financial">Financial</option>
                <option value="property">Property</option>
                <option value="other">Other</option>
              </select>
              <div class="invalid-feedback" v-if="documentErrors.document_type">{{ documentErrors.document_type }}</div>
            </div>
            <div class="mb-3">
              <label for="documentApplication" class="form-label">Application</label>
              <select class="form-select" id="documentApplication" v-model="newDocument.application">
                <option value="">Select Application</option>
                <option v-for="app in applications" :key="app.id" :value="app.id">
                  {{ app.reference_number }}
                </option>
              </select>
              <div class="invalid-feedback" v-if="documentErrors.application">{{ documentErrors.application }}</div>
            </div>
            <div class="mb-3">
              <label for="documentDescription" class="form-label">Description</label>
              <textarea class="form-control" id="documentDescription" v-model="newDocument.description" rows="3"></textarea>
            </div>
            <div class="mb-3">
              <label for="documentFile" class="form-label">File*</label>
              <input type="file" class="form-control" id="documentFile" @change="handleFileChange" required>
              <div class="invalid-feedback" v-if="documentErrors.file">{{ documentErrors.file }}</div>
              <div class="form-text" v-if="selectedFile">
                Selected file: {{ selectedFile.name }} ({{ formatFileSize(selectedFile.size) }})
              </div>
            </div>
            <div class="alert alert-danger" v-if="documentErrors.general">{{ documentErrors.general }}</div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeUploadDocumentModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="uploadDocument" :disabled="uploading">
              <span v-if="uploading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Upload
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Version Modal -->
    <div class="modal fade" id="createVersionModal" tabindex="-1" aria-labelledby="createVersionModalLabel" aria-hidden="true" ref="createVersionModalRef">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="createVersionModalLabel">Upload New Version</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeCreateVersionModal"></button>
          </div>
          <div class="modal-body">
            <p>Upload a new version for document: <strong>{{ selectedDocument?.title }}</strong></p>
            <div class="mb-3">
              <label for="versionDescription" class="form-label">Description of Changes</label>
              <textarea class="form-control" id="versionDescription" v-model="versionData.description" rows="3"></textarea>
            </div>
            <div class="mb-3">
              <label for="versionFile" class="form-label">File*</label>
              <input type="file" class="form-control" id="versionFile" @change="handleVersionFileChange" required>
              <div class="invalid-feedback" v-if="versionErrors.file">{{ versionErrors.file }}</div>
              <div class="form-text" v-if="selectedVersionFile">
                Selected file: {{ selectedVersionFile.name }} ({{ formatFileSize(selectedVersionFile.size) }})
              </div>
            </div>
            <div class="alert alert-danger" v-if="versionErrors.general">{{ versionErrors.general }}</div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeCreateVersionModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="createVersion" :disabled="creatingVersion">
              <span v-if="creatingVersion" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Upload New Version
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useDocumentStore } from '@/store/document'
import { useApplicationStore } from '@/store/application'
import { Modal } from 'bootstrap'

export default {
  name: 'DocumentsView',
  setup() {
    const documentStore = useDocumentStore()
    const applicationStore = useApplicationStore()
    
    // State
    const filters = ref({
      search: '',
      document_type: '',
      application: ''
    })
    
    // Modal references
    const uploadDocumentModalRef = ref(null)
    const createVersionModalRef = ref(null)
    let uploadDocumentModal = null
    let createVersionModal = null
    
    // New document form
    const newDocument = ref({
      title: '',
      document_type: '',
      application: '',
      description: ''
    })
    const selectedFile = ref(null)
    const documentErrors = ref({
      title: '',
      document_type: '',
      application: '',
      file: '',
      general: ''
    })
    const uploading = ref(false)
    
    // Create version form
    const selectedDocument = ref(null)
    const versionData = ref({
      description: ''
    })
    const selectedVersionFile = ref(null)
    const versionErrors = ref({
      file: '',
      general: ''
    })
    const creatingVersion = ref(false)
    
    // Computed properties
    const documents = computed(() => documentStore.documents)
    const applications = computed(() => applicationStore.applications)
    const loading = computed(() => documentStore.loading)
    const error = computed(() => documentStore.error)
    const paginationInfo = computed(() => documentStore.getPaginationInfo)
    const hasFilters = computed(() => {
      return filters.value.search || filters.value.document_type || filters.value.application
    })
    
    // Methods
    const fetchDocuments = async () => {
      try {
        await documentStore.fetchDocuments()
      } catch (error) {
        console.error('Error fetching documents:', error)
      }
    }
    
    const fetchApplications = async () => {
      try {
        await applicationStore.fetchApplications()
      } catch (error) {
        console.error('Error fetching applications:', error)
      }
    }
    
    const handleSearchInput = () => {
      documentStore.setFilters({ search: filters.value.search })
    }
    
    const applyFilters = () => {
      documentStore.setFilters({
        documentType: filters.value.document_type,
        application: filters.value.application
      })
    }
    
    const clearSearch = () => {
      filters.value.search = ''
      documentStore.setFilters({ search: '' })
    }
    
    const clearFilters = () => {
      filters.value = {
        search: '',
        document_type: '',
        application: ''
      }
      documentStore.clearFilters()
    }
    
    const goToPage = (page) => {
      if (page < 1 || page > paginationInfo.value.totalPages) return
      documentStore.setPage(page)
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
    }
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    const getApplicationReference = (applicationId) => {
      if (!applicationId) return 'N/A'
      const app = applications.value.find(app => app.id === applicationId)
      return app ? app.reference_number : `App #${applicationId}`
    }
    
    // Initialize modals
    const initModals = () => {
      if (uploadDocumentModalRef.value) {
        uploadDocumentModal = new Modal(uploadDocumentModalRef.value)
      }
      if (createVersionModalRef.value) {
        createVersionModal = new Modal(createVersionModalRef.value)
      }
    }
    
    // Upload document modal
    const showUploadDocumentModal = () => {
      // Reset form
      newDocument.value = {
        title: '',
        document_type: '',
        application: '',
        description: ''
      }
      selectedFile.value = null
      documentErrors.value = {
        title: '',
        document_type: '',
        application: '',
        file: '',
        general: ''
      }
      
      // Show modal
      if (uploadDocumentModal) {
        uploadDocumentModal.show()
      }
    }
    
    const closeUploadDocumentModal = () => {
      if (uploadDocumentModal) {
        uploadDocumentModal.hide()
      }
    }
    
    const handleFileChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        selectedFile.value = file
        documentErrors.value.file = ''
      } else {
        selectedFile.value = null
      }
    }
    
    const validateDocumentForm = () => {
      let isValid = true
      documentErrors.value = {
        title: '',
        document_type: '',
        application: '',
        file: '',
        general: ''
      }
      
      if (!newDocument.value.title) {
        documentErrors.value.title = 'Title is required'
        isValid = false
      }
      
      if (!newDocument.value.document_type) {
        documentErrors.value.document_type = 'Document type is required'
        isValid = false
      }
      
      if (!selectedFile.value) {
        documentErrors.value.file = 'File is required'
        isValid = false
      }
      
      return isValid
    }
    
    const uploadDocument = async () => {
      if (!validateDocumentForm()) {
        return
      }
      
      uploading.value = true
      
      try {
        // Create FormData for file upload
        const formData = new FormData()
        formData.append('title', newDocument.value.title)
        formData.append('document_type', newDocument.value.document_type)
        formData.append('file', selectedFile.value)
        
        if (newDocument.value.application) {
          formData.append('application', newDocument.value.application)
        }
        
        if (newDocument.value.description) {
          formData.append('description', newDocument.value.description)
        }
        
        await documentStore.createDocument(formData)
        closeUploadDocumentModal()
        fetchDocuments()
      } catch (error) {
        documentErrors.value.general = error.message || 'Failed to upload document'
        console.error('Error uploading document:', error)
      } finally {
        uploading.value = false
      }
    }
    
    // View document
    const viewDocument = (document) => {
      // Open document in new tab if URL is available
      if (document.file_url) {
        window.open(document.file_url, '_blank')
      }
    }
    
    // Download document
    const downloadDocument = async (document) => {
      try {
        await documentStore.downloadDocument(document.id)
      } catch (error) {
        console.error('Error downloading document:', error)
      }
    }
    
    // Create version modal
    const showCreateVersionModal = (document) => {
      selectedDocument.value = document
      versionData.value = {
        description: ''
      }
      selectedVersionFile.value = null
      versionErrors.value = {
        file: '',
        general: ''
      }
      
      if (createVersionModal) {
        createVersionModal.show()
      }
    }
    
    const closeCreateVersionModal = () => {
      if (createVersionModal) {
        createVersionModal.hide()
      }
    }
    
    const handleVersionFileChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        selectedVersionFile.value = file
        versionErrors.value.file = ''
      } else {
        selectedVersionFile.value = null
      }
    }
    
    const validateVersionForm = () => {
      let isValid = true
      versionErrors.value = {
        file: '',
        general: ''
      }
      
      if (!selectedVersionFile.value) {
        versionErrors.value.file = 'File is required'
        isValid = false
      }
      
      return isValid
    }
    
    const createVersion = async () => {
      if (!validateVersionForm()) {
        return
      }
      
      creatingVersion.value = true
      
      try {
        // Create FormData for file upload
        const formData = new FormData()
        formData.append('file', selectedVersionFile.value)
        
        if (versionData.value.description) {
          formData.append('description', versionData.value.description)
        }
        
        await documentStore.createDocumentVersion(selectedDocument.value.id, formData)
        closeCreateVersionModal()
        fetchDocuments()
      } catch (error) {
        versionErrors.value.general = error.message || 'Failed to create new version'
        console.error('Error creating new version:', error)
      } finally {
        creatingVersion.value = false
      }
    }
    
    const canCreateVersion = (document) => {
      // Logic to determine if user can create a new version
      // For now, allow creating new versions for all documents
      return true
    }
    
    // Fetch documents and applications on component mount
    onMounted(() => {
      fetchDocuments()
      fetchApplications()
      
      // Initialize modals after DOM is ready
      setTimeout(() => {
        initModals()
      }, 100)
    })
    
    return {
      documents,
      applications,
      loading,
      error,
      filters,
      paginationInfo,
      hasFilters,
      fetchDocuments,
      handleSearchInput,
      applyFilters,
      clearSearch,
      clearFilters,
      goToPage,
      formatDate,
      formatFileSize,
      getApplicationReference,
      
      // Upload document modal
      uploadDocumentModalRef,
      newDocument,
      selectedFile,
      documentErrors,
      uploading,
      showUploadDocumentModal,
      closeUploadDocumentModal,
      handleFileChange,
      uploadDocument,
      
      // View and download document
      viewDocument,
      downloadDocument,
      
      // Create version modal
      createVersionModalRef,
      selectedDocument,
      versionData,
      selectedVersionFile,
      versionErrors,
      creatingVersion,
      showCreateVersionModal,
      closeCreateVersionModal,
      handleVersionFileChange,
      createVersion,
      canCreateVersion
    }
  }
}
</script>

<style scoped>
.documents-view {
  min-height: 100vh;
}

.invalid-feedback {
  display: block;
}
</style>
