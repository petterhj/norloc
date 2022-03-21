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
    </header>
    <nav class="bg-red-50" id="submenu" v-if="subMenuItems && subMenuItems.length > 0">
      {{ subMenuItems }}
    </nav>
  </section>
</template>


<script lang="ts" setup>
  import { storeToRefs } from 'pinia'
  import { useMenu } from "@/store/navbar";

  const menuStore = useMenu()
  const { menuItems, subMenuItems } = storeToRefs(menuStore)
</script>

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
      relative
      px-1
      text-zinc-500
      hover:bg-zinc-200
    ;

    &:not(.logo) {
      @apply mr-4;

      &:not(:last-of-type):after {
        @apply
          content-['|']
          absolute
          -right-3
          text-zinc-300
        ;
      }
    }
  }
}
</style>