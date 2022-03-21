<template>
  <div class="bg-light-200">
    <NuxtPage />
  </div>
</template>

<script setup>
const route = useRoute()

useMeta({
  title: computed(() => route.meta.title ? `${route.meta.title} | Norske opptakssteder` : 'Norske opptakssteder')
})
</script>
