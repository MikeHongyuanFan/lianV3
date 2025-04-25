<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Notes & Reminders</h2>
      <button 
        @click="showAddNoteForm = !showAddNoteForm" 
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {{ showAddNoteForm ? 'Cancel' : 'Add Note' }}
      </button>
    </div>
    
    <!-- Add Note Form -->
    <div v-if="showAddNoteForm" class="bg-gray-50 p-4 rounded-md mb-6">
      <h3 class="text-lg font-medium mb-3">Add New Note</h3>
      
      <form @submit.prevent="addNote" class="space-y-4">
        <div>
          <label for="content" class="block text-sm font-medium text-gray-700">Note Content</label>
          <textarea 
            id="content" 
            v-model="newNote.content"
            rows="4"
            class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            required
          ></textarea>
        </div>
        
        <div>
          <div class="flex items-center">
            <input 
              type="checkbox" 
              id="set_reminder" 
              v-model="newNote.has_reminder"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label for="set_reminder" class="ml-2 block text-sm text-gray-900">
              Set Reminder
            </label>
          </div>
        </div>
        
        <div v-if="newNote.has_reminder">
          <label for="remind_date" class="block text-sm font-medium text-gray-700">Reminder Date</label>
          <input 
            type="date" 
            id="remind_date" 
            v-model="newNote.remind_date"
            class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            required
          />
        </div>
        
        <div class="flex justify-end">
          <button 
            type="submit" 
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="submitting"
          >
            <span v-if="submitting">Saving...</span>
            <span v-else>Save Note</span>
          </button>
        </div>
      </form>
    </div>
    
    <!-- Notes Timeline -->
    <div v-if="notes && notes.length > 0" class="space-y-4">
      <div v-for="note in notes" :key="note.id" class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
        <div class="p-4 bg-gray-50 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <div>
              <span class="text-sm font-medium text-gray-900">{{ note.created_by_name }}</span>
              <span class="text-sm text-gray-500 ml-2">{{ formatDate(note.created_at) }}</span>
            </div>
            <div v-if="note.remind_date" class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-yellow-500 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
              </svg>
              <span class="text-xs font-medium" :class="isReminderDue(note.remind_date) ? 'text-red-600' : 'text-yellow-600'">
                Reminder: {{ formatDate(note.remind_date) }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="p-4">
          <p class="text-sm text-gray-700 whitespace-pre-line">{{ note.content }}</p>
        </div>
      </div>
    </div>
    <div v-else class="bg-gray-50 p-4 rounded-md">
      <p class="text-sm text-gray-500">No notes added for this application</p>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import axios from 'axios'

const props = defineProps({
  notes: {
    type: Array,
    default: () => []
  },
  applicationId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['note-added'])

const showAddNoteForm = ref(false)
const submitting = ref(false)
const newNote = ref({
  content: '',
  has_reminder: false,
  remind_date: null
})

const addNote = async () => {
  submitting.value = true
  
  try {
    const noteData = {
      content: newNote.value.content,
      remind_date: newNote.value.has_reminder ? newNote.value.remind_date : null
    }
    
    await axios.post(`/api/applications/${props.applicationId}/add_note/`, noteData)
    
    // Reset form
    newNote.value = {
      content: '',
      has_reminder: false,
      remind_date: null
    }
    showAddNoteForm.value = false
    
    // Notify parent to refresh data
    emit('note-added')
    
  } catch (error) {
    console.error('Error adding note:', error)
    alert('Failed to add note. Please try again.')
  } finally {
    submitting.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const isReminderDue = (dateString) => {
  if (!dateString) return false
  const reminderDate = new Date(dateString)
  const today = new Date()
  
  // Set time to 00:00:00 for both dates to compare just the date
  reminderDate.setHours(0, 0, 0, 0)
  today.setHours(0, 0, 0, 0)
  
  return reminderDate <= today
}
</script>
