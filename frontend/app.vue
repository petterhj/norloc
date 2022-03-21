<template>
  <div class="bg-light-200">
    <Navbar />
    <section class="p-10">
      <NuxtPage />
    </section>
  </div>
</template>

<script setup>
const route = useRoute()
const titleBase = 'Norske opptakssteder'

useMeta({
  title: computed(() => {
    return route.meta.title ? `${route.meta.title} | ${titleBase}` : titleBase
  })
})
</script>
