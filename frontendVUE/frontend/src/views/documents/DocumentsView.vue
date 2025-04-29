<template>
  <div class="documents-view">
    <div class="container-fluid py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Documents</h1>
        <button class="btn btn-primary">
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
        <button class="btn btn-primary mt-3" v-if="!hasFilters">
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
                          <button class="btn btn-sm btn-outline-info" @click="createVersion(doc)" v-if="canCreateVersion(doc)">
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
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useDocumentStore } from '@/store/document'
import { useApplicationStore } from '@/store/application'
import documentService from '@/services/document.service'

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
        document_type: filters.value.document_type,
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
    
    const getApplicationReference = (applicationId) => {
      if (!applicationId) return 'N/A'
      const app = applications.value.find(app => app.id === applicationId)
      return app ? app.reference_number : `App #${applicationId}`
    }
    
    const viewDocument = (document) => {
      // In a real implementation, this would open the document for viewing
      window.open(document.file_url, '_blank')
    }
    
    const downloadDocument = async (document) => {
      try {
        await documentService.downloadDocument(document.id)
      } catch (error) {
        console.error('Error downloading document:', error)
      }
    }
    
    const createVersion = (document) => {
      // In a real implementation, this would open a modal to upload a new version
      console.log('Create new version for document:', document.id)
    }
    
    const canCreateVersion = (document) => {
      // Logic to determine if user can create a new version
      return true
    }
    
    // Fetch documents and applications on component mount
    onMounted(() => {
      fetchDocuments()
      fetchApplications()
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
      getApplicationReference,
      viewDocument,
      downloadDocument,
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
</style>
