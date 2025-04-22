<template>
  <div class="step-container">
    <h2 class="step-title">Valuer & Quantity Surveyor Information</h2>
    <p class="step-description">Enter details about the valuer and quantity surveyor for this loan application.</p>
    
    <div class="section-container">
      <h3 class="section-title">Valuer Information</h3>
      <div class="form-grid">
        <div class="form-group">
          <label for="valuer_company_name">Company Name</label>
          <input 
            type="text" 
            id="valuer_company_name" 
            v-model="localFormData.valuer_info.company_name"
            @input="validateAndEmit"
            placeholder="Valuer Company Name"
            class="form-control"
          />
          <span v-if="errors.valuer_company_name" class="error-message">{{ errors.valuer_company_name }}</span>
        </div>
        
        <div class="form-group">
          <label for="valuer_contact_name">Contact Name</label>
          <input 
            type="text" 
            id="valuer_contact_name" 
            v-model="localFormData.valuer_info.contact_name"
            @input="validateAndEmit"
            placeholder="Contact Person"
            class="form-control"
          />
          <span v-if="errors.valuer_contact_name" class="error-message">{{ errors.valuer_contact_name }}</span>
        </div>
        
        <div class="form-group">
          <label for="valuer_phone">Phone</label>
          <input 
            type="tel" 
            id="valuer_phone" 
            v-model="localFormData.valuer_info.phone"
            @input="validateAndEmit"
            placeholder="Phone Number"
            class="form-control"
          />
          <span v-if="errors.valuer_phone" class="error-message">{{ errors.valuer_phone }}</span>
        </div>
        
        <div class="form-group">
          <label for="valuer_email">Email</label>
          <input 
            type="email" 
            id="valuer_email" 
            v-model="localFormData.valuer_info.email"
            @input="validateAndEmit"
            placeholder="Email Address"
            class="form-control"
          />
          <span v-if="errors.valuer_email" class="error-message">{{ errors.valuer_email }}</span>
        </div>
        
        <div class="form-group full-width">
          <label for="valuer_notes">Additional Notes</label>
          <textarea 
            id="valuer_notes" 
            v-model="localFormData.valuer_info.notes"
            @input="validateAndEmit"
            rows="3"
            placeholder="Any additional information about the valuer..."
            class="form-control"
          ></textarea>
        </div>
      </div>
    </div>
    
    <div class="section-container" v-if="showQSSection">
      <h3 class="section-title">Quantity Surveyor Information</h3>
      <div class="form-grid">
        <div class="form-group">
          <label for="qs_company_name">Company Name</label>
          <input 
            type="text" 
            id="qs_company_name" 
            v-model="localFormData.qs_info.company_name"
            @input="validateAndEmit"
            placeholder="QS Company Name"
            class="form-control"
          />
          <span v-if="errors.qs_company_name" class="error-message">{{ errors.qs_company_name }}</span>
        </div>
        
        <div class="form-group">
          <label for="qs_contact_name">Contact Name</label>
          <input 
            type="text" 
            id="qs_contact_name" 
            v-model="localFormData.qs_info.contact_name"
            @input="validateAndEmit"
            placeholder="Contact Person"
            class="form-control"
          />
          <span v-if="errors.qs_contact_name" class="error-message">{{ errors.qs_contact_name }}</span>
        </div>
        
        <div class="form-group">
          <label for="qs_phone">Phone</label>
          <input 
            type="tel" 
            id="qs_phone" 
            v-model="localFormData.qs_info.phone"
            @input="validateAndEmit"
            placeholder="Phone Number"
            class="form-control"
          />
          <span v-if="errors.qs_phone" class="error-message">{{ errors.qs_phone }}</span>
        </div>
        
        <div class="form-group">
          <label for="qs_email">Email</label>
          <input 
            type="email" 
            id="qs_email" 
            v-model="localFormData.qs_info.email"
            @input="validateAndEmit"
            placeholder="Email Address"
            class="form-control"
          />
          <span v-if="errors.qs_email" class="error-message">{{ errors.qs_email }}</span>
        </div>
        
        <div class="form-group full-width">
          <label for="qs_notes">Additional Notes</label>
          <textarea 
            id="qs_notes" 
            v-model="localFormData.qs_info.notes"
            @input="validateAndEmit"
            rows="3"
            placeholder="Any additional information about the quantity surveyor..."
            class="form-control"
          ></textarea>
        </div>
      </div>
    </div>
    
    <div class="toggle-section" v-if="!showQSSection">
      <button @click="toggleQSSection" class="btn btn-secondary">
        Add Quantity Surveyor Information
      </button>
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

// Show/hide QS section
const showQSSection = ref(false);

// Local copy of form data
const localFormData = reactive({
  valuer_info: {
    company_name: '',
    contact_name: '',
    phone: '',
    email: '',
    notes: ''
  },
  qs_info: {
    company_name: '',
    contact_name: '',
    phone: '',
    email: '',
    notes: ''
  }
});

// Form validation errors
const errors = reactive({
  valuer_company_name: '',
  valuer_contact_name: '',
  valuer_phone: '',
  valuer_email: '',
  qs_company_name: '',
  qs_contact_name: '',
  qs_phone: '',
  qs_email: ''
});

// Watch for parent form data changes
watch(() => props.formData, (newVal) => {
  if (newVal.valuer_info) {
    localFormData.valuer_info = { ...newVal.valuer_info };
  }
  
  if (newVal.qs_info) {
    localFormData.qs_info = { ...newVal.qs_info };
    
    // Show QS section if we have QS info
    if (newVal.qs_info.company_name || newVal.qs_info.contact_name || 
        newVal.qs_info.phone || newVal.qs_info.email) {
      showQSSection.value = true;
    }
  }
}, { deep: true });

// Toggle QS section visibility
function toggleQSSection() {
  showQSSection.value = !showQSSection.value;
  validateAndEmit();
}

// Validate form and emit changes
function validateAndEmit() {
  validateForm();
  
  emit('update:formData', {
    ...props.formData,
    valuer_info: localFormData.valuer_info,
    qs_info: localFormData.qs_info
  });
  
  emit('validate', isFormValid.value);
}

function validateForm() {
  // Reset errors
  Object.keys(errors).forEach(key => {
    errors[key] = '';
  });
  
  // Valuer validation
  if (!localFormData.valuer_info.company_name) {
    errors.valuer_company_name = 'Valuer company name is required';
  }
  
  if (!localFormData.valuer_info.contact_name) {
    errors.valuer_contact_name = 'Valuer contact name is required';
  }
  
  if (!localFormData.valuer_info.phone) {
    errors.valuer_phone = 'Valuer phone number is required';
  } else if (!/^(?:\+?61|0)[2-478](?:[ -]?[0-9]){8}$/.test(localFormData.valuer_info.phone.replace(/\s/g, ''))) {
    errors.valuer_phone = 'Please enter a valid Australian phone number';
  }
  
  if (!localFormData.valuer_info.email) {
    errors.valuer_email = 'Valuer email is required';
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(localFormData.valuer_info.email)) {
    errors.valuer_email = 'Please enter a valid email address';
  }
  
  // QS validation (only if QS section is shown)
  if (showQSSection.value) {
    if (!localFormData.qs_info.company_name) {
      errors.qs_company_name = 'QS company name is required';
    }
    
    if (!localFormData.qs_info.contact_name) {
      errors.qs_contact_name = 'QS contact name is required';
    }
    
    if (!localFormData.qs_info.phone) {
      errors.qs_phone = 'QS phone number is required';
    } else if (!/^(?:\+?61|0)[2-478](?:[ -]?[0-9]){8}$/.test(localFormData.qs_info.phone.replace(/\s/g, ''))) {
      errors.qs_phone = 'Please enter a valid Australian phone number';
    }
    
    if (!localFormData.qs_info.email) {
      errors.qs_email = 'QS email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(localFormData.qs_info.email)) {
      errors.qs_email = 'Please enter a valid email address';
    }
  }
}

const isFormValid = computed(() => {
  // For valuer info, always check
  const valuerValid = !errors.valuer_company_name && 
                      !errors.valuer_contact_name && 
                      !errors.valuer_phone && 
                      !errors.valuer_email;
  
  // For QS info, only check if the section is shown
  if (showQSSection.value) {
    const qsValid = !errors.qs_company_name && 
                    !errors.qs_contact_name && 
                    !errors.qs_phone && 
                    !errors.qs_email;
    return valuerValid && qsValid;
  }
  
  return valuerValid;
});

// Initialize component
onMounted(() => {
  // Initialize with data from parent if available
  if (props.formData.valuer_info) {
    localFormData.valuer_info = { ...props.formData.valuer_info };
  }
  
  if (props.formData.qs_info) {
    localFormData.qs_info = { ...props.formData.qs_info };
    
    // Show QS section if we have QS info
    if (props.formData.qs_info.company_name || props.formData.qs_info.contact_name || 
        props.formData.qs_info.phone || props.formData.qs_info.email) {
      showQSSection.value = true;
    }
  }
  
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

.section-container {
  background-color: #f7fafc;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #4a5568;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
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

textarea.form-control {
  resize: vertical;
}

.error-message {
  display: block;
  color: #e53e3e;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.toggle-section {
  text-align: center;
  margin-top: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary {
  background-color: #a0aec0;
  color: white;
}

.btn-secondary:hover {
  background-color: #718096;
}
</style>
