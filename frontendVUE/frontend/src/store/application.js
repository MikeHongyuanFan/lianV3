import { defineStore } from 'pinia'
import applicationService from '@/services/application.service'
import feeService from '@/services/fee.service'

export const useApplicationStore = defineStore('application', {
  state: () => ({
    applications: [],
    currentApplication: null,
    totalApplications: 0,
    loading: false,
    error: null,
    filters: {
      search: '',
      status: '',
      stage: '',
      borrower: null,
      dateFrom: null,
      dateTo: null
    },
    pagination: {
      limit: 10,
      offset: 0
    }
  }),

  getters: {
    getApplicationById: (state) => (id) => {
      return state.applications.find(app => app.id === id) || null
    },
    
    getFilteredApplications: (state) => {
      return state.applications
    },
    
    getPaginationInfo: (state) => {
      return {
        currentPage: Math.floor(state.pagination.offset / state.pagination.limit) + 1,
        totalPages: Math.ceil(state.totalApplications / state.pagination.limit),
        totalItems: state.totalApplications,
        itemsPerPage: state.pagination.limit
      }
    },
    
    hasApplications: (state) => {
      return state.applications && state.applications.length > 0
    }
  },

  actions: {
    async fetchApplications() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          limit: this.pagination.limit,
          offset: this.pagination.offset,
          search: this.filters.search || undefined,
          status: this.filters.status || undefined,
          stage: this.filters.stage || undefined,
          borrower: this.filters.borrower || undefined,
          date_from: this.filters.dateFrom || undefined,
          date_to: this.filters.dateTo || undefined
        }
        
        const response = await applicationService.getApplications(params)
        
        // Ensure applications is always an array
        if (Array.isArray(response.results)) {
          this.applications = response.results
        } else {
          this.applications = []
          console.warn('Expected array for applications.results but got:', response.results)
        }
        
        this.totalApplications = response.count || 0
        return response
      } catch (error) {
        this.error = error.message || 'Failed to fetch applications'
        this.applications = [] // Ensure applications is an array even on error
        console.error('Error in fetchApplications:', error)
        return { results: [], count: 0 }
      } finally {
        this.loading = false
      }
    },
    
    async fetchApplication(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await applicationService.getApplicationById(id)
        this.currentApplication = response
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch application with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createApplication(applicationData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await applicationService.createApplication(applicationData)
        // Refresh applications list after creation
        await this.fetchApplications()
        return response
      } catch (error) {
        this.error = error.message || 'Failed to create application'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createApplicationWithCascade(applicationData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await applicationService.createApplicationWithCascade(applicationData)
        // Refresh applications list after creation
        await this.fetchApplications()
        return response
      } catch (error) {
        this.error = error.message || 'Failed to create application with related entities'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateApplication(id, applicationData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await applicationService.updateApplication(id, applicationData)
        
        // Update the application in the list if it exists
        const index = this.applications.findIndex(app => app.id === id)
        if (index !== -1) {
          this.applications[index] = { ...this.applications[index], ...response }
        }
        
        // Update current application if it's the one being edited
        if (this.currentApplication && this.currentApplication.id === id) {
          this.currentApplication = { ...this.currentApplication, ...response }
        }
        
        return response
      } catch (error) {
        this.error = error.message || `Failed to update application with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteApplication(id) {
      this.loading = true
      this.error = null
      
      try {
        await applicationService.deleteApplication(id)
        
        // Remove the application from the list
        this.applications = this.applications.filter(app => app.id !== id)
        
        // Clear current application if it's the one being deleted
        if (this.currentApplication && this.currentApplication.id === id) {
          this.currentApplication = null
        }
        
        // Refresh the list to update counts
        await this.fetchApplications()
      } catch (error) {
        this.error = error.message || `Failed to delete application with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateApplicationStage(id, stage) {
      this.loading = true
      this.error = null
      
      try {
        const response = await applicationService.updateStage(id, stage)
        
        // Update the application in the list if it exists
        const index = this.applications.findIndex(app => app.id === id)
        if (index !== -1) {
          this.applications[index].stage = stage
          this.applications[index].stage_display = response.stage_display
        }
        
        // Update current application if it's the one being edited
        if (this.currentApplication && this.currentApplication.id === id) {
          this.currentApplication.stage = stage
          this.currentApplication.stage_display = response.stage_display
        }
        
        return response
      } catch (error) {
        this.error = error.message || `Failed to update stage for application with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async validateApplicationSchema(schemaData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await applicationService.validateSchema(schemaData)
        return response
      } catch (error) {
        this.error = error.message || 'Failed to validate application schema'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchApplicationGuarantors(id) {
      try {
        const response = await applicationService.getGuarantors(id)
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch guarantors for application with ID ${id}`
        throw error
      }
    },
    
    async fetchApplicationNotes(id, limit = 10, offset = 0) {
      try {
        const params = { limit, offset }
        const response = await applicationService.getNotes(id, params)
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch notes for application with ID ${id}`
        throw error
      }
    },
    
    async addApplicationNote(id, content) {
      try {
        const noteData = { content }
        const response = await applicationService.addNote(id, noteData)
        return response
      } catch (error) {
        this.error = error.message || `Failed to add note to application with ID ${id}`
        throw error
      }
    },
    
    async fetchApplicationDocuments(id, limit = 10, offset = 0, documentType = null) {
      try {
        const params = { 
          limit, 
          offset,
          document_type: documentType || undefined
        }
        const response = await applicationService.getDocuments(id, params)
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch documents for application with ID ${id}`
        throw error
      }
    },
    
    async uploadApplicationDocument(id, documentData) {
      try {
        const response = await applicationService.uploadDocument(id, documentData)
        return response
      } catch (error) {
        this.error = error.message || `Failed to upload document to application with ID ${id}`
        throw error
      }
    },
    
    async fetchApplicationFees(id, limit = 10, offset = 0, isPaid = null, feeType = null) {
      try {
        const params = { 
          limit, 
          offset,
          is_paid: isPaid !== null ? isPaid : undefined,
          fee_type: feeType || undefined
        }
        const response = await applicationService.getFees(id, params)
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch fees for application with ID ${id}`
        throw error
      }
    },
    
    async addApplicationFee(id, feeData) {
      try {
        const response = await applicationService.addFee(id, feeData)
        return response
      } catch (error) {
        this.error = error.message || `Failed to add fee to application with ID ${id}`
        throw error
      }
    },
    
    async markFeePaid(id, paymentData) {
      try {
        const response = await feeService.markFeePaid(id, paymentData)
        return response
      } catch (error) {
        this.error = error.message || `Failed to mark fee with ID ${id} as paid`
        throw error
      }
    },
    
    async fetchApplicationRepayments(id, limit = 10, offset = 0, isPaid = null) {
      try {
        const params = { 
          limit, 
          offset,
          is_paid: isPaid !== null ? isPaid : undefined
        }
        const response = await applicationService.getRepayments(id, params)
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch repayments for application with ID ${id}`
        throw error
      }
    },
    
    async addApplicationRepayment(id, repaymentData) {
      try {
        const response = await applicationService.addRepayment(id, repaymentData)
        return response
      } catch (error) {
        this.error = error.message || `Failed to add repayment to application with ID ${id}`
        throw error
      }
    },
    
    async recordApplicationPayment(id, paymentData) {
      try {
        const response = await applicationService.recordPayment(id, paymentData)
        return response
      } catch (error) {
        this.error = error.message || `Failed to record payment for application with ID ${id}`
        throw error
      }
    },
    
    async fetchApplicationLedger(id, limit = 10, offset = 0) {
      try {
        const params = { limit, offset }
        const response = await applicationService.getLedger(id, params)
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch ledger for application with ID ${id}`
        throw error
      }
    },
    
    // Pagination and filtering actions
    setPage(page) {
      const offset = (page - 1) * this.pagination.limit
      this.pagination.offset = offset
      this.fetchApplications()
    },
    
    setLimit(limit) {
      this.pagination.limit = limit
      this.pagination.offset = 0 // Reset to first page
      this.fetchApplications()
    },
    
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.offset = 0 // Reset to first page
      this.fetchApplications()
    },
    
    clearFilters() {
      this.filters = {
        search: '',
        status: '',
        stage: '',
        borrower: null,
        dateFrom: null,
        dateTo: null
      }
      this.fetchApplications()
    }
  }
})
