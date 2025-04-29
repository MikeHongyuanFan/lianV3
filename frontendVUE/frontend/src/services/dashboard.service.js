import api from './api'

/**
 * Service for dashboard-related API calls
 */
class DashboardService {
  /**
   * Get dashboard data
   * @returns {Promise<Object>} Dashboard data
   */
  async getDashboardData() {
    try {
      // Using only the implemented report endpoints with error handling for each request
      const applicationVolumePromise = this.getApplicationVolumeReport().catch(error => {
        console.warn('Failed to fetch application volume report:', error)
        return { data: this.getDefaultApplicationVolumeData() }
      })
      
      const applicationStatusPromise = this.getApplicationStatusReport().catch(error => {
        console.warn('Failed to fetch application status report:', error)
        return { data: this.getDefaultApplicationStatusData() }
      })
      
      const repaymentCompliancePromise = this.getRepaymentComplianceReport().catch(error => {
        console.warn('Failed to fetch repayment compliance report:', error)
        return { data: this.getDefaultRepaymentComplianceData() }
      })
      
      // Wait for all requests to complete
      const [
        applicationVolumeResponse,
        applicationStatusResponse,
        repaymentComplianceResponse
      ] = await Promise.all([
        applicationVolumePromise,
        applicationStatusPromise,
        repaymentCompliancePromise
      ])
      
      // Mock data for endpoints that are not yet implemented
      const brokerPerformance = {
        brokers: [],
        applications_by_broker: {},
        loan_amount_by_broker: {},
        success_rate_by_broker: {}
      }
      
      const loanPortfolio = {
        total_active_loans: 0,
        total_loan_amount: 0,
        avg_interest_rate: 0,
        avg_loan_term: 0,
        loans_by_type: {},
        loans_by_purpose: {},
        risk_distribution: {}
      }
      
      // Combine all data into a single dashboard object
      return {
        applicationVolume: applicationVolumeResponse.data,
        applicationStatus: applicationStatusResponse.data,
        repaymentCompliance: repaymentComplianceResponse.data,
        brokerPerformance: brokerPerformance,
        loanPortfolio: loanPortfolio
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
      // Return default data on error
      return this.getDefaultDashboardData()
    }
  }
  
  /**
   * Get application volume report
   * @param {Object} params - Filter parameters
   * @returns {Promise<Object>} Application volume report data
   */
  async getApplicationVolumeReport(params = {}) {
    try {
      const response = await api.get('/reports/application-volume/', { params })
      return response
    } catch (error) {
      console.error('Error fetching application volume report:', error)
      throw error
    }
  }
  
  /**
   * Get application status report
   * @param {Object} params - Filter parameters
   * @returns {Promise<Object>} Application status report data
   */
  async getApplicationStatusReport(params = {}) {
    try {
      const response = await api.get('/reports/application-status/', { params })
      return response
    } catch (error) {
      console.error('Error fetching application status report:', error)
      throw error
    }
  }
  
  /**
   * Get repayment compliance report
   * @param {Object} params - Filter parameters
   * @returns {Promise<Object>} Repayment compliance report data
   */
  async getRepaymentComplianceReport(params = {}) {
    try {
      const response = await api.get('/reports/repayment-compliance/', { params })
      return response
    } catch (error) {
      console.error('Error fetching repayment compliance report:', error)
      throw error
    }
  }
  
  /**
   * Get default dashboard data
   * @returns {Object} Default dashboard data
   */
  getDefaultDashboardData() {
    return {
      applicationVolume: this.getDefaultApplicationVolumeData(),
      applicationStatus: this.getDefaultApplicationStatusData(),
      repaymentCompliance: this.getDefaultRepaymentComplianceData(),
      brokerPerformance: {
        brokers: [],
        applications_by_broker: {},
        loan_amount_by_broker: {},
        success_rate_by_broker: {}
      },
      loanPortfolio: {
        total_active_loans: 0,
        total_loan_amount: 0,
        avg_interest_rate: 0,
        avg_loan_term: 0,
        loans_by_type: {},
        loans_by_purpose: {},
        risk_distribution: {}
      }
    }
  }
  
  /**
   * Get default application volume data
   * @returns {Object} Default application volume data
   */
  getDefaultApplicationVolumeData() {
    return {
      total_applications: 0,
      total_loan_amount: 0,
      average_loan_amount: 0,
      stage_breakdown: {},
      time_breakdown: [],
      bd_breakdown: [],
      type_breakdown: {}
    }
  }
  
  /**
   * Get default application status data
   * @returns {Object} Default application status data
   */
  getDefaultApplicationStatusData() {
    return {
      total_active: 0,
      total_settled: 0,
      total_declined: 0,
      total_withdrawn: 0,
      active_by_stage: {},
      avg_time_in_stage: {},
      inquiry_to_approval_rate: 0,
      approval_to_settlement_rate: 0,
      overall_success_rate: 0
    }
  }
  
  /**
   * Get default repayment compliance data
   * @returns {Object} Default repayment compliance data
   */
  getDefaultRepaymentComplianceData() {
    return {
      total_repayments: 0,
      paid_on_time: 0,
      paid_late: 0,
      missed: 0,
      compliance_rate: 0,
      average_days_late: 0,
      total_amount_due: 0,
      total_amount_paid: 0,
      payment_rate: 0,
      monthly_breakdown: []
    }
  }
}

export default new DashboardService()
