<script setup>
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/store/user';
import NavBar from '@/components/nav/NavBar.vue';

const store = useUserStore();
const { isSignedIn, user } = storeToRefs(store);
</script>

<template>
  <NavBar />

  <div class="m-6">
    <router-view />
  </div>

  <div class="fixed bottom-0 w-full p-4 bg-base-300 text-accent-focus">
    <span class="text-neutral">Signed in:</span> {{ isSignedIn }} |
    <span class="text-neutral">User:</span> {{ user }}
  </div>
</template>
