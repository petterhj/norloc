<script setup>
import Movies from '@/components/Movies.vue';
</script>

<template>
  <Movies />
  <div class="mt-6">
    <RouterLink :to="{ name: 'productions' }">
      Se alle
    </RouterLink>
  </div>
</template>
