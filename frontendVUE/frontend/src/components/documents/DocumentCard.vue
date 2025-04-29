<template>
  <div 
    class="document-card bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer"
    @click="$emit('click')"
  >
    <div class="flex justify-between items-start">
      <h3 class="text-lg font-semibold">{{ document.title }}</h3>
      <span
        v-if="document.document_type"
        class="document-type-badge px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800"
      >
        {{ formatDocumentType(document.document_type_display || document.document_type) }}
      </span>
    </div>
    
    <p v-if="document.description" class="mt-2 text-gray-600 line-clamp-2">
      {{ document.description }}
    </p>
    
    <div class="mt-3 text-sm text-gray-500">
      <div class="flex items-center">
        <span class="material-icons text-sm mr-2">description</span>
        {{ document.file_name }}
      </div>
      <div class="flex items-center">
        <span class="material-icons text-sm mr-2">straighten</span>
        {{ formatFileSize(document.file_size) }}
      </div>
      <div class="flex items-center">
        <span class="material-icons text-sm mr-2">person</span>
        {{ document.created_by_name }}
      </div>
    </div>
    
    <div class="mt-3 text-xs text-gray-500">
      Uploaded: {{ formatDate(document.created_at) }}
      <span v-if="document.version > 1" class="ml-2 px-2 py-0.5 bg-gray-100 rounded-full">
        Version {{ document.version }}
      </span>
    </div>
    
    <div v-if="showActions" class="mt-3 flex justify-end space-x-2">
      <button 
        @click.stop="$emit('download')" 
        class="text-blue-600 hover:text-blue-800"
        title="Download document"
      >
        <span class="material-icons">download</span>
      </button>
      <button 
        v-if="canEdit" 
        @click.stop="$emit('edit')" 
        class="text-blue-600 hover:text-blue-800"
        title="Edit document"
      >
        <span class="material-icons">edit</span>
      </button>
      <button 
        v-if="canDelete" 
        @click.stop="$emit('delete')" 
        class="text-red-600 hover:text-red-800"
        title="Delete document"
      >
        <span class="material-icons">delete</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DocumentCard',
  props: {
    document: {
      type: Object,
      required: true
    },
    showActions: {
      type: Boolean,
      default: false
    },
    canEdit: {
      type: Boolean,
      default: false
    },
    canDelete: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click', 'download', 'edit', 'delete'],
  setup() {
    const formatDocumentType = (type) => {
      if (!type) return 'Unknown'
      
      // If it's already formatted (from document_type_display), return as is
      if (type.includes(' ')) return type
      
      // Convert snake_case to Title Case
      return type
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    const formatFileSize = (bytes) => {
      if (!bytes) return 'Unknown size'
      
      const units = ['B', 'KB', 'MB', 'GB']
      let size = bytes
      let unitIndex = 0
      
      while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024
        unitIndex++
      }
      
      return `${size.toFixed(1)} ${units[unitIndex]}`
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Unknown'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
    
    return {
      formatDocumentType,
      formatFileSize,
      formatDate
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
