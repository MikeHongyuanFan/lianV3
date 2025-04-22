<template>
  <div class="min-h-screen bg-gray-100">
    <NavBar />
    <main class="container mx-auto p-4">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
</script>

<style>
@import './assets/main.css';
</style>
