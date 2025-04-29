<template>
  <Teleport to="body">
    <transition name="modal-fade">
      <div v-if="modelValue" class="modal-backdrop" @click.self="closeOnBackdrop && close()">
        <div class="modal-container" :class="[size]">
          <div class="modal-content">
            <div class="modal-header">
              <h3 class="modal-title">{{ title }}</h3>
              <button v-if="showCloseButton" class="modal-close" @click="close">
                <span>&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <slot></slot>
            </div>
            <div v-if="$slots.footer" class="modal-footer">
              <slot name="footer"></slot>
            </div>
            <div v-else-if="showDefaultFooter" class="modal-footer">
              <button class="btn btn-secondary" @click="close">{{ cancelText }}</button>
              <button class="btn btn-primary" @click="confirm">{{ confirmText }}</button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'BaseModal',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'md',
      validator: (value: string) => ['sm', 'md', 'lg', 'xl'].includes(value)
    },
    closeOnBackdrop: {
      type: Boolean,
      default: true
    },
    showCloseButton: {
      type: Boolean,
      default: true
    },
    showDefaultFooter: {
      type: Boolean,
      default: false
    },
    confirmText: {
      type: String,
      default: 'Confirm'
    },
    cancelText: {
      type: String,
      default: 'Cancel'
    }
  },
  emits: ['update:modelValue', 'confirm', 'cancel'],
  setup(props, { emit }) {
    // Close the modal
    const close = () => {
      emit('update:modelValue', false)
      emit('cancel')
    }

    // Confirm action
    const confirm = () => {
      emit('confirm')
      emit('update:modelValue', false)
    }

    return {
      close,
      confirm
    }
  }
})
</script>

<style scoped>
.modal-backdrop {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4;
}

.modal-container {
  @apply bg-white rounded-lg shadow-lg w-full max-h-[90vh] overflow-hidden;
}

.modal-container.sm {
  @apply max-w-sm;
}

.modal-container.md {
  @apply max-w-md;
}

.modal-container.lg {
  @apply max-w-lg;
}

.modal-container.xl {
  @apply max-w-xl;
}

.modal-content {
  @apply flex flex-col max-h-[90vh];
}

.modal-header {
  @apply flex justify-between items-center p-4 border-b border-gray-200;
}

.modal-title {
  @apply text-lg font-medium text-gray-900;
}

.modal-close {
  @apply text-gray-400 hover:text-gray-500 focus:outline-none;
}

.modal-body {
  @apply p-4 overflow-y-auto;
}

.modal-footer {
  @apply flex justify-end space-x-2 p-4 border-t border-gray-200;
}

/* Transition effects */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>