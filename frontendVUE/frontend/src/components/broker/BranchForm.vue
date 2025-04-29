<template>
  <div class="branch-form">
    <form @submit.prevent="handleSubmit">
      <div class="form-group mb-4">
        <label for="name" class="form-label">Branch Name</label>
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
        <label for="address" class="form-label">Address</label>
        <input
          type="text"
          id="address"
          v-model="form.address"
          class="form-control"
          :class="{ 'is-invalid': errors.address }"
          required
        />
        <div v-if="errors.address" class="invalid-feedback">
          {{ errors.address }}
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

export default {
  name: 'BranchForm',
  props: {
    branch: {
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
    const errors = ref({})

    // Initialize form with branch data if provided, otherwise use empty values
    const form = reactive({
      name: '',
      address: '',
      phone: '',
      email: ''
    })

    // Computed property for submit button text
    const submitButtonText = computed(() => {
      return props.branch ? 'Update Branch' : 'Create Branch'
    })

    // Initialize form with branch data if editing
    const initializeForm = () => {
      if (props.branch) {
        form.name = props.branch.name || ''
        form.address = props.branch.address || ''
        form.phone = props.branch.phone || ''
        form.email = props.branch.email || ''
      }
    }

    // Handle form submission
    const handleSubmit = () => {
      errors.value = {}
      
      // Basic validation
      if (!form.name) errors.value.name = 'Branch name is required'
      if (!form.address) errors.value.address = 'Address is required'
      if (!form.phone) errors.value.phone = 'Phone is required'
      if (!form.email) errors.value.email = 'Email is required'
      
      // If there are validation errors, don't submit
      if (Object.keys(errors.value).length > 0) return
      
      // Prepare data for submission
      const branchData = {
        name: form.name,
        address: form.address,
        phone: form.phone,
        email: form.email
      }
      
      // Emit submit event with branch data
      emit('submit', branchData)
    }

    // Initialize form on component mount
    onMounted(() => {
      initializeForm()
    })

    return {
      form,
      errors,
      submitButtonText,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.branch-form {
  max-width: 800px;
  margin: 0 auto;
}
</style>
