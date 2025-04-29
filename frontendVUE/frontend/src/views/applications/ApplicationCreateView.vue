<template>
  <div class="application-create-container">
    <div class="page-header">
      <h1>Create New Application</h1>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-container">
      <p>Processing...</p>
    </div>

    <!-- Error display -->
    <AlertMessage v-if="error" :message="error" type="error" />

    <!-- Step indicator -->
    <div class="step-indicator">
      <div 
        v-for="(step, index) in steps" 
        :key="index" 
        class="step" 
        :class="{ 'active': currentStep === index, 'completed': currentStep > index }"
      >
        <div class="step-number">{{ index + 1 }}</div>
        <div class="step-title">{{ step.title }}</div>
      </div>
    </div>

    <!-- Form container -->
    <div v-if="!loading" class="form-container">
      <!-- Step 1: Basic Information -->
      <div v-if="currentStep === 0" class="step-content">
        <h2>Basic Information</h2>
        <p>Enter the basic details for this loan application.</p>
        
        <div class="form-group">
          <label for="application-type">Application Type*</label>
          <select 
            id="application-type" 
            v-model="formData.application_type"
            :class="{ 'error': v$.application_type.$error }"
          >
            <option value="">Select Application Type</option>
            <option value="residential">Residential</option>
            <option value="commercial">Commercial</option>
            <option value="personal">Personal</option>
            <option value="business">Business</option>
          </select>
          <div v-if="v$.application_type.$error" class="error-message">
            {{ v$.application_type.$errors[0].$message }}
          </div>
        </div>

        <div class="form-group">
          <label for="purpose">Purpose*</label>
          <input 
            type="text" 
            id="purpose" 
            v-model="formData.purpose"
            placeholder="Purpose of the loan"
            :class="{ 'error': v$.purpose.$error }"
          />
          <div v-if="v$.purpose.$error" class="error-message">
            {{ v$.purpose.$errors[0].$message }}
          </div>
        </div>

        <div class="form-group">
          <label for="loan-amount">Loan Amount*</label>
          <input 
            type="number" 
            id="loan-amount" 
            v-model.number="formData.loan_amount"
            placeholder="Enter loan amount"
            :class="{ 'error': v$.loan_amount.$error }"
          />
          <div v-if="v$.loan_amount.$error" class="error-message">
            {{ v$.loan_amount.$errors[0].$message }}
          </div>
        </div>

        <div class="form-group">
          <label for="loan-term">Loan Term (months)*</label>
          <input 
            type="number" 
            id="loan-term" 
            v-model.number="formData.loan_term"
            placeholder="Enter loan term in months"
            :class="{ 'error': v$.loan_term.$error }"
          />
          <div v-if="v$.loan_term.$error" class="error-message">
            {{ v$.loan_term.$errors[0].$message }}
          </div>
        </div>

        <div class="form-group">
          <label for="interest-rate">Interest Rate (%)*</label>
          <input 
            type="number" 
            id="interest-rate" 
            v-model.number="formData.interest_rate"
            placeholder="Enter interest rate"
            step="0.01"
            :class="{ 'error': v$.interest_rate.$error }"
          />
          <div v-if="v$.interest_rate.$error" class="error-message">
            {{ v$.interest_rate.$errors[0].$message }}
          </div>
        </div>

        <div class="form-group">
          <label for="repayment-frequency">Repayment Frequency*</label>
          <select 
            id="repayment-frequency" 
            v-model="formData.repayment_frequency"
            :class="{ 'error': v$.repayment_frequency.$error }"
          >
            <option value="">Select Frequency</option>
            <option value="weekly">Weekly</option>
            <option value="fortnightly">Fortnightly</option>
            <option value="monthly">Monthly</option>
          </select>
          <div v-if="v$.repayment_frequency.$error" class="error-message">
            {{ v$.repayment_frequency.$errors[0].$message }}
          </div>
        </div>

        <div class="form-group">
          <label for="estimated-settlement-date">Estimated Settlement Date*</label>
          <input 
            type="date" 
            id="estimated-settlement-date" 
            v-model="formData.estimated_settlement_date"
            :class="{ 'error': v$.estimated_settlement_date.$error }"
          />
          <div v-if="v$.estimated_settlement_date.$error" class="error-message">
            {{ v$.estimated_settlement_date.$errors[0].$message }}
          </div>
        </div>
      </div>

      <!-- Step 2: Broker and Branch Information -->
      <div v-if="currentStep === 1" class="step-content">
        <h2>Broker and Branch Information</h2>
        <p>Select the broker, branch, and BDM for this application.</p>
        
        <div class="form-group">
          <label for="broker">Broker*</label>
          <select 
            id="broker" 
            v-model="formData.broker"
            :class="{ 'error': v$.broker.$error }"
          >
            <option value="">Select Broker</option>
            <option v-for="broker in brokers" :key="broker.id" :value="broker.id">
              {{ broker.name }}
            </option>
          </select>
          <div v-if="v$.broker.$error" class="error-message">
            {{ v$.broker.$errors[0].$message }}
          </div>
        </div>

        <div class="form-group">
          <label for="branch">Branch*</label>
          <select 
            id="branch" 
            v-model="formData.branch"
            :class="{ 'error': v$.branch.$error }"
          >
            <option value="">Select Branch</option>
            <option v-for="branch in branches" :key="branch.id" :value="branch.id">
              {{ branch.name }}
            </option>
          </select>
          <div v-if="v$.branch.$error" class="error-message">
            {{ v$.branch.$errors[0].$message }}
          </div>
        </div>

        <div class="form-group">
          <label for="bdm">BDM</label>
          <select 
            id="bdm" 
            v-model="formData.bd"
          >
            <option value="">Select BDM</option>
            <option v-for="bdm in bdms" :key="bdm.id" :value="bdm.id">
              {{ bdm.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Step 3: Security Information -->
      <div v-if="currentStep === 2" class="step-content">
        <h2>Security Information</h2>
        <p>Enter details about the security for this loan.</p>
        
        <div class="form-group">
          <label for="security-address">Security Address*</label>
          <input 
            type="text" 
            id="security-address" 
            v-model="formData.security_address"
            placeholder="Enter security property address"
            :class="{ 'error': v$.security_address.$error }"
          />
          <div v-if="v$.security_address.$error" class="error-message">
            {{ v$.security_address.$errors[0].$message }}
          </div>
        </div>

        <div class="form-group">
          <label for="security-type">Security Type*</label>
          <select 
            id="security-type" 
            v-model="formData.security_type"
            :class="{ 'error': v$.security_type.$error }"
          >
            <option value="">Select Security Type</option>
            <option value="residential_property">Residential Property</option>
            <option value="commercial_property">Commercial Property</option>
            <option value="land">Land</option>
            <option value="vehicle">Vehicle</option>
            <option value="equipment">Equipment</option>
            <option value="other">Other</option>
          </select>
          <div v-if="v$.security_type.$error" class="error-message">
            {{ v$.security_type.$errors[0].$message }}
          </div>
        </div>

        <div class="form-group">
          <label for="security-value">Security Value*</label>
          <input 
            type="number" 
            id="security-value" 
            v-model.number="formData.security_value"
            placeholder="Enter security value"
            :class="{ 'error': v$.security_value.$error }"
          />
          <div v-if="v$.security_value.$error" class="error-message">
            {{ v$.security_value.$errors[0].$message }}
          </div>
        </div>
      </div>

      <!-- Step 4: Borrower Information -->
      <div v-if="currentStep === 3" class="step-content">
        <h2>Borrower Information</h2>
        <p>Add borrowers to this application. At least one borrower is required.</p>
        
        <!-- Borrower list -->
        <div v-if="formData.borrowers.length > 0" class="borrowers-list">
          <h3>Selected Borrowers</h3>
          <div v-for="(borrower, index) in formData.borrowers" :key="index" class="borrower-item">
            <div class="borrower-info">
              <div class="borrower-name">{{ borrower.first_name }} {{ borrower.last_name }}</div>
              <div class="borrower-email">{{ borrower.email }}</div>
              <div class="borrower-type">{{ formatBorrowerType(borrower.borrower_type) }}</div>
            </div>
            <div class="borrower-actions">
              <button type="button" class="action-button edit" @click="editBorrower(index)">Edit</button>
              <button type="button" class="action-button delete" @click="removeBorrower(index)">Remove</button>
            </div>
          </div>
        </div>
        
        <div v-else class="no-borrowers">
          <p>No borrowers added yet. Please add at least one borrower.</p>
        </div>
        
        <!-- Add borrower button -->
        <div class="add-borrower-container">
          <BaseButton @click="showAddBorrowerModal = true" variant="secondary">
            Add Borrower
          </BaseButton>
        </div>
        
        <!-- Borrower form modal -->
        <div v-if="showAddBorrowerModal" class="modal-overlay">
          <div class="modal-container">
            <div class="modal-header">
              <h3>{{ editingBorrowerIndex !== null ? 'Edit Borrower' : 'Add Borrower' }}</h3>
              <button type="button" class="close-button" @click="cancelBorrowerForm">&times;</button>
            </div>
            <div class="modal-body">
              <BorrowerForm
                :borrower="editingBorrowerIndex !== null ? formData.borrowers[editingBorrowerIndex] : {}"
                :mode="editingBorrowerIndex !== null ? 'edit' : 'create'"
                :loading="borrowerFormLoading"
                @submit="saveBorrower"
                @cancel="cancelBorrowerForm"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Step 5: Guarantor Information -->
      <div v-if="currentStep === 4" class="step-content">
        <h2>Guarantor Information</h2>
        <p>Add guarantors to this application (optional).</p>
        
        <!-- Guarantor list -->
        <div v-if="formData.guarantors.length > 0" class="guarantors-list">
          <h3>Selected Guarantors</h3>
          <div v-for="(guarantor, index) in formData.guarantors" :key="index" class="guarantor-item">
            <div class="guarantor-info">
              <div class="guarantor-name">{{ guarantor.first_name }} {{ guarantor.last_name }}</div>
              <div class="guarantor-email">{{ guarantor.email }}</div>
              <div class="guarantor-relationship">{{ formatRelationship(guarantor.relationship_to_borrower) }}</div>
            </div>
            <div class="guarantor-actions">
              <button type="button" class="action-button edit" @click="editGuarantor(index)">Edit</button>
              <button type="button" class="action-button delete" @click="removeGuarantor(index)">Remove</button>
            </div>
          </div>
        </div>
        
        <div v-else class="no-guarantors">
          <p>No guarantors added yet. Adding guarantors is optional.</p>
        </div>
        
        <!-- Add guarantor button -->
        <div class="add-guarantor-container">
          <BaseButton @click="showAddGuarantorModal = true" variant="secondary">
            Add Guarantor
          </BaseButton>
        </div>
        
        <!-- Guarantor form modal -->
        <div v-if="showAddGuarantorModal" class="modal-overlay">
          <div class="modal-container">
            <div class="modal-header">
              <h3>{{ editingGuarantorIndex !== null ? 'Edit Guarantor' : 'Add Guarantor' }}</h3>
              <button type="button" class="close-button" @click="cancelGuarantorForm">&times;</button>
            </div>
            <div class="modal-body">
              <GuarantorForm
                :guarantor="editingGuarantorIndex !== null ? formData.guarantors[editingGuarantorIndex] : {}"
                :mode="editingGuarantorIndex !== null ? 'edit' : 'create'"
                :loading="guarantorFormLoading"
                @submit="saveGuarantor"
                @cancel="cancelGuarantorForm"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Step 6: Review and Submit -->
      <div v-if="currentStep === 5" class="step-content">
        <h2>Review and Submit</h2>
        <p>Review the application details before submitting.</p>
        
        <div class="review-section">
          <h3>Basic Information</h3>
          <div class="review-grid">
            <div class="review-item">
              <div class="review-label">Application Type:</div>
              <div class="review-value">{{ formatApplicationType(formData.application_type) }}</div>
            </div>
            <div class="review-item">
              <div class="review-label">Purpose:</div>
              <div class="review-value">{{ formData.purpose }}</div>
            </div>
            <div class="review-item">
              <div class="review-label">Loan Amount:</div>
              <div class="review-value">${{ formatCurrency(formData.loan_amount) }}</div>
            </div>
            <div class="review-item">
              <div class="review-label">Loan Term:</div>
              <div class="review-value">{{ formData.loan_term }} months</div>
            </div>
            <div class="review-item">
              <div class="review-label">Interest Rate:</div>
              <div class="review-value">{{ formData.interest_rate }}%</div>
            </div>
            <div class="review-item">
              <div class="review-label">Repayment Frequency:</div>
              <div class="review-value">{{ formatRepaymentFrequency(formData.repayment_frequency) }}</div>
            </div>
            <div class="review-item">
              <div class="review-label">Estimated Settlement Date:</div>
              <div class="review-value">{{ formatDate(formData.estimated_settlement_date) }}</div>
            </div>
          </div>
        </div>
        
        <div class="review-section">
          <h3>Broker and Branch Information</h3>
          <div class="review-grid">
            <div class="review-item">
              <div class="review-label">Broker:</div>
              <div class="review-value">{{ getBrokerName(formData.broker) }}</div>
            </div>
            <div class="review-item">
              <div class="review-label">Branch:</div>
              <div class="review-value">{{ getBranchName(formData.branch) }}</div>
            </div>
            <div class="review-item">
              <div class="review-label">BDM:</div>
              <div class="review-value">{{ getBDMName(formData.bd) || 'Not specified' }}</div>
            </div>
          </div>
        </div>
        
        <div class="review-section">
          <h3>Security Information</h3>
          <div class="review-grid">
            <div class="review-item">
              <div class="review-label">Security Address:</div>
              <div class="review-value">{{ formData.security_address }}</div>
            </div>
            <div class="review-item">
              <div class="review-label">Security Type:</div>
              <div class="review-value">{{ formatSecurityType(formData.security_type) }}</div>
            </div>
            <div class="review-item">
              <div class="review-label">Security Value:</div>
              <div class="review-value">${{ formatCurrency(formData.security_value) }}</div>
            </div>
          </div>
        </div>
        
        <div class="review-section">
          <h3>Borrowers</h3>
          <div v-if="formData.borrowers.length > 0" class="review-list">
            <div v-for="(borrower, index) in formData.borrowers" :key="index" class="review-list-item">
              <div class="review-list-primary">{{ borrower.first_name }} {{ borrower.last_name }}</div>
              <div class="review-list-secondary">{{ borrower.email }} | {{ formatBorrowerType(borrower.borrower_type) }}</div>
            </div>
          </div>
          <div v-else class="review-empty">
            <p>No borrowers added. Please go back and add at least one borrower.</p>
          </div>
        </div>
        
        <div class="review-section">
          <h3>Guarantors</h3>
          <div v-if="formData.guarantors.length > 0" class="review-list">
            <div v-for="(guarantor, index) in formData.guarantors" :key="index" class="review-list-item">
              <div class="review-list-primary">{{ guarantor.first_name }} {{ guarantor.last_name }}</div>
              <div class="review-list-secondary">{{ guarantor.email }} | {{ formatRelationship(guarantor.relationship_to_borrower) }}</div>
            </div>
          </div>
          <div v-else class="review-empty">
            <p>No guarantors added (optional).</p>
          </div>
        </div>
        
        <div v-if="formData.borrowers.length === 0" class="validation-error">
          <p>Please go back and add at least one borrower before submitting.</p>
        </div>
      </div>

      <!-- Navigation buttons -->
      <div class="form-navigation">
        <BaseButton 
          v-if="currentStep > 0" 
          @click="previousStep" 
          variant="secondary"
        >
          Previous
        </BaseButton>
        
        <BaseButton 
          v-if="currentStep < steps.length - 1" 
          @click="nextStep" 
          variant="primary"
        >
          Next
        </BaseButton>
        
        <BaseButton 
          v-if="currentStep === steps.length - 1" 
          @click="submitApplication" 
          variant="primary"
        >
          Submit Application
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useVuelidate } from '@vuelidate/core'
import { required, minValue, helpers } from '@vuelidate/validators'
import { useApplicationStore } from '@/store/application'
import { useBrokerStore } from '@/store/broker'
import BaseButton from '@/components/BaseButton.vue'
import AlertMessage from '@/components/AlertMessage.vue'
import BorrowerForm from '@/components/BorrowerForm.vue'
import GuarantorForm from '@/components/GuarantorForm.vue'

export default {
  name: 'ApplicationCreateView',
  components: {
    BaseButton,
    AlertMessage,
    BorrowerForm,
    GuarantorForm
  },
  setup() {
    const router = useRouter()
    const applicationStore = useApplicationStore()
    const brokerStore = useBrokerStore()
    
    // Form data
    const formData = reactive({
      application_type: '',
      purpose: '',
      loan_amount: null,
      loan_term: null,
      interest_rate: null,
      repayment_frequency: '',
      estimated_settlement_date: '',
      broker: null,
      branch: null,
      bd: null,
      security_address: '',
      security_type: '',
      security_value: null,
      stage: 'inquiry', // Default stage for new applications
      product_id: 'default', // This would be replaced with actual product selection
      borrowers: [],
      guarantors: []
    })
    
    // Form validation rules
    const rules = computed(() => {
      return {
        application_type: { required: helpers.withMessage('Application type is required', required) },
        purpose: { required: helpers.withMessage('Purpose is required', required) },
        loan_amount: { 
          required: helpers.withMessage('Loan amount is required', required),
          minValue: helpers.withMessage('Loan amount must be greater than 0', minValue(1))
        },
        loan_term: { 
          required: helpers.withMessage('Loan term is required', required),
          minValue: helpers.withMessage('Loan term must be greater than 0', minValue(1))
        },
        interest_rate: { 
          required: helpers.withMessage('Interest rate is required', required),
          minValue: helpers.withMessage('Interest rate must be greater than 0', minValue(0.01))
        },
        repayment_frequency: { required: helpers.withMessage('Repayment frequency is required', required) },
        estimated_settlement_date: { required: helpers.withMessage('Estimated settlement date is required', required) },
        broker: { required: helpers.withMessage('Broker is required', required) },
        branch: { required: helpers.withMessage('Branch is required', required) },
        security_address: { required: helpers.withMessage('Security address is required', required) },
        security_type: { required: helpers.withMessage('Security type is required', required) },
        security_value: { 
          required: helpers.withMessage('Security value is required', required),
          minValue: helpers.withMessage('Security value must be greater than 0', minValue(1))
        }
      }
    })
    
    const v$ = useVuelidate(rules, formData)
    
    // Multi-step form
    const steps = [
      { title: 'Basic Information' },
      { title: 'Broker & Branch' },
      { title: 'Security' },
      { title: 'Borrowers' },
      { title: 'Guarantors' },
      { title: 'Review & Submit' }
    ]
    
    const currentStep = ref(0)
    const loading = ref(false)
    const error = ref(null)
    
    // Store data
    const brokers = computed(() => brokerStore.brokers)
    const branches = computed(() => brokerStore.branches)
    const bdms = computed(() => brokerStore.bdms)
    
    // Borrower form state
    const showAddBorrowerModal = ref(false)
    const editingBorrowerIndex = ref(null)
    const borrowerFormLoading = ref(false)
    
    // Guarantor form state
    const showAddGuarantorModal = ref(false)
    const editingGuarantorIndex = ref(null)
    const guarantorFormLoading = ref(false)
    
    // Methods
    const nextStep = async () => {
      // Validate current step
      let validationPassed = false
      
      switch (currentStep.value) {
        case 0: // Basic Information
          v$.value.application_type.$touch()
          v$.value.purpose.$touch()
          v$.value.loan_amount.$touch()
          v$.value.loan_term.$touch()
          v$.value.interest_rate.$touch()
          v$.value.repayment_frequency.$touch()
          v$.value.estimated_settlement_date.$touch()
          
          validationPassed = !v$.value.application_type.$error &&
                            !v$.value.purpose.$error &&
                            !v$.value.loan_amount.$error &&
                            !v$.value.loan_term.$error &&
                            !v$.value.interest_rate.$error &&
                            !v$.value.repayment_frequency.$error &&
                            !v$.value.estimated_settlement_date.$error
          break
          
        case 1: // Broker and Branch
          v$.value.broker.$touch()
          v$.value.branch.$touch()
          
          validationPassed = !v$.value.broker.$error &&
                            !v$.value.branch.$error
          break
          
        case 2: // Security
          v$.value.security_address.$touch()
          v$.value.security_type.$touch()
          v$.value.security_value.$touch()
          
          validationPassed = !v$.value.security_address.$error &&
                            !v$.value.security_type.$error &&
                            !v$.value.security_value.$error
          break
          
        case 3: // Borrowers
          validationPassed = formData.borrowers.length > 0
          if (!validationPassed) {
            error.value = 'Please add at least one borrower'
            setTimeout(() => {
              error.value = null
            }, 3000)
          }
          break
          
        case 4: // Guarantors
          // Guarantors are optional
          validationPassed = true
          break
          
        default:
          validationPassed = true
      }
      
      if (validationPassed) {
        currentStep.value++
      }
    }
    
    const previousStep = () => {
      if (currentStep.value > 0) {
        currentStep.value--
      }
    }
    
    const submitApplication = async () => {
      // Validate that we have at least one borrower
      if (formData.borrowers.length === 0) {
        error.value = 'Please add at least one borrower before submitting'
        return
      }
      
      try {
        loading.value = true
        error.value = null
        
        // Use the cascade endpoint to create the application with related entities
        const response = await applicationStore.createApplicationWithCascade(formData)
        
        // Navigate to the application detail page
        router.push({ name: 'application-detail', params: { id: response.id } })
      } catch (err) {
        error.value = err.message || 'Failed to create application'
        console.error('Error creating application:', err)
      } finally {
        loading.value = false
      }
    }
    
    // Borrower methods
    const saveBorrower = (borrowerData) => {
      borrowerFormLoading.value = true
      
      try {
        if (editingBorrowerIndex.value !== null) {
          // Update existing borrower
          formData.borrowers[editingBorrowerIndex.value] = borrowerData
        } else {
          // Add new borrower
          formData.borrowers.push(borrowerData)
        }
        
        // Close modal and reset state
        showAddBorrowerModal.value = false
        editingBorrowerIndex.value = null
      } catch (err) {
        error.value = err.message || 'Failed to save borrower'
        console.error('Error saving borrower:', err)
      } finally {
        borrowerFormLoading.value = false
      }
    }
    
    const editBorrower = (index) => {
      editingBorrowerIndex.value = index
      showAddBorrowerModal.value = true
    }
    
    const removeBorrower = (index) => {
      formData.borrowers.splice(index, 1)
    }
    
    const cancelBorrowerForm = () => {
      showAddBorrowerModal.value = false
      editingBorrowerIndex.value = null
    }
    
    // Guarantor methods
    const saveGuarantor = (guarantorData) => {
      guarantorFormLoading.value = true
      
      try {
        if (editingGuarantorIndex.value !== null) {
          // Update existing guarantor
          formData.guarantors[editingGuarantorIndex.value] = guarantorData
        } else {
          // Add new guarantor
          formData.guarantors.push(guarantorData)
        }
        
        // Close modal and reset state
        showAddGuarantorModal.value = false
        editingGuarantorIndex.value = null
      } catch (err) {
        error.value = err.message || 'Failed to save guarantor'
        console.error('Error saving guarantor:', err)
      } finally {
        guarantorFormLoading.value = false
      }
    }
    
    const editGuarantor = (index) => {
      editingGuarantorIndex.value = index
      showAddGuarantorModal.value = true
    }
    
    const removeGuarantor = (index) => {
      formData.guarantors.splice(index, 1)
    }
    
    const cancelGuarantorForm = () => {
      showAddGuarantorModal.value = false
      editingGuarantorIndex.value = null
    }
    
    // Formatting methods
    const formatBorrowerType = (type) => {
      const types = {
        individual: 'Individual',
        company: 'Company',
        trust: 'Trust'
      }
      return types[type] || type
    }
    
    const formatRelationship = (relationship) => {
      const relationships = {
        spouse: 'Spouse',
        parent: 'Parent',
        child: 'Child',
        sibling: 'Sibling',
        business_partner: 'Business Partner',
        friend: 'Friend',
        other: 'Other'
      }
      return relationships[relationship] || relationship
    }
    
    const formatApplicationType = (type) => {
      const types = {
        residential: 'Residential',
        commercial: 'Commercial',
        personal: 'Personal',
        business: 'Business'
      }
      return types[type] || type
    }
    
    const formatSecurityType = (type) => {
      const types = {
        residential_property: 'Residential Property',
        commercial_property: 'Commercial Property',
        land: 'Land',
        vehicle: 'Vehicle',
        equipment: 'Equipment',
        other: 'Other'
      }
      return types[type] || type
    }
    
    const formatRepaymentFrequency = (frequency) => {
      const frequencies = {
        weekly: 'Weekly',
        fortnightly: 'Fortnightly',
        monthly: 'Monthly'
      }
      return frequencies[frequency] || frequency
    }
    
    const formatCurrency = (value) => {
      if (!value) return '0.00'
      return parseFloat(value).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    const getBrokerName = (brokerId) => {
      if (!brokerId) return 'Not specified'
      const broker = brokers.value.find(b => b.id === brokerId)
      return broker ? broker.name : `Broker #${brokerId}`
    }
    
    const getBranchName = (branchId) => {
      if (!branchId) return 'Not specified'
      const branch = branches.value.find(b => b.id === branchId)
      return branch ? branch.name : `Branch #${branchId}`
    }
    
    const getBDMName = (bdmId) => {
      if (!bdmId) return null
      const bdm = bdms.value.find(b => b.id === bdmId)
      return bdm ? bdm.name : `BDM #${bdmId}`
    }
    
    // Fetch required data
    const fetchData = async () => {
      try {
        loading.value = true
        error.value = null
        
        await Promise.all([
          brokerStore.fetchBrokers(),
          brokerStore.fetchBranches(),
          brokerStore.fetchBDMs()
        ])
      } catch (err) {
        error.value = err.message || 'Failed to load required data'
        console.error('Error loading data:', err)
      } finally {
        loading.value = false
      }
    }
    
    onMounted(() => {
      fetchData()
    })
    
    return {
      formData,
      v$,
      steps,
      currentStep,
      loading,
      error,
      brokers,
      branches,
      bdms,
      nextStep,
      previousStep,
      submitApplication,
      // Borrower methods
      showAddBorrowerModal,
      editingBorrowerIndex,
      borrowerFormLoading,
      saveBorrower,
      editBorrower,
      removeBorrower,
      cancelBorrowerForm,
      // Guarantor methods
      showAddGuarantorModal,
      editingGuarantorIndex,
      guarantorFormLoading,
      saveGuarantor,
      editGuarantor,
      removeGuarantor,
      cancelGuarantorForm,
      // Formatting methods
      formatBorrowerType,
      formatRelationship,
      formatApplicationType,
      formatSecurityType,
      formatRepaymentFrequency,
      formatCurrency,
      formatDate,
      getBrokerName,
      getBranchName,
      getBDMName
    }
  }
}
</script>

<style scoped>
.application-create-container {
  padding: 1.5rem;
}

.page-header {
  margin-bottom: 2rem;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  background-color: #f9fafb;
  border-radius: 0.5rem;
}

.step-indicator {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
  position: relative;
}

.step-indicator::before {
  content: '';
  position: absolute;
  top: 1.5rem;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #e5e7eb;
  z-index: 1;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2;
  flex: 1;
}

.step-number {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background-color: #e5e7eb;
  color: #6b7280;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.step.active .step-number {
  background-color: #3b82f6;
  color: white;
}

.step.completed .step-number {
  background-color: #10b981;
  color: white;
}

.step-title {
  font-size: 0.875rem;
  color: #6b7280;
  text-align: center;
}

.step.active .step-title {
  color: #3b82f6;
  font-weight: 600;
}

.step.completed .step-title {
  color: #10b981;
  font-weight: 600;
}

.form-container {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  padding: 1.5rem;
}

.step-content {
  margin-bottom: 2rem;
}

.step-content h2 {
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
}

.step-content p {
  margin-bottom: 1.5rem;
  color: #6b7280;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
}

.form-group input.error,
.form-group select.error {
  border-color: #ef4444;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.form-navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.placeholder-message {
  background-color: #f9fafb;
  border: 1px dashed #d1d5db;
  border-radius: 0.375rem;
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}

/* Borrower and Guarantor styles */
.borrowers-list,
.guarantors-list {
  margin-bottom: 1.5rem;
}

.borrowers-list h3,
.guarantors-list h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.borrower-item,
.guarantor-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  margin-bottom: 0.5rem;
  background-color: #f9fafb;
}

.borrower-info,
.guarantor-info {
  flex: 1;
}

.borrower-name,
.guarantor-name {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.borrower-email,
.guarantor-email,
.borrower-type,
.guarantor-relationship {
  font-size: 0.875rem;
  color: #6b7280;
}

.borrower-actions,
.guarantor-actions {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  cursor: pointer;
  border: none;
}

.action-button.edit {
  background-color: #dbeafe;
  color: #1e40af;
}

.action-button.delete {
  background-color: #fee2e2;
  color: #b91c1c;
}

.no-borrowers,
.no-guarantors {
  padding: 1.5rem;
  background-color: #f9fafb;
  border-radius: 0.375rem;
  text-align: center;
  color: #6b7280;
  margin-bottom: 1.5rem;
}

.add-borrower-container,
.add-guarantor-container {
  margin-bottom: 1.5rem;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 50;
}

.modal-container {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
}

.modal-body {
  padding: 1.5rem;
}

/* Review section styles */
.review-section {
  margin-bottom: 2rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  overflow: hidden;
}

.review-section h3 {
  padding: 0.75rem 1rem;
  background-color: #f3f4f6;
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.review-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.review-item {
  display: flex;
  flex-direction: column;
}

.review-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.review-value {
  font-weight: 500;
}

.review-list {
  padding: 1rem;
}

.review-list-item {
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  margin-bottom: 0.5rem;
  background-color: #f9fafb;
}

.review-list-primary {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.review-list-secondary {
  font-size: 0.875rem;
  color: #6b7280;
}

.review-empty {
  padding: 1rem;
  color: #6b7280;
  font-style: italic;
}

.validation-error {
  padding: 1rem;
  background-color: #fee2e2;
  border-radius: 0.375rem;
  color: #b91c1c;
  margin-top: 1rem;
}
</style>
