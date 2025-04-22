<template>
  <div class="application-form-container">
    <div class="steps-indicator">
      <div 
        v-for="(step, index) in steps" 
        :key="index"
        :class="['step', { 'active': currentStep === index, 'completed': currentStep > index }]"
        @click="goToStep(index)"
      >
        {{ step.name }}
      </div>
    </div>

    <div class="form-content">
      <component 
        :is="steps[currentStep].component" 
        :formData="formData"
        @update:formData="updateFormData"
        @validate="validateCurrentStep"
      ></component>
    </div>

    <div class="form-navigation">
      <button 
        v-if="currentStep > 0" 
        @click="prevStep" 
        class="btn btn-secondary"
      >
        Previous
      </button>
      <button 
        v-if="currentStep < steps.length - 1" 
        @click="nextStep" 
        class="btn btn-primary"
        :disabled="!isCurrentStepValid"
      >
        Next
      </button>
      <button 
        v-else 
        @click="submitForm" 
        class="btn btn-success"
        :disabled="!isFormValid || isSubmitting"
      >
        {{ isSubmitting ? 'Submitting...' : 'Submit Application' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// Import step components
import ApplicationDetailsStep from './steps/ApplicationDetailsStep.vue';
import BorrowerInfoStep from './steps/BorrowerInfoStep.vue';
import GuarantorInfoStep from './steps/GuarantorInfoStep.vue';
import CompanyBorrowerStep from './steps/CompanyBorrowerStep.vue';
import LoanDetailsStep from './steps/LoanDetailsStep.vue';
import PropertySecurityStep from './steps/PropertySecurityStep.vue';
import ValuerQSInfoStep from './steps/ValuerQSInfoStep.vue';
import DocumentUploadStep from './steps/DocumentUploadStep.vue';

const router = useRouter();
const currentStep = ref(0);
const isSubmitting = ref(false);
const stepValidation = reactive({
  0: false, // Application Details
  1: false, // Borrower Info
  2: false, // Guarantor Info
  3: false, // Company Borrower
  4: false, // Loan Details
  5: false, // Property/Security
  6: false, // Valuer & QS
  7: false  // Document Upload
});

const steps = [
  { name: 'Application Details', component: ApplicationDetailsStep },
  { name: 'Borrower Information', component: BorrowerInfoStep },
  { name: 'Guarantor Information', component: GuarantorInfoStep },
  { name: 'Company Borrower', component: CompanyBorrowerStep },
  { name: 'Loan Details', component: LoanDetailsStep },
  { name: 'Property/Security', component: PropertySecurityStep },
  { name: 'Valuer & QS Info', component: ValuerQSInfoStep },
  { name: 'Document Upload', component: DocumentUploadStep }
];

const formData = reactive({
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
      // Additional borrower fields
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
  repayment_frequency: '',
  estimated_settlement_date: '',
  
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
});

const isCurrentStepValid = computed(() => {
  return stepValidation[currentStep.value];
});

const isFormValid = computed(() => {
  // Check if all steps are valid
  return Object.values(stepValidation).every(valid => valid);
});

function updateFormData(newData) {
  Object.assign(formData, newData);
}

function validateCurrentStep(isValid) {
  stepValidation[currentStep.value] = isValid;
}

function goToStep(stepIndex) {
  // Only allow navigation to completed steps or the current step + 1
  if (stepIndex <= currentStep.value + 1 && 
      (stepIndex === 0 || stepValidation[stepIndex - 1])) {
    currentStep.value = stepIndex;
  }
}

function nextStep() {
  if (currentStep.value < steps.length - 1 && stepValidation[currentStep.value]) {
    currentStep.value++;
  }
}

function prevStep() {
  if (currentStep.value > 0) {
    currentStep.value--;
  }
}

async function submitForm() {
  if (!isFormValid.value) return;
  
  isSubmitting.value = true;
  
  try {
    // Format the data for API submission
    const applicationData = {
      reference_number: formData.reference_number,
      loan_amount: formData.loan_amount,
      loan_term: formData.loan_term,
      interest_rate: formData.interest_rate,
      purpose: formData.purpose,
      repayment_frequency: formData.repayment_frequency,
      application_type: formData.application_type,
      product_id: formData.product_id,
      estimated_settlement_date: formData.estimated_settlement_date,
      branch_id: formData.branch_id,
      bd_id: formData.bd_id,
      stage: formData.stage,
      valuer_info: formData.valuer_info,
      qs_info: formData.qs_info,
      property: formData.property,
      borrowers: formData.borrowers,
      guarantors: formData.guarantors,
      company_borrowers: formData.company_borrowers
    };
    
    // Submit the application with all related entities in a single request
    const response = await axios.post('/api/applications/', applicationData);
    
    // Handle document uploads separately if needed
    if (formData.documents.length > 0) {
      const applicationId = response.data.id;
      const formDataObj = new FormData();
      
      formData.documents.forEach((doc, index) => {
        formDataObj.append(`document_${index}`, doc.file);
        formDataObj.append(`document_${index}_type`, doc.type);
      });
      
      await axios.post(`/api/applications/${applicationId}/documents/`, formDataObj, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    }
    
    // Handle signature upload if present
    if (formData.signature) {
      const applicationId = response.data.id;
      const signatureData = new FormData();
      signatureData.append('signature', formData.signature);
      signatureData.append('signature_date', formData.signature_date);
      
      await axios.post(`/api/applications/${applicationId}/signature/`, signatureData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    }
    
    // Redirect to application detail page or success page
    router.push({ name: 'ApplicationDetail', params: { id: response.data.id } });
  } catch (error) {
    console.error('Error submitting application:', error);
    // Handle error (show error message to user)
  } finally {
    isSubmitting.value = false;
  }
}

onMounted(() => {
  // Initialize any data needed from API (e.g., product list, branch list, etc.)
});
</script>

<style scoped>
.application-form-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.steps-indicator {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
  overflow-x: auto;
  padding-bottom: 1rem;
}

.step {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: #f0f0f0;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  margin-right: 0.5rem;
}

.step.active {
  background-color: #4299e1;
  color: white;
}

.step.completed {
  background-color: #48bb78;
  color: white;
}

.form-content {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-navigation {
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #4299e1;
  color: white;
}

.btn-primary:hover {
  background-color: #3182ce;
}

.btn-secondary {
  background-color: #a0aec0;
  color: white;
}

.btn-secondary:hover {
  background-color: #718096;
}

.btn-success {
  background-color: #48bb78;
  color: white;
}

.btn-success:hover {
  background-color: #38a169;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
