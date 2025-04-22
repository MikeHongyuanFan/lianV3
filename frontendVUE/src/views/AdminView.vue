<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Admin Dashboard</h1>
    
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold mb-4">User Management</h2>
      
      <div class="overflow-x-auto">
        <table class="min-w-full bg-white">
          <thead>
            <tr>
              <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Role
              </th>
              <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="4" class="py-4 px-4 text-center">Loading users...</td>
            </tr>
            <tr v-else-if="users.length === 0">
              <td colspan="4" class="py-4 px-4 text-center">No users found</td>
            </tr>
            <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
              <td class="py-2 px-4 border-b border-gray-200">
                {{ user.first_name }} {{ user.last_name }}
              </td>
              <td class="py-2 px-4 border-b border-gray-200">
                {{ user.email }}
              </td>
              <td class="py-2 px-4 border-b border-gray-200">
                <span 
                  :class="{
                    'px-2 py-1 text-xs rounded-full': true,
                    'bg-blue-100 text-blue-800': user.role === 'admin',
                    'bg-green-100 text-green-800': user.role === 'broker',
                    'bg-purple-100 text-purple-800': user.role === 'bd',
                    'bg-gray-100 text-gray-800': user.role === 'client'
                  }"
                >
                  {{ user.role }}
                </span>
              </td>
              <td class="py-2 px-4 border-b border-gray-200">
                <button 
                  class="text-blue-600 hover:text-blue-900 mr-2"
                  @click="editUser(user)"
                >
                  Edit
                </button>
                <button 
                  class="text-red-600 hover:text-red-900"
                  @click="deleteUser(user.id)"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const users = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await api.get('/users/')
    users.value = response
  } catch (error) {
    console.error('Error fetching users:', error)
  } finally {
    loading.value = false
  }
})

function editUser(user) {
  // Implement edit user functionality
  console.log('Edit user:', user)
}

async function deleteUser(userId) {
  if (!confirm('Are you sure you want to delete this user?')) {
    return
  }
  
  try {
    await api.delete(`/users/${userId}/`)
    users.value = users.value.filter(user => user.id !== userId)
  } catch (error) {
    console.error('Error deleting user:', error)
  }
}
</script>
