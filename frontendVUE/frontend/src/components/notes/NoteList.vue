<template>
  <div class="note-list">
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="loader"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
      <button @click="fetchNotes" class="underline">Try again</button>
    </div>
    
    <!-- Empty state -->
    <div v-else-if="!notes.length" class="text-center py-8 bg-gray-50 rounded-lg">
      <p class="text-gray-500 mb-4">No notes found</p>
      <button
        v-if="showCreateButton"
        @click="$emit('create')"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
      >
        Create Note
      </button>
    </div>
    
    <!-- Notes list -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <NoteItem
        v-for="note in notes"
        :key="note.id"
        :note="note"
        :show-actions="showActions"
        @edit="$emit('edit', note.id)"
        @delete="$emit('delete', note)"
        @view-application="$emit('view-application', $event)"
        @view-borrower="$emit('view-borrower', $event)"
        @click="$emit('view', note.id)"
      />
    </div>
    
    <!-- Pagination -->
    <div v-if="notes.length && showPagination" class="pagination-container flex justify-between items-center mt-6">
      <div class="text-sm text-gray-500">
        Showing {{ currentPage * itemsPerPage - itemsPerPage + 1 }} 
        to {{ Math.min(currentPage * itemsPerPage, totalItems) }} 
        of {{ totalItems }} notes
      </div>
      
      <div class="flex items-center space-x-2">
        <button
          @click="$emit('prev-page')"
          :disabled="currentPage === 1"
          class="px-3 py-1 border rounded-md"
          :class="currentPage === 1 ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'"
        >
          Previous
        </button>
        
        <span class="px-3 py-1">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        
        <button
          @click="$emit('next-page')"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 border rounded-md"
          :class="currentPage === totalPages ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import NoteItem from '@/components/notes/NoteItem.vue'

export default {
  name: 'NoteList',
  components: {
    NoteItem
  },
  props: {
    notes: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    },
    showActions: {
      type: Boolean,
      default: true
    },
    showCreateButton: {
      type: Boolean,
      default: true
    },
    showPagination: {
      type: Boolean,
      default: true
    },
    currentPage: {
      type: Number,
      default: 1
    },
    totalPages: {
      type: Number,
      default: 1
    },
    itemsPerPage: {
      type: Number,
      default: 10
    },
    totalItems: {
      type: Number,
      default: 0
    }
  },
  emits: [
    'create', 
    'edit', 
    'delete', 
    'view', 
    'view-application', 
    'view-borrower', 
    'prev-page', 
    'next-page',
    'fetch'
  ],
  setup(props, { emit }) {
    const fetchNotes = () => {
      emit('fetch')
    }
    
    return {
      fetchNotes
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
