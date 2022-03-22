<template>
  <section>
    <header>
      <NuxtLink
        :to="{ name: 'index' }"
        class="font-semibold logo">Norske opptakssteder</NuxtLink>
      <span class="text-accent px-2">&#9642;</span>
      <NuxtLink
        v-for="item in menuItems"
        :key="item.page"
        :to="{ name: item.page }">{{ item.label }}</NuxtLink>
      <NuxtLink to="/er404">Feil</NuxtLink>
    </header>
  </section>
</template>


<script setup lang="ts">
  const menuItems = [
    {label: 'Produksjoner', page: 'productions'},
    {label: 'Steder', page: 'locations'},
    {label: 'Folk', page: 'index'},
    {label: 'Kart', page: 'map'}
  ]
</script>

<style scoped>
header {
  @apply 
    p-[1.2rem]
    bg-white
    font-sans
    uppercase
    text-zinc-400
    tracking-widest
  ;

  a {
    @apply
      relative
      text-zinc-500
      hover:bg-zinc-200
    ;

    &:not(.logo) {
      @apply mr-6;

      &.router-link-active {
        @apply bg-zinc-200;
      }

      &:not(:last-of-type):after {
        @apply
          content-['|']
          absolute
          -right-4
          text-zinc-300
        ;
      }
    }
  }
}
</style>