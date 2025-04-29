import { defineStore } from 'pinia'
import borrowerService from '@/services/borrower.service'

export const useBorrowerStore = defineStore('borrower', {
  state: () => ({
    borrowers: [],
    currentBorrower: null,
    totalBorrowers: 0,
    loading: false,
    error: null,
    filters: {
      search: '',
      borrowerType: ''
    },
    pagination: {
      limit: 10,
      offset: 0
    }
  }),

  getters: {
    getBorrowerById: (state) => (id) => {
      return state.borrowers.find(borrower => borrower.id === id) || null
    },
    
    getFilteredBorrowers: (state) => {
      return state.borrowers
    },
    
    getPaginationInfo: (state) => {
      return {
        currentPage: Math.floor(state.pagination.offset / state.pagination.limit) + 1,
        totalPages: Math.ceil(state.totalBorrowers / state.pagination.limit),
        totalItems: state.totalBorrowers,
        itemsPerPage: state.pagination.limit
      }
    },
    
    hasBorrowers: (state) => {
      return state.borrowers.length > 0
    }
  },

  actions: {
    async fetchBorrowers() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          limit: this.pagination.limit,
          offset: this.pagination.offset,
          search: this.filters.search || undefined,
          borrower_type: this.filters.borrowerType || undefined
        }
        
        const response = await borrowerService.getBorrowers(params)
        this.borrowers = response.results
        this.totalBorrowers = response.count
        return response
      } catch (error) {
        this.error = error.message || 'Failed to fetch borrowers'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchBorrowerById(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await borrowerService.getBorrowerById(id)
        this.currentBorrower = response
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch borrower with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createBorrower(borrowerData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await borrowerService.createBorrower(borrowerData)
        // Refresh borrowers list after creation
        await this.fetchBorrowers()
        return response
      } catch (error) {
        this.error = error.message || 'Failed to create borrower'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateBorrower(id, borrowerData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await borrowerService.updateBorrower(id, borrowerData)
        
        // Update the borrower in the list if it exists
        const index = this.borrowers.findIndex(borrower => borrower.id === id)
        if (index !== -1) {
          this.borrowers[index] = { ...this.borrowers[index], ...response }
        }
        
        // Update current borrower if it's the one being edited
        if (this.currentBorrower && this.currentBorrower.id === id) {
          this.currentBorrower = { ...this.currentBorrower, ...response }
        }
        
        return response
      } catch (error) {
        this.error = error.message || `Failed to update borrower with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteBorrower(id) {
      this.loading = true
      this.error = null
      
      try {
        await borrowerService.deleteBorrower(id)
        
        // Remove the borrower from the list
        this.borrowers = this.borrowers.filter(borrower => borrower.id !== id)
        
        // Clear current borrower if it's the one being deleted
        if (this.currentBorrower && this.currentBorrower.id === id) {
          this.currentBorrower = null
        }
        
        // Refresh the list to update counts
        await this.fetchBorrowers()
      } catch (error) {
        this.error = error.message || `Failed to delete borrower with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // Pagination and filtering actions
    setPage(page) {
      const offset = (page - 1) * this.pagination.limit
      this.pagination.offset = offset
      this.fetchBorrowers()
    },
    
    setLimit(limit) {
      this.pagination.limit = limit
      this.pagination.offset = 0 // Reset to first page
      this.fetchBorrowers()
    },
    
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.offset = 0 // Reset to first page
      this.fetchBorrowers()
    },
    
    clearFilters() {
      this.filters = {
        search: '',
        borrowerType: ''
      }
      this.fetchBorrowers()
    }
  }
})
