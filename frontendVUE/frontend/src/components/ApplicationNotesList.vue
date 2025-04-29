<template>
  <div class="application-notes-container">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-xl font-semibold">Application Notes</h3>
      <button
        @click="showAddNoteForm = true"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
      >
        Add Note
      </button>
    </div>

    <!-- Add Note Form -->
    <div v-if="showAddNoteForm" class="mb-6 p-4 bg-gray-50 rounded-lg">
      <h3 class="text-lg font-medium mb-3">Add New Note</h3>
      <form @submit.prevent="addNote">
        <div class="mb-3">
          <label for="note_title" class="block text-sm font-medium text-gray-700 mb-1">Title</label>
          <input
            id="note_title"
            v-model="newNote.title"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div class="mb-3">
          <label for="note_content" class="block text-sm font-medium text-gray-700 mb-1">Content *</label>
          <textarea
            id="note_content"
            v-model="newNote.content"
            rows="4"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          ></textarea>
        </div>
        
        <div class="mb-3">
          <label for="note_remind_date" class="block text-sm font-medium text-gray-700 mb-1">Reminder Date</label>
          <input
            id="note_remind_date"
            v-model="newNote.remind_date"
            type="datetime-local"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="cancelAddNote"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
            :disabled="addingNote"
          >
            {{ addingNote ? 'Adding...' : 'Add Note' }}
          </button>
        </div>
      </form>
    </div>
    
    <!-- Notes List -->
    <NoteList
      :notes="notes"
      :loading="loading"
      :error="error"
      :show-actions="true"
      :show-create-button="false"
      :show-pagination="true"
      :current-page="currentPage"
      :total-pages="totalPages"
      :items-per-page="itemsPerPage"
      :total-items="totalNotes"
      @edit="navigateToEditNote"
      @delete="confirmDeleteNote"
      @view="navigateToViewNote"
      @view-application="navigateToApplication"
      @view-borrower="navigateToBorrower"
      @prev-page="prevPage"
      @next-page="nextPage"
      @fetch="fetchNotes"
    />
    
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
import { useRouter } from 'vue-router'
import { useNoteStore } from '@/store/note'
import NoteList from '@/components/notes/NoteList.vue'

export default {
  name: 'ApplicationNotesList',
  components: {
    NoteList
  },
  props: {
    applicationId: {
      type: [Number, String],
      required: true
    }
  },
  setup(props) {
    const router = useRouter()
    const noteStore = useNoteStore()
    
    // Local state
    const notes = ref([])
    const loading = ref(false)
    const error = ref(null)
    const totalNotes = ref(0)
    const itemsPerPage = ref(10)
    const currentPage = ref(1)
    const showAddNoteForm = ref(false)
    const showDeleteModal = ref(false)
    const addingNote = ref(false)
    const deletingNote = ref(false)
    const noteToDelete = ref(null)
    
    // Form data
    const newNote = ref({
      title: '',
      content: '',
      remind_date: '',
      application: parseInt(props.applicationId)
    })
    
    // Computed properties
    const totalPages = computed(() => Math.ceil(totalNotes.value / itemsPerPage.value))
    
    // Methods
    const fetchNotes = async () => {
      loading.value = true
      error.value = null
      
      try {
        const params = {
          limit: itemsPerPage.value,
          offset: (currentPage.value - 1) * itemsPerPage.value,
          application: props.applicationId
        }
        
        const response = await noteStore.fetchNotes(params)
        notes.value = response.results
        totalNotes.value = response.count
      } catch (err) {
        error.value = err.message || 'Failed to load notes'
        console.error('Error fetching notes:', err)
      } finally {
        loading.value = false
      }
    }
    
    const addNote = async () => {
      if (!newNote.value.content) return
      
      addingNote.value = true
      
      try {
        const noteData = {
          title: newNote.value.title || null,
          content: newNote.value.content,
          application: parseInt(props.applicationId),
          remind_date: newNote.value.remind_date || null
        }
        
        await noteStore.createNote(noteData)
        
        // Reset form and hide it
        newNote.value = {
          title: '',
          content: '',
          remind_date: '',
          application: parseInt(props.applicationId)
        }
        showAddNoteForm.value = false
        
        // Refresh notes
        await fetchNotes()
      } catch (error) {
        console.error('Error adding note:', error)
      } finally {
        addingNote.value = false
      }
    }
    
    const cancelAddNote = () => {
      newNote.value = {
        title: '',
        content: '',
        remind_date: '',
        application: parseInt(props.applicationId)
      }
      showAddNoteForm.value = false
    }
    
    const confirmDeleteNote = (note) => {
      noteToDelete.value = note
      showDeleteModal.value = true
    }
    
    const deleteNote = async () => {
      if (!noteToDelete.value) return
      
      deletingNote.value = true
      
      try {
        await noteStore.deleteNote(noteToDelete.value.id)
        showDeleteModal.value = false
        noteToDelete.value = null
        
        // Refresh notes
        await fetchNotes()
      } catch (error) {
        console.error('Error deleting note:', error)
      } finally {
        deletingNote.value = false
      }
    }
    
    const navigateToEditNote = (id) => {
      router.push({ name: 'note-edit', params: { id } })
    }
    
    const navigateToViewNote = (id) => {
      router.push({ name: 'note-detail', params: { id } })
    }
    
    const navigateToApplication = (id) => {
      // Already on application view, no need to navigate
    }
    
    const navigateToBorrower = (id) => {
      router.push({ name: 'borrower-detail', params: { id } })
    }
    
    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
        fetchNotes()
      }
    }
    
    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
        fetchNotes()
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      fetchNotes()
    })
    
    return {
      notes,
      loading,
      error,
      totalNotes,
      itemsPerPage,
      currentPage,
      totalPages,
      showAddNoteForm,
      showDeleteModal,
      addingNote,
      deletingNote,
      newNote,
      fetchNotes,
      addNote,
      cancelAddNote,
      confirmDeleteNote,
      deleteNote,
      navigateToEditNote,
      navigateToViewNote,
      navigateToApplication,
      navigateToBorrower,
      prevPage,
      nextPage
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
