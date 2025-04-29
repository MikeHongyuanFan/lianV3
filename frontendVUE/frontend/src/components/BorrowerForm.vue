<template>
  <div class="borrower-form">
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="first_name">First Name *</label>
        <BaseInput
          id="first_name"
          v-model="borrowerData.first_name"
          :error="errors.first_name"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="last_name">Last Name *</label>
        <BaseInput
          id="last_name"
          v-model="borrowerData.last_name"
          :error="errors.last_name"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="email">Email *</label>
        <BaseInput
          id="email"
          v-model="borrowerData.email"
          type="email"
          :error="errors.email"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="phone_number">Phone Number *</label>
        <BaseInput
          id="phone_number"
          v-model="borrowerData.phone_number"
          :error="errors.phone_number"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="address">Address *</label>
        <BaseInput
          id="address"
          v-model="borrowerData.address"
          :error="errors.address"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="borrower_type">Borrower Type *</label>
        <select
          id="borrower_type"
          v-model="borrowerData.borrower_type"
          :class="{ 'error': errors.borrower_type }"
          required
        >
          <option value="">Select Borrower Type</option>
          <option value="individual">Individual</option>
          <option value="company">Company</option>
          <option value="trust">Trust</option>
        </select>
        <div v-if="errors.borrower_type" class="error-message">{{ errors.borrower_type }}</div>
      </div>
      
      <div class="form-group">
        <label for="date_of_birth">Date of Birth</label>
        <BaseInput
          id="date_of_birth"
          v-model="borrowerData.date_of_birth"
          type="date"
          :error="errors.date_of_birth"
        />
      </div>
      
      <div class="form-group">
        <label for="employment_status">Employment Status</label>
        <select
          id="employment_status"
          v-model="borrowerData.employment_status"
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
      
      <div class="form-group">
        <label for="annual_income">Annual Income</label>
        <BaseInput
          id="annual_income"
          v-model="borrowerData.annual_income"
          type="number"
          step="0.01"
          :error="errors.annual_income"
        />
      </div>
      
      <div class="form-group">
        <label for="credit_score">Credit Score</label>
        <BaseInput
          id="credit_score"
          v-model="borrowerData.credit_score"
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
  name: 'BorrowerForm',
  components: {
    BaseInput,
    BaseButton
  },
  props: {
    borrower: {
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
    const borrowerData = reactive({
      first_name: '',
      last_name: '',
      email: '',
      phone_number: '',
      address: '',
      borrower_type: '',
      date_of_birth: '',
      employment_status: '',
      annual_income: '',
      credit_score: ''
    })
    
    const errors = ref({})
    
    const submitButtonText = computed(() => {
      return props.mode === 'create' ? 'Create Borrower' : 'Update Borrower'
    })
    
    const validateForm = () => {
      const newErrors = {}
      
      if (!borrowerData.first_name) {
        newErrors.first_name = 'First name is required'
      }
      
      if (!borrowerData.last_name) {
        newErrors.last_name = 'Last name is required'
      }
      
      if (!borrowerData.email) {
        newErrors.email = 'Email is required'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(borrowerData.email)) {
        newErrors.email = 'Please enter a valid email address'
      }
      
      if (!borrowerData.phone_number) {
        newErrors.phone_number = 'Phone number is required'
      }
      
      if (!borrowerData.address) {
        newErrors.address = 'Address is required'
      }
      
      if (!borrowerData.borrower_type) {
        newErrors.borrower_type = 'Borrower type is required'
      }
      
      if (borrowerData.date_of_birth && !/^\d{4}-\d{2}-\d{2}$/.test(borrowerData.date_of_birth)) {
        newErrors.date_of_birth = 'Please enter a valid date in YYYY-MM-DD format'
      }
      
      if (borrowerData.annual_income && isNaN(parseFloat(borrowerData.annual_income))) {
        newErrors.annual_income = 'Annual income must be a number'
      }
      
      if (borrowerData.credit_score && isNaN(parseInt(borrowerData.credit_score))) {
        newErrors.credit_score = 'Credit score must be a number'
      }
      
      errors.value = newErrors
      return Object.keys(newErrors).length === 0
    }
    
    const submitForm = () => {
      if (validateForm()) {
        const formData = { ...borrowerData }
        
        // Convert numeric fields to appropriate types
        if (formData.annual_income) {
          formData.annual_income = parseFloat(formData.annual_income)
        }
        
        if (formData.credit_score) {
          formData.credit_score = parseInt(formData.credit_score)
        }
        
        emit('submit', formData)
      }
    }
    
    onMounted(() => {
      // If editing an existing borrower, populate the form
      if (props.mode === 'edit' && props.borrower) {
        Object.keys(borrowerData).forEach(key => {
          if (props.borrower[key] !== undefined) {
            borrowerData[key] = props.borrower[key]
          }
        })
      }
    })
    
    return {
      borrowerData,
      errors,
      submitButtonText,
      submitForm
    }
  }
}
</script>

<style scoped>
.borrower-form {
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
