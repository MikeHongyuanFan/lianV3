<template>
  <div 
    class="note-item bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow"
    :class="{ 'border-l-4 border-yellow-400': hasReminder }"
  >
    <div class="flex justify-between items-start">
      <h3 class="text-lg font-semibold">{{ note.title || 'Untitled Note' }}</h3>
      <div class="flex space-x-2">
        <button 
          v-if="showActions"
          @click.stop="$emit('edit')" 
          class="text-blue-600 hover:text-blue-800"
          title="Edit note"
        >
          <span class="material-icons text-sm">edit</span>
        </button>
        <button 
          v-if="showActions"
          @click.stop="$emit('delete')" 
          class="text-red-600 hover:text-red-800"
          title="Delete note"
        >
          <span class="material-icons text-sm">delete</span>
        </button>
      </div>
    </div>
    
    <div class="mt-2">
      <p class="text-gray-700 whitespace-pre-line">{{ note.content }}</p>
    </div>
    
    <div class="mt-3 text-sm text-gray-500 flex justify-between items-center">
      <div>
        <span>By {{ note.created_by_name }}</span>
        <span class="mx-1">•</span>
        <span>{{ formatDate(note.created_at) }}</span>
      </div>
      
      <div v-if="hasReminder" class="flex items-center text-yellow-600">
        <span class="material-icons text-sm mr-1">notifications</span>
        <span>{{ formatReminderDate(note.remind_date) }}</span>
      </div>
    </div>
    
    <div v-if="note.application" class="mt-2 text-xs text-gray-500">
      <span class="flex items-center">
        <span class="material-icons text-xs mr-1">description</span>
        <span>
          Application: 
          <button 
            @click.stop="$emit('view-application', note.application)" 
            class="text-blue-600 hover:underline"
          >
            View
          </button>
        </span>
      </span>
    </div>
    
    <div v-if="note.borrower" class="mt-1 text-xs text-gray-500">
      <span class="flex items-center">
        <span class="material-icons text-xs mr-1">person</span>
        <span>
          Borrower: 
          <button 
            @click.stop="$emit('view-borrower', note.borrower)" 
            class="text-blue-600 hover:underline"
          >
            View
          </button>
        </span>
      </span>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'NoteItem',
  props: {
    note: {
      type: Object,
      required: true
    },
    showActions: {
      type: Boolean,
      default: false
    }
  },
  emits: ['edit', 'delete', 'view-application', 'view-borrower'],
  setup(props) {
    const hasReminder = computed(() => {
      return !!props.note.remind_date
    })
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Unknown'
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
    
    const formatReminderDate = (dateString) => {
      if (!dateString) return ''
      
      const reminderDate = new Date(dateString)
      const now = new Date()
      
      // Check if reminder is in the past
      if (reminderDate < now) {
        return 'Reminder passed'
      }
      
      // Check if reminder is today
      if (
        reminderDate.getDate() === now.getDate() &&
        reminderDate.getMonth() === now.getMonth() &&
        reminderDate.getFullYear() === now.getFullYear()
      ) {
        return `Today at ${reminderDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
      }
      
      // Check if reminder is tomorrow
      const tomorrow = new Date(now)
      tomorrow.setDate(tomorrow.getDate() + 1)
      if (
        reminderDate.getDate() === tomorrow.getDate() &&
        reminderDate.getMonth() === tomorrow.getMonth() &&
        reminderDate.getFullYear() === tomorrow.getFullYear()
      ) {
        return `Tomorrow at ${reminderDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
      }
      
      // Otherwise show full date
      return `Reminder: ${reminderDate.toLocaleDateString()}`
    }
    
    return {
      hasReminder,
      formatDate,
      formatReminderDate
    }
  }
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
