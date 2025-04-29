<template>
  <div class="note-detail-container">
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchNoteData" class="underline">Try again</button>
    </div>
    
    <!-- Note details -->
    <div v-else-if="note" class="bg-white rounded-lg shadow-md p-6">
      <div class="flex justify-between items-start mb-6">
        <div>
          <h1 class="text-2xl font-bold">{{ note.title || 'Untitled Note' }}</h1>
          <div class="text-sm text-gray-500 mt-1">
            <span>By {{ note.created_by_name }}</span>
            <span class="mx-1">•</span>
            <span>{{ formatDateTime(note.created_at) }}</span>
          </div>
        </div>
        
        <div class="flex space-x-2">
          <button
            @click="navigateToEdit"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
          >
            Edit
          </button>
          <button
            @click="confirmDelete"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none"
          >
            Delete
          </button>
        </div>
      </div>
      
      <!-- Reminder badge -->
      <div v-if="note.remind_date" class="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md flex items-center">
        <span class="material-icons text-yellow-500 mr-2">notifications</span>
        <div>
          <p class="font-medium text-yellow-700">Reminder set for {{ formatDateTime(note.remind_date) }}</p>
          <p v-if="isReminderPast" class="text-sm text-yellow-600">This reminder has passed</p>
        </div>
      </div>
      
      <!-- Note content -->
      <div class="note-content mb-6 p-4 bg-gray-50 rounded-md">
        <p class="whitespace-pre-line">{{ note.content }}</p>
      </div>
      
      <!-- Related information -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-if="note.application" class="related-info">
          <h3 class="text-sm font-medium text-gray-500 mb-2">Related Application</h3>
          <div class="p-3 bg-blue-50 rounded-md">
            <button 
              @click="navigateToApplication(note.application)" 
              class="text-blue-600 hover:underline font-medium"
            >
              View Application
            </button>
          </div>
        </div>
        
        <div v-if="note.borrower" class="related-info">
          <h3 class="text-sm font-medium text-gray-500 mb-2">Related Borrower</h3>
          <div class="p-3 bg-blue-50 rounded-md">
            <button 
              @click="navigateToBorrower(note.borrower)" 
              class="text-blue-600 hover:underline font-medium"
            >
              View Borrower
            </button>
          </div>
        </div>
      </div>
      
      <!-- System information -->
      <div class="mt-6">
        <h3 class="text-sm font-medium text-gray-500">System Information</h3>
        <div class="mt-2 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <p class="text-xs text-gray-500">Created</p>
            <p>{{ formatDateTime(note.created_at) }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-500">Last Updated</p>
            <p>{{ formatDateTime(note.updated_at) }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-500">ID</p>
            <p>{{ note.id }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Delete confirmation modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
        <h3 class="text-lg font-bold mb-4">Confirm Deletion</h3>
        <p class="mb-6">Are you sure you want to delete this note? This action cannot be undone.</p>
        <div class="flex justify-end space-x-3">
          <button
            @click="showDeleteModal = false"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
          >
            Cancel
          </button>
          <button
            @click="deleteNote"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none"
            :disabled="deletingNote"
          >
            {{ deletingNote ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNoteStore } from '@/store/note'

export default {
  name: 'NoteDetailView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const noteStore = useNoteStore()
    
    // Local state
    const noteId = ref(parseInt(route.params.id))
    const showDeleteModal = ref(false)
    const deletingNote = ref(false)
    
    // Computed properties
    const note = computed(() => noteStore.currentNote)
    const loading = computed(() => noteStore.loading)
    const error = computed(() => noteStore.error)
    
    const isReminderPast = computed(() => {
      if (!note.value?.remind_date) return false
      const reminderDate = new Date(note.value.remind_date)
      const now = new Date()
      return reminderDate < now
    })
    
    // Methods
    const fetchNoteData = async () => {
      try {
        await noteStore.fetchNoteById(noteId.value)
      } catch (error) {
        console.error('Error fetching note:', error)
      }
    }
    
    const navigateToEdit = () => {
      router.push({ name: 'note-edit', params: { id: noteId.value } })
    }
    
    const confirmDelete = () => {
      showDeleteModal.value = true
    }
    
    const deleteNote = async () => {
      deletingNote.value = true
      
      try {
        await noteStore.deleteNote(noteId.value)
        showDeleteModal.value = false
        router.push({ name: 'note-list' })
      } catch (error) {
        console.error('Error deleting note:', error)
      } finally {
        deletingNote.value = false
      }
    }
    
    const navigateToApplication = (applicationId) => {
      router.push({ name: 'application-detail', params: { id: applicationId } })
    }
    
    const navigateToBorrower = (borrowerId) => {
      router.push({ name: 'borrower-detail', params: { id: borrowerId } })
    }
    
    const formatDateTime = (dateString) => {
      if (!dateString) return 'Not provided'
      const date = new Date(dateString)
      return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`
    }
    
    // Lifecycle hooks
    onMounted(() => {
      fetchNoteData()
    })
    
    return {
      note,
      loading,
      error,
      isReminderPast,
      showDeleteModal,
      deletingNote,
      fetchNoteData,
      navigateToEdit,
      confirmDelete,
      deleteNote,
      navigateToApplication,
      navigateToBorrower,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
