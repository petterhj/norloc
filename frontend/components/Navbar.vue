<template>
  <header>
    <NuxtLink
      :to="{ name: 'index' }"
      class="font-semibold">Norske opptakssteder</NuxtLink>
    <span class="text-accent px-2">&#9642;</span>
    <NuxtLink
      :to="{ name: 'index' }">Produksjoner</NuxtLink> |
    <NuxtLink
      :to="{ name: 'index' }">Steder</NuxtLink> |
    <NuxtLink
      :to="{ name: 'index' }">Folk</NuxtLink> |
    <NuxtLink
      :to="{ name: 'index' }">Kart</NuxtLink>
  </header>
</template>

<style scoped>
header {
  @apply 
    bg-white
    p-[1.2rem]
    font-sans
    uppercase
    text-zinc-400
    tracking-widest
  ;

  a {
    @apply
      text-zinc-500
      hover:bg-zinc-200
    ;
  }
}
</style>