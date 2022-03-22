<template>
  <nav>
    <div class="flex gap-3" v-for="(item, index) in menuItems" :key="index">
      <span>{{ item.label }}:</span>
      <!--select 
        v-if="item.dropdown"
        @change="onDropdownMenuSelect($event, item.items)">
      >
        <option 
          v-for="(item, index) in item.items" :key="index"
        >
          {{item.label}}
        </option>
      </select-->
      <div class="flex gap-3"><!-- v-else-->
        <span v-for="(item, index) in item.items" :key="index" class="link">
          <NuxtLink
            :to="{ name: 'index', params: item.params }">{{ item.label }}</NuxtLink>
        </span>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
interface MenuItem {
  label: String
  page?: String
  items?: MenuItem[]
  params?: object
}

const props = defineProps<{
  menuItems: MenuItem[]
}>()
</script>

<style scoped>
nav {
  @apply
    px-[1.2rem]
    py-2
    flex
    gap-6
    bg-neutral-700
    font-sans
    uppercase
    tracking-widest
  ;
}
</style>
