import { defineStore } from 'pinia'
import feeService from '@/services/fee.service'

export const useFeeStore = defineStore('fee', {
  state: () => ({
    fees: [],
    currentFee: null,
    totalFees: 0,
    loading: false,
    error: null,
    filters: {
      application: null,
      isPaid: null,
      feeType: '',
      dateFrom: '',
      dateTo: ''
    },
    pagination: {
      limit: 10,
      offset: 0
    }
  }),

  getters: {
    getFeeById: (state) => (id) => {
      return state.fees.find(fee => fee.id === parseInt(id)) || null
    },
    
    getFilteredFees: (state) => {
      return state.fees
    },
    
    getPaginationInfo: (state) => {
      return {
        currentPage: Math.floor(state.pagination.offset / state.pagination.limit) + 1,
        totalPages: Math.ceil(state.totalFees / state.pagination.limit),
        totalItems: state.totalFees,
        itemsPerPage: state.pagination.limit
      }
    },
    
    hasFees: (state) => {
      return state.fees.length > 0
    },
    
    // Get total amount of fees
    getTotalAmount: (state) => {
      return state.fees.reduce((total, fee) => total + parseFloat(fee.amount), 0).toFixed(2)
    },
    
    // Get total amount of paid fees
    getTotalPaidAmount: (state) => {
      return state.fees
        .filter(fee => fee.is_paid)
        .reduce((total, fee) => total + parseFloat(fee.amount), 0)
        .toFixed(2)
    },
    
    // Get total amount of unpaid fees
    getTotalUnpaidAmount: (state) => {
      return state.fees
        .filter(fee => !fee.is_paid)
        .reduce((total, fee) => total + parseFloat(fee.amount), 0)
        .toFixed(2)
    }
  },

  actions: {
    async fetchFees() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          limit: this.pagination.limit,
          offset: this.pagination.offset,
          application: this.filters.application || undefined,
          is_paid: this.filters.isPaid !== null ? this.filters.isPaid : undefined,
          fee_type: this.filters.feeType || undefined,
          date_from: this.filters.dateFrom || undefined,
          date_to: this.filters.dateTo || undefined
        }
        
        const response = await feeService.getFees(params)
        this.fees = response.results
        this.totalFees = response.count
        return response
      } catch (error) {
        this.error = error.message || 'Failed to fetch fees'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchFeeById(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await feeService.getFeeById(id)
        this.currentFee = response
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch fee with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createFee(feeData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await feeService.createFee(feeData)
        // Refresh fees list after creation
        await this.fetchFees()
        return response
      } catch (error) {
        this.error = error.message || 'Failed to create fee'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateFee(id, feeData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await feeService.updateFee(id, feeData)
        
        // Update the fee in the list if it exists
        const index = this.fees.findIndex(fee => fee.id === parseInt(id))
        if (index !== -1) {
          this.fees[index] = { ...this.fees[index], ...response }
        }
        
        // Update current fee if it's the one being edited
        if (this.currentFee && this.currentFee.id === parseInt(id)) {
          this.currentFee = { ...this.currentFee, ...response }
        }
        
        return response
      } catch (error) {
        this.error = error.message || `Failed to update fee with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteFee(id) {
      this.loading = true
      this.error = null
      
      try {
        await feeService.deleteFee(id)
        
        // Remove the fee from the list
        this.fees = this.fees.filter(fee => fee.id !== parseInt(id))
        
        // Clear current fee if it's the one being deleted
        if (this.currentFee && this.currentFee.id === parseInt(id)) {
          this.currentFee = null
        }
        
        // Refresh the list to update counts
        await this.fetchFees()
      } catch (error) {
        this.error = error.message || `Failed to delete fee with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async markFeePaid(id, paymentData = {}) {
      this.loading = true
      this.error = null
      
      try {
        const response = await feeService.markFeePaid(id, paymentData)
        
        // Update the fee in the list if it exists
        const index = this.fees.findIndex(fee => fee.id === parseInt(id))
        if (index !== -1) {
          this.fees[index] = { ...this.fees[index], ...response.fee }
        }
        
        // Update current fee if it's the one being marked as paid
        if (this.currentFee && this.currentFee.id === parseInt(id)) {
          this.currentFee = { ...this.currentFee, ...response.fee }
        }
        
        return response
      } catch (error) {
        this.error = error.message || `Failed to mark fee with ID ${id} as paid`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // Pagination and filtering actions
    setPage(page) {
      const offset = (page - 1) * this.pagination.limit
      this.pagination.offset = offset
      this.fetchFees()
    },
    
    setLimit(limit) {
      this.pagination.limit = limit
      this.pagination.offset = 0 // Reset to first page
      this.fetchFees()
    },
    
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.offset = 0 // Reset to first page
      this.fetchFees()
    },
    
    clearFilters() {
      this.filters = {
        application: null,
        isPaid: null,
        feeType: '',
        dateFrom: '',
        dateTo: ''
      }
      this.fetchFees()
    }
  }
})
