import { defineStore } from 'pinia'
import brokerService from '@/services/broker.service'

export const useBrokerStore = defineStore('broker', {
  state: () => ({
    brokers: [],
    currentBroker: null,
    branches: [],
    currentBranch: null,
    bdms: [],
    currentBDM: null,
    totalBrokers: 0,
    totalBranches: 0,
    totalBDMs: 0,
    loading: false,
    error: null,
    filters: {
      search: '',
      branch: null
    },
    pagination: {
      limit: 10,
      offset: 0
    }
  }),

  getters: {
    getBrokerById: (state) => (id) => {
      return state.brokers.find(broker => broker.id === id) || null
    },
    
    getBranchById: (state) => (id) => {
      return state.branches.find(branch => branch.id === id) || null
    },
    
    getBDMById: (state) => (id) => {
      return state.bdms.find(bdm => bdm.id === id) || null
    },
    
    getPaginationInfo: (state) => {
      return {
        currentPage: Math.floor(state.pagination.offset / state.pagination.limit) + 1,
        totalPages: Math.ceil(state.totalBrokers / state.pagination.limit),
        totalItems: state.totalBrokers,
        itemsPerPage: state.pagination.limit
      }
    },
    
    getBranchPaginationInfo: (state) => {
      return {
        currentPage: Math.floor(state.pagination.offset / state.pagination.limit) + 1,
        totalPages: Math.ceil(state.totalBranches / state.pagination.limit),
        totalItems: state.totalBranches,
        itemsPerPage: state.pagination.limit
      }
    },
    
    getBDMPaginationInfo: (state) => {
      return {
        currentPage: Math.floor(state.pagination.offset / state.pagination.limit) + 1,
        totalPages: Math.ceil(state.totalBDMs / state.pagination.limit),
        totalItems: state.totalBDMs,
        itemsPerPage: state.pagination.limit
      }
    },
    
    hasBrokers: (state) => {
      return state.brokers.length > 0
    },
    
    hasBranches: (state) => {
      return state.branches.length > 0
    },
    
    hasBDMs: (state) => {
      return state.bdms.length > 0
    }
  },

  actions: {
    // Broker actions
    async fetchBrokers() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          limit: this.pagination.limit,
          offset: this.pagination.offset,
          search: this.filters.search || undefined,
          branch: this.filters.branch || undefined
        }
        
        const response = await brokerService.getBrokers(params)
        this.brokers = response.results
        this.totalBrokers = response.count
        return response
      } catch (error) {
        this.error = error.message || 'Failed to fetch brokers'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchBrokerById(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.getBrokerById(id)
        this.currentBroker = response
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch broker with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createBroker(brokerData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.createBroker(brokerData)
        // Add the new broker to the list if it's not already there
        const exists = this.brokers.some(broker => broker.id === response.id)
        if (!exists) {
          this.brokers.push(response)
          this.totalBrokers++
        }
        return response
      } catch (error) {
        this.error = error.message || 'Failed to create broker'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateBroker(id, brokerData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.updateBroker(id, brokerData)
        // Update the broker in the list
        const index = this.brokers.findIndex(broker => broker.id === id)
        if (index !== -1) {
          this.brokers[index] = response
        }
        // Update current broker if it's the one being edited
        if (this.currentBroker && this.currentBroker.id === id) {
          this.currentBroker = response
        }
        return response
      } catch (error) {
        this.error = error.message || `Failed to update broker with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteBroker(id) {
      this.loading = true
      this.error = null
      
      try {
        await brokerService.deleteBroker(id)
        // Remove the broker from the list
        this.brokers = this.brokers.filter(broker => broker.id !== id)
        this.totalBrokers--
        // Clear current broker if it's the one being deleted
        if (this.currentBroker && this.currentBroker.id === id) {
          this.currentBroker = null
        }
        return { success: true }
      } catch (error) {
        this.error = error.message || `Failed to delete broker with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchBrokerApplications(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.getBrokerApplications(id)
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch applications for broker with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchBrokerStats(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.getBrokerStats(id)
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch stats for broker with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // Branch actions
    async fetchBranches() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          limit: this.pagination.limit,
          offset: this.pagination.offset,
          search: this.filters.search || undefined
        }
        
        const response = await brokerService.getBranches(params)
        this.branches = response.results
        this.totalBranches = response.count
        return response
      } catch (error) {
        this.error = error.message || 'Failed to fetch branches'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchBranchById(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.getBranchById(id)
        this.currentBranch = response
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch branch with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createBranch(branchData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.createBranch(branchData)
        // Add the new branch to the list if it's not already there
        const exists = this.branches.some(branch => branch.id === response.id)
        if (!exists) {
          this.branches.push(response)
          this.totalBranches++
        }
        return response
      } catch (error) {
        this.error = error.message || 'Failed to create branch'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateBranch(id, branchData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.updateBranch(id, branchData)
        // Update the branch in the list
        const index = this.branches.findIndex(branch => branch.id === id)
        if (index !== -1) {
          this.branches[index] = response
        }
        // Update current branch if it's the one being edited
        if (this.currentBranch && this.currentBranch.id === id) {
          this.currentBranch = response
        }
        return response
      } catch (error) {
        this.error = error.message || `Failed to update branch with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteBranch(id) {
      this.loading = true
      this.error = null
      
      try {
        await brokerService.deleteBranch(id)
        // Remove the branch from the list
        this.branches = this.branches.filter(branch => branch.id !== id)
        this.totalBranches--
        // Clear current branch if it's the one being deleted
        if (this.currentBranch && this.currentBranch.id === id) {
          this.currentBranch = null
        }
        return { success: true }
      } catch (error) {
        this.error = error.message || `Failed to delete branch with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchBrokersInBranch(branchId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.getBrokersInBranch(branchId)
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch brokers for branch with ID ${branchId}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchBDMsInBranch(branchId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.getBDMsInBranch(branchId)
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch BDMs for branch with ID ${branchId}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // BDM actions
    async fetchBDMs() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          limit: this.pagination.limit,
          offset: this.pagination.offset,
          search: this.filters.search || undefined,
          branch: this.filters.branch || undefined
        }
        
        const response = await brokerService.getBDMs(params)
        this.bdms = response.results
        this.totalBDMs = response.count
        return response
      } catch (error) {
        this.error = error.message || 'Failed to fetch BDMs'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchBDMById(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.getBDMById(id)
        this.currentBDM = response
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch BDM with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createBDM(bdmData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.createBDM(bdmData)
        // Add the new BDM to the list if it's not already there
        const exists = this.bdms.some(bdm => bdm.id === response.id)
        if (!exists) {
          this.bdms.push(response)
          this.totalBDMs++
        }
        return response
      } catch (error) {
        this.error = error.message || 'Failed to create BDM'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateBDM(id, bdmData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.updateBDM(id, bdmData)
        // Update the BDM in the list
        const index = this.bdms.findIndex(bdm => bdm.id === id)
        if (index !== -1) {
          this.bdms[index] = response
        }
        // Update current BDM if it's the one being edited
        if (this.currentBDM && this.currentBDM.id === id) {
          this.currentBDM = response
        }
        return response
      } catch (error) {
        this.error = error.message || `Failed to update BDM with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteBDM(id) {
      this.loading = true
      this.error = null
      
      try {
        await brokerService.deleteBDM(id)
        // Remove the BDM from the list
        this.bdms = this.bdms.filter(bdm => bdm.id !== id)
        this.totalBDMs--
        // Clear current BDM if it's the one being deleted
        if (this.currentBDM && this.currentBDM.id === id) {
          this.currentBDM = null
        }
        return { success: true }
      } catch (error) {
        this.error = error.message || `Failed to delete BDM with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchBDMApplications(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await brokerService.getBDMApplications(id)
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch applications for BDM with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // Pagination and filtering actions
    setPage(page) {
      const offset = (page - 1) * this.pagination.limit
      this.pagination.offset = offset
      this.fetchBrokers()
    },
    
    setBranchPage(page) {
      const offset = (page - 1) * this.pagination.limit
      this.pagination.offset = offset
      this.fetchBranches()
    },
    
    setBDMPage(page) {
      const offset = (page - 1) * this.pagination.limit
      this.pagination.offset = offset
      this.fetchBDMs()
    },
    
    setLimit(limit) {
      this.pagination.limit = limit
      this.pagination.offset = 0 // Reset to first page
      this.fetchBrokers()
    },
    
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.offset = 0 // Reset to first page
      this.fetchBrokers()
    },
    
    setBranchFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.offset = 0 // Reset to first page
      this.fetchBranches()
    },
    
    setBDMFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.offset = 0 // Reset to first page
      this.fetchBDMs()
    },
    
    clearFilters() {
      this.filters = {
        search: '',
        branch: null
      }
      this.fetchBrokers()
    }
  }
})
