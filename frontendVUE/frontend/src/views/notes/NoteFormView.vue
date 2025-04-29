<template>
  <div class="note-form-container">
    <h1 class="text-2xl font-bold mb-6">{{ isEditing ? 'Edit Note' : 'Create New Note' }}</h1>
    
    <!-- Error alert -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p class="font-bold">Error</p>
      <p>{{ error }}</p>
    </div>
    
    <!-- Note form -->
    <form @submit.prevent="submitForm" class="bg-white rounded-lg shadow-md p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Title -->
        <div class="form-group">
          <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Title</label>
          <input
            id="title"
            v-model="noteForm.title"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.title }"
          />
          <p v-if="validationErrors.title" class="mt-1 text-sm text-red-600">{{ validationErrors.title }}</p>
        </div>
        
        <!-- Reminder Date -->
        <div class="form-group">
          <label for="remind_date" class="block text-sm font-medium text-gray-700 mb-1">Reminder Date</label>
          <input
            id="remind_date"
            v-model="noteForm.remind_date"
            type="datetime-local"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.remind_date }"
          />
          <p v-if="validationErrors.remind_date" class="mt-1 text-sm text-red-600">{{ validationErrors.remind_date }}</p>
        </div>
        
        <!-- Content -->
        <div class="col-span-2">
          <label for="content" class="block text-sm font-medium text-gray-700 mb-1">Content *</label>
          <textarea
            id="content"
            v-model="noteForm.content"
            rows="6"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.content }"
            required
          ></textarea>
          <p v-if="validationErrors.content" class="mt-1 text-sm text-red-600">{{ validationErrors.content }}</p>
        </div>
        
        <!-- Related Entities -->
        <div class="col-span-2">
          <h2 class="text-lg font-semibold mb-4">Related Information</h2>
        </div>
        
        <!-- Application -->
        <div class="form-group">
          <label for="application" class="block text-sm font-medium text-gray-700 mb-1">Related Application</label>
          <select
            id="application"
            v-model="noteForm.application"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.application }"
          >
            <option value="">None</option>
            <option v-for="app in applications" :key="app.id" :value="app.id">
              {{ app.reference_number }} - {{ app.purpose }}
            </option>
          </select>
          <p v-if="validationErrors.application" class="mt-1 text-sm text-red-600">{{ validationErrors.application }}</p>
        </div>
        
        <!-- Borrower -->
        <div class="form-group">
          <label for="borrower" class="block text-sm font-medium text-gray-700 mb-1">Related Borrower</label>
          <select
            id="borrower"
            v-model="noteForm.borrower"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.borrower }"
          >
            <option value="">None</option>
            <option v-for="borrower in borrowers" :key="borrower.id" :value="borrower.id">
              {{ borrower.first_name }} {{ borrower.last_name }}
            </option>
          </select>
          <p v-if="validationErrors.borrower" class="mt-1 text-sm text-red-600">{{ validationErrors.borrower }}</p>
        </div>
      </div>
      
      <!-- Form Actions -->
      <div class="mt-6 flex justify-end space-x-3">
        <button
          type="button"
          @click="navigateBack"
          class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
        >
          Cancel
        </button>
        <button
          type="submit"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
          :disabled="loading"
        >
          {{ loading ? 'Saving...' : (isEditing ? 'Update Note' : 'Create Note') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNoteStore } from '@/store/note'
import { useApplicationStore } from '@/store/application'
import { useBorrowerStore } from '@/store/borrower'

export default {
  name: 'NoteFormView',
  props: {
    id: {
      type: [Number, String],
      default: null
    },
    isEditing: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const route = useRoute()
    const router = useRouter()
    const noteStore = useNoteStore()
    const applicationStore = useApplicationStore()
    const borrowerStore = useBorrowerStore()
    
    // Local state
    const noteId = ref(props.id ? parseInt(props.id) : null)
    const validationErrors = ref({})
    const applications = ref([])
    const borrowers = ref([])
    
    // Form data
    const noteForm = reactive({
      title: '',
      content: '',
      application: '',
      borrower: '',
      remind_date: ''
    })
    
    // Computed properties
    const note = computed(() => noteStore.currentNote)
    const loading = computed(() => noteStore.loading)
    const error = computed(() => noteStore.error)
    
    // Methods
    const fetchNoteData = async () => {
      if (!noteId.value) return
      
      try {
        await noteStore.fetchNoteById(noteId.value)
        
        // Populate form with note data
        noteForm.title = note.value.title || ''
        noteForm.content = note.value.content || ''
        noteForm.application = note.value.application || ''
        noteForm.borrower = note.value.borrower || ''
        
        // Format remind_date for datetime-local input
        if (note.value.remind_date) {
          const date = new Date(note.value.remind_date)
          noteForm.remind_date = formatDateTimeForInput(date)
        } else {
          noteForm.remind_date = ''
        }
      } catch (error) {
        console.error('Error fetching note:', error)
      }
    }
    
    const fetchRelatedData = async () => {
      try {
        // Fetch applications for dropdown
        const appResponse = await applicationStore.fetchApplications()
        applications.value = appResponse.results || []
        
        // Fetch borrowers for dropdown
        const borrowerResponse = await borrowerStore.fetchBorrowers()
        borrowers.value = borrowerResponse.results || []
      } catch (error) {
        console.error('Error fetching related data:', error)
      }
    }
    
    const formatDateTimeForInput = (date) => {
      if (!date) return ''
      
      // Format date as YYYY-MM-DDThh:mm
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      
      return `${year}-${month}-${day}T${hours}:${minutes}`
    }
    
    const validateForm = () => {
      const errors = {}
      
      if (!noteForm.content) {
        errors.content = 'Content is required'
      }
      
      if (noteForm.remind_date) {
        const reminderDate = new Date(noteForm.remind_date)
        if (isNaN(reminderDate.getTime())) {
          errors.remind_date = 'Invalid date format'
        }
      }
      
      validationErrors.value = errors
      return Object.keys(errors).length === 0
    }
    
    const submitForm = async () => {
      if (!validateForm()) return
      
      try {
        const noteData = {
          content: noteForm.content,
          title: noteForm.title || null,
          application: noteForm.application || null,
          borrower: noteForm.borrower || null,
          remind_date: noteForm.remind_date || null
        }
        
        if (props.isEditing) {
          await noteStore.updateNote(noteId.value, noteData)
        } else {
          await noteStore.createNote(noteData)
        }
        
        // Navigate back to note list
        router.push({ name: 'note-list' })
      } catch (error) {
        console.error('Error saving note:', error)
      }
    }
    
    const navigateBack = () => {
      if (props.isEditing && noteId.value) {
        router.push({ name: 'note-detail', params: { id: noteId.value } })
      } else {
        router.push({ name: 'note-list' })
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      // If editing, fetch note data
      if (props.isEditing && noteId.value) {
        fetchNoteData()
      }
      
      // Fetch related data for dropdowns
      fetchRelatedData()
      
      // Check for query parameters
      if (route.query.application) {
        noteForm.application = parseInt(route.query.application)
      }
      
      if (route.query.borrower) {
        noteForm.borrower = parseInt(route.query.borrower)
      }
    })
    
    return {
      note,
      loading,
      error,
      noteForm,
      validationErrors,
      applications,
      borrowers,
      submitForm,
      navigateBack
    }
  }
}
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}
</style>
