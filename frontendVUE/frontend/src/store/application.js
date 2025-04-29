import { defineStore } from 'pinia'
import applicationService from '@/services/application.service'
import feeService from '@/services/fee.service'
import repaymentService from '@/services/repayment.service'

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
        }
        
        // Update current application if it's the one being edited
        if (this.currentApplication && this.currentApplication.id === id) {
          this.currentApplication.stage = stage
        }
        
        return response
      } catch (error) {
        this.error = error.message || `Failed to update stage for application with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // Fee-related actions
    async fetchApplicationFees(applicationId, limit = 10, offset = 0, isPaid = null, feeType = null) {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          application: applicationId,
          limit,
          offset
        }
        
        if (isPaid !== null) {
          params.is_paid = isPaid
        }
        
        if (feeType) {
          params.fee_type = feeType
        }
        
        const response = await feeService.getFees(params)
        return response
      } catch (error) {
        this.error = error.message || 'Failed to fetch application fees'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async addApplicationFee(applicationId, feeData) {
      this.loading = true
      this.error = null
      
      try {
        const data = {
          ...feeData,
          application: applicationId
        }
        
        const response = await feeService.createFee(data)
        return response
      } catch (error) {
        this.error = error.message || 'Failed to add fee'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async markFeePaid(feeId, paymentData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await feeService.markFeePaid(feeId, paymentData)
        return response
      } catch (error) {
        this.error = error.message || 'Failed to mark fee as paid'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // Repayment-related actions
    async fetchApplicationRepayments(applicationId, limit = 10, offset = 0, isPaid = null, dateFrom = null, dateTo = null) {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          application: applicationId,
          limit,
          offset
        }
        
        if (isPaid !== null) {
          params.is_paid = isPaid
        }
        
        if (dateFrom) {
          params.date_from = dateFrom
        }
        
        if (dateTo) {
          params.date_to = dateTo
        }
        
        const response = await repaymentService.getRepayments(params)
        return response
      } catch (error) {
        this.error = error.message || 'Failed to fetch application repayments'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async addApplicationRepayment(applicationId, repaymentData) {
      this.loading = true
      this.error = null
      
      try {
        const data = {
          ...repaymentData,
          application: applicationId
        }
        
        const response = await repaymentService.createRepayment(data)
        return response
      } catch (error) {
        this.error = error.message || 'Failed to add repayment'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async markRepaymentPaid(repaymentId, paymentData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await repaymentService.markRepaymentPaid(repaymentId, paymentData)
        return response
      } catch (error) {
        this.error = error.message || 'Failed to mark repayment as paid'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
