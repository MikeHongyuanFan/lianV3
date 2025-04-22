<template>
  <div class="loan-details-step">
    <h2 class="step-title">Loan Details</h2>
    
    <div class="form-section">
      <div class="form-row">
        <div class="form-group">
          <label for="loanAmount">Loan Amount*</label>
          <div class="input-with-prefix">
            <span class="input-prefix">$</span>
            <input 
              type="number" 
              id="loanAmount" 
              v-model="localFormData.loan_amount" 
              class="form-control"
              required
              min="1"
              step="0.01"
              @input="validateForm"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="loanTerm">Loan Term (months)*</label>
          <input 
            type="number" 
            id="loanTerm" 
            v-model="localFormData.loan_term" 
            class="form-control"
            required
            min="1"
            @input="validateForm"
          />
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="interestRate">Interest Rate (%)*</label>
          <input 
            type="number" 
            id="interestRate" 
            v-model="localFormData.interest_rate" 
            class="form-control"
            required
            min="0"
            step="0.01"
            @input="validateForm"
          />
        </div>
        
        <div class="form-group">
          <label for="repaymentFrequency">Repayment Frequency*</label>
          <select 
            id="repaymentFrequency" 
            v-model="localFormData.repayment_frequency" 
            class="form-control"
            required
            @change="validateForm"
          >
            <option value="">Select frequency</option>
            <option value="weekly">Weekly</option>
            <option value="fortnightly">Fortnightly</option>
            <option value="monthly">Monthly</option>
            <option value="quarterly">Quarterly</option>
            <option value="annually">Annually</option>
            <option value="interest_only">Interest Only</option>
          </select>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="purpose">Loan Purpose*</label>
          <select 
            id="purpose" 
            v-model="localFormData.purpose" 
            class="form-control"
            required
            @change="validateForm"
          >
            <option value="">Select purpose</option>
            <option value="purchase">Property Purchase</option>
            <option value="refinance">Refinance</option>
            <option value="construction">Construction</option>
            <option value="investment">Investment</option>
            <option value="business">Business</option>
            <option value="debt_consolidation">Debt Consolidation</option>
            <option value="other">Other</option>
          </select>
        </div>
        
        <div class="form-group" v-if="localFormData.purpose === 'other'">
          <label for="otherPurpose">Specify Other Purpose*</label>
          <input 
            type="text" 
            id="otherPurpose" 
            v-model="localFormData.other_purpose" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="estimatedSettlementDate">Estimated Settlement Date*</label>
          <input 
            type="date" 
            id="estimatedSettlementDate" 
            v-model="localFormData.estimated_settlement_date" 
            class="form-control"
            required
            :min="minSettlementDate"
            @input="validateForm"
          />
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group full-width">
          <label for="additionalNotes">Additional Notes</label>
          <textarea 
            id="additionalNotes" 
            v-model="localFormData.additional_notes" 
            class="form-control"
            rows="4"
            @input="validateForm"
          ></textarea>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="repaymentCalculation">Estimated Monthly Repayment</label>
          <div class="input-with-prefix">
            <span class="input-prefix">$</span>
            <input 
              type="text" 
              id="repaymentCalculation" 
              :value="estimatedMonthlyRepayment" 
              class="form-control"
              disabled
            />
          </div>
          <small class="form-text text-muted">This is an estimate only and may vary based on actual loan terms.</small>
        </div>
        
        <div class="form-group">
          <label for="totalRepayable">Total Repayable</label>
          <div class="input-with-prefix">
            <span class="input-prefix">$</span>
            <input 
              type="text" 
              id="totalRepayable" 
              :value="totalRepayable" 
              class="form-control"
              disabled
            />
          </div>
          <small class="form-text text-muted">Includes principal and interest over the full loan term.</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue';

const props = defineProps({
  formData: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['update:formData', 'validate']);

// Create a local copy of the form data to work with
const localFormData = reactive({
  loan_amount: '',
  loan_term: '',
  interest_rate: '',
  purpose: '',
  other_purpose: '',
  repayment_frequency: '',
  estimated_settlement_date: '',
  additional_notes: ''
});

// Minimum settlement date (today)
const minSettlementDate = computed(() => {
  const today = new Date();
  return today.toISOString().split('T')[0];
});

// Calculate estimated monthly repayment
const estimatedMonthlyRepayment = computed(() => {
  if (!localFormData.loan_amount || !localFormData.loan_term || !localFormData.interest_rate) {
    return 'N/A';
  }
  
  const principal = parseFloat(localFormData.loan_amount);
  const monthlyRate = parseFloat(localFormData.interest_rate) / 100 / 12;
  const numberOfPayments = parseInt(localFormData.loan_term);
  
  // Handle interest-only loans
  if (localFormData.repayment_frequency === 'interest_only') {
    return (principal * monthlyRate).toFixed(2);
  }
  
  // Calculate monthly payment using the formula: P * r * (1 + r)^n / ((1 + r)^n - 1)
  const payment = principal * monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments) / 
                 (Math.pow(1 + monthlyRate, numberOfPayments) - 1);
  
  return isNaN(payment) ? 'N/A' : payment.toFixed(2);
});

// Calculate total repayable amount
const totalRepayable = computed(() => {
  if (!localFormData.loan_amount || !localFormData.loan_term || !localFormData.interest_rate) {
    return 'N/A';
  }
  
  const principal = parseFloat(localFormData.loan_amount);
  const monthlyRate = parseFloat(localFormData.interest_rate) / 100 / 12;
  const numberOfPayments = parseInt(localFormData.loan_term);
  
  // Handle interest-only loans
  if (localFormData.repayment_frequency === 'interest_only') {
    return (principal + (principal * monthlyRate * numberOfPayments)).toFixed(2);
  }
  
  // Calculate monthly payment
  const monthlyPayment = principal * monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments) / 
                        (Math.pow(1 + monthlyRate, numberOfPayments) - 1);
  
  // Total repayable is monthly payment * number of payments
  const total = monthlyPayment * numberOfPayments;
  
  return isNaN(total) ? 'N/A' : total.toFixed(2);
});

// Initialize the local form data from props
onMounted(() => {
  if (props.formData) {
    localFormData.loan_amount = props.formData.loan_amount || '';
    localFormData.loan_term = props.formData.loan_term || '';
    localFormData.interest_rate = props.formData.interest_rate || '';
    localFormData.purpose = props.formData.purpose || '';
    localFormData.other_purpose = props.formData.other_purpose || '';
    localFormData.repayment_frequency = props.formData.repayment_frequency || '';
    localFormData.estimated_settlement_date = props.formData.estimated_settlement_date || '';
    localFormData.additional_notes = props.formData.additional_notes || '';
  }
  
  validateForm();
});

// Watch for changes in the local form data and emit updates
watch(localFormData, (newValue) => {
  emit('update:formData', {
    loan_amount: newValue.loan_amount,
    loan_term: newValue.loan_term,
    interest_rate: newValue.interest_rate,
    purpose: newValue.purpose,
    other_purpose: newValue.other_purpose,
    repayment_frequency: newValue.repayment_frequency,
    estimated_settlement_date: newValue.estimated_settlement_date,
    additional_notes: newValue.additional_notes
  });
}, { deep: true });

// Validate the form
function validateForm() {
  let isValid = true;
  
  // Check required fields
  if (!localFormData.loan_amount || !localFormData.loan_term || !localFormData.interest_rate || 
      !localFormData.purpose || !localFormData.repayment_frequency || !localFormData.estimated_settlement_date) {
    isValid = false;
  }
  
  // Check if other purpose is specified when purpose is 'other'
  if (localFormData.purpose === 'other' && !localFormData.other_purpose) {
    isValid = false;
  }
  
  // Validate numeric fields
  if (localFormData.loan_amount && (isNaN(parseFloat(localFormData.loan_amount)) || parseFloat(localFormData.loan_amount) <= 0)) {
    isValid = false;
  }
  
  if (localFormData.loan_term && (isNaN(parseInt(localFormData.loan_term)) || parseInt(localFormData.loan_term) <= 0)) {
    isValid = false;
  }
  
  if (localFormData.interest_rate && (isNaN(parseFloat(localFormData.interest_rate)) || parseFloat(localFormData.interest_rate) < 0)) {
    isValid = false;
  }
  
  // Validate settlement date is not in the past
  if (localFormData.estimated_settlement_date) {
    const settlementDate = new Date(localFormData.estimated_settlement_date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (settlementDate < today) {
      isValid = false;
    }
  }
  
  emit('validate', isValid);
}
</script>

<style scoped>
.loan-details-step {
  padding: 1rem 0;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #2d3748;
}

.form-section {
  background-color: #f7fafc;
  border-radius: 8px;
  padding: 1.5rem;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -0.5rem;
  margin-bottom: 1rem;
}

.form-group {
  flex: 1;
  min-width: 200px;
  padding: 0 0.5rem;
  margin-bottom: 1rem;
}

.form-group.full-width {
  flex-basis: 100%;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #cbd5e0;
  border-radius: 4px;
  font-size: 1rem;
}

.input-with-prefix {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: 0.5rem;
  color: #4a5568;
  font-weight: 500;
}

.input-with-prefix .form-control {
  padding-left: 1.5rem;
}

.form-text {
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.text-muted {
  color: #718096;
}

textarea.form-control {
  resize: vertical;
  min-height: 100px;
}
</style>
