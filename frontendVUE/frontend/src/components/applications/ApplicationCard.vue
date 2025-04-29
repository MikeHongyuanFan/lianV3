<template>
  <div class="application-card" @click="viewApplication">
    <div class="card-header">
      <h3 class="reference-number">{{ application.reference_number }}</h3>
      <ApplicationStatusBadge :stage="application.stage" :stage_display="application.stage_display" />
    </div>
    
    <div class="card-body">
      <div class="info-row">
        <span class="label">Type:</span>
        <span class="value">{{ application.application_type }}</span>
      </div>
      
      <div class="info-row">
        <span class="label">Purpose:</span>
        <span class="value">{{ application.purpose }}</span>
      </div>
      
      <div class="info-row">
        <span class="label">Amount:</span>
        <span class="value">${{ formatCurrency(application.loan_amount) }}</span>
      </div>
      
      <div class="info-row">
        <span class="label">Broker:</span>
        <span class="value">{{ application.broker_name || 'N/A' }}</span>
      </div>
      
      <div class="info-row">
        <span class="label">Borrowers:</span>
        <span class="value">{{ application.borrower_count || 0 }}</span>
      </div>
      
      <div class="info-row">
        <span class="label">Created:</span>
        <span class="value">{{ formatDate(application.created_at) }}</span>
      </div>
      
      <div class="info-row" v-if="application.estimated_settlement_date">
        <span class="label">Est. Settlement:</span>
        <span class="value">{{ formatDate(application.estimated_settlement_date) }}</span>
      </div>
    </div>
    
    <div class="card-footer">
      <BaseButton @click.stop="viewApplication" variant="primary" size="small">View</BaseButton>
      <BaseButton @click.stop="editApplication" variant="secondary" size="small">Edit</BaseButton>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import ApplicationStatusBadge from '@/components/applications/ApplicationStatusBadge.vue'
import BaseButton from '@/components/BaseButton.vue'

export default {
  name: 'ApplicationCard',
  components: {
    ApplicationStatusBadge,
    BaseButton
  },
  props: {
    application: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const router = useRouter()
    
    const viewApplication = () => {
      router.push({ name: 'application-detail', params: { id: props.application.id } })
    }
    
    const editApplication = () => {
      router.push({ name: 'application-edit', params: { id: props.application.id } })
    }
    
    const formatCurrency = (value) => {
      return parseFloat(value).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
    
    return {
      viewApplication,
      editApplication,
      formatCurrency,
      formatDate
    }
  }
}
</script>

<style scoped>
.application-card {
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: all 0.2s ease;
  cursor: pointer;
}

.application-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.reference-number {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.card-body {
  padding: 1rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.info-row:last-child {
  margin-bottom: 0;
}

.label {
  font-weight: 500;
  color: #6b7280;
}

.value {
  font-weight: 500;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1rem;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
}
</style>
