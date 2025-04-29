<template>
  <div v-if="show" :class="alertClasses" role="alert">
    <button v-if="dismissible" type="button" class="close" @click="dismiss">
      <span>&times;</span>
    </button>
    <div v-if="message">{{ message }}</div>
    <slot v-else></slot>
  </div>
</template>

<script>
export default {
  name: 'AlertMessage',
  props: {
    type: {
      type: String,
      default: 'info',
      validator: value => ['success', 'info', 'warning', 'danger', 'error'].includes(value)
    },
    message: {
      type: String,
      default: ''
    },
    dismissible: {
      type: Boolean,
      default: true
    },
    timeout: {
      type: Number,
      default: 0 // 0 means no auto-dismiss
    }
  },
  data() {
    return {
      show: true,
      timer: null
    }
  },
  computed: {
    alertClasses() {
      // Map 'error' to 'danger' for Bootstrap compatibility
      const typeClass = this.type === 'error' ? 'danger' : this.type;
      
      return [
        'alert',
        `alert-${typeClass}`,
        { 'alert-dismissible': this.dismissible }
      ]
    }
  },
  mounted() {
    if (this.timeout > 0) {
      this.timer = setTimeout(() => {
        this.dismiss()
      }, this.timeout)
    }
  },
  beforeUnmount() {
    if (this.timer) {
      clearTimeout(this.timer)
    }
  },
  methods: {
    dismiss() {
      this.show = false
      this.$emit('dismissed')
    }
  }
}
</script>

<style scoped>
.alert {
  position: relative;
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border: 1px solid transparent;
  border-radius: 0.25rem;
}

.alert-success {
  color: #155724;
  background-color: #d4edda;
  border-color: #c3e6cb;
}

.alert-info {
  color: #0c5460;
  background-color: #d1ecf1;
  border-color: #bee5eb;
}

.alert-warning {
  color: #856404;
  background-color: #fff3cd;
  border-color: #ffeeba;
}

.alert-danger {
  color: #721c24;
  background-color: #f8d7da;
  border-color: #f5c6cb;
}

.alert-dismissible {
  padding-right: 4rem;
}

.alert-dismissible .close {
  position: absolute;
  top: 0;
  right: 0;
  padding: 0.75rem 1.25rem;
  color: inherit;
  background-color: transparent;
  border: 0;
  cursor: pointer;
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
  opacity: 0.5;
}

.alert-dismissible .close:hover {
  opacity: 1;
}
</style>
