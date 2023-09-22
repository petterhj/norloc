<script setup>
import { decode } from 'blurhash';
import { onMounted, ref } from 'vue';

const props = defineProps({
  hash: {
    type: String,
    required: true,
  },
  aspectRatio: {
    type: Number,
    default: 1
  },
});

const canvas = ref(null);

onMounted(() => {
  const pixels = decode(props.hash, 32, 32);
  const imageData = new ImageData(pixels, 32, 32);
  const context = canvas.value.getContext('2d');
  context.putImageData(imageData, 0, 0);
});
</script>

<template>
  <div
    class="relative h-0"
    :style="`padding-bottom: ${aspectRatio * 100}%`"
  >
    <canvas
      ref="canvas"
      class="absolute top-0 left-0 right-0 bottom-0 w-full h-full"
      width="32"
      height="32"
    />
  </div>
</template>
