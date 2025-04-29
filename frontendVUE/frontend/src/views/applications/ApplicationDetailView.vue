<template>
  <MainLayout>
    <div class="application-detail-container">
      <div class="page-header mb-6">
        <h1 class="text-2xl font-bold">Application Detail</h1>
        <div class="flex space-x-2 mt-4">
          <button
            v-for="tab in tabs"
            :key="tab"
            @click="activeTab = tab"
            :class="['px-4 py-2 rounded-md', activeTab === tab ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700']"
          >
            {{ tab }}
          </button>
        </div>
      </div>

      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="loader"></div>
      </div>

      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        <p>{{ error }}</p>
        <button @click="fetchApplication" class="underline">Try again</button>
      </div>

      <div v-else-if="application">
        <!-- Overview Tab -->
        <div v-if="activeTab === 'Overview'" class="space-y-6">
          <div class="bg-white p-6 rounded-md shadow-md">
            <h2 class="text-lg font-semibold mb-4">Loan Details</h2>
            <p><strong>Reference Number:</strong> {{ application.reference_number }}</p>
            <p><strong>Loan Amount:</strong> {{ formatCurrency(application.loan_amount) }}</p>
            <p><strong>Loan Term:</strong> {{ application.loan_term }} months</p>
            <p><strong>Status:</strong> {{ formatStatus(application.status) }}</p>
            <p><strong>Stage:</strong> {{ application.stage_display || formatStage(application.stage) }}</p>
          </div>

          <div class="bg-white p-6 rounded-md shadow-md">
            <h2 class="text-lg font-semibold mb-4">Applicant Details</h2>
            <p><strong>Borrower Count:</strong> {{ application.borrower_count }}</p>
            <p><strong>Guarantor Count:</strong> {{ application.guarantor_count }}</p>
          </div>

          <div class="bg-white p-6 rounded-md shadow-md">
            <h2 class="text-lg font-semibold mb-4">Important Dates</h2>
            <p><strong>Estimated Settlement Date:</strong> {{ formatDate(application.estimated_settlement_date) }}</p>
            <p><strong>Created At:</strong> {{ formatDate(application.created_at) }}</p>
          </div>
        </div>

        <!-- Placeholder for other tabs -->
        <div v-else>
          <p class="text-gray-500">Feature coming soon...</p>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useApplicationStore } from '@/store/application';
import MainLayout from '@/layouts/MainLayout.vue';

export default {
  name: 'ApplicationDetailView',
  components: { MainLayout },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const applicationStore = useApplicationStore();

    const loading = computed(() => applicationStore.loading);
    const error = computed(() => applicationStore.error);
    const application = computed(() => applicationStore.currentApplication);

    const tabs = ['Overview', 'Borrowers', 'Notes', 'Fees', 'Repayments', 'Documents', 'Ledger'];
    const activeTab = ref('Overview');

    const fetchApplication = async () => {
      try {
        const id = route.params.id;
        await applicationStore.fetchApplication(id);
      } catch (e) {
        console.error('Failed to fetch application:', e);
        
        // Show appropriate error message based on status code
        let errorMessage = 'Failed to load application details';
        
        if (e.status === 404) {
          errorMessage = `Application with ID ${id} not found`;
        } else if (e.status === 401) {
          errorMessage = 'You do not have permission to view this application';
        } else if (e.status === 403) {
          errorMessage = 'Access forbidden to this application';
        }
        
        // Use toast or notification system if available
        if (window.$toast) {
          window.$toast.error(errorMessage);
        } else {
          alert(errorMessage);
        }
        
        // Redirect to applications list
        router.push('/applications');
      }
    };

    const formatCurrency = (amount) => {
      if (amount == null) return 'N/A';
      return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
    };

    const formatStatus = (status) => {
      if (!status) return 'Unknown';
      return status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ');
    };

    const formatStage = (stage) => {
      if (!stage) return 'Unknown';
      return stage.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'Unknown';
      const date = new Date(dateString);
      return date.toLocaleDateString();
    };

    onMounted(() => {
      fetchApplication();
    });

    return {
      loading,
      error,
      application,
      tabs,
      activeTab,
      fetchApplication,
      formatCurrency,
      formatStatus,
      formatStage,
      formatDate
    };
  }
};
</script>

<style scoped>
.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
