<template>
  <header>
    <NuxtLink :to="{ name: 'index' }" class="font-semibold">
      Norske opptakssteder
    </NuxtLink>
    <span class="text-red-700">&#9642;</span>
    <NuxtLink :to="{ name: 'index' }">
      Produksjoner
    </NuxtLink> |
    <NuxtLink :to="{ name: 'index' }">
      Steder
    </NuxtLink>
  </header>
</template>

<style scoped>
header {
  @apply 
  bg-white
    p-5
    font-sans
    uppercase
    text-gray-500
    tracking-widest
  ;

  a {
    @apply hover:bg-gray-200;
  }
}
</style>