import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useReportStore } from '../reports'
import axios from 'axios'

// Mock axios
vi.mock('axios')

// Mock document methods for PDF/CSV download tests
const mockCreateObjectURL = vi.fn()
const mockRevokeObjectURL = vi.fn()
const originalCreateElement = document.createElement
const mockAppendChild = vi.fn()
const mockRemoveChild = vi.fn()
const mockClick = vi.fn()

describe('Report Store', () => {
  beforeEach(() => {
    // Create a fresh pinia instance for each test
    setActivePinia(createPinia())
    
    // Reset all mocks
    vi.resetAllMocks()
    
    // Setup document mocks
    window.URL.createObjectURL = mockCreateObjectURL
    window.URL.revokeObjectURL = mockRevokeObjectURL
    document.createElement = (tag) => {
      const element = originalCreateElement.call(document, tag)
      element.click = mockClick
      return element
    }
    document.body.appendChild = mockAppendChild
    document.body.removeChild = mockRemoveChild
    
    // Mock createObjectURL to return a fake URL
    mockCreateObjectURL.mockReturnValue('blob:fake-url')
  })
  
  it('sets filters correctly', () => {
    // Get store instance
    const store = useReportStore()
    
    // Initial state
    expect(store.filters).toEqual({
      dateRange: {
        start: null,
        end: null
      },
      bdm: null,
      broker: null,
      branch: null
    })
    
    // Set filters
    const newFilters = {
      dateRange: {
        start: '2023-01-01',
        end: '2023-01-31'
      },
      bdm: 5,
      broker: 10
    }
    
    store.setFilters(newFilters)
    
    // Verify state was updated correctly
    expect(store.filters).toEqual({
      dateRange: {
        start: '2023-01-01',
        end: '2023-01-31'
      },
      bdm: 5,
      broker: 10,
      branch: null
    })
  })
  
  it('fetches repayment compliance report', async () => {
    // Mock data
    const mockReportData = {
      summary: {
        total_repayments: 100,
        on_time: 80,
        late: 15,
        missed: 5
      },
      repayments: [
        { id: 1, due_date: '2023-01-15', amount: 5000, status: 'paid', days_late: 0 },
        { id: 2, due_date: '2023-01-15', amount: 3000, status: 'late', days_late: 5 }
      ]
    }
    
    // Setup mock response
    axios.get.mockResolvedValue({ data: mockReportData })
    
    // Get store instance
    const store = useReportStore()
    store.filters = {
      dateRange: {
        start: '2023-01-01',
        end: '2023-01-31'
      },
      bdm: 5,
      broker: null,
      branch: null
    }
    
    // Call the action
    const result = await store.fetchRepaymentComplianceReport()
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/api/reports/repayment-compliance/', { 
      params: { 
        start_date: '2023-01-01',
        end_date: '2023-01-31',
        bdm_id: 5
      } 
    })
    
    // Verify state was updated correctly
    expect(store.repaymentComplianceData).toEqual(mockReportData)
    expect(store.loading).toBe(false)
    expect(store.error).toBe(null)
    
    // Verify return value
    expect(result).toEqual(mockReportData)
  })
  
  it('handles fetch repayment compliance report error', async () => {
    // Setup mock error response
    const errorMessage = 'Invalid date range'
    axios.get.mockRejectedValue({ 
      response: { data: { message: errorMessage } }
    })
    
    // Get store instance
    const store = useReportStore()
    
    // Call the action
    const result = await store.fetchRepaymentComplianceReport()
    
    // Verify state was updated correctly
    expect(store.repaymentComplianceData).toBe(null)
    expect(store.loading).toBe(false)
    expect(store.error).toBe(errorMessage)
    
    // Verify return value
    expect(result).toBe(null)
  })
  
  it('fetches application volume report', async () => {
    // Mock data
    const mockReportData = {
      summary: {
        total_applications: 50,
        approved: 30,
        pending: 15,
        rejected: 5
      },
      by_month: [
        { month: 'Jan 2023', count: 15 },
        { month: 'Feb 2023', count: 20 },
        { month: 'Mar 2023', count: 15 }
      ],
      by_bdm: [
        { bdm_name: 'John Smith', count: 25 },
        { bdm_name: 'Jane Doe', count: 25 }
      ]
    }
    
    // Setup mock response
    axios.get.mockResolvedValue({ data: mockReportData })
    
    // Get store instance
    const store = useReportStore()
    store.filters = {
      dateRange: {
        start: '2023-01-01',
        end: '2023-03-31'
      },
      bdm: null,
      broker: 10,
      branch: null
    }
    
    // Call the action
    const result = await store.fetchApplicationVolumeReport()
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/api/reports/application-volume/', { 
      params: { 
        start_date: '2023-01-01',
        end_date: '2023-03-31',
        broker_id: 10
      } 
    })
    
    // Verify state was updated correctly
    expect(store.applicationVolumeData).toEqual(mockReportData)
    expect(store.loading).toBe(false)
    expect(store.error).toBe(null)
    
    // Verify return value
    expect(result).toEqual(mockReportData)
  })
  
  it('fetches application status report', async () => {
    // Mock data
    const mockReportData = {
      summary: {
        total_applications: 100,
        by_status: {
          inquiry: 20,
          submitted: 30,
          approved: 40,
          settled: 10
        }
      },
      applications: [
        { id: 1, reference_number: 'APP001', status: 'approved', loan_amount: 500000 },
        { id: 2, reference_number: 'APP002', status: 'submitted', loan_amount: 350000 }
      ]
    }
    
    // Setup mock response
    axios.get.mockResolvedValue({ data: mockReportData })
    
    // Get store instance
    const store = useReportStore()
    store.filters = {
      dateRange: {
        start: null,
        end: null
      },
      bdm: null,
      broker: null,
      branch: 3
    }
    
    // Call the action
    const result = await store.fetchApplicationStatusReport()
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/api/reports/application-status/', { 
      params: { 
        branch_id: 3
      } 
    })
    
    // Verify state was updated correctly
    expect(store.applicationStatusData).toEqual(mockReportData)
    expect(store.loading).toBe(false)
    expect(store.error).toBe(null)
    
    // Verify return value
    expect(result).toEqual(mockReportData)
  })
  
  it('exports report as PDF', async () => {
    // Mock blob data
    const mockBlob = new Blob(['fake pdf data'], { type: 'application/pdf' })
    
    // Setup mock response
    axios.get.mockResolvedValue({ data: mockBlob })
    
    // Get store instance
    const store = useReportStore()
    store.filters = {
      dateRange: {
        start: '2023-01-01',
        end: '2023-01-31'
      },
      bdm: 5,
      broker: null,
      branch: null
    }
    
    // Call the action
    const result = await store.exportReportPDF('repayment-compliance')
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/api/reports/export-pdf/', { 
      params: { 
        start_date: '2023-01-01',
        end_date: '2023-01-31',
        bdm_id: 5,
        report_type: 'repayment-compliance'
      },
      responseType: 'blob'
    })
    
    // Verify URL creation and download link
    expect(mockCreateObjectURL).toHaveBeenCalledWith(expect.any(Blob))
    expect(mockAppendChild).toHaveBeenCalled()
    expect(mockClick).toHaveBeenCalled()
    expect(mockRemoveChild).toHaveBeenCalled()
    
    // Verify return value
    expect(result).toBe(true)
  })
  
  it('exports report as CSV', async () => {
    // Mock blob data
    const mockBlob = new Blob(['id,name,value\n1,test,100'], { type: 'text/csv' })
    
    // Setup mock response
    axios.get.mockResolvedValue({ data: mockBlob })
    
    // Get store instance
    const store = useReportStore()
    store.filters = {
      dateRange: {
        start: '2023-01-01',
        end: '2023-01-31'
      },
      bdm: null,
      broker: 10,
      branch: null
    }
    
    // Call the action
    const result = await store.exportReportCSV('application-volume')
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/api/reports/export-csv/', { 
      params: { 
        start_date: '2023-01-01',
        end_date: '2023-01-31',
        broker_id: 10,
        report_type: 'application-volume'
      },
      responseType: 'blob'
    })
    
    // Verify URL creation and download link
    expect(mockCreateObjectURL).toHaveBeenCalledWith(expect.any(Blob))
    expect(mockAppendChild).toHaveBeenCalled()
    expect(mockClick).toHaveBeenCalled()
    expect(mockRemoveChild).toHaveBeenCalled()
    
    // Verify return value
    expect(result).toBe(true)
  })
  
  it('handles export error', async () => {
    // Setup mock error response
    const errorMessage = 'Export failed'
    axios.get.mockRejectedValue({ 
      response: { data: { message: errorMessage } }
    })
    
    // Get store instance
    const store = useReportStore()
    
    // Call the action
    const result = await store.exportReportPDF('application-status')
    
    // Verify state was updated correctly
    expect(store.error).toBe(errorMessage)
    
    // Verify URL creation and download link were not called
    expect(mockCreateObjectURL).not.toHaveBeenCalled()
    expect(mockAppendChild).not.toHaveBeenCalled()
    expect(mockClick).not.toHaveBeenCalled()
    
    // Verify return value
    expect(result).toBe(false)
  })
})