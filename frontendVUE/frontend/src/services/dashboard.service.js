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
      // Using only the implemented report endpoints
      const applicationVolumePromise = api.get('/reports/application-volume/')
      const applicationStatusPromise = api.get('/reports/application-status/')
      const repaymentCompliancePromise = api.get('/reports/repayment-compliance/')
      
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
      // Return mock data on error
      return {
        applicationVolume: {
          total_applications: 0,
          total_loan_amount: 0,
          average_loan_amount: 0,
          stage_breakdown: {},
          time_breakdown: [],
          bd_breakdown: [],
          type_breakdown: {}
        },
        applicationStatus: {
          total_active: 0,
          total_settled: 0,
          total_declined: 0,
          total_withdrawn: 0,
          active_by_stage: {},
          avg_time_in_stage: {},
          inquiry_to_approval_rate: 0,
          approval_to_settlement_rate: 0,
          overall_success_rate: 0
        },
        repaymentCompliance: {
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
        },
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
  }
  
  /**
   * Get application volume report
   * @param {Object} params - Filter parameters
   * @returns {Promise<Object>} Application volume report data
   */
  async getApplicationVolumeReport(params = {}) {
    try {
      const response = await api.get('/reports/application-volume/', { params })
      return response.data
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
      return response.data
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
      return response.data
    } catch (error) {
      console.error('Error fetching repayment compliance report:', error)
      throw error
    }
  }
  
  /**
   * Get broker performance report (not yet implemented in backend)
   * @param {Object} params - Filter parameters
   * @returns {Promise<Object>} Broker performance report data
   */
  async getBrokerPerformanceReport(params = {}) {
    try {
      // This endpoint is not yet implemented in the backend
      // Return mock data instead
      return {
        brokers: [],
        applications_by_broker: {},
        loan_amount_by_broker: {},
        success_rate_by_broker: {}
      }
    } catch (error) {
      console.error('Error fetching broker performance report:', error)
      throw error
    }
  }
  
  /**
   * Get loan portfolio report (not yet implemented in backend)
   * @param {Object} params - Filter parameters
   * @returns {Promise<Object>} Loan portfolio report data
   */
  async getLoanPortfolioReport(params = {}) {
    try {
      // This endpoint is not yet implemented in the backend
      // Return mock data instead
      return {
        total_active_loans: 0,
        total_loan_amount: 0,
        avg_interest_rate: 0,
        avg_loan_term: 0,
        loans_by_type: {},
        loans_by_purpose: {},
        risk_distribution: {}
      }
    } catch (error) {
      console.error('Error fetching loan portfolio report:', error)
      throw error
    }
  }
}

// Create a single instance of the service
const dashboardService = new DashboardService()

// Export the instance
export default dashboardService
