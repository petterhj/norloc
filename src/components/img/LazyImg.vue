<script setup>
import { ref } from 'vue';
import { vIntersectionObserver } from '@vueuse/components';
import { supabase } from '@/lib/supabase';
import BlurhashImg from './BlurhashImg.vue';

const props = defineProps({
  src: {
    type: String,
    required: false,
    default: null,
  },
  bucket: {
    type: String,
    required: false,
    default: null,
  },
  path: {
    type: String,
    required: false,
    default: null,
  },
  blurhash: {
    type: String,
    required: false,
    default: null,
  },
  alt: {
    type: String,
    required: false,
    default: null,
  },
});

const image = ref(null);
const isLoaded = ref(false);

function setSrc(src) {
  // console.log(image.value, src);
  image.value.src = src;
  image.value.onload = () => {
    isLoaded.value = true;
  };
}

async function onIntersect([{ isIntersecting }]) {
  if (!isIntersecting || isLoaded.value) {
    return;
  }

  if (props.src) {
    setSrc(props.src);
    return;
  }
  
  if (props.bucket && props.path) {
    try {
      const { data: { publicUrl }, error } = await supabase.storage
        .from(props.bucket)
        .getPublicUrl(props.path);

      if (error) throw error;

      setSrc(publicUrl);
    } catch (error) {
      console.error(error);
    }
  }
}
</script>

<template>
  <div
    class="relative w-full h-full bg-base-300"
    v-intersection-observer="onIntersect"
  >
    <blurhash-img
      v-if="blurhash"
      :hash="blurhash"
      :aspect-ratio="1"
      class="absolute top-0 left-0 transition-opacity duration-500 h-full w-full"
      :class="isLoaded ? 'opacity-0' : 'opacity-100'"
    />
    <img
      v-if="src || (bucket && path)"
      ref="image"
      class="absolute top-0 left-0 transition-opacity duration-500 h-full w-full"
      :alt="alt"
      :class="isLoaded ? 'opacity-100' : 'opacity-0'"
    >
    <div
      v-if="!blurhash && (!bucket || !path)"
      class="w-full h-full flex flex-col justify-center items-center text-sm p-8"
    >
      <span>{{ alt }}</span>
    </div>
  </div>
</template>