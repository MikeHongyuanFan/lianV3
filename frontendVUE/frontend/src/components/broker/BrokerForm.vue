<template>
  <div class="broker-form">
    <form @submit.prevent="handleSubmit">
      <div class="form-group mb-4">
        <label for="name" class="form-label">Name</label>
        <input
          type="text"
          id="name"
          v-model="form.name"
          class="form-control"
          :class="{ 'is-invalid': errors.name }"
          required
        />
        <div v-if="errors.name" class="invalid-feedback">
          {{ errors.name }}
        </div>
      </div>

      <div class="form-group mb-4">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          id="email"
          v-model="form.email"
          class="form-control"
          :class="{ 'is-invalid': errors.email }"
          required
        />
        <div v-if="errors.email" class="invalid-feedback">
          {{ errors.email }}
        </div>
      </div>

      <div class="form-group mb-4">
        <label for="phone" class="form-label">Phone</label>
        <input
          type="tel"
          id="phone"
          v-model="form.phone"
          class="form-control"
          :class="{ 'is-invalid': errors.phone }"
          required
        />
        <div v-if="errors.phone" class="invalid-feedback">
          {{ errors.phone }}
        </div>
      </div>

      <div class="form-group mb-4">
        <label for="branch_id" class="form-label">Branch</label>
        <select
          id="branch_id"
          v-model="form.branch_id"
          class="form-select"
          :class="{ 'is-invalid': errors.branch_id }"
          required
        >
          <option value="" disabled>Select a branch</option>
          <option v-for="branch in branches" :key="branch.id" :value="branch.id">
            {{ branch.name }}
          </option>
        </select>
        <div v-if="errors.branch_id" class="invalid-feedback">
          {{ errors.branch_id }}
        </div>
      </div>

      <div class="form-group mb-4">
        <label for="company" class="form-label">Company</label>
        <input
          type="text"
          id="company"
          v-model="form.company"
          class="form-control"
          :class="{ 'is-invalid': errors.company }"
        />
        <div v-if="errors.company" class="invalid-feedback">
          {{ errors.company }}
        </div>
      </div>

      <div class="form-group mb-4">
        <label for="address" class="form-label">Address</label>
        <input
          type="text"
          id="address"
          v-model="form.address"
          class="form-control"
          :class="{ 'is-invalid': errors.address }"
        />
        <div v-if="errors.address" class="invalid-feedback">
          {{ errors.address }}
        </div>
      </div>

      <h4 class="mt-5 mb-3">Commission Details</h4>

      <div class="form-group mb-4">
        <label for="commission_bank_name" class="form-label">Bank Name</label>
        <input
          type="text"
          id="commission_bank_name"
          v-model="form.commission_bank_name"
          class="form-control"
          :class="{ 'is-invalid': errors.commission_bank_name }"
        />
        <div v-if="errors.commission_bank_name" class="invalid-feedback">
          {{ errors.commission_bank_name }}
        </div>
      </div>

      <div class="form-group mb-4">
        <label for="commission_account_name" class="form-label">Account Name</label>
        <input
          type="text"
          id="commission_account_name"
          v-model="form.commission_account_name"
          class="form-control"
          :class="{ 'is-invalid': errors.commission_account_name }"
        />
        <div v-if="errors.commission_account_name" class="invalid-feedback">
          {{ errors.commission_account_name }}
        </div>
      </div>

      <div class="form-group mb-4">
        <label for="commission_account_number" class="form-label">Account Number</label>
        <input
          type="text"
          id="commission_account_number"
          v-model="form.commission_account_number"
          class="form-control"
          :class="{ 'is-invalid': errors.commission_account_number }"
        />
        <div v-if="errors.commission_account_number" class="invalid-feedback">
          {{ errors.commission_account_number }}
        </div>
      </div>

      <div class="form-group mb-4">
        <label for="commission_bsb" class="form-label">BSB</label>
        <input
          type="text"
          id="commission_bsb"
          v-model="form.commission_bsb"
          class="form-control"
          :class="{ 'is-invalid': errors.commission_bsb }"
        />
        <div v-if="errors.commission_bsb" class="invalid-feedback">
          {{ errors.commission_bsb }}
        </div>
      </div>

      <div class="d-flex justify-content-between mt-5">
        <button type="button" class="btn btn-secondary" @click="$emit('cancel')">
          Cancel
        </button>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ submitButtonText }}
          <span v-if="loading" class="spinner-border spinner-border-sm ms-2" role="status"></span>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useBrokerStore } from '@/store/broker'

export default {
  name: 'BrokerForm',
  props: {
    broker: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const brokerStore = useBrokerStore()
    const branches = ref([])
    const errors = ref({})

    // Initialize form with broker data if provided, otherwise use empty values
    const form = reactive({
      name: '',
      email: '',
      phone: '',
      branch_id: '',
      company: '',
      address: '',
      commission_bank_name: '',
      commission_account_name: '',
      commission_account_number: '',
      commission_bsb: ''
    })

    // Computed property for submit button text
    const submitButtonText = computed(() => {
      return props.broker ? 'Update Broker' : 'Create Broker'
    })

    // Load branches for dropdown
    const loadBranches = async () => {
      try {
        await brokerStore.fetchBranches()
        branches.value = brokerStore.branches
      } catch (error) {
        console.error('Failed to load branches:', error)
      }
    }

    // Initialize form with broker data if editing
    const initializeForm = () => {
      if (props.broker) {
        form.name = props.broker.name || ''
        form.email = props.broker.email || ''
        form.phone = props.broker.phone || ''
        form.branch_id = props.broker.branch?.id || ''
        form.company = props.broker.company || ''
        form.address = props.broker.address || ''
        form.commission_bank_name = props.broker.commission_bank_name || ''
        form.commission_account_name = props.broker.commission_account_name || ''
        form.commission_account_number = props.broker.commission_account_number || ''
        form.commission_bsb = props.broker.commission_bsb || ''
      }
    }

    // Handle form submission
    const handleSubmit = () => {
      errors.value = {}
      
      // Basic validation
      if (!form.name) errors.value.name = 'Name is required'
      if (!form.email) errors.value.email = 'Email is required'
      if (!form.phone) errors.value.phone = 'Phone is required'
      if (!form.branch_id) errors.value.branch_id = 'Branch is required'
      
      // If there are validation errors, don't submit
      if (Object.keys(errors.value).length > 0) return
      
      // Prepare data for submission
      const brokerData = {
        name: form.name,
        email: form.email,
        phone: form.phone,
        branch_id: form.branch_id,
        company: form.company || null,
        address: form.address || null,
        commission_bank_name: form.commission_bank_name || null,
        commission_account_name: form.commission_account_name || null,
        commission_account_number: form.commission_account_number || null,
        commission_bsb: form.commission_bsb || null
      }
      
      // Emit submit event with broker data
      emit('submit', brokerData)
    }

    // Load branches and initialize form on component mount
    onMounted(() => {
      loadBranches()
      initializeForm()
    })

    return {
      form,
      errors,
      branches,
      submitButtonText,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.broker-form {
  max-width: 800px;
  margin: 0 auto;
}
</style>
