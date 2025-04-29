<template>
  <div class="bdm-form">
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
  name: 'BDMForm',
  props: {
    bdm: {
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

    // Initialize form with BDM data if provided, otherwise use empty values
    const form = reactive({
      name: '',
      email: '',
      phone: '',
      branch_id: ''
    })

    // Computed property for submit button text
    const submitButtonText = computed(() => {
      return props.bdm ? 'Update BDM' : 'Create BDM'
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

    // Initialize form with BDM data if editing
    const initializeForm = () => {
      if (props.bdm) {
        form.name = props.bdm.name || ''
        form.email = props.bdm.email || ''
        form.phone = props.bdm.phone || ''
        form.branch_id = props.bdm.branch?.id || ''
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
      // If there are validation errors, don't submit
      if (Object.keys(errors.value).length > 0) return
      
      // Prepare data for submission
      const bdmData = {
        name: form.name,
        email: form.email,
        phone: form.phone,
        branch_id: form.branch_id
      }
      
      // Emit submit event with BDM data
      emit('submit', bdmData)
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
.bdm-form {
  max-width: 800px;
  margin: 0 auto;
}
</style>
