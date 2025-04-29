<template>
  <div class="borrowers-list-container">
    <h3>Borrowers</h3>
    
    <div v-if="loading" class="loading-state">
      <p>Loading borrowers...</p>
    </div>
    
    <AlertMessage v-if="error" :message="error" type="error" />
    
    <div v-if="!loading && borrowers.length === 0" class="empty-state">
      <p>No borrowers associated with this application.</p>
      <BaseButton @click="showAddBorrowerModal = true" variant="secondary">Add Borrower</BaseButton>
    </div>
    
    <div v-if="!loading && borrowers.length > 0" class="borrowers-grid">
      <div v-for="borrower in borrowers" :key="borrower.id" class="borrower-card">
        <div class="borrower-header">
          <h4>{{ borrower.first_name }} {{ borrower.last_name }}</h4>
          <span class="borrower-type-badge">{{ formatBorrowerType(borrower.borrower_type) }}</span>
        </div>
        <div class="borrower-details">
          <p><strong>Email:</strong> {{ borrower.email }}</p>
          <p><strong>Phone:</strong> {{ borrower.phone_number }}</p>
          <p><strong>Address:</strong> {{ borrower.address }}</p>
        </div>
        <div class="borrower-actions">
          <router-link :to="`/borrowers/${borrower.id}`" class="view-link">View Details</router-link>
          <button @click="removeBorrower(borrower.id)" class="remove-button">Remove</button>
        </div>
      </div>
    </div>
    
    <!-- Add Borrower Modal -->
    <div v-if="showAddBorrowerModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Add Borrower</h3>
          <button @click="showAddBorrowerModal = false" class="close-button">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="borrower-select">Select Existing Borrower</label>
            <select id="borrower-select" v-model="selectedBorrower" class="form-control">
              <option value="">-- Select Borrower --</option>
              <option v-for="borrower in availableBorrowers" :key="borrower.id" :value="borrower.id">
                {{ borrower.first_name }} {{ borrower.last_name }} ({{ borrower.email }})
              </option>
            </select>
          </div>
          <div class="form-actions">
            <BaseButton @click="showAddBorrowerModal = false" variant="secondary">Cancel</BaseButton>
            <BaseButton @click="addBorrower" variant="primary" :disabled="!selectedBorrower">Add</BaseButton>
          </div>
          <div class="divider">OR</div>
          <div class="create-new">
            <router-link :to="{name: 'borrower-create', query: { application: applicationId }}" class="create-link">
              Create New Borrower
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import AlertMessage from './AlertMessage.vue'
import BaseButton from './BaseButton.vue'
import { useBorrowerStore } from '@/store/borrower'

export default {
  name: 'ApplicationBorrowersList',
  components: {
    AlertMessage,
    BaseButton
  },
  props: {
    applicationId: {
      type: [Number, String],
      required: true
    },
    borrowers: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    }
  },
  emits: ['update-borrowers'],
  setup(props, { emit }) {
    const borrowerStore = useBorrowerStore()
    
    const showAddBorrowerModal = ref(false)
    const selectedBorrower = ref('')
    const availableBorrowers = ref([])
    const loadingBorrowers = ref(false)
    
    const formatBorrowerType = (type) => {
      if (!type) return 'Unknown'
      return type.charAt(0).toUpperCase() + type.slice(1)
    }
    
    const fetchAvailableBorrowers = async () => {
      loadingBorrowers.value = true
      try {
        // Set a large limit to get all borrowers
        borrowerStore.setLimit(100)
        await borrowerStore.fetchBorrowers()
        
        // Filter out borrowers that are already associated with this application
        const currentBorrowerIds = props.borrowers.map(b => b.id)
        availableBorrowers.value = borrowerStore.borrowers.filter(
          b => !currentBorrowerIds.includes(b.id)
        )
      } catch (error) {
        console.error('Error fetching available borrowers:', error)
      } finally {
        loadingBorrowers.value = false
      }
    }
    
    const addBorrower = async () => {
      if (!selectedBorrower.value) return
      
      try {
        // Get the current borrowers and add the new one
        const updatedBorrowers = [...props.borrowers.map(b => b.id), parseInt(selectedBorrower.value)]
        
        // Emit event to parent component to update borrowers
        emit('update-borrowers', updatedBorrowers)
        
        // Reset and close modal
        selectedBorrower.value = ''
        showAddBorrowerModal.value = false
      } catch (error) {
        console.error('Error adding borrower:', error)
      }
    }
    
    const removeBorrower = async (borrowerId) => {
      try {
        // Get the current borrowers and remove the specified one
        const updatedBorrowers = props.borrowers
          .filter(b => b.id !== borrowerId)
          .map(b => b.id)
        
        // Emit event to parent component to update borrowers
        emit('update-borrowers', updatedBorrowers)
      } catch (error) {
        console.error('Error removing borrower:', error)
      }
    }
    
    // Watch for modal opening to fetch available borrowers
    const handleModalOpen = () => {
      if (showAddBorrowerModal.value) {
        fetchAvailableBorrowers()
      }
    }
    
    return {
      showAddBorrowerModal,
      selectedBorrower,
      availableBorrowers,
      formatBorrowerType,
      addBorrower,
      removeBorrower,
      handleModalOpen
    }
  },
  watch: {
    showAddBorrowerModal(newVal) {
      if (newVal) {
        this.handleModalOpen()
      }
    }
  }
}
</script>

<style scoped>
.borrowers-list-container {
  margin-bottom: 2rem;
}

.borrowers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.borrower-card {
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 1rem;
  background-color: #f8fafc;
}

.borrower-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.borrower-header h4 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.borrower-type-badge {
  background-color: #e2e8f0;
  color: #4a5568;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
}

.borrower-details {
  margin-bottom: 1rem;
}

.borrower-details p {
  margin: 0.25rem 0;
  font-size: 0.875rem;
}

.borrower-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.view-link {
  color: #3182ce;
  text-decoration: none;
}

.view-link:hover {
  text-decoration: underline;
}

.remove-button {
  color: #e53e3e;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  font-size: 0.875rem;
}

.remove-button:hover {
  text-decoration: underline;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 50;
}

.modal-container {
  background-color: white;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #4a5568;
}

.modal-body {
  padding: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.divider {
  text-align: center;
  margin: 1rem 0;
  color: #718096;
}

.create-new {
  text-align: center;
}

.create-link {
  color: #3182ce;
  text-decoration: none;
}

.create-link:hover {
  text-decoration: underline;
}

.loading-state, .empty-state {
  padding: 2rem;
  text-align: center;
  color: #718096;
}
</style>
        </div>
        
        <div class="borrower-details">
          <div class="detail-item">
            <div class="detail-label">Email:</div>
            <div class="detail-value">{{ borrower.email }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">Phone:</div>
            <div class="detail-value">{{ borrower.phone_number }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">Address:</div>
            <div class="detail-value">{{ borrower.address }}</div>
          </div>
          <div v-if="borrower.date_of_birth" class="detail-item">
            <div class="detail-label">Date of Birth:</div>
            <div class="detail-value">{{ formatDate(borrower.date_of_birth) }}</div>
          </div>
          <div v-if="borrower.employment_status" class="detail-item">
            <div class="detail-label">Employment:</div>
            <div class="detail-value">{{ formatEmploymentStatus(borrower.employment_status) }}</div>
          </div>
          <div v-if="borrower.annual_income" class="detail-item">
            <div class="detail-label">Annual Income:</div>
            <div class="detail-value">${{ formatCurrency(borrower.annual_income) }}</div>
          </div>
        </div>
        
        <div class="borrower-actions">
          <BaseButton @click="viewBorrower(borrower.id)" variant="secondary" size="small">View Details</BaseButton>
          <BaseButton @click="editBorrower(borrower)" variant="secondary" size="small">Edit</BaseButton>
        </div>
      </div>
    </div>
    
    <div v-if="!loading && borrowers.length > 0" class="add-borrower-action">
      <BaseButton @click="showAddBorrowerModal = true" variant="secondary">Add Another Borrower</BaseButton>
    </div>
    
    <!-- Borrower form modal -->
    <div v-if="showAddBorrowerModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>{{ editingBorrower ? 'Edit Borrower' : 'Add Borrower' }}</h3>
          <button type="button" class="close-button" @click="cancelBorrowerForm">&times;</button>
        </div>
        <div class="modal-body">
          <BorrowerForm
            :borrower="editingBorrower"
            :mode="editingBorrower ? 'edit' : 'create'"
            :loading="formLoading"
            @submit="saveBorrower"
            @cancel="cancelBorrowerForm"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/BaseButton.vue'
import AlertMessage from '@/components/AlertMessage.vue'
import BorrowerForm from '@/components/BorrowerForm.vue'

export default {
  name: 'ApplicationBorrowersList',
  components: {
    BaseButton,
    AlertMessage,
    BorrowerForm
  },
  props: {
    applicationId: {
      type: [Number, String],
      required: true
    },
    borrowers: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    }
  },
  emits: ['add-borrower', 'update-borrower'],
  setup(props, { emit }) {
    const router = useRouter()
    
    const showAddBorrowerModal = ref(false)
    const editingBorrower = ref(null)
    const formLoading = ref(false)
    
    const saveBorrower = async (borrowerData) => {
      formLoading.value = true
      
      try {
        if (editingBorrower.value) {
          // Update existing borrower
          emit('update-borrower', {
            borrowerId: editingBorrower.value.id,
            borrowerData,
            onSuccess: () => {
              showAddBorrowerModal.value = false
              editingBorrower.value = null
            },
            onError: (error) => {
              console.error('Error updating borrower:', error)
            }
          })
        } else {
          // Add new borrower
          emit('add-borrower', {
            applicationId: props.applicationId,
            borrowerData,
            onSuccess: () => {
              showAddBorrowerModal.value = false
            },
            onError: (error) => {
              console.error('Error adding borrower:', error)
            }
          })
        }
      } finally {
        formLoading.value = false
      }
    }
    
    const editBorrower = (borrower) => {
      editingBorrower.value = borrower
      showAddBorrowerModal.value = true
    }
    
    const viewBorrower = (borrowerId) => {
      router.push({ name: 'borrower-detail', params: { id: borrowerId } })
    }
    
    const cancelBorrowerForm = () => {
      showAddBorrowerModal.value = false
      editingBorrower.value = null
    }
    
    const formatBorrowerType = (type) => {
      const types = {
        individual: 'Individual',
        company: 'Company',
        trust: 'Trust'
      }
      return types[type] || type
    }
    
    const formatEmploymentStatus = (status) => {
      const statuses = {
        full_time: 'Full Time',
        part_time: 'Part Time',
        self_employed: 'Self Employed',
        unemployed: 'Unemployed',
        retired: 'Retired'
      }
      return statuses[status] || status
    }
    
    const formatCurrency = (value) => {
      if (!value) return '0.00'
      return parseFloat(value).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    return {
      showAddBorrowerModal,
      editingBorrower,
      formLoading,
      saveBorrower,
      editBorrower,
      viewBorrower,
      cancelBorrowerForm,
      formatBorrowerType,
      formatEmploymentStatus,
      formatCurrency,
      formatDate
    }
  }
}
</script>

<style scoped>
.borrowers-list-container {
  margin-bottom: 2rem;
}

.borrowers-list-container h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.loading-state,
.empty-state {
  padding: 2rem;
  text-align: center;
  background-color: #f9fafb;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.empty-state p {
  margin-bottom: 1rem;
  color: #6b7280;
}

.borrowers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.borrower-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  overflow: hidden;
  background-color: white;
}

.borrower-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f3f4f6;
  border-bottom: 1px solid #e5e7eb;
}

.borrower-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.borrower-type-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  background-color: #e0f2fe;
  color: #0369a1;
}

.borrower-details {
  padding: 1rem;
}

.detail-item {
  margin-bottom: 0.5rem;
}

.detail-label {
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 0.125rem;
}

.detail-value {
  font-size: 0.875rem;
}

.borrower-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
}

.add-borrower-action {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 50;
}

.modal-container {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
}

.modal-body {
  padding: 1.5rem;
}
</style>
