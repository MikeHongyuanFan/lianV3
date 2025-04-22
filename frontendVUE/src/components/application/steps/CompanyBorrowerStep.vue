<template>
  <div class="step-container">
    <h2 class="step-title">Company Borrower Information</h2>
    <p class="step-description">Enter details about the company borrower(s) for this loan application.</p>
    
    <div v-if="localFormData.company_borrowers.length === 0" class="empty-state">
      <p>No company borrowers added yet.</p>
      <button @click="addCompanyBorrower" class="btn btn-primary">Add Company Borrower</button>
    </div>
    
    <div v-else>
      <div v-for="(company, index) in localFormData.company_borrowers" :key="index" class="company-borrower-card">
        <div class="card-header">
          <h3>Company Borrower {{ index + 1 }}</h3>
          <button v-if="localFormData.company_borrowers.length > 1" @click="removeCompanyBorrower(index)" class="btn btn-danger btn-sm">
            Remove
          </button>
        </div>
        
        <div class="form-grid">
          <div class="form-group">
            <label :for="`company_name_${index}`">Company Name</label>
            <input 
              type="text" 
              :id="`company_name_${index}`" 
              v-model="company.company_name"
              @input="validateAndEmit"
              placeholder="Company Name"
              class="form-control"
            />
            <span v-if="errors[index]?.company_name" class="error-message">{{ errors[index].company_name }}</span>
          </div>
          
          <div class="form-group">
            <label :for="`abn_${index}`">ABN</label>
            <input 
              type="text" 
              :id="`abn_${index}`" 
              v-model="company.abn"
              @input="validateAndEmit"
              placeholder="Australian Business Number"
              class="form-control"
            />
            <span v-if="errors[index]?.abn" class="error-message">{{ errors[index].abn }}</span>
          </div>
          
          <div class="form-group">
            <label :for="`acn_${index}`">ACN</label>
            <input 
              type="text" 
              :id="`acn_${index}`" 
              v-model="company.acn"
              @input="validateAndEmit"
              placeholder="Australian Company Number"
              class="form-control"
            />
            <span v-if="errors[index]?.acn" class="error-message">{{ errors[index].acn }}</span>
          </div>
          
          <div class="form-group">
            <label :for="`business_type_${index}`">Business Type</label>
            <select 
              :id="`business_type_${index}`" 
              v-model="company.business_type"
              @change="validateAndEmit"
              class="form-control"
            >
              <option value="">Select Business Type</option>
              <option value="sole_proprietorship">Sole Proprietorship</option>
              <option value="partnership">Partnership</option>
              <option value="pty_ltd">Proprietary Limited (Pty Ltd)</option>
              <option value="public_company">Public Company</option>
              <option value="trust">Trust</option>
              <option value="non_profit">Non-Profit Organization</option>
            </select>
            <span v-if="errors[index]?.business_type" class="error-message">{{ errors[index].business_type }}</span>
          </div>
          
          <div class="form-group">
            <label :for="`years_in_business_${index}`">Years in Business</label>
            <input 
              type="number" 
              :id="`years_in_business_${index}`" 
              v-model="company.years_in_business"
              @input="validateAndEmit"
              min="0"
              step="0.5"
              class="form-control"
            />
            <span v-if="errors[index]?.years_in_business" class="error-message">{{ errors[index].years_in_business }}</span>
          </div>
          
          <div class="form-group">
            <label :for="`industry_${index}`">Industry</label>
            <input 
              type="text" 
              :id="`industry_${index}`" 
              v-model="company.industry"
              @input="validateAndEmit"
              placeholder="e.g., Construction, Retail, Healthcare"
              class="form-control"
            />
            <span v-if="errors[index]?.industry" class="error-message">{{ errors[index].industry }}</span>
          </div>
        </div>
        
        <h4 class="section-title">Registered Address</h4>
        <div class="form-grid">
          <div class="form-group">
            <label :for="`street_${index}`">Street Address</label>
            <input 
              type="text" 
              :id="`street_${index}`" 
              v-model="company.registered_address.street"
              @input="validateAndEmit"
              placeholder="Street Address"
              class="form-control"
            />
            <span v-if="errors[index]?.registered_address?.street" class="error-message">{{ errors[index].registered_address.street }}</span>
          </div>
          
          <div class="form-group">
            <label :for="`city_${index}`">City</label>
            <input 
              type="text" 
              :id="`city_${index}`" 
              v-model="company.registered_address.city"
              @input="validateAndEmit"
              placeholder="City"
              class="form-control"
            />
            <span v-if="errors[index]?.registered_address?.city" class="error-message">{{ errors[index].registered_address.city }}</span>
          </div>
          
          <div class="form-group">
            <label :for="`state_${index}`">State</label>
            <input 
              type="text" 
              :id="`state_${index}`" 
              v-model="company.registered_address.state"
              @input="validateAndEmit"
              placeholder="State"
              class="form-control"
            />
            <span v-if="errors[index]?.registered_address?.state" class="error-message">{{ errors[index].registered_address.state }}</span>
          </div>
          
          <div class="form-group">
            <label :for="`postal_code_${index}`">Postal Code</label>
            <input 
              type="text" 
              :id="`postal_code_${index}`" 
              v-model="company.registered_address.postal_code"
              @input="validateAndEmit"
              placeholder="Postal Code"
              class="form-control"
            />
            <span v-if="errors[index]?.registered_address?.postal_code" class="error-message">{{ errors[index].registered_address.postal_code }}</span>
          </div>
          
          <div class="form-group">
            <label :for="`country_${index}`">Country</label>
            <input 
              type="text" 
              :id="`country_${index}`" 
              v-model="company.registered_address.country"
              @input="validateAndEmit"
              placeholder="Country"
              class="form-control"
            />
            <span v-if="errors[index]?.registered_address?.country" class="error-message">{{ errors[index].registered_address.country }}</span>
          </div>
        </div>
        
        <h4 class="section-title">Financial Information</h4>
        <div class="form-grid">
          <div class="form-group">
            <label :for="`annual_revenue_${index}`">Annual Revenue ($)</label>
            <input 
              type="number" 
              :id="`annual_revenue_${index}`" 
              v-model="company.financial_info.annual_revenue"
              @input="validateAndEmit"
              min="0"
              step="1000"
              class="form-control"
            />
            <span v-if="errors[index]?.financial_info?.annual_revenue" class="error-message">{{ errors[index].financial_info.annual_revenue }}</span>
          </div>
          
          <div class="form-group">
            <label :for="`net_profit_${index}`">Net Profit ($)</label>
            <input 
              type="number" 
              :id="`net_profit_${index}`" 
              v-model="company.financial_info.net_profit"
              @input="validateAndEmit"
              step="1000"
              class="form-control"
            />
            <span v-if="errors[index]?.financial_info?.net_profit" class="error-message">{{ errors[index].financial_info.net_profit }}</span>
          </div>
          
          <div class="form-group">
            <label :for="`assets_${index}`">Total Assets ($)</label>
            <input 
              type="number" 
              :id="`assets_${index}`" 
              v-model="company.financial_info.assets"
              @input="validateAndEmit"
              min="0"
              step="1000"
              class="form-control"
            />
            <span v-if="errors[index]?.financial_info?.assets" class="error-message">{{ errors[index].financial_info.assets }}</span>
          </div>
          
          <div class="form-group">
            <label :for="`liabilities_${index}`">Total Liabilities ($)</label>
            <input 
              type="number" 
              :id="`liabilities_${index}`" 
              v-model="company.financial_info.liabilities"
              @input="validateAndEmit"
              min="0"
              step="1000"
              class="form-control"
            />
            <span v-if="errors[index]?.financial_info?.liabilities" class="error-message">{{ errors[index].financial_info.liabilities }}</span>
          </div>
        </div>
        
        <h4 class="section-title">Directors</h4>
        <div v-if="company.directors.length === 0" class="empty-state">
          <p>No directors added yet.</p>
        </div>
        
        <div v-else class="directors-list">
          <div v-for="(director, dirIndex) in company.directors" :key="dirIndex" class="director-item">
            <div class="director-name">{{ director.first_name }} {{ director.last_name }}</div>
            <button @click="removeDirector(index, dirIndex)" class="btn btn-danger btn-sm">Remove</button>
          </div>
        </div>
        
        <div class="add-director-form">
          <div class="form-grid">
            <div class="form-group">
              <label :for="`director_first_name_${index}`">First Name</label>
              <input 
                type="text" 
                :id="`director_first_name_${index}`" 
                v-model="newDirector.first_name"
                placeholder="First Name"
                class="form-control"
              />
            </div>
            
            <div class="form-group">
              <label :for="`director_last_name_${index}`">Last Name</label>
              <input 
                type="text" 
                :id="`director_last_name_${index}`" 
                v-model="newDirector.last_name"
                placeholder="Last Name"
                class="form-control"
              />
            </div>
            
            <div class="form-group">
              <label :for="`director_email_${index}`">Email</label>
              <input 
                type="email" 
                :id="`director_email_${index}`" 
                v-model="newDirector.email"
                placeholder="Email"
                class="form-control"
              />
            </div>
            
            <div class="form-group">
              <label :for="`director_phone_${index}`">Phone</label>
              <input 
                type="tel" 
                :id="`director_phone_${index}`" 
                v-model="newDirector.phone"
                placeholder="Phone"
                class="form-control"
              />
            </div>
          </div>
          
          <button @click="addDirector(index)" class="btn btn-secondary">Add Director</button>
        </div>
      </div>
      
      <div class="form-actions">
        <button @click="addCompanyBorrower" class="btn btn-primary">Add Another Company Borrower</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';

const props = defineProps({
  formData: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['update:formData', 'validate']);

// Local copy of form data
const localFormData = reactive({
  company_borrowers: []
});

// Initialize with empty company borrower if none exists
if (!props.formData.company_borrowers || props.formData.company_borrowers.length === 0) {
  localFormData.company_borrowers = [{
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
  }];
} else {
  // Deep copy the company borrowers from props
  localFormData.company_borrowers = JSON.parse(JSON.stringify(props.formData.company_borrowers));
}

// Form validation
const errors = ref([]);

// New director form
const newDirector = reactive({
  first_name: '',
  last_name: '',
  email: '',
  phone: ''
});

// Watch for parent form data changes
watch(() => props.formData.company_borrowers, (newVal) => {
  if (newVal && newVal.length > 0) {
    localFormData.company_borrowers = JSON.parse(JSON.stringify(newVal));
  }
}, { deep: true });

// Add a new company borrower
function addCompanyBorrower() {
  localFormData.company_borrowers.push({
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
  });
  
  validateAndEmit();
}

// Remove a company borrower
function removeCompanyBorrower(index) {
  localFormData.company_borrowers.splice(index, 1);
  validateAndEmit();
}

// Add a director to a company
function addDirector(companyIndex) {
  if (!newDirector.first_name || !newDirector.last_name) {
    return; // Don't add empty directors
  }
  
  localFormData.company_borrowers[companyIndex].directors.push({
    first_name: newDirector.first_name,
    last_name: newDirector.last_name,
    email: newDirector.email,
    phone: newDirector.phone
  });
  
  // Reset the new director form
  newDirector.first_name = '';
  newDirector.last_name = '';
  newDirector.email = '';
  newDirector.phone = '';
  
  validateAndEmit();
}

// Remove a director from a company
function removeDirector(companyIndex, directorIndex) {
  localFormData.company_borrowers[companyIndex].directors.splice(directorIndex, 1);
  validateAndEmit();
}

// Validate form and emit changes
function validateAndEmit() {
  validateForm();
  
  emit('update:formData', {
    ...props.formData,
    company_borrowers: localFormData.company_borrowers
  });
  
  emit('validate', isFormValid.value);
}

function validateForm() {
  // Reset errors
  errors.value = [];
  
  // Validate each company borrower
  localFormData.company_borrowers.forEach((company, index) => {
    const companyErrors = {};
    
    // Company name validation
    if (!company.company_name) {
      companyErrors.company_name = 'Company name is required';
    }
    
    // ABN validation
    if (!company.abn) {
      companyErrors.abn = 'ABN is required';
    } else if (!/^\d{11}$/.test(company.abn.replace(/\s/g, ''))) {
      companyErrors.abn = 'ABN must be 11 digits';
    }
    
    // ACN validation
    if (!company.acn) {
      companyErrors.acn = 'ACN is required';
    } else if (!/^\d{9}$/.test(company.acn.replace(/\s/g, ''))) {
      companyErrors.acn = 'ACN must be 9 digits';
    }
    
    // Business type validation
    if (!company.business_type) {
      companyErrors.business_type = 'Business type is required';
    }
    
    // Years in business validation
    if (!company.years_in_business) {
      companyErrors.years_in_business = 'Years in business is required';
    } else if (isNaN(company.years_in_business) || company.years_in_business < 0) {
      companyErrors.years_in_business = 'Years in business must be a positive number';
    }
    
    // Industry validation
    if (!company.industry) {
      companyErrors.industry = 'Industry is required';
    }
    
    // Registered address validation
    const addressErrors = {};
    if (!company.registered_address.street) {
      addressErrors.street = 'Street address is required';
    }
    if (!company.registered_address.city) {
      addressErrors.city = 'City is required';
    }
    if (!company.registered_address.state) {
      addressErrors.state = 'State is required';
    }
    if (!company.registered_address.postal_code) {
      addressErrors.postal_code = 'Postal code is required';
    }
    if (!company.registered_address.country) {
      addressErrors.country = 'Country is required';
    }
    
    if (Object.keys(addressErrors).length > 0) {
      companyErrors.registered_address = addressErrors;
    }
    
    // Financial info validation
    const financialErrors = {};
    if (!company.financial_info.annual_revenue) {
      financialErrors.annual_revenue = 'Annual revenue is required';
    }
    if (!company.financial_info.net_profit) {
      financialErrors.net_profit = 'Net profit is required';
    }
    if (!company.financial_info.assets) {
      financialErrors.assets = 'Total assets is required';
    }
    if (!company.financial_info.liabilities) {
      financialErrors.liabilities = 'Total liabilities is required';
    }
    
    if (Object.keys(financialErrors).length > 0) {
      companyErrors.financial_info = financialErrors;
    }
    
    // Add errors for this company if any
    if (Object.keys(companyErrors).length > 0) {
      errors.value[index] = companyErrors;
    }
  });
}

const isFormValid = computed(() => {
  return errors.value.length === 0 || errors.value.every(error => !error);
});

onMounted(() => {
  validateAndEmit();
});
</script>

<style scoped>
.step-container {
  width: 100%;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2d3748;
}

.step-description {
  color: #718096;
  margin-bottom: 2rem;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  background-color: #f7fafc;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.company-borrower-card {
  background-color: #f7fafc;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.card-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 1.5rem 0 1rem;
  color: #4a5568;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #4a5568;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
}

.error-message {
  display: block;
  color: #e53e3e;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.directors-list {
  margin-bottom: 1.5rem;
}

.director-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background-color: #edf2f7;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.add-director-form {
  background-color: #edf2f7;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-actions {
  margin-top: 2rem;
  text-align: center;
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

.btn-danger {
  background-color: #e53e3e;
  color: white;
}

.btn-danger:hover {
  background-color: #c53030;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}
</style>
