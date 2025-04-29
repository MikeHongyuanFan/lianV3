<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>The page you are looking for does not exist or has been moved.</p>
      <router-link to="/dashboard" class="btn btn-primary">Go to Dashboard</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView'
}
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  text-align: center;
  padding: 2rem;
}

.not-found-content {
  max-width: 500px;
}

h1 {
  font-size: 6rem;
  margin-bottom: 1rem;
  color: #343a40;
}

h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #343a40;
}

p {
  margin-bottom: 2rem;
  color: #6c757d;
}
</style>
