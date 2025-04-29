<template>
  <span class="status-badge" :class="getStatusClass">
    {{ stage_display || formatStage(stage) }}
  </span>
</template>

<script>
export default {
  name: 'ApplicationStatusBadge',
  props: {
    stage: {
      type: String,
      required: true
    },
    stage_display: {
      type: String,
      default: ''
    }
  },
  computed: {
    getStatusClass() {
      const stageClasses = {
        inquiry: 'status-inquiry',
        pre_approval: 'status-pre-approval',
        valuation: 'status-valuation',
        formal_approval: 'status-formal-approval',
        settlement: 'status-settlement',
        funded: 'status-funded',
        declined: 'status-declined',
        withdrawn: 'status-withdrawn'
      }
      
      return stageClasses[this.stage] || 'status-default'
    }
  },
  methods: {
    formatStage(stage) {
      if (!stage) return 'Unknown'
      
      // Convert snake_case to Title Case
      return stage
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
  }
}
</script>

<style scoped>
.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-align: center;
  white-space: nowrap;
}

.status-inquiry {
  background-color: #e0f2fe;
  color: #0369a1;
}

.status-pre-approval {
  background-color: #fef3c7;
  color: #92400e;
}

.status-valuation {
  background-color: #dbeafe;
  color: #1e40af;
}

.status-formal-approval {
  background-color: #dcfce7;
  color: #166534;
}

.status-settlement {
  background-color: #f3e8ff;
  color: #6b21a8;
}

.status-funded {
  background-color: #d1fae5;
  color: #065f46;
}

.status-declined {
  background-color: #fee2e2;
  color: #b91c1c;
}

.status-withdrawn {
  background-color: #f3f4f6;
  color: #4b5563;
}

.status-default {
  background-color: #e5e7eb;
  color: #374151;
}
</style>
