<template>
  <div class="note-list-container">
    <div class="header-section">
      <h1 class="text-2xl font-bold mb-4">Notes</h1>
      <div class="flex justify-between items-center mb-6">
        <div class="search-filter-container flex items-center space-x-4">
          <!-- Search input -->
          <div class="search-container">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by title or content"
              class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              @input="debounceSearch"
            />
          </div>
          
          <!-- Application filter -->
          <div class="filter-container" v-if="applications.length > 0">
            <select
              v-model="selectedApplication"
              class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="applyFilters"
            >
              <option value="">All Applications</option>
              <option v-for="app in applications" :key="app.id" :value="app.id">
                {{ app.reference_number }}
              </option>
            </select>
          </div>
          
          <!-- Date range filters -->
          <div class="filter-container flex items-center space-x-2">
            <input
              v-model="dateFrom"
              type="date"
              class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="applyFilters"
            />
            <span>to</span>
            <input
              v-model="dateTo"
              type="date"
              class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="applyFilters"
            />
          </div>
          
          <!-- Clear filters button -->
          <button
            v-if="hasActiveFilters"
            @click="clearFilters"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
          >
            Clear Filters
          </button>
        </div>
        
        <!-- Create new note button -->
        <button
          @click="navigateToCreate"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
        >
          Create New Note
        </button>
      </div>
    </div>
    
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchNotes" class="underline">Try again</button>
    </div>
    
    <!-- Empty state -->
    <div v-else-if="!hasNotes" class="text-center py-12">
      <p class="text-gray-500 mb-4">No notes found</p>
      <button
        @click="navigateToCreate"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
      >
        Create Your First Note
      </button>
    </div>
    
    <!-- Notes list -->
    <div v-else class="notes-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <NoteItem
        v-for="note in notes"
        :key="note.id"
        :note="note"
        :show-actions="true"
        @edit="navigateToEdit(note.id)"
        @delete="confirmDelete(note)"
        @view-application="navigateToApplication"
        @view-borrower="navigateToBorrower"
        @click="navigateToDetail(note.id)"
      />
    </div>
    
    <!-- Pagination -->
    <div v-if="hasNotes" class="pagination-container flex justify-between items-center mt-6">
      <div class="text-sm text-gray-500">
        Showing {{ paginationInfo.currentPage * paginationInfo.itemsPerPage - paginationInfo.itemsPerPage + 1 }} 
        to {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }} 
        of {{ paginationInfo.totalItems }} notes
      </div>
      
      <div class="flex items-center space-x-2">
        <button
          @click="prevPage"
          :disabled="paginationInfo.currentPage === 1"
          class="px-3 py-1 border rounded-md"
          :class="paginationInfo.currentPage === 1 ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'"
        >
          Previous
        </button>
        
        <span class="px-3 py-1">
          Page {{ paginationInfo.currentPage }} of {{ paginationInfo.totalPages }}
        </span>
        
        <button
          @click="nextPage"
          :disabled="paginationInfo.currentPage === paginationInfo.totalPages"
          class="px-3 py-1 border rounded-md"
          :class="paginationInfo.currentPage === paginationInfo.totalPages ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'"
        >
          Next
        </button>
        
        <select
          v-model="itemsPerPage"
          class="ml-4 px-2 py-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          @change="changeItemsPerPage"
        >
          <option :value="10">10 per page</option>
          <option :value="25">25 per page</option>
          <option :value="50">50 per page</option>
        </select>
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
import { useRouter, useRoute } from 'vue-router'
import { useNoteStore } from '@/store/note'
import { useApplicationStore } from '@/store/application'
import NoteItem from '@/components/notes/NoteItem.vue'

export default {
  name: 'NoteListView',
  components: {
    NoteItem
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const noteStore = useNoteStore()
    const applicationStore = useApplicationStore()
    
    // Local state
    const searchQuery = ref('')
    const selectedApplication = ref('')
    const dateFrom = ref('')
    const dateTo = ref('')
    const itemsPerPage = ref(10)
    const searchTimeout = ref(null)
    const showDeleteModal = ref(false)
    const deletingNote = ref(false)
    const noteToDelete = ref(null)
    const applications = ref([])
    
    // Computed properties
    const notes = computed(() => noteStore.notes)
    const loading = computed(() => noteStore.loading)
    const error = computed(() => noteStore.error)
    const hasNotes = computed(() => noteStore.hasNotes)
    const paginationInfo = computed(() => noteStore.getPaginationInfo)
    const hasActiveFilters = computed(() => searchQuery.value || selectedApplication.value || dateFrom.value || dateTo.value)
    
    // Methods
    const fetchNotes = async () => {
      try {
        await noteStore.fetchNotes()
      } catch (error) {
        console.error('Error fetching notes:', error)
      }
    }
    
    const fetchApplications = async () => {
      try {
        const response = await applicationStore.fetchApplications()
        applications.value = response.results || []
      } catch (error) {
        console.error('Error fetching applications:', error)
      }
    }
    
    const navigateToDetail = (id) => {
      router.push({ name: 'note-detail', params: { id } })
    }
    
    const navigateToCreate = () => {
      router.push({ name: 'note-create' })
    }
    
    const navigateToEdit = (id) => {
      router.push({ name: 'note-edit', params: { id } })
    }
    
    const navigateToApplication = (id) => {
      router.push({ name: 'application-detail', params: { id } })
    }
    
    const navigateToBorrower = (id) => {
      router.push({ name: 'borrower-detail', params: { id } })
    }
    
    const debounceSearch = () => {
      clearTimeout(searchTimeout.value)
      searchTimeout.value = setTimeout(() => {
        applyFilters()
      }, 300)
    }
    
    const applyFilters = () => {
      noteStore.setFilters({
        search: searchQuery.value,
        application: selectedApplication.value,
        dateFrom: dateFrom.value,
        dateTo: dateTo.value
      })
    }
    
    const clearFilters = () => {
      searchQuery.value = ''
      selectedApplication.value = ''
      dateFrom.value = ''
      dateTo.value = ''
      noteStore.clearFilters()
    }
    
    const prevPage = () => {
      if (paginationInfo.value.currentPage > 1) {
        noteStore.setPage(paginationInfo.value.currentPage - 1)
      }
    }
    
    const nextPage = () => {
      if (paginationInfo.value.currentPage < paginationInfo.value.totalPages) {
        noteStore.setPage(paginationInfo.value.currentPage + 1)
      }
    }
    
    const changeItemsPerPage = () => {
      noteStore.setLimit(itemsPerPage.value)
    }
    
    const confirmDelete = (note) => {
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
      } catch (error) {
        console.error('Error deleting note:', error)
      } finally {
        deletingNote.value = false
      }
    }
    
    // Initialize with query parameters if present
    const initializeFromQuery = () => {
      if (route.query.search) {
        searchQuery.value = route.query.search
      }
      
      if (route.query.application) {
        selectedApplication.value = route.query.application
      }
      
      if (route.query.date_from) {
        dateFrom.value = route.query.date_from
      }
      
      if (route.query.date_to) {
        dateTo.value = route.query.date_to
      }
      
      // Apply filters if any query parameters were set
      if (hasActiveFilters.value) {
        applyFilters()
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      // Set initial items per page
      noteStore.setLimit(itemsPerPage.value)
      
      // Initialize from query parameters
      initializeFromQuery()
      
      // Fetch notes and applications
      fetchNotes()
      fetchApplications()
    })
    
    return {
      notes,
      loading,
      error,
      hasNotes,
      paginationInfo,
      searchQuery,
      selectedApplication,
      dateFrom,
      dateTo,
      itemsPerPage,
      hasActiveFilters,
      showDeleteModal,
      deletingNote,
      applications,
      fetchNotes,
      navigateToDetail,
      navigateToCreate,
      navigateToEdit,
      navigateToApplication,
      navigateToBorrower,
      debounceSearch,
      applyFilters,
      clearFilters,
      prevPage,
      nextPage,
      changeItemsPerPage,
      confirmDelete,
      deleteNote
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
