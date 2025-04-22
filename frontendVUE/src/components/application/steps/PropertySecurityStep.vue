<template>
  <div class="step-container">
    <h2 class="step-title">Property & Security Information</h2>
    <p class="step-description">Enter details about the property or security for this loan application.</p>
    
    <div class="form-grid">
      <div class="form-group full-width">
        <label>Property Type</label>
        <div class="radio-group">
          <label class="radio-label">
            <input 
              type="radio" 
              v-model="localFormData.property.property_type" 
              value="residential"
              @change="validateAndEmit"
            />
            Residential
          </label>
          <label class="radio-label">
            <input 
              type="radio" 
              v-model="localFormData.property.property_type" 
              value="commercial"
              @change="validateAndEmit"
            />
            Commercial
          </label>
          <label class="radio-label">
            <input 
              type="radio" 
              v-model="localFormData.property.property_type" 
              value="industrial"
              @change="validateAndEmit"
            />
            Industrial
          </label>
          <label class="radio-label">
            <input 
              type="radio" 
              v-model="localFormData.property.property_type" 
              value="land"
              @change="validateAndEmit"
            />
            Land
          </label>
          <label class="radio-label">
            <input 
              type="radio" 
              v-model="localFormData.property.property_type" 
              value="other"
              @change="validateAndEmit"
            />
            Other
          </label>
        </div>
        <span v-if="errors.property_type" class="error-message">{{ errors.property_type }}</span>
      </div>
      
      <div class="form-group full-width">
        <label>Is this an existing property?</label>
        <div class="radio-group">
          <label class="radio-label">
            <input 
              type="radio" 
              v-model="localFormData.property.is_existing_property" 
              :value="true"
              @change="validateAndEmit"
            />
            Yes
          </label>
          <label class="radio-label">
            <input 
              type="radio" 
              v-model="localFormData.property.is_existing_property" 
              :value="false"
              @change="validateAndEmit"
            />
            No (Construction/Development)
          </label>
        </div>
      </div>
      
      <div class="form-group">
        <label for="security_type">Security Type</label>
        <select 
          id="security_type" 
          v-model="localFormData.property.security_type"
          @change="validateAndEmit"
          class="form-control"
        >
          <option value="">Select Security Type</option>
          <option value="first_mortgage">First Mortgage</option>
          <option value="second_mortgage">Second Mortgage</option>
          <option value="caveat">Caveat</option>
          <option value="company_charge">Company Charge</option>
          <option value="guarantee">Personal Guarantee</option>
          <option value="other">Other</option>
        </select>
        <span v-if="errors.security_type" class="error-message">{{ errors.security_type }}</span>
      </div>
      
      <div class="form-group">
        <label for="estimated_value">Estimated Value ($)</label>
        <input 
          type="number" 
          id="estimated_value" 
          v-model="localFormData.property.estimated_value"
          @input="validateAndEmit"
          min="0"
          step="1000"
          class="form-control"
        />
        <span v-if="errors.estimated_value" class="error-message">{{ errors.estimated_value }}</span>
      </div>
      
      <div class="form-group">
        <label for="purchase_price">Purchase Price ($)</label>
        <input 
          type="number" 
          id="purchase_price" 
          v-model="localFormData.property.purchase_price"
          @input="validateAndEmit"
          min="0"
          step="1000"
          class="form-control"
        />
        <span v-if="errors.purchase_price" class="error-message">{{ errors.purchase_price }}</span>
      </div>
    </div>
    
    <h3 class="section-title">Property Address</h3>
    <div class="form-grid">
      <div class="form-group full-width">
        <label for="street">Street Address</label>
        <input 
          type="text" 
          id="street" 
          v-model="localFormData.property.address.street"
          @input="validateAndEmit"
          placeholder="Street Address"
          class="form-control"
        />
        <span v-if="errors.street" class="error-message">{{ errors.street }}</span>
      </div>
      
      <div class="form-group">
        <label for="city">City/Suburb</label>
        <input 
          type="text" 
          id="city" 
          v-model="localFormData.property.address.city"
          @input="validateAndEmit"
          placeholder="City/Suburb"
          class="form-control"
        />
        <span v-if="errors.city" class="error-message">{{ errors.city }}</span>
      </div>
      
      <div class="form-group">
        <label for="state">State</label>
        <select 
          id="state" 
          v-model="localFormData.property.address.state"
          @change="validateAndEmit"
          class="form-control"
        >
          <option value="">Select State</option>
          <option value="NSW">New South Wales</option>
          <option value="VIC">Victoria</option>
          <option value="QLD">Queensland</option>
          <option value="WA">Western Australia</option>
          <option value="SA">South Australia</option>
          <option value="TAS">Tasmania</option>
          <option value="ACT">Australian Capital Territory</option>
          <option value="NT">Northern Territory</option>
        </select>
        <span v-if="errors.state" class="error-message">{{ errors.state }}</span>
      </div>
      
      <div class="form-group">
        <label for="postal_code">Postal Code</label>
        <input 
          type="text" 
          id="postal_code" 
          v-model="localFormData.property.address.postal_code"
          @input="validateAndEmit"
          placeholder="Postal Code"
          class="form-control"
        />
        <span v-if="errors.postal_code" class="error-message">{{ errors.postal_code }}</span>
      </div>
      
      <div class="form-group">
        <label for="country">Country</label>
        <input 
          type="text" 
          id="country" 
          v-model="localFormData.property.address.country"
          @input="validateAndEmit"
          placeholder="Country"
          class="form-control"
          value="Australia"
        />
        <span v-if="errors.country" class="error-message">{{ errors.country }}</span>
      </div>
    </div>
    
    <div v-if="!localFormData.property.is_existing_property" class="construction-section">
      <h3 class="section-title">Construction Details</h3>
      <div class="form-grid">
        <div class="form-group">
          <label for="land_value">Land Value ($)</label>
          <input 
            type="number" 
            id="land_value" 
            v-model="localFormData.property.construction_details.land_value"
            @input="validateAndEmit"
            min="0"
            step="1000"
            class="form-control"
          />
          <span v-if="errors.land_value" class="error-message">{{ errors.land_value }}</span>
        </div>
        
        <div class="form-group">
          <label for="construction_cost">Construction Cost ($)</label>
          <input 
            type="number" 
            id="construction_cost" 
            v-model="localFormData.property.construction_details.construction_cost"
            @input="validateAndEmit"
            min="0"
            step="1000"
            class="form-control"
          />
          <span v-if="errors.construction_cost" class="error-message">{{ errors.construction_cost }}</span>
        </div>
        
        <div class="form-group">
          <label for="soft_costs">Soft Costs ($)</label>
          <input 
            type="number" 
            id="soft_costs" 
            v-model="localFormData.property.construction_details.soft_costs"
            @input="validateAndEmit"
            min="0"
            step="1000"
            class="form-control"
          />
          <span v-if="errors.soft_costs" class="error-message">{{ errors.soft_costs }}</span>
        </div>
        
        <div class="form-group">
          <label for="estimated_completion_date">Estimated Completion Date</label>
          <input 
            type="date" 
            id="estimated_completion_date" 
            v-model="localFormData.property.construction_details.estimated_completion_date"
            @input="validateAndEmit"
            class="form-control"
          />
          <span v-if="errors.estimated_completion_date" class="error-message">{{ errors.estimated_completion_date }}</span>
        </div>
        
        <div class="form-group full-width">
          <label for="project_description">Project Description</label>
          <textarea 
            id="project_description" 
            v-model="localFormData.property.construction_details.project_description"
            @input="validateAndEmit"
            rows="4"
            class="form-control"
            placeholder="Describe the construction project..."
          ></textarea>
          <span v-if="errors.project_description" class="error-message">{{ errors.project_description }}</span>
        </div>
      </div>
    </div>
    
    <div class="form-group full-width">
      <label for="additional_notes">Additional Notes</label>
      <textarea 
        id="additional_notes" 
        v-model="localFormData.property.additional_notes"
        @input="validateAndEmit"
        rows="4"
        class="form-control"
        placeholder="Any additional information about the property or security..."
      ></textarea>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, onMounted, watch } from 'vue';

const props = defineProps({
  formData: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['update:formData', 'validate']);

// Initialize local form data with defaults
const localFormData = reactive({
  property: {
    address: {
      street: '',
      city: '',
      state: '',
      postal_code: '',
      country: 'Australia'
    },
    property_type: '',
    estimated_value: '',
    purchase_price: '',
    is_existing_property: true,
    security_type: '',
    additional_notes: '',
    construction_details: {
      land_value: '',
      construction_cost: '',
      soft_costs: '',
      estimated_completion_date: '',
      project_description: ''
    }
  }
});

// Form validation errors
const errors = reactive({
  property_type: '',
  security_type: '',
  estimated_value: '',
  purchase_price: '',
  street: '',
  city: '',
  state: '',
  postal_code: '',
  country: '',
  land_value: '',
  construction_cost: '',
  estimated_completion_date: '',
  project_description: ''
});

// Watch for parent form data changes
watch(() => props.formData.property, (newVal) => {
  if (newVal) {
    // Deep copy the property data
    localFormData.property = JSON.parse(JSON.stringify(newVal));
    
    // Ensure construction_details exists
    if (!localFormData.property.construction_details) {
      localFormData.property.construction_details = {
        land_value: '',
        construction_cost: '',
        soft_costs: '',
        estimated_completion_date: '',
        project_description: ''
      };
    }
  }
}, { deep: true });

// Validate form and emit changes
function validateAndEmit() {
  validateForm();
  
  emit('update:formData', {
    ...props.formData,
    property: localFormData.property
  });
  
  emit('validate', isFormValid.value);
}

function validateForm() {
  // Reset errors
  Object.keys(errors).forEach(key => {
    errors[key] = '';
  });
  
  // Property type validation
  if (!localFormData.property.property_type) {
    errors.property_type = 'Property type is required';
  }
  
  // Security type validation
  if (!localFormData.property.security_type) {
    errors.security_type = 'Security type is required';
  }
  
  // Estimated value validation
  if (!localFormData.property.estimated_value) {
    errors.estimated_value = 'Estimated value is required';
  } else if (isNaN(localFormData.property.estimated_value) || localFormData.property.estimated_value <= 0) {
    errors.estimated_value = 'Estimated value must be a positive number';
  }
  
  // Purchase price validation
  if (!localFormData.property.purchase_price) {
    errors.purchase_price = 'Purchase price is required';
  } else if (isNaN(localFormData.property.purchase_price) || localFormData.property.purchase_price <= 0) {
    errors.purchase_price = 'Purchase price must be a positive number';
  }
  
  // Address validation
  if (!localFormData.property.address.street) {
    errors.street = 'Street address is required';
  }
  
  if (!localFormData.property.address.city) {
    errors.city = 'City/Suburb is required';
  }
  
  if (!localFormData.property.address.state) {
    errors.state = 'State is required';
  }
  
  if (!localFormData.property.address.postal_code) {
    errors.postal_code = 'Postal code is required';
  } else if (!/^\d{4}$/.test(localFormData.property.address.postal_code)) {
    errors.postal_code = 'Postal code must be 4 digits';
  }
  
  if (!localFormData.property.address.country) {
    errors.country = 'Country is required';
  }
  
  // Construction details validation (only if not an existing property)
  if (!localFormData.property.is_existing_property) {
    if (!localFormData.property.construction_details.land_value) {
      errors.land_value = 'Land value is required';
    } else if (isNaN(localFormData.property.construction_details.land_value) || localFormData.property.construction_details.land_value <= 0) {
      errors.land_value = 'Land value must be a positive number';
    }
    
    if (!localFormData.property.construction_details.construction_cost) {
      errors.construction_cost = 'Construction cost is required';
    } else if (isNaN(localFormData.property.construction_details.construction_cost) || localFormData.property.construction_details.construction_cost <= 0) {
      errors.construction_cost = 'Construction cost must be a positive number';
    }
    
    if (!localFormData.property.construction_details.estimated_completion_date) {
      errors.estimated_completion_date = 'Estimated completion date is required';
    }
    
    if (!localFormData.property.construction_details.project_description) {
      errors.project_description = 'Project description is required';
    }
  }
}

const isFormValid = computed(() => {
  // Check if there are any errors
  return !Object.values(errors).some(error => error);
});

// Initialize component
onMounted(() => {
  // Initialize with data from parent if available
  if (props.formData.property) {
    localFormData.property = JSON.parse(JSON.stringify(props.formData.property));
    
    // Ensure construction_details exists
    if (!localFormData.property.construction_details) {
      localFormData.property.construction_details = {
        land_value: '',
        construction_cost: '',
        soft_costs: '',
        estimated_completion_date: '',
        project_description: ''
      };
    }
  }
  
  // Set default country if not set
  if (!localFormData.property.address.country) {
    localFormData.property.address.country = 'Australia';
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

.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.radio-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.radio-label input {
  margin-right: 0.5rem;
}

.construction-section {
  background-color: #f7fafc;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}
</style>
