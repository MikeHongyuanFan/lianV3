<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">Borrowers & Guarantors</h2>
    
    <!-- Borrowers Section -->
    <div class="mb-8">
      <h3 class="text-lg font-medium mb-3">Borrowers</h3>
      
      <div v-if="borrowers && borrowers.length > 0">
        <div v-for="(borrower, index) in borrowers" :key="borrower.id" class="mb-4">
          <div class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
            <div class="p-4 bg-gray-50 border-b border-gray-200">
              <div class="flex justify-between items-center">
                <h4 class="text-md font-medium">
                  {{ borrower.is_company ? borrower.company_name : `${borrower.first_name} ${borrower.last_name}` }}
                </h4>
                <span class="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
                  {{ borrower.is_company ? 'Company' : 'Individual' }}
                </span>
              </div>
            </div>
            
            <div class="p-4">
              <!-- Company Borrower -->
              <div v-if="borrower.is_company">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p class="text-sm font-medium text-gray-500">Company Details</p>
                    <p class="text-sm">ABN: {{ borrower.company_abn }}</p>
                    <p class="text-sm">ACN: {{ borrower.company_acn }}</p>
                    <p class="text-sm">Business Type: {{ borrower.business_type }}</p>
                    <p class="text-sm">Years in Business: {{ borrower.years_in_business }}</p>
                    <p class="text-sm">Industry: {{ borrower.industry }}</p>
                  </div>
                  
                  <div>
                    <p class="text-sm font-medium text-gray-500">Registered Address</p>
                    <p class="text-sm">
                      {{ borrower.registered_address.street }}<br>
                      {{ borrower.registered_address.city }}, {{ borrower.registered_address.state }} {{ borrower.registered_address.postal_code }}<br>
                      {{ borrower.registered_address.country }}
                    </p>
                  </div>
                </div>
                
                <div class="mt-4">
                  <p class="text-sm font-medium text-gray-500">Financial Information</p>
                  <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                    <div>
                      <p class="text-xs text-gray-500">Annual Revenue</p>
                      <p class="text-sm">${{ formatCurrency(borrower.financial_info.annual_revenue) }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Net Profit</p>
                      <p class="text-sm">${{ formatCurrency(borrower.financial_info.net_profit) }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Assets</p>
                      <p class="text-sm">${{ formatCurrency(borrower.financial_info.assets) }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Liabilities</p>
                      <p class="text-sm">${{ formatCurrency(borrower.financial_info.liabilities) }}</p>
                    </div>
                  </div>
                </div>
                
                <div class="mt-4">
                  <p class="text-sm font-medium text-gray-500">Directors</p>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-2 mt-1">
                    <div v-for="(director, idx) in borrower.directors" :key="idx" class="bg-gray-50 p-2 rounded">
                      <p class="text-sm">{{ director.first_name }} {{ director.last_name }}</p>
                      <p class="text-xs text-gray-500">{{ director.email }}</p>
                      <p class="text-xs text-gray-500">{{ director.phone }}</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Individual Borrower -->
              <div v-else>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p class="text-sm font-medium text-gray-500">Contact Information</p>
                    <p class="text-sm">Email: {{ borrower.email }}</p>
                    <p class="text-sm">Phone: {{ borrower.phone }}</p>
                    <p class="text-sm">Date of Birth: {{ formatDate(borrower.dob) }}</p>
                    <p class="text-sm">Tax ID: {{ borrower.tax_id }}</p>
                    <p class="text-sm">Marital Status: {{ borrower.marital_status }}</p>
                    <p class="text-sm">Residency Status: {{ borrower.residency_status }}</p>
                  </div>
                  
                  <div>
                    <p class="text-sm font-medium text-gray-500">Address</p>
                    <p class="text-sm">
                      {{ borrower.address.street }}<br>
                      {{ borrower.address.city }}, {{ borrower.address.state }} {{ borrower.address.postal_code }}<br>
                      {{ borrower.address.country }}
                    </p>
                  </div>
                </div>
                
                <div class="mt-4">
                  <p class="text-sm font-medium text-gray-500">Employment Information</p>
                  <p class="text-sm">Employer: {{ borrower.employment_info.employer }}</p>
                  <p class="text-sm">Position: {{ borrower.employment_info.position }}</p>
                  <p class="text-sm">Income: ${{ formatCurrency(borrower.employment_info.income) }}</p>
                  <p class="text-sm">Years Employed: {{ borrower.employment_info.years_employed }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="bg-gray-50 p-4 rounded-md">
        <p class="text-sm text-gray-500">No borrowers associated with this application</p>
      </div>
    </div>
    
    <!-- Guarantors Section -->
    <div>
      <h3 class="text-lg font-medium mb-3">Guarantors</h3>
      
      <div v-if="guarantors && guarantors.length > 0">
        <div v-for="(guarantor, index) in guarantors" :key="guarantor.id" class="mb-4">
          <div class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
            <div class="p-4 bg-gray-50 border-b border-gray-200">
              <div class="flex justify-between items-center">
                <h4 class="text-md font-medium">
                  {{ guarantor.first_name }} {{ guarantor.last_name }}
                </h4>
                <span class="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">
                  {{ guarantor.guarantor_type }} Guarantor
                </span>
              </div>
            </div>
            
            <div class="p-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p class="text-sm font-medium text-gray-500">Contact Information</p>
                  <p class="text-sm">Email: {{ guarantor.email }}</p>
                  <p class="text-sm">Phone: {{ guarantor.phone }}</p>
                  <p class="text-sm">Date of Birth: {{ formatDate(guarantor.dob) }}</p>
                  <p class="text-sm">Relationship to Borrower: {{ guarantor.relationship_to_borrower }}</p>
                </div>
                
                <div>
                  <p class="text-sm font-medium text-gray-500">Address</p>
                  <p class="text-sm">
                    {{ guarantor.address.street }}<br>
                    {{ guarantor.address.city }}, {{ guarantor.address.state }} {{ guarantor.address.postal_code }}<br>
                    {{ guarantor.address.country }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="bg-gray-50 p-4 rounded-md">
        <p class="text-sm text-gray-500">No guarantors associated with this application</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  borrowers: {
    type: Array,
    default: () => []
  },
  guarantors: {
    type: Array,
    default: () => []
  }
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US').format(value)
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}
</script>
