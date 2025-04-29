<template>
  <div class="guarantors-list-container">
    <h3>Guarantors</h3>
    
    <div v-if="loading" class="loading-state">
      <p>Loading guarantors...</p>
    </div>
    
    <AlertMessage v-if="error" :message="error" type="error" />
    
    <div v-if="!loading && guarantors.length === 0" class="empty-state">
      <p>No guarantors associated with this application.</p>
      <BaseButton @click="showAddGuarantorModal = true" variant="secondary">Add Guarantor</BaseButton>
    </div>
    
    <div v-if="!loading && guarantors.length > 0" class="guarantors-grid">
      <div v-for="guarantor in guarantors" :key="guarantor.id" class="guarantor-card">
        <div class="guarantor-header">
          <h4>{{ guarantor.first_name }} {{ guarantor.last_name }}</h4>
          <span class="relationship-badge">{{ formatRelationship(guarantor.relationship_to_borrower) }}</span>
        </div>
        <div class="guarantor-details">
          <p><strong>Email:</strong> {{ guarantor.email }}</p>
          <p><strong>Phone:</strong> {{ guarantor.phone_number }}</p>
          <p><strong>Address:</strong> {{ guarantor.address }}</p>
        </div>
        <div class="guarantor-actions">
          <router-link :to="`/guarantors/${guarantor.id}`" class="view-link">View Details</router-link>
          <button @click="removeGuarantor(guarantor.id)" class="remove-button">Remove</button>
        </div>
      </div>
    </div>
    
    <!-- Add Guarantor Modal -->
    <div v-if="showAddGuarantorModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Add Guarantor</h3>
          <button @click="showAddGuarantorModal = false" class="close-button">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="guarantor-select">Select Existing Guarantor</label>
            <select id="guarantor-select" v-model="selectedGuarantor" class="form-control">
              <option value="">-- Select Guarantor --</option>
              <option v-for="guarantor in availableGuarantors" :key="guarantor.id" :value="guarantor.id">
                {{ guarantor.first_name }} {{ guarantor.last_name }} ({{ guarantor.email }})
              </option>
            </select>
          </div>
          <div class="form-actions">
            <BaseButton @click="showAddGuarantorModal = false" variant="secondary">Cancel</BaseButton>
            <BaseButton @click="addGuarantor" variant="primary" :disabled="!selectedGuarantor">Add</BaseButton>
          </div>
          <div class="divider">OR</div>
          <div class="create-new">
            <router-link :to="{name: 'guarantor-create', query: { application: applicationId }}" class="create-link">
              Create New Guarantor
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
import { useGuarantorStore } from '@/store/guarantor'

export default {
  name: 'ApplicationGuarantorsList',
  components: {
    AlertMessage,
    BaseButton
  },
  props: {
    applicationId: {
      type: [Number, String],
      required: true
    },
    guarantors: {
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
  emits: ['update-guarantors'],
  setup(props, { emit }) {
    const guarantorStore = useGuarantorStore()
    
    const showAddGuarantorModal = ref(false)
    const selectedGuarantor = ref('')
    const availableGuarantors = ref([])
    const loadingGuarantors = ref(false)
    
    const formatRelationship = (relationship) => {
      if (!relationship) return 'Unknown'
      
      // Convert snake_case to Title Case
      return relationship
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    const fetchAvailableGuarantors = async () => {
      loadingGuarantors.value = true
      try {
        // Set a large limit to get all guarantors
        guarantorStore.setLimit(100)
        await guarantorStore.fetchGuarantors()
        
        // Filter out guarantors that are already associated with this application
        const currentGuarantorIds = props.guarantors.map(g => g.id)
        availableGuarantors.value = guarantorStore.guarantors.filter(
          g => !currentGuarantorIds.includes(g.id)
        )
      } catch (error) {
        console.error('Error fetching available guarantors:', error)
      } finally {
        loadingGuarantors.value = false
      }
    }
    
    const addGuarantor = async () => {
      if (!selectedGuarantor.value) return
      
      try {
        // Emit event to parent component to update guarantors
        emit('update-guarantors', parseInt(selectedGuarantor.value))
        
        // Reset and close modal
        selectedGuarantor.value = ''
        showAddGuarantorModal.value = false
      } catch (error) {
        console.error('Error adding guarantor:', error)
      }
    }
    
    const removeGuarantor = async (guarantorId) => {
      try {
        // Emit event to parent component to remove guarantor
        emit('remove-guarantor', guarantorId)
      } catch (error) {
        console.error('Error removing guarantor:', error)
      }
    }
    
    // Watch for modal opening to fetch available guarantors
    const handleModalOpen = () => {
      if (showAddGuarantorModal.value) {
        fetchAvailableGuarantors()
      }
    }
    
    return {
      showAddGuarantorModal,
      selectedGuarantor,
      availableGuarantors,
      formatRelationship,
      addGuarantor,
      removeGuarantor,
      handleModalOpen
    }
  },
  watch: {
    showAddGuarantorModal(newVal) {
      if (newVal) {
        this.handleModalOpen()
      }
    }
  }
}
</script>

<style scoped>
.guarantors-list-container {
  margin-bottom: 2rem;
}

.guarantors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.guarantor-card {
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 1rem;
  background-color: #f8fafc;
}

.guarantor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.guarantor-header h4 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.relationship-badge {
  background-color: #e2e8f0;
  color: #4a5568;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
}

.guarantor-details {
  margin-bottom: 1rem;
}

.guarantor-details p {
  margin: 0.25rem 0;
  font-size: 0.875rem;
}

.guarantor-actions {
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
        
        <div class="guarantor-details">
          <div class="detail-item">
            <div class="detail-label">Email:</div>
            <div class="detail-value">{{ guarantor.email }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">Phone:</div>
            <div class="detail-value">{{ guarantor.phone_number }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">Address:</div>
            <div class="detail-value">{{ guarantor.address }}</div>
          </div>
          <div v-if="guarantor.date_of_birth" class="detail-item">
            <div class="detail-label">Date of Birth:</div>
            <div class="detail-value">{{ formatDate(guarantor.date_of_birth) }}</div>
          </div>
          <div v-if="guarantor.employment_status" class="detail-item">
            <div class="detail-label">Employment:</div>
            <div class="detail-value">{{ formatEmploymentStatus(guarantor.employment_status) }}</div>
          </div>
          <div v-if="guarantor.annual_income" class="detail-item">
            <div class="detail-label">Annual Income:</div>
            <div class="detail-value">${{ formatCurrency(guarantor.annual_income) }}</div>
          </div>
        </div>
        
        <div class="guarantor-actions">
          <BaseButton @click="viewGuarantor(guarantor.id)" variant="secondary" size="small">View Details</BaseButton>
          <BaseButton @click="editGuarantor(guarantor)" variant="secondary" size="small">Edit</BaseButton>
        </div>
      </div>
    </div>
    
    <div v-if="!loading && guarantors.length > 0" class="add-guarantor-action">
      <BaseButton @click="showAddGuarantorModal = true" variant="secondary">Add Another Guarantor</BaseButton>
    </div>
    
    <!-- Guarantor form modal -->
    <div v-if="showAddGuarantorModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>{{ editingGuarantor ? 'Edit Guarantor' : 'Add Guarantor' }}</h3>
          <button type="button" class="close-button" @click="cancelGuarantorForm">&times;</button>
        </div>
        <div class="modal-body">
          <GuarantorForm
            :guarantor="editingGuarantor"
            :mode="editingGuarantor ? 'edit' : 'create'"
            :loading="formLoading"
            @submit="saveGuarantor"
            @cancel="cancelGuarantorForm"
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
import GuarantorForm from '@/components/GuarantorForm.vue'

export default {
  name: 'ApplicationGuarantorsList',
  components: {
    BaseButton,
    AlertMessage,
    GuarantorForm
  },
  props: {
    applicationId: {
      type: [Number, String],
      required: true
    },
    guarantors: {
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
  emits: ['add-guarantor', 'update-guarantor'],
  setup(props, { emit }) {
    const router = useRouter()
    
    const showAddGuarantorModal = ref(false)
    const editingGuarantor = ref(null)
    const formLoading = ref(false)
    
    const saveGuarantor = async (guarantorData) => {
      formLoading.value = true
      
      try {
        if (editingGuarantor.value) {
          // Update existing guarantor
          emit('update-guarantor', {
            guarantorId: editingGuarantor.value.id,
            guarantorData,
            onSuccess: () => {
              showAddGuarantorModal.value = false
              editingGuarantor.value = null
            },
            onError: (error) => {
              console.error('Error updating guarantor:', error)
            }
          })
        } else {
          // Add new guarantor
          emit('add-guarantor', {
            applicationId: props.applicationId,
            guarantorData,
            onSuccess: () => {
              showAddGuarantorModal.value = false
            },
            onError: (error) => {
              console.error('Error adding guarantor:', error)
            }
          })
        }
      } finally {
        formLoading.value = false
      }
    }
    
    const editGuarantor = (guarantor) => {
      editingGuarantor.value = guarantor
      showAddGuarantorModal.value = true
    }
    
    const viewGuarantor = (guarantorId) => {
      router.push({ name: 'guarantor-detail', params: { id: guarantorId } })
    }
    
    const cancelGuarantorForm = () => {
      showAddGuarantorModal.value = false
      editingGuarantor.value = null
    }
    
    const formatRelationship = (relationship) => {
      const relationships = {
        spouse: 'Spouse',
        parent: 'Parent',
        child: 'Child',
        sibling: 'Sibling',
        business_partner: 'Business Partner',
        friend: 'Friend',
        other: 'Other'
      }
      return relationships[relationship] || relationship
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
      showAddGuarantorModal,
      editingGuarantor,
      formLoading,
      saveGuarantor,
      editGuarantor,
      viewGuarantor,
      cancelGuarantorForm,
      formatRelationship,
      formatEmploymentStatus,
      formatCurrency,
      formatDate
    }
  }
}
</script>

<style scoped>
.guarantors-list-container {
  margin-bottom: 2rem;
}

.guarantors-list-container h3 {
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

.guarantors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.guarantor-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  overflow: hidden;
  background-color: white;
}

.guarantor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f3f4f6;
  border-bottom: 1px solid #e5e7eb;
}

.guarantor-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.relationship-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  background-color: #dbeafe;
  color: #1e40af;
}

.guarantor-details {
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

.guarantor-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
}

.add-guarantor-action {
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
