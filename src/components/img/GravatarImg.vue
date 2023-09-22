<script setup>
import md5 from 'md5';
import { computed } from 'vue';

const props = defineProps({
  email: String,
  alt: {
    type: String,
    default: null,
  },
  size: {
    type: Number,
    default: 80
  },
  defaultImg: {
    type: String,
    default: 'retro',
  },
  rating: {
    type: String,
    default: 'g'
  },
});

const src = computed(() => {
  return [
    'https://www.gravatar.com/avatar/',
    md5(props.email.trim().toLowerCase()),
    `?s=${props.size}`,
    `&d=${props.defaultImg}`,
    `&r=${props.rating}`
  ].join('');
});
</script>

<template>
  <img :src="src" :alt="alt">
</template>
