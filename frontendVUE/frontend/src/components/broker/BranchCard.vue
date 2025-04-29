<template>
  <div class="branch-card card mb-4">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="card-title mb-0">{{ branch.name }}</h5>
        <div class="branch-actions">
          <button class="btn btn-sm btn-outline-primary me-2" @click="$emit('view', branch)">
            <i class="bi bi-eye"></i> View
          </button>
          <button class="btn btn-sm btn-outline-secondary me-2" @click="$emit('edit', branch)">
            <i class="bi bi-pencil"></i> Edit
          </button>
          <button class="btn btn-sm btn-outline-danger" @click="confirmDelete">
            <i class="bi bi-trash"></i> Delete
          </button>
        </div>
      </div>
      
      <div class="branch-info">
        <div class="row">
          <div class="col-md-6">
            <p class="mb-1">
              <i class="bi bi-geo-alt me-2"></i>
              {{ branch.address }}
            </p>
            <p class="mb-1">
              <i class="bi bi-telephone me-2"></i>
              <a :href="`tel:${branch.phone}`">{{ branch.phone }}</a>
            </p>
          </div>
          <div class="col-md-6">
            <p class="mb-1">
              <i class="bi bi-envelope me-2"></i>
              <a :href="`mailto:${branch.email}`">{{ branch.email }}</a>
            </p>
            <p class="mb-1">
              <i class="bi bi-person me-2"></i>
              Manager: {{ branch.manager }}
            </p>
          </div>
        </div>
      </div>
      
      <div class="branch-stats mt-3">
        <div class="row">
          <div class="col-6">
            <button class="btn btn-sm btn-outline-info w-100" @click="$emit('view-brokers', branch)">
              <i class="bi bi-people me-1"></i> Brokers
            </button>
          </div>
          <div class="col-6">
            <button class="btn btn-sm btn-outline-info w-100" @click="$emit('view-bdms', branch)">
              <i class="bi bi-briefcase me-1"></i> BDMs
            </button>
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
            Are you sure you want to delete branch {{ branch.name }}?
            This action cannot be undone and may affect associated brokers and BDMs.
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
  name: 'BranchCard',
  props: {
    branch: {
      type: Object,
      required: true
    }
  },
  emits: ['view', 'edit', 'delete', 'view-brokers', 'view-bdms'],
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
      emit('delete', props.branch)
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
.branch-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.branch-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.branch-info {
  font-size: 0.9rem;
}

.branch-info i {
  width: 20px;
  text-align: center;
}

.branch-stats {
  border-top: 1px solid #eee;
  padding-top: 15px;
}
</style>
