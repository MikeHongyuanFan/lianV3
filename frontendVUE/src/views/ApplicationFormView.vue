<template>
  <div class="application-form-view">
    <h1 class="page-title">New Loan Application</h1>
    <ApplicationForm />
  </div>
</template>

<script setup>
import ApplicationForm from '@/components/application/ApplicationForm.vue';
</script>

<style scoped>
.application-form-view {
  padding: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: #2d3748;
}
</style>
