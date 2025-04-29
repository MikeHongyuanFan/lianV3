<template>
  <div class="application-overview">
    <div class="overview-section">
      <h3>Basic Information</h3>
      <div class="overview-grid">
        <div class="overview-item">
          <div class="overview-label">Reference Number:</div>
          <div class="overview-value">{{ application.reference_number }}</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">Application Type:</div>
          <div class="overview-value">{{ formatApplicationType(application.application_type) }}</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">Purpose:</div>
          <div class="overview-value">{{ application.purpose }}</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">Loan Amount:</div>
          <div class="overview-value">${{ formatCurrency(application.loan_amount) }}</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">Loan Term:</div>
          <div class="overview-value">{{ application.loan_term }} months</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">Interest Rate:</div>
          <div class="overview-value">{{ application.interest_rate }}%</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">Repayment Frequency:</div>
          <div class="overview-value">{{ formatRepaymentFrequency(application.repayment_frequency) }}</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">Estimated Settlement Date:</div>
          <div class="overview-value">{{ formatDate(application.estimated_settlement_date) }}</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">Created At:</div>
          <div class="overview-value">{{ formatDate(application.created_at) }}</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">Current Stage:</div>
          <div class="overview-value">
            <span class="stage-badge" :class="getStageClass(application.stage)">
              {{ application.stage_display }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="overview-section">
      <h3>Broker and Branch Information</h3>
      <div class="overview-grid">
        <div class="overview-item">
          <div class="overview-label">Broker:</div>
          <div class="overview-value">{{ application.broker_name || 'Not specified' }}</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">Branch:</div>
          <div class="overview-value">{{ application.branch_name || 'Not specified' }}</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">BDM:</div>
          <div class="overview-value">{{ application.bd_name || 'Not specified' }}</div>
        </div>
      </div>
    </div>

    <div class="overview-section">
      <h3>Security Information</h3>
      <div class="overview-grid">
        <div class="overview-item">
          <div class="overview-label">Security Address:</div>
          <div class="overview-value">{{ application.security_address }}</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">Security Type:</div>
          <div class="overview-value">{{ formatSecurityType(application.security_type) }}</div>
        </div>
        <div class="overview-item">
          <div class="overview-label">Security Value:</div>
          <div class="overview-value">${{ formatCurrency(application.security_value) }}</div>
        </div>
      </div>
    </div>

    <div v-if="showBorrowers" class="overview-section">
      <h3>Borrowers</h3>
      <div v-if="application.borrowers && application.borrowers.length > 0" class="overview-list">
        <div v-for="(borrower, index) in application.borrowers" :key="index" class="overview-list-item">
          <div class="overview-list-primary">{{ borrower.first_name }} {{ borrower.last_name }}</div>
          <div class="overview-list-secondary">{{ borrower.email }} | {{ formatBorrowerType(borrower.borrower_type) }}</div>
        </div>
      </div>
      <div v-else class="overview-empty">
        <p>No borrowers associated with this application.</p>
      </div>
    </div>

    <div v-if="showGuarantors" class="overview-section">
      <h3>Guarantors</h3>
      <div v-if="application.guarantors && application.guarantors.length > 0" class="overview-list">
        <div v-for="(guarantor, index) in application.guarantors" :key="index" class="overview-list-item">
          <div class="overview-list-primary">{{ guarantor.first_name }} {{ guarantor.last_name }}</div>
          <div class="overview-list-secondary">{{ guarantor.email }} | {{ formatRelationship(guarantor.relationship_to_borrower) }}</div>
        </div>
      </div>
      <div v-else class="overview-empty">
        <p>No guarantors associated with this application.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApplicationOverview',
  props: {
    application: {
      type: Object,
      required: true
    },
    showBorrowers: {
      type: Boolean,
      default: true
    },
    showGuarantors: {
      type: Boolean,
      default: true
    }
  },
  methods: {
    formatBorrowerType(type) {
      const types = {
        individual: 'Individual',
        company: 'Company',
        trust: 'Trust'
      }
      return types[type] || type
    },
    
    formatRelationship(relationship) {
      const relationships = {
        spouse: 'Spouse',
        parent: 'Parent',
        child: 'Child',
        sibling: 'Sibling',
        business_partner: 'Business Partner',
        friend: 'Friend',
        other: 'Other'
      }
      return relationships[relationship] || relationship
    },
    
    formatApplicationType(type) {
      const types = {
        residential: 'Residential',
        commercial: 'Commercial',
        personal: 'Personal',
        business: 'Business'
      }
      return types[type] || type
    },
    
    formatSecurityType(type) {
      const types = {
        residential_property: 'Residential Property',
        commercial_property: 'Commercial Property',
        land: 'Land',
        vehicle: 'Vehicle',
        equipment: 'Equipment',
        other: 'Other'
      }
      return types[type] || type
    },
    
    formatRepaymentFrequency(frequency) {
      const frequencies = {
        weekly: 'Weekly',
        fortnightly: 'Fortnightly',
        monthly: 'Monthly'
      }
      return frequencies[frequency] || frequency
    },
    
    formatCurrency(value) {
      if (!value) return '0.00'
      return parseFloat(value).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    },
    
    formatDate(dateString) {
      if (!dateString) return 'Not specified'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    },
    
    getStageClass(stage) {
      const stageClasses = {
        inquiry: 'stage-inquiry',
        pre_approval: 'stage-pre-approval',
        valuation: 'stage-valuation',
        formal_approval: 'stage-formal-approval',
        settlement: 'stage-settlement',
        funded: 'stage-funded',
        declined: 'stage-declined',
        withdrawn: 'stage-withdrawn'
      }
      
      return stageClasses[stage] || 'stage-default'
    }
  }
}
</script>

<style scoped>
.application-overview {
  margin-bottom: 2rem;
}

.overview-section {
  margin-bottom: 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  overflow: hidden;
}

.overview-section h3 {
  padding: 0.75rem 1rem;
  background-color: #f3f4f6;
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.overview-item {
  display: flex;
  flex-direction: column;
}

.overview-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.overview-value {
  font-weight: 500;
}

.overview-list {
  padding: 1rem;
}

.overview-list-item {
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  margin-bottom: 0.5rem;
  background-color: #f9fafb;
}

.overview-list-primary {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.overview-list-secondary {
  font-size: 0.875rem;
  color: #6b7280;
}

.overview-empty {
  padding: 1rem;
  color: #6b7280;
  font-style: italic;
}

.stage-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.stage-inquiry {
  background-color: #e0f2fe;
  color: #0369a1;
}

.stage-pre-approval {
  background-color: #fef3c7;
  color: #92400e;
}

.stage-valuation {
  background-color: #dbeafe;
  color: #1e40af;
}

.stage-formal-approval {
  background-color: #dcfce7;
  color: #166534;
}

.stage-settlement {
  background-color: #f3e8ff;
  color: #6b21a8;
}

.stage-funded {
  background-color: #d1fae5;
  color: #065f46;
}

.stage-declined {
  background-color: #fee2e2;
  color: #b91c1c;
}

.stage-withdrawn {
  background-color: #f3f4f6;
  color: #4b5563;
}
</style>
