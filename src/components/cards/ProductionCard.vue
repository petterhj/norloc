<script setup>
import { computed } from 'vue';
import LazyImg from '@/components/img/LazyImg.vue';

const props = defineProps({
  production: {
    type: Object,
    required: true,
  },
});

const productionTooltip = computed(() => {
  const { title, release_date } = props.production;
  return `${title} (${release_date.substring(0, 4)})`;
});

const productionRoute = computed(() => {
  const { type, slug } = props.production;
  return {
    name: 'production',
    params: { type: type.toLowerCase(), slug },
  };
});
</script>

<template>
  <div class="tooltip tooltip-bottom" :data-tip="productionTooltip">
    <router-link :to="productionRoute">
      <div class="indicator h-full w-full">
        <span
          v-if="!production.published"
          class="indicator-item indicator-center badge badge-warning"
        >
          {{ $t('general.unpublished').toUpperCase() }}
        </span> 
        <lazy-img
          class="rounded-md overflow-hidden"
          bucket="productions"
          :path="production.poster_path"
          :blurhash="production.blur_hash"
          :alt="productionTooltip"
        />
        
        <!-- <div
          v-else
          class="
            flex items-center
            h-full w-full
            rounded-md bg-base-300
          "
        >
          {{ productionTooltip }}
        </div> -->
      </div>
    </router-link>
  </div>
</template>
