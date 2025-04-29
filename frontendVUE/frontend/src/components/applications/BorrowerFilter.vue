<template>
  <div class="borrower-filter">
    <label for="borrower-filter">Borrower:</label>
    <div class="select-container">
      <select 
        id="borrower-filter" 
        v-model="selectedBorrowerId" 
        @change="onBorrowerChange"
        class="borrower-select"
      >
        <option value="">All Borrowers</option>
        <option v-for="borrower in borrowers" :key="borrower.id" :value="borrower.id">
          {{ borrower.first_name }} {{ borrower.last_name }}
        </option>
      </select>
      <div v-if="loading" class="loading-indicator">Loading...</div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useBorrowerStore } from '@/store/borrower'

export default {
  name: 'BorrowerFilter',
  props: {
    modelValue: {
      type: [Number, null],
      default: null
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const borrowerStore = useBorrowerStore()
    const borrowers = ref([])
    const loading = ref(false)
    const selectedBorrowerId = ref(props.modelValue)
    
    // Watch for external changes to modelValue
    watch(() => props.modelValue, (newValue) => {
      selectedBorrowerId.value = newValue
    })
    
    // Fetch borrowers for the dropdown
    const fetchBorrowers = async () => {
      loading.value = true
      try {
        // Set a higher limit to get more borrowers for the dropdown
        borrowerStore.pagination.limit = 100
        await borrowerStore.fetchBorrowers()
        borrowers.value = borrowerStore.borrowers
      } catch (error) {
        console.error('Error fetching borrowers:', error)
      } finally {
        loading.value = false
      }
    }
    
    // Handle borrower selection change
    const onBorrowerChange = () => {
      emit('update:modelValue', selectedBorrowerId.value)
    }
    
    // Fetch borrowers on component mount
    onMounted(() => {
      fetchBorrowers()
    })
    
    return {
      borrowers,
      loading,
      selectedBorrowerId,
      onBorrowerChange
    }
  }
}
</script>

<style scoped>
.borrower-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.select-container {
  position: relative;
  min-width: 200px;
}

.borrower-select {
  width: 100%;
  padding: 0.375rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  appearance: auto;
  background-color: white;
}

.loading-indicator {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.75rem;
  color: #6b7280;
}
</style>
