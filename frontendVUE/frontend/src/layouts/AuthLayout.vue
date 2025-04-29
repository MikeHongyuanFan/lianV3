<template>
  <div class="auth-layout">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="text-center mb-4 mt-5">
            <h2 class="mb-0">CRM Loan Management System</h2>
            <p class="text-muted">Manage your loan applications efficiently</p>
          </div>
          <div class="card shadow-sm">
            <div class="card-body p-4">
              <router-view />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthLayout'
}
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 2rem 0;
}
</style>
