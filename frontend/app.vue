<template>
  <div class="flex flex-col h-screen">
    <Header />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
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
