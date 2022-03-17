<template>
  <div class="bg-dark-800 text-neutral-500 font-serif">
    <NuxtPage />
  </div>
</template>

<script setup>
const route = useRoute()

useMeta({
  title: computed(() => route.meta.title ? `${route.meta.title} | Norske opptakssteder` : 'Norske opptakssteder')
})
</script>