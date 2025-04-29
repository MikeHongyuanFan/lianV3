import { defineStore } from 'pinia'
import noteService from '@/services/note.service'

export const useNoteStore = defineStore('note', {
  state: () => ({
    notes: [],
    currentNote: null,
    totalNotes: 0,
    loading: false,
    error: null,
    filters: {
      search: '',
      application: null,
      dateFrom: '',
      dateTo: ''
    },
    pagination: {
      limit: 10,
      offset: 0
    }
  }),

  getters: {
    getNoteById: (state) => (id) => {
      return state.notes.find(note => note.id === parseInt(id)) || null
    },
    
    getFilteredNotes: (state) => {
      return state.notes
    },
    
    getPaginationInfo: (state) => {
      return {
        currentPage: Math.floor(state.pagination.offset / state.pagination.limit) + 1,
        totalPages: Math.ceil(state.totalNotes / state.pagination.limit),
        totalItems: state.totalNotes,
        itemsPerPage: state.pagination.limit
      }
    },
    
    hasNotes: (state) => {
      return state.notes.length > 0
    }
  },

  actions: {
    async fetchNotes() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          limit: this.pagination.limit,
          offset: this.pagination.offset,
          search: this.filters.search || undefined,
          application: this.filters.application || undefined,
          date_from: this.filters.dateFrom || undefined,
          date_to: this.filters.dateTo || undefined
        }
        
        const response = await noteService.getNotes(params)
        this.notes = response.results
        this.totalNotes = response.count
        return response
      } catch (error) {
        this.error = error.message || 'Failed to fetch notes'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchNoteById(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await noteService.getNoteById(id)
        this.currentNote = response
        return response
      } catch (error) {
        this.error = error.message || `Failed to fetch note with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createNote(noteData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await noteService.createNote(noteData)
        // Refresh notes list after creation
        await this.fetchNotes()
        return response
      } catch (error) {
        this.error = error.message || 'Failed to create note'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateNote(id, noteData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await noteService.updateNote(id, noteData)
        
        // Update the note in the list if it exists
        const index = this.notes.findIndex(note => note.id === parseInt(id))
        if (index !== -1) {
          this.notes[index] = { ...this.notes[index], ...response }
        }
        
        // Update current note if it's the one being edited
        if (this.currentNote && this.currentNote.id === parseInt(id)) {
          this.currentNote = { ...this.currentNote, ...response }
        }
        
        return response
      } catch (error) {
        this.error = error.message || `Failed to update note with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteNote(id) {
      this.loading = true
      this.error = null
      
      try {
        await noteService.deleteNote(id)
        
        // Remove the note from the list
        this.notes = this.notes.filter(note => note.id !== parseInt(id))
        
        // Clear current note if it's the one being deleted
        if (this.currentNote && this.currentNote.id === parseInt(id)) {
          this.currentNote = null
        }
        
        // Refresh the list to update counts
        await this.fetchNotes()
      } catch (error) {
        this.error = error.message || `Failed to delete note with ID ${id}`
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // Pagination and filtering actions
    setPage(page) {
      const offset = (page - 1) * this.pagination.limit
      this.pagination.offset = offset
      this.fetchNotes()
    },
    
    setLimit(limit) {
      this.pagination.limit = limit
      this.pagination.offset = 0 // Reset to first page
      this.fetchNotes()
    },
    
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.offset = 0 // Reset to first page
      this.fetchNotes()
    },
    
    clearFilters() {
      this.filters = {
        search: '',
        application: null,
        dateFrom: '',
        dateTo: ''
      }
      this.fetchNotes()
    }
  }
})
