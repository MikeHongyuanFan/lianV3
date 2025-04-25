<template>
  <div class="step-container">
    <h2 class="step-title">Application Details</h2>
    <p class="step-description">Enter the basic information about this loan application.</p>
    
    <div class="form-grid">
      <div class="form-group">
        <label for="reference_number">Reference Number</label>
        <input 
          type="text" 
          id="reference_number" 
          v-model="localFormData.reference_number"
          @input="validateAndEmit"
          placeholder="e.g., APP-2025-0001"
          class="form-control"
        />
        <span v-if="errors.reference_number" class="error-message">{{ errors.reference_number }}</span>
      </div>
      
      <div class="form-group">
        <label for="application_type">Application Type</label>
        <select 
          id="application_type" 
          v-model="localFormData.application_type"
          @change="validateAndEmit"
          class="form-control"
        >
          <option value="">Select Application Type</option>
          <option value="residential">Residential</option>
          <option value="commercial">Commercial</option>
          <option value="construction">Construction</option>
          <option value="refinance">Refinance</option>
          <option value="investment">Investment</option>
        </select>
        <span v-if="errors.application_type" class="error-message">{{ errors.application_type }}</span>
      </div>
      
      <div class="form-group">
        <label for="product_id">Loan Product</label>
        <select 
          id="product_id" 
          v-model="localFormData.product_id"
          @change="validateAndEmit"
          class="form-control"
        >
          <option value="">Select Loan Product</option>
          <option v-for="product in products" :key="product.id" :value="product.id">
            {{ product.name }}
          </option>
        </select>
        <span v-if="errors.product_id" class="error-message">{{ errors.product_id }}</span>
      </div>
      
      <div class="form-group">
        <label for="branch_id">Branch</label>
        <select 
          id="branch_id" 
          v-model="localFormData.branch_id"
          @change="validateAndEmit"
          class="form-control"
        >
          <option value="">Select Branch</option>
          <option v-for="branch in branches" :key="branch.id" :value="branch.id">
            {{ branch.name }}
          </option>
        </select>
        <span v-if="errors.branch_id" class="error-message">{{ errors.branch_id }}</span>
      </div>
      
      <div class="form-group">
        <label for="bd_id">Business Development Manager</label>
        <select 
          id="bd_id" 
          v-model="localFormData.bd_id"
          @change="validateAndEmit"
          class="form-control"
        >
          <option value="">Select BDM</option>
          <option v-for="bdm in bdms" :key="bdm.id" :value="bdm.id">
            {{ bdm.name }}
          </option>
        </select>
        <span v-if="errors.bd_id" class="error-message">{{ errors.bd_id }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import axios from 'axios';

const props = defineProps({
  formData: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['update:formData', 'validate']);

// Local copy of form data
const localFormData = reactive({
  reference_number: props.formData.reference_number || '',
  application_type: props.formData.application_type || '',
  product_id: props.formData.product_id || '',
  branch_id: props.formData.branch_id || '',
  bd_id: props.formData.bd_id || ''
});

// Form validation
const errors = reactive({
  reference_number: '',
  application_type: '',
  product_id: '',
  branch_id: '',
  bd_id: ''
});

// Data for dropdowns
const products = ref([]);
const branches = ref([]);
const bdms = ref([]);

// Watch for parent form data changes
watch(() => props.formData, (newVal) => {
  localFormData.reference_number = newVal.reference_number || '';
  localFormData.application_type = newVal.application_type || '';
  localFormData.product_id = newVal.product_id || '';
  localFormData.branch_id = newVal.branch_id || '';
  localFormData.bd_id = newVal.bd_id || '';
}, { deep: true });

// Validate form and emit changes
function validateAndEmit() {
  validateForm();
  
  emit('update:formData', {
    ...props.formData,
    reference_number: localFormData.reference_number,
    application_type: localFormData.application_type,
    product_id: localFormData.product_id,
    branch_id: localFormData.branch_id,
    bd_id: localFormData.bd_id
  });
  
  emit('validate', isFormValid.value);
}

function validateForm() {
  // Reset errors
  errors.reference_number = '';
  errors.application_type = '';
  errors.product_id = '';
  errors.branch_id = '';
  errors.bd_id = '';
  
  // Validate reference number
  if (!localFormData.reference_number) {
    errors.reference_number = 'Reference number is required';
  } else if (!/^[A-Za-z0-9-]+$/.test(localFormData.reference_number)) {
    errors.reference_number = 'Reference number can only contain letters, numbers, and hyphens';
  }
  
  // Validate application type
  if (!localFormData.application_type) {
    errors.application_type = 'Application type is required';
  }
  
  // Validate product
  if (!localFormData.product_id) {
    errors.product_id = 'Loan product is required';
  }
  
  // Validate branch
  if (!localFormData.branch_id) {
    errors.branch_id = 'Branch is required';
  }
  
  // Validate BDM
  if (!localFormData.bd_id) {
    errors.bd_id = 'Business Development Manager is required';
  }
}

const isFormValid = computed(() => {
  return !errors.reference_number && 
         !errors.application_type && 
         !errors.product_id && 
         !errors.branch_id && 
         !errors.bd_id;
});

// Fetch data for dropdowns
async function fetchProducts() {
  try {
    const response = await axios.get('/api/products/');
    products.value = response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    // For demo purposes, add some sample products
    products.value = [
      { id: 1, name: 'Residential Home Loan' },
      { id: 2, name: 'Commercial Property Loan' },
      { id: 3, name: 'Construction Loan' },
      { id: 4, name: 'Investment Property Loan' }
    ];
  }
}

async function fetchBranches() {
  try {
    const response = await axios.get('/api/branches/');
    branches.value = response.data;
  } catch (error) {
    console.error('Error fetching branches:', error);
    // For demo purposes, add some sample branches
    branches.value = [
      { id: 1, name: 'Sydney CBD' },
      { id: 2, name: 'Melbourne CBD' },
      { id: 3, name: 'Brisbane CBD' },
      { id: 4, name: 'Perth CBD' }
    ];
  }
}

async function fetchBDMs() {
  try {
    const response = await axios.get('/api/bdms/');
    bdms.value = response.data;
  } catch (error) {
    console.error('Error fetching BDMs:', error);
    // For demo purposes, add some sample BDMs
    bdms.value = [
      { id: 1, name: 'John Smith' },
      { id: 2, name: 'Jane Doe' },
      { id: 3, name: 'Michael Johnson' },
      { id: 4, name: 'Sarah Williams' }
    ];
  }
}

onMounted(async () => {
  await Promise.all([
    fetchProducts(),
    fetchBranches(),
    fetchBDMs()
  ]);
  
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
</style>
