import { defineStore } from 'pinia'
import documentService from '@/services/document.service'

export const useDocumentStore = defineStore('document', {
  state: () => ({
    documents: [],
    currentDocument: null,
    totalDocuments: 0,
    loading: false,
    error: null,
    filters: {
      search: '',
      documentType: '',
      application: null,
      borrower: null
    },
    pagination: {
      limit: 10,
      offset: 0
    }
  }),

  getters: {
    getDocumentById: (state) => (id) => {
      return state.documents.find(document => document.id === parseInt(id)) || null
    },
    
    getFilteredDocuments: (state) => {
      return state.documents
    },
    
    getPaginationInfo: (state) => {
      return {
        currentPage: Math.floor(state.pagination.offset / state.pagination.limit) + 1,
        totalPages: Math.ceil(state.totalDocuments / state.pagination.limit),
        totalItems: state.totalDocuments,
        itemsPerPage: state.pagination.limit
      }
    },
    
    hasDocuments: (state) => {
      return state.documents.length > 0
    }
  },

  actions: {
    async fetchDocuments() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          limit: this.pagination.limit,
          offset: this.pagination.offset,
          search: this.filters.search || undefined,
          document_type: this.filters.documentType || undefined,
          application: this.filters.application || undefined,
          borrower: this.filters.borrower || undefined
        }
        
        const response = await documentService.getDocuments(params)
        this.documents = response.results
        this.totalDocuments = response.count
        return response
      } catch (error) {
        this.error = error.message || 'Failed to fetch documents'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchDocumentById(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await documentService.getDocumentById(id)
        this.currentDocument = response
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch document with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createDocument(documentData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await documentService.createDocument(documentData)
        // Refresh documents list after creation
        await this.fetchDocuments()
        return response
      } catch (error) {
        this.error = error.message || 'Failed to create document'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateDocument(id, documentData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await documentService.updateDocument(id, documentData)
        
        // Update the document in the list if it exists
        const index = this.documents.findIndex(document => document.id === parseInt(id))
        if (index !== -1) {
          this.documents[index] = { ...this.documents[index], ...response }
        }
        
        // Update current document if it's the one being edited
        if (this.currentDocument && this.currentDocument.id === parseInt(id)) {
          this.currentDocument = { ...this.currentDocument, ...response }
        }
        
        return response
      } catch (error) {
        this.error = error.message || `Failed to update document with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteDocument(id) {
      this.loading = true
      this.error = null
      
      try {
        await documentService.deleteDocument(id)
        
        // Remove the document from the list
        this.documents = this.documents.filter(document => document.id !== parseInt(id))
        
        // Clear current document if it's the one being deleted
        if (this.currentDocument && this.currentDocument.id === parseInt(id)) {
          this.currentDocument = null
        }
        
        // Refresh the list to update counts
        await this.fetchDocuments()
      } catch (error) {
        this.error = error.message || `Failed to delete document with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async downloadDocument(id) {
      this.loading = true
      this.error = null
      
      try {
        const blob = await documentService.downloadDocument(id)
        
        // Get document details to determine filename
        const document = this.getDocumentById(id) || this.currentDocument
        const fileName = document?.file_name || `document-${id}.pdf`
        
        // Create download link and trigger download
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', fileName)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        return blob
      } catch (error) {
        this.error = error.message || `Failed to download document with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createDocumentVersion(id, versionData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await documentService.createDocumentVersion(id, versionData)
        
        // Refresh current document to show new version
        if (this.currentDocument && this.currentDocument.id === parseInt(id)) {
          await this.fetchDocumentById(response.document_id)
        }
        
        return response
      } catch (error) {
        this.error = error.message || `Failed to create new version for document with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // Pagination and filtering actions
    setPage(page) {
      const offset = (page - 1) * this.pagination.limit
      this.pagination.offset = offset
      this.fetchDocuments()
    },
    
    setLimit(limit) {
      this.pagination.limit = limit
      this.pagination.offset = 0 // Reset to first page
      this.fetchDocuments()
    },
    
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.offset = 0 // Reset to first page
      this.fetchDocuments()
    },
    
    clearFilters() {
      this.filters = {
        search: '',
        documentType: '',
        application: null,
        borrower: null
      }
      this.fetchDocuments()
    }
  }
})
