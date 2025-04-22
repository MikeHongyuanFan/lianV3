import { defineStore } from 'pinia'
import axios from 'axios'

export const useReportStore = defineStore('reports', {
  state: () => ({
    repaymentComplianceData: null,
    applicationVolumeData: null,
    applicationStatusData: null,
    filters: {
      dateRange: {
        start: null,
        end: null
      },
      bdm: null,
      broker: null,
      branch: null
    },
    loading: false,
    error: null
  }),
  
  actions: {
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
    },
    
    async fetchRepaymentComplianceReport() {
      this.loading = true
      this.error = null
      
      try {
        const params = this._buildFilterParams()
        const response = await axios.get('/api/reports/repayment-compliance/', { params })
        this.repaymentComplianceData = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch repayment compliance report'
        console.error('Error fetching repayment compliance report:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async fetchApplicationVolumeReport() {
      this.loading = true
      this.error = null
      
      try {
        const params = this._buildFilterParams()
        const response = await axios.get('/api/reports/application-volume/', { params })
        this.applicationVolumeData = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch application volume report'
        console.error('Error fetching application volume report:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async fetchApplicationStatusReport() {
      this.loading = true
      this.error = null
      
      try {
        const params = this._buildFilterParams()
        const response = await axios.get('/api/reports/application-status/', { params })
        this.applicationStatusData = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch application status report'
        console.error('Error fetching application status report:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async exportReportPDF(reportType) {
      try {
        const params = this._buildFilterParams()
        const response = await axios.get(`/api/reports/export-pdf/`, { 
          params: { ...params, report_type: reportType },
          responseType: 'blob'
        })
        
        // Create a download link for the PDF
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `${reportType}-report.pdf`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        return true
      } catch (error) {
        this.error = error.response?.data?.message || `Failed to export ${reportType} report as PDF`
        console.error(`Error exporting ${reportType} report as PDF:`, error)
        return false
      }
    },
    
    async exportReportCSV(reportType) {
      try {
        const params = this._buildFilterParams()
        const response = await axios.get(`/api/reports/export-csv/`, { 
          params: { ...params, report_type: reportType },
          responseType: 'blob'
        })
        
        // Create a download link for the CSV
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `${reportType}-report.csv`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        return true
      } catch (error) {
        this.error = error.response?.data?.message || `Failed to export ${reportType} report as CSV`
        console.error(`Error exporting ${reportType} report as CSV:`, error)
        return false
      }
    },
    
    // Helper method to build filter parameters
    _buildFilterParams() {
      const params = {}
      
      if (this.filters.dateRange.start) {
        params.start_date = this.filters.dateRange.start
      }
      
      if (this.filters.dateRange.end) {
        params.end_date = this.filters.dateRange.end
      }
      
      if (this.filters.bdm) {
        params.bdm_id = this.filters.bdm
      }
      
      if (this.filters.broker) {
        params.broker_id = this.filters.broker
      }
      
      if (this.filters.branch) {
        params.branch_id = this.filters.branch
      }
      
      return params
    }
  }
})