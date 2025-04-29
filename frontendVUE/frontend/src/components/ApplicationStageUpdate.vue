<template>
  <div class="stage-update-container">
    <h3>Update Application Stage</h3>
    
    <div class="current-stage">
      <div class="stage-label">Current Stage:</div>
      <div class="stage-value">
        <span class="stage-badge" :class="getStageClass(currentStage)">
          {{ getStageDisplay(currentStage) }}
        </span>
      </div>
    </div>
    
    <div class="stage-selection">
      <label for="new-stage">Select New Stage:</label>
      <select id="new-stage" v-model="selectedStage" :disabled="loading">
        <option value="">Select Stage</option>
        <option v-for="stage in availableStages" :key="stage.value" :value="stage.value">
          {{ stage.label }}
        </option>
      </select>
    </div>
    
    <div class="stage-actions">
      <BaseButton 
        @click="updateStage" 
        variant="primary" 
        :disabled="!selectedStage || loading || selectedStage === currentStage"
        :loading="loading"
      >
        Update Stage
      </BaseButton>
    </div>
    
    <AlertMessage v-if="error" :message="error" type="error" />
    <AlertMessage v-if="success" :message="success" type="success" />
    
    <div class="stage-flow">
      <h4>Application Stage Flow</h4>
      <div class="stage-flow-diagram">
        <div 
          v-for="(stage, index) in stageFlow" 
          :key="stage.value"
          class="stage-flow-item"
          :class="{
            'active': stage.value === currentStage,
            'completed': isStageCompleted(stage.value),
            'available': isStageAvailable(stage.value)
          }"
        >
          <div class="stage-flow-number">{{ index + 1 }}</div>
          <div class="stage-flow-label">{{ stage.label }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import BaseButton from '@/components/BaseButton.vue'
import AlertMessage from '@/components/AlertMessage.vue'

export default {
  name: 'ApplicationStageUpdate',
  components: {
    BaseButton,
    AlertMessage
  },
  props: {
    applicationId: {
      type: [Number, String],
      required: true
    },
    currentStage: {
      type: String,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update-stage'],
  setup(props, { emit }) {
    const selectedStage = ref('')
    const error = ref('')
    const success = ref('')
    
    // Define all possible stages and their display values
    const allStages = [
      { value: 'inquiry', label: 'Inquiry' },
      { value: 'pre_approval', label: 'Pre-Approval' },
      { value: 'valuation', label: 'Valuation' },
      { value: 'formal_approval', label: 'Formal Approval' },
      { value: 'settlement', label: 'Settlement' },
      { value: 'funded', label: 'Funded' },
      { value: 'declined', label: 'Declined' },
      { value: 'withdrawn', label: 'Withdrawn' }
    ]
    
    // Define the normal flow of stages (excluding declined and withdrawn)
    const stageFlow = [
      { value: 'inquiry', label: 'Inquiry' },
      { value: 'pre_approval', label: 'Pre-Approval' },
      { value: 'valuation', label: 'Valuation' },
      { value: 'formal_approval', label: 'Formal Approval' },
      { value: 'settlement', label: 'Settlement' },
      { value: 'funded', label: 'Funded' }
    ]
    
    // Define stage transitions - which stages can follow the current stage
    const stageTransitions = {
      inquiry: ['pre_approval', 'declined', 'withdrawn'],
      pre_approval: ['valuation', 'declined', 'withdrawn'],
      valuation: ['formal_approval', 'declined', 'withdrawn'],
      formal_approval: ['settlement', 'declined', 'withdrawn'],
      settlement: ['funded', 'declined', 'withdrawn'],
      funded: ['withdrawn'],
      declined: ['inquiry'],
      withdrawn: ['inquiry']
    }
    
    // Compute available stages based on current stage
    const availableStages = computed(() => {
      const allowedTransitions = stageTransitions[props.currentStage] || []
      return allStages.filter(stage => allowedTransitions.includes(stage.value))
    })
    
    // Reset selected stage when current stage changes
    watch(() => props.currentStage, () => {
      selectedStage.value = ''
      error.value = ''
      success.value = ''
    })
    
    // Check if a stage is completed (comes before current stage in the flow)
    const isStageCompleted = (stage) => {
      const currentIndex = stageFlow.findIndex(s => s.value === props.currentStage)
      const stageIndex = stageFlow.findIndex(s => s.value === stage)
      
      // Special cases for declined and withdrawn
      if (props.currentStage === 'declined' || props.currentStage === 'withdrawn') {
        return false
      }
      
      return stageIndex < currentIndex
    }
    
    // Check if a stage is available for selection
    const isStageAvailable = (stage) => {
      return availableStages.value.some(s => s.value === stage)
    }
    
    // Get display name for a stage
    const getStageDisplay = (stage) => {
      const stageObj = allStages.find(s => s.value === stage)
      return stageObj ? stageObj.label : stage
    }
    
    // Get CSS class for stage badge
    const getStageClass = (stage) => {
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
    
    // Update the application stage
    const updateStage = () => {
      if (!selectedStage.value || selectedStage.value === props.currentStage) {
        return
      }
      
      error.value = ''
      success.value = ''
      
      emit('update-stage', {
        applicationId: props.applicationId,
        stage: selectedStage.value,
        onSuccess: () => {
          success.value = `Application stage updated to ${getStageDisplay(selectedStage.value)}`
          selectedStage.value = ''
          
          // Clear success message after 3 seconds
          setTimeout(() => {
            success.value = ''
          }, 3000)
        },
        onError: (err) => {
          error.value = err.message || 'Failed to update application stage'
        }
      })
    }
    
    return {
      selectedStage,
      error,
      success,
      availableStages,
      stageFlow,
      updateStage,
      getStageDisplay,
      getStageClass,
      isStageCompleted,
      isStageAvailable
    }
  }
}
</script>

<style scoped>
.stage-update-container {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.stage-update-container h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.25rem;
  font-weight: 600;
}

.current-stage {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.stage-label {
  font-weight: 500;
  margin-right: 0.5rem;
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

.stage-selection {
  margin-bottom: 1.5rem;
}

.stage-selection label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.stage-selection select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: white;
}

.stage-actions {
  margin-bottom: 1.5rem;
}

.stage-flow {
  margin-top: 2rem;
}

.stage-flow h4 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.stage-flow-diagram {
  display: flex;
  justify-content: space-between;
  position: relative;
}

.stage-flow-diagram::before {
  content: '';
  position: absolute;
  top: 1.5rem;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #e5e7eb;
  z-index: 1;
}

.stage-flow-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2;
  flex: 1;
}

.stage-flow-number {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background-color: #e5e7eb;
  color: #6b7280;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.stage-flow-label {
  font-size: 0.75rem;
  color: #6b7280;
  text-align: center;
}

.stage-flow-item.active .stage-flow-number {
  background-color: #3b82f6;
  color: white;
}

.stage-flow-item.active .stage-flow-label {
  color: #3b82f6;
  font-weight: 600;
}

.stage-flow-item.completed .stage-flow-number {
  background-color: #10b981;
  color: white;
}

.stage-flow-item.completed .stage-flow-label {
  color: #10b981;
  font-weight: 600;
}

.stage-flow-item.available .stage-flow-number {
  border: 2px dashed #3b82f6;
}
</style>
