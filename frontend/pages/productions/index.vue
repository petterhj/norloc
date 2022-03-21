<template>
  <div>
    
  </div>
</template>

<script setup>
  import { useMenu } from "@/store/navbar";

  definePageMeta({
    title: 'Produksjoner'
  })

  const menuStore = useMenu()

  menuStore.$patch({
    subMenuItems: [{label: 'Produksjoner', page: 'productions'}],
  })

// const subMenuItems = useLocales()
// subMenuItems.push('foo')
// console.log(subMenuItems)

// const menuItems = useMenu()
// console.log(menuItems)

// useState('useSubItems', () => [
//   {label: 'Produksjoner', page: 'productions'}
// ])

// const subMenuItems = useSubItems()
// console.log(subMenuItems)
// subMenuItems.push({label: 'Kart', page: 'index'})

// const { data: products } = await useFetch(`/cdn/stories`, {
//   baseURL: config.apiURL,
//   params: { token: config.apiToken },
// });
</script>