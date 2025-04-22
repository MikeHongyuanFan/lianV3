<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Broker Dashboard</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">My Applications</h2>
        
        <div v-if="loading" class="py-4 text-center">
          Loading applications...
        </div>
        
        <div v-else-if="applications.length === 0" class="py-4 text-center">
          No applications found. Create your first application!
        </div>
        
        <ul v-else class="divide-y divide-gray-200">
          <li v-for="app in applications" :key="app.id" class="py-4">
            <div class="flex justify-between">
              <div>
                <p class="font-medium">{{ app.reference_number }}</p>
                <p class="text-sm text-gray-500">
                  ${{ app.loan_amount }} - {{ app.purpose }}
                </p>
              </div>
              <div>
                <span 
                  :class="{
                    'px-2 py-1 text-xs rounded-full': true,
                    'bg-yellow-100 text-yellow-800': app.stage === 'inquiry',
                    'bg-blue-100 text-blue-800': app.stage === 'application',
                    'bg-purple-100 text-purple-800': app.stage === 'assessment',
                    'bg-green-100 text-green-800': app.stage === 'approved',
                    'bg-red-100 text-red-800': app.stage === 'declined'
                  }"
                >
                  {{ app.stage }}
                </span>
              </div>
            </div>
          </li>
        </ul>
        
        <div class="mt-4">
          <button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
            New Application
          </button>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">My Borrowers</h2>
        
        <div v-if="loadingBorrowers" class="py-4 text-center">
          Loading borrowers...
        </div>
        
        <div v-else-if="borrowers.length === 0" class="py-4 text-center">
          No borrowers found.
        </div>
        
        <ul v-else class="divide-y divide-gray-200">
          <li v-for="borrower in borrowers" :key="borrower.id" class="py-4">
            <div class="flex justify-between">
              <div>
                <p class="font-medium">{{ borrower.first_name }} {{ borrower.last_name }}</p>
                <p class="text-sm text-gray-500">
                  {{ borrower.email }} - {{ borrower.phone }}
                </p>
              </div>
              <div>
                <button class="text-blue-600 hover:text-blue-900">
                  View
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const applications = ref([])
const borrowers = ref([])
const loading = ref(true)
const loadingBorrowers = ref(true)

onMounted(async () => {
  try {
    // In a real app, these would be filtered by the broker's ID
    const appResponse = await api.get('/applications/')
    applications.value = appResponse
  } catch (error) {
    console.error('Error fetching applications:', error)
  } finally {
    loading.value = false
  }
  
  try {
    const borrowerResponse = await api.get('/borrowers/')
    borrowers.value = borrowerResponse
  } catch (error) {
    console.error('Error fetching borrowers:', error)
  } finally {
    loadingBorrowers.value = false
  }
})
</script>
