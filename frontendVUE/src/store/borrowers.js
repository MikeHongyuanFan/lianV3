import { defineStore } from 'pinia'
import axios from 'axios'

export const useBorrowerStore = defineStore('borrowers', {
  state: () => ({
    borrowers: [],
    currentBorrower: null,
    loading: false,
    error: null
  }),
  
  getters: {
    getBorrowerById: (state) => (id) => {
      return state.borrowers.find(borrower => borrower.id === id)
    }
  },
  
  actions: {
    async fetchBorrowers() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/borrowers/')
        this.borrowers = response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch borrowers'
        console.error('Error fetching borrowers:', error)
      } finally {
        this.loading = false
      }
    },
    
    async fetchBorrowerById(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`/api/borrowers/${id}/`)
        this.currentBorrower = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || `Failed to fetch borrower with ID ${id}`
        console.error(`Error fetching borrower with ID ${id}:`, error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async createBorrower(borrowerData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/borrowers/', borrowerData)
        this.borrowers.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create borrower'
        console.error('Error creating borrower:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async updateBorrower(id, borrowerData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.put(`/api/borrowers/${id}/`, borrowerData)
        
        // Update local state
        const index = this.borrowers.findIndex(borrower => borrower.id === id)
        if (index !== -1) {
          this.borrowers[index] = response.data
        }
        
        if (this.currentBorrower && this.currentBorrower.id === id) {
          this.currentBorrower = response.data
        }
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || `Failed to update borrower with ID ${id}`
        console.error(`Error updating borrower with ID ${id}:`, error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async deleteBorrower(id) {
      this.loading = true
      this.error = null
      
      try {
        await axios.delete(`/api/borrowers/${id}/`)
        
        // Update local state
        this.borrowers = this.borrowers.filter(borrower => borrower.id !== id)
        
        if (this.currentBorrower && this.currentBorrower.id === id) {
          this.currentBorrower = null
        }
        
        return true
      } catch (error) {
        this.error = error.response?.data?.message || `Failed to delete borrower with ID ${id}`
        console.error(`Error deleting borrower with ID ${id}:`, error)
        return false
      } finally {
        this.loading = false
      }
    }
  }
})