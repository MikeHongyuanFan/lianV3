<template>
  <div class="links-container">
    <h3 class="text-lg font-semibold mb-4">Quick Links</h3>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="bg-white p-4 rounded-lg shadow">
        <h4 class="font-medium mb-2">Borrowers</h4>
        <div class="flex flex-col space-y-2">
          <router-link to="/borrowers" class="text-blue-600 hover:text-blue-800">
            View All Borrowers
          </router-link>
          <router-link to="/borrowers/create" class="text-blue-600 hover:text-blue-800">
            Create New Borrower
          </router-link>
        </div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <h4 class="font-medium mb-2">Guarantors</h4>
        <div class="flex flex-col space-y-2">
          <router-link to="/guarantors" class="text-blue-600 hover:text-blue-800">
            View All Guarantors
          </router-link>
          <router-link to="/guarantors/create" class="text-blue-600 hover:text-blue-800">
            Create New Guarantor
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BorrowerGuarantorLinks'
}
</script>

<style scoped>
.links-container {
  margin-bottom: 2rem;
}
</style>
