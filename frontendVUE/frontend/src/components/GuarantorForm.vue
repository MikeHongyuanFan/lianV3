<template>
  <div class="guarantor-form">
    <form @submit.prevent="submitForm">
      <!-- Guarantor Type Selection -->
      <div class="form-group">
        <label for="guarantor_type">Guarantor Type *</label>
        <select
          id="guarantor_type"
          v-model="guarantorData.guarantor_type"
          :class="{ 'error': errors.guarantor_type }"
          required
          @change="handleGuarantorTypeChange"
        >
          <option value="">Select Guarantor Type</option>
          <option value="individual">Individual</option>
          <option value="company">Company</option>
        </select>
        <div v-if="errors.guarantor_type" class="error-message">{{ errors.guarantor_type }}</div>
      </div>
      
      <!-- Individual Guarantor Fields -->
      <div v-if="guarantorData.guarantor_type === 'individual' || !guarantorData.guarantor_type">
        <div class="form-group">
          <label for="first_name">First Name *</label>
          <BaseInput
            id="first_name"
            v-model="guarantorData.first_name"
            :error="errors.first_name"
            :required="guarantorData.guarantor_type === 'individual'"
          />
        </div>
        
        <div class="form-group">
          <label for="last_name">Last Name *</label>
          <BaseInput
            id="last_name"
            v-model="guarantorData.last_name"
            :error="errors.last_name"
            :required="guarantorData.guarantor_type === 'individual'"
          />
        </div>
        
        <div class="form-group">
          <label for="date_of_birth">Date of Birth</label>
          <BaseInput
            id="date_of_birth"
            v-model="guarantorData.date_of_birth"
            type="date"
            :error="errors.date_of_birth"
          />
        </div>
      </div>
      
      <!-- Company Guarantor Fields -->
      <div v-if="guarantorData.guarantor_type === 'company'">
        <div class="form-group">
          <label for="company_name">Company Name *</label>
          <BaseInput
            id="company_name"
            v-model="guarantorData.company_name"
            :error="errors.company_name"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="company_abn">Company ABN</label>
          <BaseInput
            id="company_abn"
            v-model="guarantorData.company_abn"
            :error="errors.company_abn"
          />
        </div>
        
        <div class="form-group">
          <label for="company_acn">Company ACN</label>
          <BaseInput
            id="company_acn"
            v-model="guarantorData.company_acn"
            :error="errors.company_acn"
          />
        </div>
      </div>
      
      <!-- Common Fields for Both Types -->
      <div class="form-group">
        <label for="email">Email *</label>
        <BaseInput
          id="email"
          v-model="guarantorData.email"
          type="email"
          :error="errors.email"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="phone_number">Phone Number *</label>
        <BaseInput
          id="phone_number"
          v-model="guarantorData.phone_number"
          :error="errors.phone_number"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="address">Address *</label>
        <BaseInput
          id="address"
          v-model="guarantorData.address"
          :error="errors.address"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="relationship_to_borrower">Relationship to Borrower *</label>
        <select
          id="relationship_to_borrower"
          v-model="guarantorData.relationship_to_borrower"
          :class="{ 'error': errors.relationship_to_borrower }"
          required
        >
          <option value="">Select Relationship</option>
          <option value="spouse">Spouse</option>
          <option value="parent">Parent</option>
          <option value="child">Child</option>
          <option value="sibling">Sibling</option>
          <option value="business_partner">Business Partner</option>
          <option value="friend">Friend</option>
          <option value="other">Other</option>
        </select>
        <div v-if="errors.relationship_to_borrower" class="error-message">{{ errors.relationship_to_borrower }}</div>
      </div>
      
      <div class="form-group" v-if="guarantorData.guarantor_type === 'individual'">
        <label for="employment_status">Employment Status</label>
        <select
          id="employment_status"
          v-model="guarantorData.employment_status"
          :class="{ 'error': errors.employment_status }"
        >
          <option value="">Select Employment Status</option>
          <option value="full_time">Full Time</option>
          <option value="part_time">Part Time</option>
          <option value="self_employed">Self Employed</option>
          <option value="unemployed">Unemployed</option>
          <option value="retired">Retired</option>
        </select>
        <div v-if="errors.employment_status" class="error-message">{{ errors.employment_status }}</div>
      </div>
      
      <div class="form-group" v-if="guarantorData.guarantor_type === 'individual'">
        <label for="annual_income">Annual Income</label>
        <BaseInput
          id="annual_income"
          v-model="guarantorData.annual_income"
          type="number"
          step="0.01"
          :error="errors.annual_income"
        />
      </div>
      
      <div class="form-group" v-if="guarantorData.guarantor_type === 'individual'">
        <label for="credit_score">Credit Score</label>
        <BaseInput
          id="credit_score"
          v-model="guarantorData.credit_score"
          type="number"
          :error="errors.credit_score"
        />
      </div>
      
      <div class="form-actions">
        <BaseButton type="button" @click="$emit('cancel')" variant="secondary">Cancel</BaseButton>
        <BaseButton type="submit" variant="primary" :loading="loading">{{ submitButtonText }}</BaseButton>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import BaseInput from '@/components/BaseInput.vue'
import BaseButton from '@/components/BaseButton.vue'

export default {
  name: 'GuarantorForm',
  components: {
    BaseInput,
    BaseButton
  },
  props: {
    guarantor: {
      type: Object,
      default: () => ({})
    },
    loading: {
      type: Boolean,
      default: false
    },
    mode: {
      type: String,
      default: 'create',
      validator: (value) => ['create', 'edit'].includes(value)
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const guarantorData = reactive({
      guarantor_type: 'individual', // Default to individual
      first_name: '',
      last_name: '',
      email: '',
      phone_number: '',
      address: '',
      relationship_to_borrower: '',
      date_of_birth: '',
      employment_status: '',
      annual_income: '',
      credit_score: '',
      company_name: '',
      company_abn: '',
      company_acn: ''
    })
    
    const errors = ref({})
    
    const submitButtonText = computed(() => {
      return props.mode === 'create' ? 'Create Guarantor' : 'Update Guarantor'
    })
    
    const handleGuarantorTypeChange = () => {
      // Clear validation errors when type changes
      errors.value = {}
      
      // Reset fields based on guarantor type
      if (guarantorData.guarantor_type === 'individual') {
        guarantorData.company_name = ''
        guarantorData.company_abn = ''
        guarantorData.company_acn = ''
      } else if (guarantorData.guarantor_type === 'company') {
        guarantorData.first_name = ''
        guarantorData.last_name = ''
        guarantorData.date_of_birth = ''
        guarantorData.employment_status = ''
        guarantorData.annual_income = ''
        guarantorData.credit_score = ''
      }
    }
    
    const validateForm = () => {
      const newErrors = {}
      
      // Validate guarantor type
      if (!guarantorData.guarantor_type) {
        newErrors.guarantor_type = 'Guarantor type is required'
      }
      
      // Validate based on guarantor type
      if (guarantorData.guarantor_type === 'individual') {
        if (!guarantorData.first_name) {
          newErrors.first_name = 'First name is required'
        }
        
        if (!guarantorData.last_name) {
          newErrors.last_name = 'Last name is required'
        }
        
        if (guarantorData.date_of_birth && !/^\d{4}-\d{2}-\d{2}$/.test(guarantorData.date_of_birth)) {
          newErrors.date_of_birth = 'Please enter a valid date in YYYY-MM-DD format'
        }
      } else if (guarantorData.guarantor_type === 'company') {
        if (!guarantorData.company_name) {
          newErrors.company_name = 'Company name is required'
        }
        
        if (guarantorData.company_abn && !/^\d{11}$/.test(guarantorData.company_abn)) {
          newErrors.company_abn = 'ABN must be 11 digits'
        }
        
        if (guarantorData.company_acn && !/^\d{9}$/.test(guarantorData.company_acn)) {
          newErrors.company_acn = 'ACN must be 9 digits'
        }
      }
      
      // Common validations
      if (!guarantorData.email) {
        newErrors.email = 'Email is required'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(guarantorData.email)) {
        newErrors.email = 'Please enter a valid email address'
      }
      
      if (!guarantorData.phone_number) {
        newErrors.phone_number = 'Phone number is required'
      }
      
      if (!guarantorData.address) {
        newErrors.address = 'Address is required'
      }
      
      if (!guarantorData.relationship_to_borrower) {
        newErrors.relationship_to_borrower = 'Relationship to borrower is required'
      }
      
      if (guarantorData.annual_income && isNaN(parseFloat(guarantorData.annual_income))) {
        newErrors.annual_income = 'Annual income must be a number'
      }
      
      if (guarantorData.credit_score && isNaN(parseInt(guarantorData.credit_score))) {
        newErrors.credit_score = 'Credit score must be a number'
      }
      
      errors.value = newErrors
      return Object.keys(newErrors).length === 0
    }
    
    const submitForm = () => {
      if (validateForm()) {
        const formData = { ...guarantorData }
        
        // Convert numeric fields to appropriate types
        if (formData.annual_income) {
          formData.annual_income = parseFloat(formData.annual_income)
        }
        
        if (formData.credit_score) {
          formData.credit_score = parseInt(formData.credit_score)
        }
        
        // Map phone_number to phone for API compatibility
        formData.phone = formData.phone_number
        
        emit('submit', formData)
      }
    }
    
    onMounted(() => {
      // If editing an existing guarantor, populate the form
      if (props.mode === 'edit' && props.guarantor) {
        // Determine guarantor type
        if (props.guarantor.company_name) {
          guarantorData.guarantor_type = 'company'
        } else {
          guarantorData.guarantor_type = 'individual'
        }
        
        // Populate all fields
        Object.keys(guarantorData).forEach(key => {
          if (props.guarantor[key] !== undefined) {
            guarantorData[key] = props.guarantor[key]
          }
        })
        
        // Handle phone field mapping (API uses 'phone', frontend uses 'phone_number')
        if (props.guarantor.phone) {
          guarantorData.phone_number = props.guarantor.phone
        }
      }
    })
    
    return {
      guarantorData,
      errors,
      submitButtonText,
      handleGuarantorTypeChange,
      submitForm
    }
  }
}
</script>

<style scoped>
.guarantor-form {
  max-width: 600px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: white;
}

.form-group select.error {
  border-color: #ef4444;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}
</style>
