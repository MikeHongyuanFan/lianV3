<template>
  <div class="broker-card card mb-4">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="card-title mb-0">{{ broker.name }}</h5>
        <div class="broker-actions">
          <button class="btn btn-sm btn-outline-primary me-2" @click="$emit('view', broker)">
            <i class="bi bi-eye"></i> View
          </button>
          <button class="btn btn-sm btn-outline-secondary me-2" @click="$emit('edit', broker)">
            <i class="bi bi-pencil"></i> Edit
          </button>
          <button class="btn btn-sm btn-outline-danger" @click="confirmDelete">
            <i class="bi bi-trash"></i> Delete
          </button>
        </div>
      </div>
      
      <div class="broker-info">
        <div class="row">
          <div class="col-md-6">
            <p class="mb-1">
              <i class="bi bi-envelope me-2"></i>
              <a :href="`mailto:${broker.email}`">{{ broker.email }}</a>
            </p>
            <p class="mb-1">
              <i class="bi bi-telephone me-2"></i>
              <a :href="`tel:${broker.phone}`">{{ broker.phone }}</a>
            </p>
            <p class="mb-1">
              <i class="bi bi-building me-2"></i>
              {{ broker.company || 'N/A' }}
            </p>
          </div>
          <div class="col-md-6">
            <p class="mb-1">
              <i class="bi bi-geo-alt me-2"></i>
              {{ broker.address || 'N/A' }}
            </p>
            <p class="mb-1">
              <i class="bi bi-house-door me-2"></i>
              Branch: {{ broker.branch_name || 'N/A' }}
            </p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Delete confirmation modal -->
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true" ref="deleteModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="deleteModalLabel">Confirm Delete</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to delete broker {{ broker.first_name }} {{ broker.last_name }}?
            This action cannot be undone.
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="handleDelete">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { Modal } from 'bootstrap'

export default {
  name: 'BrokerCard',
  props: {
    broker: {
      type: Object,
      required: true
    }
  },
  emits: ['view', 'edit', 'delete'],
  setup(props, { emit }) {
    const deleteModal = ref(null)
    let bsModal = null

    // Initialize Bootstrap modal
    onMounted(() => {
      bsModal = new Modal(deleteModal.value)
    })

    // Show delete confirmation modal
    const confirmDelete = () => {
      bsModal.show()
    }

    // Handle delete confirmation
    const handleDelete = () => {
      bsModal.hide()
      emit('delete', props.broker)
    }

    return {
      deleteModal,
      confirmDelete,
      handleDelete
    }
  }
}
</script>

<style scoped>
.broker-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.broker-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.broker-info {
  font-size: 0.9rem;
}

.broker-info i {
  width: 20px;
  text-align: center;
}
</style>
