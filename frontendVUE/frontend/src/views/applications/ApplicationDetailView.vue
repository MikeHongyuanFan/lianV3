<template>
  <MainLayout>
    <div class="application-detail-container">
      <div class="page-header mb-6">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold">Application Detail</h1>
          <div class="flex space-x-2">
            <router-link 
              :to="`/applications/${$route.params.id}/edit`" 
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
            >
              Edit Application
            </router-link>
            <button 
              @click="goBack" 
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none"
            >
              Back to List
            </button>
          </div>
        </div>
        
        <div class="flex space-x-2 mt-4 overflow-x-auto pb-2">
          <button
            v-for="tab in tabs"
            :key="tab"
            @click="activeTab = tab"
            :class="[
              'px-4 py-2 rounded-md whitespace-nowrap',
              activeTab === tab ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
            ]"
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
            <div class="flex justify-between items-start mb-4">
              <h2 class="text-lg font-semibold">Loan Details</h2>
              <span 
                class="px-3 py-1 rounded-full text-sm font-medium"
                :class="getStageClass(application.stage)"
              >
                {{ application.stage_display || formatStage(application.stage) }}
              </span>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p><strong>Reference Number:</strong> {{ application.reference_number }}</p>
                <p><strong>Loan Amount:</strong> {{ formatCurrency(application.loan_amount) }}</p>
                <p><strong>Loan Term:</strong> {{ application.loan_term }} months</p>
                <p><strong>Interest Rate:</strong> {{ application.interest_rate }}%</p>
                <p><strong>Purpose:</strong> {{ application.purpose }}</p>
              </div>
              <div>
                <p><strong>Application Type:</strong> {{ formatApplicationType(application.application_type) }}</p>
                <p><strong>Repayment Frequency:</strong> {{ formatRepaymentFrequency(application.repayment_frequency) }}</p>
                <p><strong>Product ID:</strong> {{ application.product_id || 'N/A' }}</p>
                <p><strong>Estimated Settlement:</strong> {{ formatDate(application.estimated_settlement_date) }}</p>
                <p><strong>Created:</strong> {{ formatDate(application.created_at) }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-md shadow-md">
            <h2 class="text-lg font-semibold mb-4">Security Property</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p><strong>Address:</strong> {{ application.security_address || 'N/A' }}</p>
                <p><strong>Type:</strong> {{ application.security_type || 'N/A' }}</p>
              </div>
              <div>
                <p><strong>Value:</strong> {{ formatCurrency(application.security_value) }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-md shadow-md">
            <h2 class="text-lg font-semibold mb-4">Parties</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p><strong>Borrowers:</strong> {{ application.borrower_count || 0 }}</p>
                <p><strong>Guarantors:</strong> {{ application.guarantor_count || 0 }}</p>
              </div>
              <div>
                <p><strong>Broker:</strong> {{ application.broker_name || 'N/A' }}</p>
                <p><strong>Business Development Manager:</strong> {{ application.bd_name || 'N/A' }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Borrowers Tab -->
        <div v-else-if="activeTab === 'Borrowers'" class="space-y-6">
          <div class="bg-white p-6 rounded-md shadow-md">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-semibold">Borrowers</h2>
              <button class="px-3 py-1 bg-blue-600 text-white rounded-md text-sm">Add Borrower</button>
            </div>
            
            <div v-if="!application.borrowers || application.borrowers.length === 0" class="text-center py-4 text-gray-500">
              No borrowers associated with this application
            </div>
            
            <div v-else class="space-y-4">
              <div v-for="borrower in application.borrowers" :key="borrower.id" class="border p-4 rounded-md">
                <div class="flex justify-between">
                  <h3 class="font-medium">{{ borrower.first_name }} {{ borrower.last_name }}</h3>
                  <div class="space-x-2">
                    <button class="text-blue-600 hover:underline">View</button>
                    <button class="text-gray-600 hover:underline">Edit</button>
                  </div>
                </div>
                <p class="text-sm text-gray-600">{{ borrower.email }}</p>
                <p class="text-sm text-gray-600">{{ borrower.phone }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-md shadow-md">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-semibold">Guarantors</h2>
              <button class="px-3 py-1 bg-blue-600 text-white rounded-md text-sm">Add Guarantor</button>
            </div>
            
            <div v-if="!application.guarantors || application.guarantors.length === 0" class="text-center py-4 text-gray-500">
              No guarantors associated with this application
            </div>
            
            <div v-else class="space-y-4">
              <div v-for="guarantor in application.guarantors" :key="guarantor.id" class="border p-4 rounded-md">
                <div class="flex justify-between">
                  <h3 class="font-medium">{{ guarantor.first_name }} {{ guarantor.last_name }}</h3>
                  <div class="space-x-2">
                    <button class="text-blue-600 hover:underline">View</button>
                    <button class="text-gray-600 hover:underline">Edit</button>
                  </div>
                </div>
                <p class="text-sm text-gray-600">{{ guarantor.email }}</p>
                <p class="text-sm text-gray-600">{{ guarantor.phone }}</p>
                <p class="text-sm text-gray-600">Relationship: {{ formatRelationship(guarantor.relationship_to_borrower) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Notes Tab -->
        <div v-else-if="activeTab === 'Notes'" class="space-y-6">
          <div class="bg-white p-6 rounded-md shadow-md">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-semibold">Notes</h2>
              <button class="px-3 py-1 bg-blue-600 text-white rounded-md text-sm">Add Note</button>
            </div>
            
            <div v-if="!application.notes || application.notes.length === 0" class="text-center py-4 text-gray-500">
              No notes for this application
            </div>
            
            <div v-else class="space-y-4">
              <div v-for="note in application.notes" :key="note.id" class="border p-4 rounded-md">
                <div class="flex justify-between">
                  <h3 class="font-medium">{{ note.title || 'Note' }}</h3>
                  <span class="text-sm text-gray-500">{{ formatDate(note.created_at) }}</span>
                </div>
                <p class="mt-2">{{ note.content }}</p>
                <p class="text-sm text-gray-600 mt-2">By: {{ note.created_by_name }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Fees Tab -->
        <div v-else-if="activeTab === 'Fees'" class="space-y-6">
          <div class="bg-white p-6 rounded-md shadow-md">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-semibold">Fees</h2>
              <button class="px-3 py-1 bg-blue-600 text-white rounded-md text-sm">Add Fee</button>
            </div>
            
            <div v-if="!application.fees || application.fees.length === 0" class="text-center py-4 text-gray-500">
              No fees for this application
            </div>
            
            <div v-else>
              <table class="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="fee in application.fees" :key="fee.id">
                    <td class="px-4 py-2">{{ fee.fee_type_display || formatFeeType(fee.fee_type) }}</td>
                    <td class="px-4 py-2">{{ formatCurrency(fee.amount) }}</td>
                    <td class="px-4 py-2">{{ formatDate(fee.due_date) }}</td>
                    <td class="px-4 py-2">
                      <span 
                        class="px-2 py-1 text-xs rounded-full"
                        :class="fee.is_paid ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'"
                      >
                        {{ fee.is_paid ? 'Paid' : 'Pending' }}
                      </span>
                    </td>
                    <td class="px-4 py-2">
                      <button v-if="!fee.is_paid" class="text-blue-600 hover:underline text-sm">Mark as Paid</button>
                      <span v-else class="text-sm text-gray-500">Paid on {{ formatDate(fee.paid_date) }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Repayments Tab -->
        <div v-else-if="activeTab === 'Repayments'" class="space-y-6">
          <div class="bg-white p-6 rounded-md shadow-md">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-semibold">Repayments</h2>
              <button class="px-3 py-1 bg-blue-600 text-white rounded-md text-sm">Add Repayment</button>
            </div>
            
            <div v-if="!application.repayments || application.repayments.length === 0" class="text-center py-4 text-gray-500">
              No repayments for this application
            </div>
            
            <div v-else>
              <table class="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Payment Method</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="repayment in application.repayments" :key="repayment.id">
                    <td class="px-4 py-2">{{ formatCurrency(repayment.amount) }}</td>
                    <td class="px-4 py-2">{{ formatDate(repayment.due_date) }}</td>
                    <td class="px-4 py-2">
                      <span 
                        class="px-2 py-1 text-xs rounded-full"
                        :class="getRepaymentStatusClass(repayment.status)"
                      >
                        {{ formatRepaymentStatus(repayment.status) }}
                      </span>
                    </td>
                    <td class="px-4 py-2">{{ repayment.payment_method || 'N/A' }}</td>
                    <td class="px-4 py-2">
                      <button v-if="!repayment.is_paid" class="text-blue-600 hover:underline text-sm">Record Payment</button>
                      <span v-else class="text-sm text-gray-500">Paid on {{ formatDate(repayment.paid_date) }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Documents Tab -->
        <div v-else-if="activeTab === 'Documents'" class="space-y-6">
          <div class="bg-white p-6 rounded-md shadow-md">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-semibold">Documents</h2>
              <button class="px-3 py-1 bg-blue-600 text-white rounded-md text-sm">Upload Document</button>
            </div>
            
            <div v-if="!application.documents || application.documents.length === 0" class="text-center py-4 text-gray-500">
              No documents for this application
            </div>
            
            <div v-else>
              <table class="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Uploaded By</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Uploaded At</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="document in application.documents" :key="document.id">
                    <td class="px-4 py-2">{{ document.title }}</td>
                    <td class="px-4 py-2">{{ document.document_type_display || document.document_type }}</td>
                    <td class="px-4 py-2">{{ document.created_by_name }}</td>
                    <td class="px-4 py-2">{{ formatDate(document.created_at) }}</td>
                    <td class="px-4 py-2 space-x-2">
                      <button class="text-blue-600 hover:underline text-sm">View</button>
                      <button class="text-gray-600 hover:underline text-sm">Download</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Ledger Tab -->
        <div v-else-if="activeTab === 'Ledger'" class="space-y-6">
          <div class="bg-white p-6 rounded-md shadow-md">
            <h2 class="text-lg font-semibold mb-4">Ledger</h2>
            
            <div v-if="!application.ledger || application.ledger.length === 0" class="text-center py-4 text-gray-500">
              No ledger entries for this application
            </div>
            
            <div v-else>
              <table class="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Balance</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="entry in application.ledger" :key="entry.id">
                    <td class="px-4 py-2">{{ formatDate(entry.transaction_date) }}</td>
                    <td class="px-4 py-2">{{ entry.transaction_type_display || entry.transaction_type }}</td>
                    <td class="px-4 py-2">{{ entry.description }}</td>
                    <td class="px-4 py-2" :class="entry.amount < 0 ? 'text-red-600' : 'text-green-600'">
                      {{ formatCurrency(entry.amount) }}
                    </td>
                    <td class="px-4 py-2">{{ formatCurrency(entry.balance) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Default placeholder for other tabs -->
        <div v-else class="bg-white p-6 rounded-md shadow-md">
          <p class="text-gray-500">This tab is coming soon...</p>
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

    const goBack = () => {
      router.push('/applications');
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

    const formatApplicationType = (type) => {
      if (!type) return 'Unknown';
      return type.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    };

    const formatRepaymentFrequency = (frequency) => {
      if (!frequency) return 'Unknown';
      return frequency.charAt(0).toUpperCase() + frequency.slice(1);
    };

    const formatFeeType = (type) => {
      if (!type) return 'Unknown';
      return type.charAt(0).toUpperCase() + type.slice(1);
    };

    const formatRelationship = (relationship) => {
      if (!relationship) return 'Unknown';
      return relationship.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    };

    const formatRepaymentStatus = (status) => {
      if (!status) return 'Unknown';
      if (status === 'paid') return 'Paid';
      if (status === 'scheduled') return 'Scheduled';
      if (status.includes('overdue')) {
        const days = status.split('_').pop();
        return `Overdue (${days} days)`;
      }
      if (status.includes('due_soon')) {
        const days = status.split('_').pop();
        return `Due Soon (${days} days)`;
      }
      return status;
    };

    const getStageClass = (stage) => {
      const stageClasses = {
        'inquiry': 'bg-gray-100 text-gray-800',
        'pre_approval': 'bg-blue-100 text-blue-800',
        'valuation': 'bg-purple-100 text-purple-800',
        'formal_approval': 'bg-indigo-100 text-indigo-800',
        'settlement': 'bg-green-100 text-green-800',
        'funded': 'bg-teal-100 text-teal-800',
        'declined': 'bg-red-100 text-red-800',
        'withdrawn': 'bg-gray-100 text-gray-800'
      };
      
      return stageClasses[stage] || 'bg-gray-100 text-gray-800';
    };

    const getRepaymentStatusClass = (status) => {
      if (!status) return 'bg-gray-100 text-gray-800';
      if (status === 'paid') return 'bg-green-100 text-green-800';
      if (status === 'scheduled') return 'bg-blue-100 text-blue-800';
      if (status.includes('overdue')) return 'bg-red-100 text-red-800';
      if (status.includes('due_soon')) return 'bg-yellow-100 text-yellow-800';
      return 'bg-gray-100 text-gray-800';
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
      goBack,
      formatCurrency,
      formatStatus,
      formatStage,
      formatDate,
      formatApplicationType,
      formatRepaymentFrequency,
      formatFeeType,
      formatRelationship,
      formatRepaymentStatus,
      getStageClass,
      getRepaymentStatusClass
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
