<template>
  <div>
    <MenuBar
      v-if="route.meta.menu"
      :menu-items="route.meta.menu"
    />
    <section class="p-10">
      <slot />
    </section>
  </div>
</template>

<script setup>
const route = useRoute()
</script>
