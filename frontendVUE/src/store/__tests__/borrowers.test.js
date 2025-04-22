import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useBorrowerStore } from '../borrowers'
import axios from 'axios'

// Mock axios
vi.mock('axios')

describe('Borrower Store', () => {
  beforeEach(() => {
    // Create a fresh pinia instance for each test
    setActivePinia(createPinia())
    
    // Reset all mocks
    vi.resetAllMocks()
  })
  
  it('fetches borrowers', async () => {
    // Mock data
    const mockBorrowers = [
      { id: 1, first_name: 'John', last_name: 'Doe', email: 'john@example.com' },
      { id: 2, first_name: 'Jane', last_name: 'Smith', email: 'jane@example.com' }
    ]
    
    // Setup mock response
    axios.get.mockResolvedValue({ data: mockBorrowers })
    
    // Get store instance
    const store = useBorrowerStore()
    
    // Call the action
    await store.fetchBorrowers()
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/api/borrowers/')
    
    // Verify state was updated correctly
    expect(store.borrowers).toEqual(mockBorrowers)
    expect(store.loading).toBe(false)
    expect(store.error).toBe(null)
  })
  
  it('handles fetch borrowers error', async () => {
    // Setup mock error response
    const errorMessage = 'Network Error'
    axios.get.mockRejectedValue({ 
      response: { data: { message: errorMessage } }
    })
    
    // Get store instance
    const store = useBorrowerStore()
    
    // Call the action
    await store.fetchBorrowers()
    
    // Verify state was updated correctly
    expect(store.borrowers).toEqual([])
    expect(store.loading).toBe(false)
    expect(store.error).toBe(errorMessage)
  })
  
  it('fetches borrower by id', async () => {
    // Mock data
    const mockBorrower = { 
      id: 1, 
      first_name: 'John', 
      last_name: 'Doe', 
      email: 'john@example.com',
      phone: '1234567890',
      date_of_birth: '1980-01-01',
      address: {
        street: '123 Main St',
        city: 'Anytown',
        state: 'CA',
        postal_code: '12345',
        country: 'USA'
      }
    }
    
    // Setup mock response
    axios.get.mockResolvedValue({ data: mockBorrower })
    
    // Get store instance
    const store = useBorrowerStore()
    
    // Call the action
    const result = await store.fetchBorrowerById(1)
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/api/borrowers/1/')
    
    // Verify state was updated correctly
    expect(store.currentBorrower).toEqual(mockBorrower)
    expect(store.loading).toBe(false)
    expect(store.error).toBe(null)
    
    // Verify return value
    expect(result).toEqual(mockBorrower)
  })
  
  it('handles fetch borrower by id error', async () => {
    // Setup mock error response
    const errorMessage = 'Borrower not found'
    axios.get.mockRejectedValue({ 
      response: { data: { message: errorMessage } }
    })
    
    // Get store instance
    const store = useBorrowerStore()
    
    // Call the action
    const result = await store.fetchBorrowerById(999)
    
    // Verify state was updated correctly
    expect(store.currentBorrower).toBe(null)
    expect(store.loading).toBe(false)
    expect(store.error).toBe(errorMessage)
    
    // Verify return value
    expect(result).toBe(null)
  })
  
  it('creates borrower', async () => {
    // Mock data
    const newBorrower = {
      first_name: 'John',
      last_name: 'Doe',
      email: 'john@example.com',
      phone: '1234567890'
    }
    
    const createdBorrower = {
      id: 1,
      ...newBorrower,
      created_at: '2023-01-01T00:00:00Z'
    }
    
    // Setup mock response
    axios.post.mockResolvedValue({ data: createdBorrower })
    
    // Get store instance
    const store = useBorrowerStore()
    
    // Call the action
    const result = await store.createBorrower(newBorrower)
    
    // Verify axios was called correctly
    expect(axios.post).toHaveBeenCalledWith('/api/borrowers/', newBorrower)
    
    // Verify state was updated correctly
    expect(store.borrowers).toEqual([createdBorrower])
    expect(store.loading).toBe(false)
    expect(store.error).toBe(null)
    
    // Verify return value
    expect(result).toEqual(createdBorrower)
  })
  
  it('handles create borrower error', async () => {
    // Mock data
    const newBorrower = {
      first_name: 'John',
      // Missing required fields
    }
    
    // Setup mock error response
    const errorMessage = 'Validation error'
    axios.post.mockRejectedValue({ 
      response: { data: { message: errorMessage } }
    })
    
    // Get store instance
    const store = useBorrowerStore()
    
    // Call the action
    const result = await store.createBorrower(newBorrower)
    
    // Verify state was updated correctly
    expect(store.borrowers).toEqual([])
    expect(store.loading).toBe(false)
    expect(store.error).toBe(errorMessage)
    
    // Verify return value
    expect(result).toBe(null)
  })
  
  it('updates borrower', async () => {
    // Mock data
    const borrowerId = 1
    const updateData = {
      first_name: 'John',
      last_name: 'Smith', // Changed last name
      email: 'john@example.com',
      phone: '1234567890'
    }
    
    const updatedBorrower = {
      id: borrowerId,
      ...updateData,
      updated_at: '2023-01-02T00:00:00Z'
    }
    
    // Setup initial state
    const initialBorrower = {
      id: borrowerId,
      first_name: 'John',
      last_name: 'Doe',
      email: 'john@example.com',
      phone: '1234567890',
      updated_at: '2023-01-01T00:00:00Z'
    }
    
    // Setup mock response
    axios.put.mockResolvedValue({ data: updatedBorrower })
    
    // Get store instance
    const store = useBorrowerStore()
    store.borrowers = [initialBorrower]
    store.currentBorrower = initialBorrower
    
    // Call the action
    const result = await store.updateBorrower(borrowerId, updateData)
    
    // Verify axios was called correctly
    expect(axios.put).toHaveBeenCalledWith(`/api/borrowers/${borrowerId}/`, updateData)
    
    // Verify state was updated correctly
    expect(store.borrowers[0]).toEqual(updatedBorrower)
    expect(store.currentBorrower).toEqual(updatedBorrower)
    expect(store.loading).toBe(false)
    expect(store.error).toBe(null)
    
    // Verify return value
    expect(result).toEqual(updatedBorrower)
  })
  
  it('handles update borrower error', async () => {
    // Mock data
    const borrowerId = 1
    const updateData = {
      first_name: '', // Invalid data
      last_name: 'Smith'
    }
    
    // Setup initial state
    const initialBorrower = {
      id: borrowerId,
      first_name: 'John',
      last_name: 'Doe',
      email: 'john@example.com',
      phone: '1234567890'
    }
    
    // Setup mock error response
    const errorMessage = 'Validation error'
    axios.put.mockRejectedValue({ 
      response: { data: { message: errorMessage } }
    })
    
    // Get store instance
    const store = useBorrowerStore()
    store.borrowers = [initialBorrower]
    store.currentBorrower = initialBorrower
    
    // Call the action
    const result = await store.updateBorrower(borrowerId, updateData)
    
    // Verify state was not changed
    expect(store.borrowers[0]).toEqual(initialBorrower)
    expect(store.currentBorrower).toEqual(initialBorrower)
    expect(store.loading).toBe(false)
    expect(store.error).toBe(errorMessage)
    
    // Verify return value
    expect(result).toBe(null)
  })
  
  it('deletes borrower', async () => {
    // Mock data
    const borrowerId = 1
    
    // Setup initial state
    const borrower1 = {
      id: borrowerId,
      first_name: 'John',
      last_name: 'Doe'
    }
    
    const borrower2 = {
      id: 2,
      first_name: 'Jane',
      last_name: 'Smith'
    }
    
    // Setup mock response
    axios.delete.mockResolvedValue({})
    
    // Get store instance
    const store = useBorrowerStore()
    store.borrowers = [borrower1, borrower2]
    store.currentBorrower = borrower1
    
    // Call the action
    const result = await store.deleteBorrower(borrowerId)
    
    // Verify axios was called correctly
    expect(axios.delete).toHaveBeenCalledWith(`/api/borrowers/${borrowerId}/`)
    
    // Verify state was updated correctly
    expect(store.borrowers).toEqual([borrower2])
    expect(store.currentBorrower).toBe(null)
    expect(store.loading).toBe(false)
    expect(store.error).toBe(null)
    
    // Verify return value
    expect(result).toBe(true)
  })
  
  it('handles delete borrower error', async () => {
    // Mock data
    const borrowerId = 1
    
    // Setup initial state
    const borrower = {
      id: borrowerId,
      first_name: 'John',
      last_name: 'Doe'
    }
    
    // Setup mock error response
    const errorMessage = 'Cannot delete borrower with active applications'
    axios.delete.mockRejectedValue({ 
      response: { data: { message: errorMessage } }
    })
    
    // Get store instance
    const store = useBorrowerStore()
    store.borrowers = [borrower]
    store.currentBorrower = borrower
    
    // Call the action
    const result = await store.deleteBorrower(borrowerId)
    
    // Verify state was not changed
    expect(store.borrowers).toEqual([borrower])
    expect(store.currentBorrower).toEqual(borrower)
    expect(store.loading).toBe(false)
    expect(store.error).toBe(errorMessage)
    
    // Verify return value
    expect(result).toBe(false)
  })
  
  it('gets borrower by id from state', () => {
    // Mock data
    const borrowers = [
      { id: 1, first_name: 'John', last_name: 'Doe' },
      { id: 2, first_name: 'Jane', last_name: 'Smith' }
    ]
    
    // Get store instance
    const store = useBorrowerStore()
    store.borrowers = borrowers
    
    // Use getter
    const borrower = store.getBorrowerById(2)
    
    // Verify result
    expect(borrower).toEqual(borrowers[1])
  })
})