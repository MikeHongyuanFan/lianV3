<template>
  <div class="guarantor-info-step">
    <h2 class="step-title">Guarantor Information</h2>
    
    <div v-if="localFormData.guarantors.length === 0" class="no-guarantors">
      <p>No guarantors added yet. Do you want to add a guarantor?</p>
      <button @click="addGuarantor" class="btn btn-primary">
        Add Guarantor
      </button>
    </div>
    
    <div v-else>
      <div v-for="(guarantor, index) in localFormData.guarantors" :key="index" class="guarantor-section">
        <div class="section-header">
          <h3>Guarantor {{ index + 1 }}</h3>
          <button 
            @click="removeGuarantor(index)" 
            class="btn btn-danger btn-sm"
          >
            Remove
          </button>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="guarantorType">Guarantor Type*</label>
            <select 
              id="guarantorType" 
              v-model="guarantor.guarantor_type" 
              class="form-control"
              required
              @change="validateForm"
            >
              <option value="individual">Individual</option>
              <option value="company">Company</option>
            </select>
          </div>
        </div>
        
        <!-- Individual Guarantor Fields -->
        <div v-if="guarantor.guarantor_type === 'individual'">
          <div class="form-row">
            <div class="form-group">
              <label for="firstName">First Name*</label>
              <input 
                type="text" 
                id="firstName" 
                v-model="guarantor.first_name" 
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
                v-model="guarantor.last_name" 
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
                v-model="guarantor.email" 
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
                v-model="guarantor.phone" 
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
                v-model="guarantor.dob" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
            
            <div class="form-group">
              <label for="relationship">Relationship to Borrower*</label>
              <input 
                type="text" 
                id="relationship" 
                v-model="guarantor.relationship" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
          </div>
          
          <h4>Address</h4>
          <div class="form-row">
            <div class="form-group">
              <label for="street">Street*</label>
              <input 
                type="text" 
                id="street" 
                v-model="guarantor.address.street" 
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
                v-model="guarantor.address.city" 
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
                v-model="guarantor.address.state" 
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
                v-model="guarantor.address.postal_code" 
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
                v-model="guarantor.address.country" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
          </div>
        </div>
        
        <!-- Company Guarantor Fields -->
        <div v-else-if="guarantor.guarantor_type === 'company'">
          <div class="form-row">
            <div class="form-group">
              <label for="companyName">Company Name*</label>
              <input 
                type="text" 
                id="companyName" 
                v-model="guarantor.company_name" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
            
            <div class="form-group">
              <label for="abn">ABN*</label>
              <input 
                type="text" 
                id="abn" 
                v-model="guarantor.abn" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="acn">ACN</label>
              <input 
                type="text" 
                id="acn" 
                v-model="guarantor.acn" 
                class="form-control"
                @input="validateForm"
              />
            </div>
            
            <div class="form-group">
              <label for="contactPerson">Contact Person*</label>
              <input 
                type="text" 
                id="contactPerson" 
                v-model="guarantor.contact_person" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="contactEmail">Contact Email*</label>
              <input 
                type="email" 
                id="contactEmail" 
                v-model="guarantor.contact_email" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
            
            <div class="form-group">
              <label for="contactPhone">Contact Phone*</label>
              <input 
                type="tel" 
                id="contactPhone" 
                v-model="guarantor.contact_phone" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
          </div>
          
          <h4>Registered Address</h4>
          <div class="form-row">
            <div class="form-group">
              <label for="regStreet">Street*</label>
              <input 
                type="text" 
                id="regStreet" 
                v-model="guarantor.registered_address.street" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
            
            <div class="form-group">
              <label for="regCity">City*</label>
              <input 
                type="text" 
                id="regCity" 
                v-model="guarantor.registered_address.city" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="regState">State*</label>
              <input 
                type="text" 
                id="regState" 
                v-model="guarantor.registered_address.state" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
            
            <div class="form-group">
              <label for="regPostalCode">Postal Code*</label>
              <input 
                type="text" 
                id="regPostalCode" 
                v-model="guarantor.registered_address.postal_code" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
            
            <div class="form-group">
              <label for="regCountry">Country*</label>
              <input 
                type="text" 
                id="regCountry" 
                v-model="guarantor.registered_address.country" 
                class="form-control"
                required
                @input="validateForm"
              />
            </div>
          </div>
        </div>
        
        <hr class="guarantor-divider" v-if="index < localFormData.guarantors.length - 1" />
      </div>
      
      <div class="add-guarantor">
        <button @click="addGuarantor" class="btn btn-secondary">
          Add Another Guarantor
        </button>
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
  guarantors: []
});

// Initialize guarantor templates
const individualGuarantorTemplate = {
  guarantor_type: 'individual',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  dob: '',
  relationship: '',
  address: {
    street: '',
    city: '',
    state: '',
    postal_code: '',
    country: ''
  }
};

const companyGuarantorTemplate = {
  guarantor_type: 'company',
  company_name: '',
  abn: '',
  acn: '',
  contact_person: '',
  contact_email: '',
  contact_phone: '',
  registered_address: {
    street: '',
    city: '',
    state: '',
    postal_code: '',
    country: ''
  }
};

// Initialize the local form data from props
onMounted(() => {
  if (props.formData.guarantors && props.formData.guarantors.length > 0) {
    // Deep copy the guarantors array
    localFormData.guarantors = JSON.parse(JSON.stringify(props.formData.guarantors));
    
    // Ensure all guarantors have the complete structure
    localFormData.guarantors.forEach(guarantor => {
      if (guarantor.guarantor_type === 'individual') {
        // Initialize any missing nested objects for individual guarantor
        if (!guarantor.address) guarantor.address = { street: '', city: '', state: '', postal_code: '', country: '' };
      } else if (guarantor.guarantor_type === 'company') {
        // Initialize any missing nested objects for company guarantor
        if (!guarantor.registered_address) guarantor.registered_address = { street: '', city: '', state: '', postal_code: '', country: '' };
      }
    });
  } else {
    // Initialize with empty guarantors array
    localFormData.guarantors = [];
  }
  
  validateForm();
});

// Watch for changes in the local form data and emit updates
watch(localFormData, (newValue) => {
  emit('update:formData', { guarantors: newValue.guarantors });
}, { deep: true });

// Add a new guarantor
function addGuarantor() {
  localFormData.guarantors.push(JSON.parse(JSON.stringify(individualGuarantorTemplate)));
  validateForm();
}

// Remove a guarantor
function removeGuarantor(index) {
  localFormData.guarantors.splice(index, 1);
  validateForm();
}

// Validate the form
function validateForm() {
  let isValid = true;
  
  // Guarantors are optional, so if there are none, the form is still valid
  if (localFormData.guarantors.length === 0) {
    isValid = true;
  } else {
    // Check required fields for each guarantor
    for (const guarantor of localFormData.guarantors) {
      if (guarantor.guarantor_type === 'individual') {
        if (!guarantor.first_name || !guarantor.last_name || !guarantor.email || !guarantor.phone || 
            !guarantor.dob || !guarantor.relationship ||
            !guarantor.address.street || !guarantor.address.city || !guarantor.address.state || 
            !guarantor.address.postal_code || !guarantor.address.country) {
          isValid = false;
          break;
        }
        
        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(guarantor.email)) {
          isValid = false;
          break;
        }
      } else if (guarantor.guarantor_type === 'company') {
        if (!guarantor.company_name || !guarantor.abn || !guarantor.contact_person || 
            !guarantor.contact_email || !guarantor.contact_phone ||
            !guarantor.registered_address.street || !guarantor.registered_address.city || 
            !guarantor.registered_address.state || !guarantor.registered_address.postal_code || 
            !guarantor.registered_address.country) {
          isValid = false;
          break;
        }
        
        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(guarantor.contact_email)) {
          isValid = false;
          break;
        }
        
        // Validate ABN format (11 digits)
        const abnRegex = /^\d{11}$/;
        if (!abnRegex.test(guarantor.abn.replace(/\s/g, ''))) {
          isValid = false;
          break;
        }
      }
    }
  }
  
  emit('validate', isValid);
}
</script>

<style scoped>
.guarantor-info-step {
  padding: 1rem 0;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #2d3748;
}

.no-guarantors {
  text-align: center;
  padding: 2rem;
  background-color: #f7fafc;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.guarantor-section {
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

.guarantor-divider {
  margin: 2rem 0;
  border: 0;
  border-top: 1px solid #e2e8f0;
}

.add-guarantor {
  margin-top: 1.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #4299e1;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #3182ce;
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
