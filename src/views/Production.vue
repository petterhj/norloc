<script setup>
import { ref, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useRoute } from 'vue-router';
import { supabase } from '@/lib/supabase';
import { useUserStore } from '@/store/user';

const route = useRoute();
const userStore = useUserStore();
const { user } = storeToRefs(userStore);

const loading = ref(false);
const production = ref(null);
const runtime = ref(null);
const published = ref(null);

async function getProduction() {
  const { type, slug, tmdbid } = route.params;

  const query = supabase
    .from('productions')
    .select();

  if (type && slug) {
    query.eq('type', type.toUpperCase())
      .eq('slug', slug);  
  } else if (tmdbid) {
    query.eq('tmdb_id', tmdbid.toString());
  }

  const { data } = await query
    .limit(1)
    .single();

  production.value = data;
  runtime.value = data.runtime;
  published.value = data.published;
}

async function updateProduction() {
  try {
    loading.value = true;

    console.warn('runtime', runtime.value);

    const updates = {
      runtime: runtime.value,
      published: published.value,
    };

    const res = await supabase
      .from('productions')
      .update(updates)
      .eq('id', production.value.id)
      .select();

    console.log('update', production.value.id, updates, res);
    const { data, error } = res;

    if (error) throw error;

    const updatedData = data.find((p) => p.id === production.value.id);
    if (updatedData) {
      production.value = updatedData;
    }
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  getProduction();
});
</script>

<template>
  {{ route.params.slug }}
  {{ production }}

  <hr class="my-4">
  
  <form
    v-if="user && user.permissions.includes('productions.update')"
    class="form-widget"
    @submit.prevent="updateProduction"
  >
    <div class="form-control w-full max-w-xs">
      <label for="runtime" class="label">
        <span class="label-text">{{ $t('production.fields.runtime') }}</span>
      </label>
      <input
        id="runtime"
        type="number"
        class="input input-bordered w-full max-w-xs"
        :disabled="loading"
        v-model="runtime"
      >
    </div>
    
    <div class="form-control w-full max-w-xs">
      <label class="cursor-pointer label">
        <span class="label-text">{{ $t('production.fields.published') }}</span>
        <input
          type="checkbox"
          v-model="published"
          class="checkbox checkbox-warning"
        >
      </label>
    </div>
    
    <div class="mt-6">
      <input
        type="submit"
        class="btn btn-primary"
        :value="$t('general.save')"
        :disabled="loading"
      >
    </div>
  </form>
</template>
