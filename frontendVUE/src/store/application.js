import { defineStore } from 'pinia'
import applicationService from '@/services/applicationService'

export const useApplicationStore = defineStore('application', {
  state: () => ({
    applications: [],
    currentApplication: null,
    applicationNotes: [],
    applicationDocuments: [],
    loading: false,
    error: null,
    filters: {
      stage: null,
      application_type: null,
      broker: null,
      bd: null,
      branch: null,
      search: null
    },
    // Multi-step form data
    formData: {
      // Application details
      reference_number: '',
      application_type: '',
      product_id: '',
      
      // Borrower information
      borrowers: [
        {
          first_name: '',
          last_name: '',
          email: '',
          phone: '',
          dob: '',
          address: {
            street: '',
            city: '',
            state: '',
            postal_code: '',
            country: ''
          },
          employment_info: {
            employer: '',
            position: '',
            income: '',
            years_employed: ''
          },
          financial_info: {
            assets: '',
            liabilities: '',
            expenses: ''
          },
          bank_info: {
            bank_name: '',
            account_number: '',
            bsb: '',
            account_name: ''
          }
        }
      ],
      
      // Guarantor information
      guarantors: [],
      
      // Company borrower information
      company_borrowers: [
        {
          company_name: '',
          abn: '',
          acn: '',
          business_type: '',
          years_in_business: '',
          industry: '',
          registered_address: {
            street: '',
            city: '',
            state: '',
            postal_code: '',
            country: ''
          },
          directors: [],
          financial_info: {
            annual_revenue: '',
            net_profit: '',
            assets: '',
            liabilities: ''
          }
        }
      ],
      
      // Loan details
      loan_amount: '',
      loan_term: '',
      interest_rate: '',
      purpose: '',
      other_purpose: '',
      repayment_frequency: '',
      estimated_settlement_date: '',
      additional_notes: '',
      
      // Property/security information
      property: {
        address: {
          street: '',
          city: '',
          state: '',
          postal_code: '',
          country: ''
        },
        property_type: '',
        estimated_value: '',
        purchase_price: '',
        is_existing_property: false,
        security_type: ''
      },
      
      // Valuer & QS information
      valuer_info: {
        company_name: '',
        contact_name: '',
        phone: '',
        email: ''
      },
      qs_info: {
        company_name: '',
        contact_name: '',
        phone: '',
        email: ''
      },
      
      // Document upload
      documents: [],
      signature: null,
      signature_date: '',
      
      // Metadata
      branch_id: '',
      bd_id: '',
      stage: 'new'
    },
    currentStep: 0,
    stepValidation: {
      0: false, // Application Details
      1: false, // Borrower Info
      2: false, // Guarantor Info
      3: false, // Company Borrower
      4: false, // Loan Details
      5: false, // Property/Security
      6: false, // Valuer & QS
      7: false  // Document Upload
    }
  }),
  
  getters: {
    getApplicationById: (state) => (id) => {
      return state.applications.find(app => app.id === id)
    },
    
    filteredApplications: (state) => {
      return state.applications
    },
    
    isCurrentStepValid: (state) => {
      return state.stepValidation[state.currentStep]
    },
    
    isFormValid: (state) => {
      return Object.values(state.stepValidation).every(valid => valid)
    }
  },
  
  actions: {
    async fetchApplications(filters = {}) {
      this.loading = true
      this.error = null
      
      try {
        // Merge with existing filters
        const mergedFilters = { ...this.filters, ...filters }
        this.filters = mergedFilters
        
        const response = await applicationService.getApplications(mergedFilters)
        this.applications = response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch applications'
        console.error('Error fetching applications:', error)
      } finally {
        this.loading = false
      }
    },
    
    async fetchApplication(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await applicationService.getApplication(id)
        this.currentApplication = response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch application'
        console.error('Error fetching application:', error)
      } finally {
        this.loading = false
      }
    },
    
    async createApplication() {
      this.loading = true
      this.error = null
      
      try {
        // Create a copy of the form data for submission
        const applicationData = {
          reference_number: this.formData.reference_number,
          loan_amount: this.formData.loan_amount,
          loan_term: this.formData.loan_term,
          interest_rate: this.formData.interest_rate,
          purpose: this.formData.purpose,
          repayment_frequency: this.formData.repayment_frequency,
          application_type: this.formData.application_type,
          product_id: this.formData.product_id,
          estimated_settlement_date: this.formData.estimated_settlement_date,
          branch_id: this.formData.branch_id,
          bd_id: this.formData.bd_id,
          stage: this.formData.stage,
          valuer_info: this.formData.valuer_info,
          qs_info: this.formData.qs_info,
          property: this.formData.property,
          borrowers: this.formData.borrowers,
          guarantors: this.formData.guarantors,
          company_borrowers: this.formData.company_borrowers
        }
        
        // Submit the application with all related entities in a single request
        const response = await applicationService.createApplication(applicationData)
        
        // Handle document uploads separately if needed
        if (this.formData.documents.length > 0) {
          const applicationId = response.data.id
          const formDataObj = new FormData()
          
          this.formData.documents.forEach((doc, index) => {
            formDataObj.append(`document_${index}`, doc.file)
            formDataObj.append(`document_${index}_type`, doc.type)
          })
          
          await applicationService.uploadDocuments(applicationId, formDataObj)
        }
        
        // Handle signature upload if present
        if (this.formData.signature) {
          const applicationId = response.data.id
          const signatureData = new FormData()
          signatureData.append('signature', this.formData.signature)
          signatureData.append('signature_date', this.formData.signature_date)
          
          await applicationService.uploadSignature(applicationId, signatureData)
        }
        
        // Reset form data
        this.resetFormData()
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create application'
        console.error('Error creating application:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateApplicationStage(id, stage) {
      this.loading = true
      this.error = null
      
      try {
        const response = await applicationService.updateApplicationStage(id, stage)
        
        // Update in local state
        if (this.currentApplication && this.currentApplication.id === id) {
          this.currentApplication.stage = stage
        }
        
        const index = this.applications.findIndex(app => app.id === id)
        if (index !== -1) {
          this.applications[index].stage = stage
        }
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update application stage'
        console.error('Error updating application stage:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchApplicationNotes(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await applicationService.getNotes(id)
        this.applicationNotes = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch application notes'
        console.error('Error fetching application notes:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchApplicationDocuments(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await applicationService.getDocuments(id)
        this.applicationDocuments = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch application documents'
        console.error('Error fetching application documents:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async addApplicationNote(id, noteData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await applicationService.addNote(id, noteData)
        
        // Update notes in local state
        if (this.applicationNotes.length > 0) {
          this.applicationNotes.push(response.data)
        }
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to add application note'
        console.error('Error adding application note:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // Multi-step form actions
    nextStep() {
      if (this.currentStep < 7 && this.stepValidation[this.currentStep]) {
        this.currentStep++
      }
    },
    
    prevStep() {
      if (this.currentStep > 0) {
        this.currentStep--
      }
    },
    
    goToStep(step) {
      if (step >= 0 && step <= 7 && (step === 0 || this.stepValidation[step - 1])) {
        this.currentStep = step
      }
    },
    
    updateFormData(data) {
      // Merge the new data with the existing form data
      Object.assign(this.formData, data)
    },
    
    validateStep(step, isValid) {
      this.stepValidation[step] = isValid
    },
    
    resetFormData() {
      this.formData = {
        reference_number: '',
        application_type: '',
        product_id: '',
        
        borrowers: [
          {
            first_name: '',
            last_name: '',
            email: '',
            phone: '',
            dob: '',
            address: {
              street: '',
              city: '',
              state: '',
              postal_code: '',
              country: ''
            },
            employment_info: {
              employer: '',
              position: '',
              income: '',
              years_employed: ''
            },
            financial_info: {
              assets: '',
              liabilities: '',
              expenses: ''
            },
            bank_info: {
              bank_name: '',
              account_number: '',
              bsb: '',
              account_name: ''
            }
          }
        ],
        
        guarantors: [],
        
        company_borrowers: [
          {
            company_name: '',
            abn: '',
            acn: '',
            business_type: '',
            years_in_business: '',
            industry: '',
            registered_address: {
              street: '',
              city: '',
              state: '',
              postal_code: '',
              country: ''
            },
            directors: [],
            financial_info: {
              annual_revenue: '',
              net_profit: '',
              assets: '',
              liabilities: ''
            }
          }
        ],
        
        loan_amount: '',
        loan_term: '',
        interest_rate: '',
        purpose: '',
        other_purpose: '',
        repayment_frequency: '',
        estimated_settlement_date: '',
        additional_notes: '',
        
        property: {
          address: {
            street: '',
            city: '',
            state: '',
            postal_code: '',
            country: ''
          },
          property_type: '',
          estimated_value: '',
          purchase_price: '',
          is_existing_property: false,
          security_type: ''
        },
        
        valuer_info: {
          company_name: '',
          contact_name: '',
          phone: '',
          email: ''
        },
        qs_info: {
          company_name: '',
          contact_name: '',
          phone: '',
          email: ''
        },
        
        documents: [],
        signature: null,
        signature_date: '',
        
        branch_id: '',
        bd_id: '',
        stage: 'new'
      }
      
      this.currentStep = 0
      this.stepValidation = {
        0: false,
        1: false,
        2: false,
        3: false,
        4: false,
        5: false,
        6: false,
        7: false
      }
    }
  }
})
