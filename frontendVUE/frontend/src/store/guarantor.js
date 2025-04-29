import { defineStore } from 'pinia'
import guarantorService from '@/services/guarantor.service'

export const useGuarantorStore = defineStore('guarantor', {
  state: () => ({
    guarantors: [],
    currentGuarantor: null,
    totalGuarantors: 0,
    loading: false,
    error: null,
    filters: {
      search: '',
      relationshipToBorrower: ''
    },
    pagination: {
      limit: 10,
      offset: 0
    }
  }),

  getters: {
    getGuarantorById: (state) => (id) => {
      return state.guarantors.find(guarantor => guarantor.id === id) || null
    },
    
    getFilteredGuarantors: (state) => {
      return state.guarantors
    },
    
    getPaginationInfo: (state) => {
      return {
        currentPage: Math.floor(state.pagination.offset / state.pagination.limit) + 1,
        totalPages: Math.ceil(state.totalGuarantors / state.pagination.limit),
        totalItems: state.totalGuarantors,
        itemsPerPage: state.pagination.limit
      }
    },
    
    hasGuarantors: (state) => {
      return state.guarantors.length > 0
    }
  },

  actions: {
    async fetchGuarantors() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          limit: this.pagination.limit,
          offset: this.pagination.offset,
          search: this.filters.search || undefined,
          relationship_to_borrower: this.filters.relationshipToBorrower || undefined
        }
        
        const response = await guarantorService.getGuarantors(params)
        this.guarantors = response.results
        this.totalGuarantors = response.count
        return response
      } catch (error) {
        this.error = error.message || 'Failed to fetch guarantors'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchGuarantorById(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await guarantorService.getGuarantorById(id)
        this.currentGuarantor = response
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch guarantor with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createGuarantor(guarantorData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await guarantorService.createGuarantor(guarantorData)
        // Refresh guarantors list after creation
        await this.fetchGuarantors()
        return response
      } catch (error) {
        this.error = error.message || 'Failed to create guarantor'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateGuarantor(id, guarantorData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await guarantorService.updateGuarantor(id, guarantorData)
        
        // Update the guarantor in the list if it exists
        const index = this.guarantors.findIndex(guarantor => guarantor.id === id)
        if (index !== -1) {
          this.guarantors[index] = { ...this.guarantors[index], ...response }
        }
        
        // Update current guarantor if it's the one being edited
        if (this.currentGuarantor && this.currentGuarantor.id === id) {
          this.currentGuarantor = { ...this.currentGuarantor, ...response }
        }
        
        return response
      } catch (error) {
        this.error = error.message || `Failed to update guarantor with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteGuarantor(id) {
      this.loading = true
      this.error = null
      
      try {
        await guarantorService.deleteGuarantor(id)
        
        // Remove the guarantor from the list
        this.guarantors = this.guarantors.filter(guarantor => guarantor.id !== id)
        
        // Clear current guarantor if it's the one being deleted
        if (this.currentGuarantor && this.currentGuarantor.id === id) {
          this.currentGuarantor = null
        }
        
        // Refresh the list to update counts
        await this.fetchGuarantors()
      } catch (error) {
        this.error = error.message || `Failed to delete guarantor with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchGuaranteedApplications(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await guarantorService.getGuaranteedApplications(id)
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch applications for guarantor with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // Pagination and filtering actions
    setPage(page) {
      const offset = (page - 1) * this.pagination.limit
      this.pagination.offset = offset
      this.fetchGuarantors()
    },
    
    setLimit(limit) {
      this.pagination.limit = limit
      this.pagination.offset = 0 // Reset to first page
      this.fetchGuarantors()
    },
    
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.offset = 0 // Reset to first page
      this.fetchGuarantors()
    },
    
    clearFilters() {
      this.filters = {
        search: '',
        relationshipToBorrower: ''
      }
      this.fetchGuarantors()
    }
  }
})
