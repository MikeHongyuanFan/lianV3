<template>
  <div class="user-list-container">
    <header class="bg-gray-800 text-white py-4 mb-6">
      <div class="container mx-auto px-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold">User Management</h1>
          <router-link to="/admin/users/create" class="btn btn-primary">
            <i class="bi bi-plus-circle mr-2"></i> Add User
          </router-link>
        </div>
      </div>
    </header>

    <main class="container mx-auto px-4">
      <!-- Search and filters -->
      <div class="bg-white rounded-lg shadow p-4 mb-6">
        <div class="flex flex-wrap gap-4">
          <div class="flex-1 min-w-[200px]">
            <label for="search" class="form-label">Search</label>
            <div class="relative">
              <input
                id="search"
                v-model="searchTerm"
                type="text"
                placeholder="Search by name or email"
                class="form-input pl-10"
                @input="debouncedSearch"
              />
              <i class="bi bi-search absolute left-3 top-2.5 text-gray-400"></i>
            </div>
          </div>
          
          <div class="w-full sm:w-auto">
            <label for="role-filter" class="form-label">Role</label>
            <select
              id="role-filter"
              v-model="roleFilter"
              class="form-input"
              @change="loadUsers"
            >
              <option value="">All Roles</option>
              <option value="admin">Admin</option>
              <option value="broker">Broker</option>
              <option value="bd">Business Development</option>
              <option value="client">Client</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <p class="mt-2 text-gray-600">Loading users...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="bg-danger-100 border border-danger-300 text-danger-700 px-4 py-3 rounded mb-6">
        <p>{{ error.message }}</p>
        <button @click="loadUsers" class="text-danger-800 underline mt-2">Try again</button>
      </div>

      <!-- Empty state -->
      <div v-else-if="users.length === 0" class="text-center py-8 bg-white rounded-lg shadow">
        <i class="bi bi-people text-4xl text-gray-400"></i>
        <p class="mt-2 text-gray-600">No users found</p>
        <p class="text-gray-500 text-sm">Try adjusting your search or filters</p>
      </div>

      <!-- User list -->
      <div v-else class="bg-white rounded-lg shadow overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in users" :key="user.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center text-primary-700">
                    {{ user.first_name?.[0] || '' }}{{ user.last_name?.[0] || '' }}
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ user.first_name }} {{ user.last_name }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ user.email }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="{
                    'bg-blue-100 text-blue-800': user.role === 'admin',
                    'bg-green-100 text-green-800': user.role === 'broker',
                    'bg-purple-100 text-purple-800': user.role === 'bd',
                    'bg-yellow-100 text-yellow-800': user.role === 'client'
                  }"
                >
                  {{ user.role }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <router-link :to="`/admin/users/${user.id}`" class="text-primary-600 hover:text-primary-900 mr-3">
                  <i class="bi bi-pencil"></i> Edit
                </router-link>
                <button 
                  @click="confirmDelete(user)" 
                  class="text-danger-600 hover:text-danger-900"
                  :disabled="user.id === currentUserId"
                >
                  <i class="bi bi-trash"></i> Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalUsers > 0" class="mt-6 flex justify-between items-center">
        <div class="text-sm text-gray-700">
          Showing <span class="font-medium">{{ startIndex + 1 }}</span> to 
          <span class="font-medium">{{ Math.min(endIndex, totalUsers) }}</span> of 
          <span class="font-medium">{{ totalUsers }}</span> users
        </div>
        <div class="flex space-x-2">
          <button 
            @click="prevPage" 
            class="btn btn-secondary btn-sm"
            :disabled="currentPage === 1"
          >
            Previous
          </button>
          <button 
            @click="nextPage" 
            class="btn btn-secondary btn-sm"
            :disabled="currentPage >= totalPages"
          >
            Next
          </button>
        </div>
      </div>
    </main>

    <!-- Delete confirmation modal -->
    <BaseModal
      v-model="showDeleteModal"
      title="Confirm Delete"
      :show-default-footer="true"
      confirm-text="Delete"
      cancel-text="Cancel"
      @confirm="deleteUser"
    >
      <p>Are you sure you want to delete the user <strong>{{ userToDelete?.first_name }} {{ userToDelete?.last_name }}</strong>?</p>
      <p class="text-danger-600 mt-2">This action cannot be undone.</p>
    </BaseModal>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import BaseModal from '@/components/BaseModal.vue'
import { UserProfile } from '@/types/auth'

export default defineComponent({
  name: 'UserListView',
  components: {
    BaseModal
  },
  setup() {
    const authStore = useAuthStore()
    
    // State
    const users = ref<UserProfile[]>([])
    const totalUsers = ref(0)
    const loading = ref(false)
    const error = ref(null)
    const searchTerm = ref('')
    const roleFilter = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const showDeleteModal = ref(false)
    const userToDelete = ref<UserProfile | null>(null)
    
    // Computed properties
    const startIndex = computed(() => (currentPage.value - 1) * pageSize.value)
    const endIndex = computed(() => startIndex.value + pageSize.value)
    const totalPages = computed(() => Math.ceil(totalUsers.value / pageSize.value))
    const currentUserId = computed(() => authStore.userId)
    
    // Methods
    const loadUsers = async () => {
      loading.value = true
      error.value = null
      
      try {
        const offset = (currentPage.value - 1) * pageSize.value
        const response = await authStore.getUsers(
          pageSize.value,
          offset,
          searchTerm.value,
          roleFilter.value
        )
        
        users.value = response.results
        totalUsers.value = response.count
      } catch (err: any) {
        error.value = err
        console.error('Error loading users:', err)
      } finally {
        loading.value = false
      }
    }
    
    // Debounced search
    let searchTimeout: number | null = null
    const debouncedSearch = () => {
      if (searchTimeout) {
        clearTimeout(searchTimeout)
      }
      
      searchTimeout = window.setTimeout(() => {
        currentPage.value = 1 // Reset to first page on search
        loadUsers()
      }, 300)
    }
    
    // Pagination methods
    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
        loadUsers()
      }
    }
    
    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
        loadUsers()
      }
    }
    
    // Delete user methods
    const confirmDelete = (user: UserProfile) => {
      userToDelete.value = user
      showDeleteModal.value = true
    }
    
    const deleteUser = async () => {
      if (!userToDelete.value) return
      
      loading.value = true
      try {
        await authStore.deleteUser(userToDelete.value.id)
        loadUsers() // Reload the user list
      } catch (err: any) {
        error.value = err
        console.error('Error deleting user:', err)
      } finally {
        loading.value = false
        showDeleteModal.value = false
        userToDelete.value = null
      }
    }
    
    // Load users on component mount
    onMounted(loadUsers)
    
    return {
      users,
      totalUsers,
      loading,
      error,
      searchTerm,
      roleFilter,
      currentPage,
      startIndex,
      endIndex,
      totalPages,
      currentUserId,
      showDeleteModal,
      userToDelete,
      loadUsers,
      debouncedSearch,
      nextPage,
      prevPage,
      confirmDelete,
      deleteUser
    }
  }
})
</script>