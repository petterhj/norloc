<script setup>
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { supabase } from '@/lib/supabase';
import ProductionCard from '@/components/cards/ProductionCard.vue';

const { t } = useI18n();
const route = useRoute();

const productions = ref([]);
const loading = ref(false);
const errorMessage = ref('');

async function getProductions(type) {
  if (type && !['film', 'tv'].includes(type)) {
    console.warn(type);
    return;
  }

  const query = supabase.from('productions').select();
  
  if (type) {
    query.eq('type', type.toUpperCase());
  }
  
  query.order('release_date', { ascending: false });

  const { error, data } = await query;
  
  if (error) throw error;

  productions.value = data;
}

watch(route, async (route) => {
  const { type } = route.params;
  try {
    errorMessage.value = null;
    loading.value = true;
    await getProductions(type);
  } catch (error) {
    console.error(error);
    const { type } = route.params;
    errorMessage.value = t('productions.errors.fetch', { type });
  } finally {
    loading.value = false;
  }

}, { immediate: true });
</script>

<template>
  <div
    v-if="!loading && !errorMessage"
    class="grid grid-flow-col auto-cols-max gap-6"
  >
    <ProductionCard
      class="h-60 w-40"
      :key="production.id"
      v-for="production in productions"
      :production="production"
    />
  </div>

  <div v-else-if="errorMessage" class="alert alert-error mt-8">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="stroke-current shrink-0 h-6 w-6"
      fill="none"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
      />
    </svg>
    <span>{{ errorMessage }}</span>
  </div>
</template>
