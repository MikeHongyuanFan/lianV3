import { defineStore } from 'pinia'
import repaymentService from '@/services/repayment.service'

export const useRepaymentStore = defineStore('repayment', {
  state: () => ({
    repayments: [],
    currentRepayment: null,
    totalRepayments: 0,
    loading: false,
    error: null,
    filters: {
      application: null,
      isPaid: null,
      dateFrom: '',
      dateTo: ''
    },
    pagination: {
      limit: 10,
      offset: 0
    }
  }),

  getters: {
    getRepaymentById: (state) => (id) => {
      return state.repayments.find(repayment => repayment.id === parseInt(id)) || null
    },
    
    getFilteredRepayments: (state) => {
      return state.repayments
    },
    
    getPaginationInfo: (state) => {
      return {
        currentPage: Math.floor(state.pagination.offset / state.pagination.limit) + 1,
        totalPages: Math.ceil(state.totalRepayments / state.pagination.limit),
        totalItems: state.totalRepayments,
        itemsPerPage: state.pagination.limit
      }
    },
    
    hasRepayments: (state) => {
      return state.repayments.length > 0
    },
    
    // Get total amount of repayments
    getTotalAmount: (state) => {
      return state.repayments.reduce((total, repayment) => total + parseFloat(repayment.amount), 0).toFixed(2)
    },
    
    // Get total amount of paid repayments
    getTotalPaidAmount: (state) => {
      return state.repayments
        .filter(repayment => repayment.is_paid)
        .reduce((total, repayment) => total + parseFloat(repayment.amount), 0)
        .toFixed(2)
    },
    
    // Get total amount of unpaid repayments
    getTotalUnpaidAmount: (state) => {
      return state.repayments
        .filter(repayment => !repayment.is_paid)
        .reduce((total, repayment) => total + parseFloat(repayment.amount), 0)
        .toFixed(2)
    },
    
    // Get overdue repayments
    getOverdueRepayments: (state) => {
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      
      return state.repayments.filter(repayment => {
        if (repayment.is_paid) return false
        
        const dueDate = new Date(repayment.due_date)
        dueDate.setHours(0, 0, 0, 0)
        
        return dueDate < today
      })
    },
    
    // Get upcoming repayments (due in the next 7 days)
    getUpcomingRepayments: (state) => {
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      
      const nextWeek = new Date(today)
      nextWeek.setDate(nextWeek.getDate() + 7)
      
      return state.repayments.filter(repayment => {
        if (repayment.is_paid) return false
        
        const dueDate = new Date(repayment.due_date)
        dueDate.setHours(0, 0, 0, 0)
        
        return dueDate >= today && dueDate <= nextWeek
      })
    }
  },

  actions: {
    async fetchRepayments() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          limit: this.pagination.limit,
          offset: this.pagination.offset,
          application: this.filters.application || undefined,
          is_paid: this.filters.isPaid !== null ? this.filters.isPaid : undefined,
          date_from: this.filters.dateFrom || undefined,
          date_to: this.filters.dateTo || undefined
        }
        
        const response = await repaymentService.getRepayments(params)
        this.repayments = response.results
        this.totalRepayments = response.count
        return response
      } catch (error) {
        this.error = error.message || 'Failed to fetch repayments'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchRepaymentById(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await repaymentService.getRepaymentById(id)
        this.currentRepayment = response
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch repayment with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createRepayment(repaymentData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await repaymentService.createRepayment(repaymentData)
        // Refresh repayments list after creation
        await this.fetchRepayments()
        return response
      } catch (error) {
        this.error = error.message || 'Failed to create repayment'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateRepayment(id, repaymentData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await repaymentService.updateRepayment(id, repaymentData)
        
        // Update the repayment in the list if it exists
        const index = this.repayments.findIndex(repayment => repayment.id === parseInt(id))
        if (index !== -1) {
          this.repayments[index] = { ...this.repayments[index], ...response }
        }
        
        // Update current repayment if it's the one being edited
        if (this.currentRepayment && this.currentRepayment.id === parseInt(id)) {
          this.currentRepayment = { ...this.currentRepayment, ...response }
        }
        
        return response
      } catch (error) {
        this.error = error.message || `Failed to update repayment with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteRepayment(id) {
      this.loading = true
      this.error = null
      
      try {
        await repaymentService.deleteRepayment(id)
        
        // Remove the repayment from the list
        this.repayments = this.repayments.filter(repayment => repayment.id !== parseInt(id))
        
        // Clear current repayment if it's the one being deleted
        if (this.currentRepayment && this.currentRepayment.id === parseInt(id)) {
          this.currentRepayment = null
        }
        
        // Refresh the list to update counts
        await this.fetchRepayments()
      } catch (error) {
        this.error = error.message || `Failed to delete repayment with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async markRepaymentPaid(id, paymentData = {}) {
      this.loading = true
      this.error = null
      
      try {
        const response = await repaymentService.markRepaymentPaid(id, paymentData)
        
        // Update the repayment in the list if it exists
        const index = this.repayments.findIndex(repayment => repayment.id === parseInt(id))
        if (index !== -1) {
          this.repayments[index] = { 
            ...this.repayments[index], 
            is_paid: true,
            paid_date: response.paid_date || new Date().toISOString().split('T')[0],
            payment_method: paymentData.payment_method || this.repayments[index].payment_method
          }
        }
        
        // Update current repayment if it's the one being marked as paid
        if (this.currentRepayment && this.currentRepayment.id === parseInt(id)) {
          this.currentRepayment = { 
            ...this.currentRepayment, 
            is_paid: true,
            paid_date: response.paid_date || new Date().toISOString().split('T')[0],
            payment_method: paymentData.payment_method || this.currentRepayment.payment_method
          }
        }
        
        return response
      } catch (error) {
        this.error = error.message || `Failed to mark repayment with ID ${id} as paid`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // Pagination and filtering actions
    setPage(page) {
      const offset = (page - 1) * this.pagination.limit
      this.pagination.offset = offset
      this.fetchRepayments()
    },
    
    setLimit(limit) {
      this.pagination.limit = limit
      this.pagination.offset = 0 // Reset to first page
      this.fetchRepayments()
    },
    
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.offset = 0 // Reset to first page
      this.fetchRepayments()
    },
    
    clearFilters() {
      this.filters = {
        application: null,
        isPaid: null,
        dateFrom: '',
        dateTo: ''
      }
      this.fetchRepayments()
    }
  }
})
