<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">Application Overview</h2>
    
    <!-- Property Information -->
    <div class="mb-6">
      <h3 class="text-lg font-medium mb-2">Property Information</h3>
      <div v-if="application.property" class="bg-gray-50 p-4 rounded-md">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p class="text-sm font-medium text-gray-500">Address</p>
            <p class="text-sm">
              {{ application.property.address.street }}<br>
              {{ application.property.address.city }}, {{ application.property.address.state }} {{ application.property.address.postal_code }}<br>
              {{ application.property.address.country }}
            </p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">Property Details</p>
            <p class="text-sm">Type: {{ application.property.property_type }}</p>
            <p class="text-sm">Estimated Value: ${{ formatCurrency(application.property.estimated_value) }}</p>
            <p class="text-sm">Purchase Price: ${{ formatCurrency(application.property.purchase_price) }}</p>
            <p class="text-sm">Security Type: {{ application.property.security_type }}</p>
          </div>
        </div>
      </div>
      <div v-else class="bg-gray-50 p-4 rounded-md">
        <p class="text-sm text-gray-500">No property information available</p>
      </div>
    </div>
    
    <!-- Valuer Information -->
    <div class="mb-6">
      <h3 class="text-lg font-medium mb-2">Valuer Information</h3>
      <div v-if="application.valuer_info" class="bg-gray-50 p-4 rounded-md">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p class="text-sm font-medium text-gray-500">Company</p>
            <p class="text-sm">{{ application.valuer_info.company_name }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">Contact</p>
            <p class="text-sm">{{ application.valuer_info.contact_name }}</p>
            <p class="text-sm">{{ application.valuer_info.phone }}</p>
            <p class="text-sm">{{ application.valuer_info.email }}</p>
          </div>
        </div>
        <div v-if="application.valuer_info.notes" class="mt-2">
          <p class="text-sm font-medium text-gray-500">Notes</p>
          <p class="text-sm">{{ application.valuer_info.notes }}</p>
        </div>
      </div>
      <div v-else class="bg-gray-50 p-4 rounded-md">
        <p class="text-sm text-gray-500">No valuer information available</p>
      </div>
    </div>
    
    <!-- QS Information -->
    <div class="mb-6">
      <h3 class="text-lg font-medium mb-2">Quantity Surveyor Information</h3>
      <div v-if="application.qs_info && application.qs_info.company_name" class="bg-gray-50 p-4 rounded-md">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p class="text-sm font-medium text-gray-500">Company</p>
            <p class="text-sm">{{ application.qs_info.company_name }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">Contact</p>
            <p class="text-sm">{{ application.qs_info.contact_name }}</p>
            <p class="text-sm">{{ application.qs_info.phone }}</p>
            <p class="text-sm">{{ application.qs_info.email }}</p>
          </div>
        </div>
        <div v-if="application.qs_info.notes" class="mt-2">
          <p class="text-sm font-medium text-gray-500">Notes</p>
          <p class="text-sm">{{ application.qs_info.notes }}</p>
        </div>
      </div>
      <div v-else class="bg-gray-50 p-4 rounded-md">
        <p class="text-sm text-gray-500">No quantity surveyor information available</p>
      </div>
    </div>
    
    <!-- Signature Information -->
    <div class="mb-6">
      <h3 class="text-lg font-medium mb-2">Signature Information</h3>
      <div v-if="application.signed_by" class="bg-gray-50 p-4 rounded-md">
        <p class="text-sm">Signed by: {{ application.signed_by }}</p>
        <p class="text-sm">Signature Date: {{ formatDate(application.signature_date) }}</p>
        <div v-if="application.uploaded_pdf_path" class="mt-2">
          <p class="text-sm font-medium text-gray-500">Uploaded PDF</p>
          <a :href="application.uploaded_pdf_path" target="_blank" class="text-blue-600 hover:underline text-sm">
            View PDF
          </a>
        </div>
      </div>
      <div v-else class="bg-gray-50 p-4 rounded-md">
        <p class="text-sm text-gray-500">No signature information available</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  application: {
    type: Object,
    required: true
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
