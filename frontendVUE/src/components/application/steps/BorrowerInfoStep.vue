<template>
  <div class="borrower-info-step">
    <h2 class="step-title">Borrower Information</h2>
    
    <div v-for="(borrower, index) in localFormData.borrowers" :key="index" class="borrower-section">
      <div class="section-header">
        <h3>Borrower {{ index + 1 }}</h3>
        <button 
          v-if="localFormData.borrowers.length > 1" 
          @click="removeBorrower(index)" 
          class="btn btn-danger btn-sm"
        >
          Remove
        </button>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="firstName">First Name*</label>
          <input 
            type="text" 
            id="firstName" 
            v-model="borrower.first_name" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
        
        <div class="form-group">
          <label for="lastName">Last Name*</label>
          <input 
            type="text" 
            id="lastName" 
            v-model="borrower.last_name" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="email">Email*</label>
          <input 
            type="email" 
            id="email" 
            v-model="borrower.email" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
        
        <div class="form-group">
          <label for="phone">Phone*</label>
          <input 
            type="tel" 
            id="phone" 
            v-model="borrower.phone" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="dob">Date of Birth*</label>
          <input 
            type="date" 
            id="dob" 
            v-model="borrower.dob" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
        
        <div class="form-group">
          <label for="taxId">Tax ID</label>
          <input 
            type="text" 
            id="taxId" 
            v-model="borrower.tax_id" 
            class="form-control"
            @input="validateForm"
          />
        </div>
      </div>
      
      <h4>Residential Address</h4>
      <div class="form-row">
        <div class="form-group">
          <label for="street">Street*</label>
          <input 
            type="text" 
            id="street" 
            v-model="borrower.address.street" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
        
        <div class="form-group">
          <label for="city">City*</label>
          <input 
            type="text" 
            id="city" 
            v-model="borrower.address.city" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="state">State*</label>
          <input 
            type="text" 
            id="state" 
            v-model="borrower.address.state" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
        
        <div class="form-group">
          <label for="postalCode">Postal Code*</label>
          <input 
            type="text" 
            id="postalCode" 
            v-model="borrower.address.postal_code" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
        
        <div class="form-group">
          <label for="country">Country*</label>
          <input 
            type="text" 
            id="country" 
            v-model="borrower.address.country" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
      </div>
      
      <h4>Employment Information</h4>
      <div class="form-row">
        <div class="form-group">
          <label for="employer">Employer*</label>
          <input 
            type="text" 
            id="employer" 
            v-model="borrower.employment_info.employer" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
        
        <div class="form-group">
          <label for="position">Position*</label>
          <input 
            type="text" 
            id="position" 
            v-model="borrower.employment_info.position" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="income">Annual Income*</label>
          <input 
            type="number" 
            id="income" 
            v-model="borrower.employment_info.income" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
        
        <div class="form-group">
          <label for="yearsEmployed">Years Employed*</label>
          <input 
            type="number" 
            id="yearsEmployed" 
            v-model="borrower.employment_info.years_employed" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
      </div>
      
      <h4>Financial Information</h4>
      <div class="form-row">
        <div class="form-group">
          <label for="assets">Total Assets</label>
          <input 
            type="number" 
            id="assets" 
            v-model="borrower.financial_info.assets" 
            class="form-control"
            @input="validateForm"
          />
        </div>
        
        <div class="form-group">
          <label for="liabilities">Total Liabilities</label>
          <input 
            type="number" 
            id="liabilities" 
            v-model="borrower.financial_info.liabilities" 
            class="form-control"
            @input="validateForm"
          />
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="expenses">Monthly Expenses</label>
          <input 
            type="number" 
            id="expenses" 
            v-model="borrower.financial_info.expenses" 
            class="form-control"
            @input="validateForm"
          />
        </div>
      </div>
      
      <h4>Bank Account Information</h4>
      <div class="form-row">
        <div class="form-group">
          <label for="bankName">Bank Name*</label>
          <input 
            type="text" 
            id="bankName" 
            v-model="borrower.bank_info.bank_name" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
        
        <div class="form-group">
          <label for="accountNumber">Account Number*</label>
          <input 
            type="text" 
            id="accountNumber" 
            v-model="borrower.bank_info.account_number" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="bsb">BSB*</label>
          <input 
            type="text" 
            id="bsb" 
            v-model="borrower.bank_info.bsb" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
        
        <div class="form-group">
          <label for="accountName">Account Name*</label>
          <input 
            type="text" 
            id="accountName" 
            v-model="borrower.bank_info.account_name" 
            class="form-control"
            required
            @input="validateForm"
          />
        </div>
      </div>
      
      <hr class="borrower-divider" v-if="index < localFormData.borrowers.length - 1" />
    </div>
    
    <div class="add-borrower">
      <button @click="addBorrower" class="btn btn-secondary">
        Add Another Borrower
      </button>
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
  borrowers: []
});

// Initialize borrower template with all required fields
const borrowerTemplate = {
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  dob: '',
  tax_id: '',
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
};

// Initialize the local form data from props
onMounted(() => {
  if (props.formData.borrowers && props.formData.borrowers.length > 0) {
    // Deep copy the borrowers array
    localFormData.borrowers = JSON.parse(JSON.stringify(props.formData.borrowers));
    
    // Ensure all borrowers have the complete structure
    localFormData.borrowers.forEach(borrower => {
      // Initialize any missing nested objects
      if (!borrower.address) borrower.address = { street: '', city: '', state: '', postal_code: '', country: '' };
      if (!borrower.employment_info) borrower.employment_info = { employer: '', position: '', income: '', years_employed: '' };
      if (!borrower.financial_info) borrower.financial_info = { assets: '', liabilities: '', expenses: '' };
      if (!borrower.bank_info) borrower.bank_info = { bank_name: '', account_number: '', bsb: '', account_name: '' };
    });
  } else {
    // Initialize with one empty borrower if none exist
    localFormData.borrowers = [JSON.parse(JSON.stringify(borrowerTemplate))];
  }
  
  validateForm();
});

// Watch for changes in the local form data and emit updates
watch(localFormData, (newValue) => {
  emit('update:formData', { borrowers: newValue.borrowers });
}, { deep: true });

// Add a new borrower
function addBorrower() {
  localFormData.borrowers.push(JSON.parse(JSON.stringify(borrowerTemplate)));
  validateForm();
}

// Remove a borrower
function removeBorrower(index) {
  localFormData.borrowers.splice(index, 1);
  validateForm();
}

// Validate the form
function validateForm() {
  let isValid = true;
  
  // Check if at least one borrower exists
  if (localFormData.borrowers.length === 0) {
    isValid = false;
  } else {
    // Check required fields for each borrower
    for (const borrower of localFormData.borrowers) {
      if (!borrower.first_name || !borrower.last_name || !borrower.email || !borrower.phone || !borrower.dob ||
          !borrower.address.street || !borrower.address.city || !borrower.address.state || 
          !borrower.address.postal_code || !borrower.address.country ||
          !borrower.employment_info.employer || !borrower.employment_info.position || 
          !borrower.employment_info.income || !borrower.employment_info.years_employed ||
          !borrower.bank_info.bank_name || !borrower.bank_info.account_number || 
          !borrower.bank_info.bsb || !borrower.bank_info.account_name) {
        isValid = false;
        break;
      }
      
      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(borrower.email)) {
        isValid = false;
        break;
      }
    }
  }
  
  emit('validate', isValid);
}
</script>

<style scoped>
.borrower-info-step {
  padding: 1rem 0;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #2d3748;
}

.borrower-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: #f7fafc;
  border-radius: 8px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
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

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #cbd5e0;
  border-radius: 4px;
  font-size: 1rem;
}

h4 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #4a5568;
}

.borrower-divider {
  margin: 2rem 0;
  border: 0;
  border-top: 1px solid #e2e8f0;
}

.add-borrower {
  margin-top: 1.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary {
  background-color: #a0aec0;
  color: white;
  border: none;
}

.btn-secondary:hover {
  background-color: #718096;
}

.btn-danger {
  background-color: #e53e3e;
  color: white;
  border: none;
}

.btn-danger:hover {
  background-color: #c53030;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>
