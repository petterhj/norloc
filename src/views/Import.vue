<script setup>
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { supabase } from '@/lib/supabase';
import AlertBoxOutlineIcon from 'icons/AlertBoxOutline.vue';
import LazyImg from '@/components/img/LazyImg.vue';

const { t } = useI18n();

const loading = ref(false);
const query = ref('oslo 31 august');
const queryType = ref('film');
const searchResults = ref([]);
const errorMessage = ref('');

async function searchMovie() {
  try {
    loading.value = true;
    errorMessage.value = null;

    const { data, error } = await supabase.functions.invoke(
      'search_movie',
      { body: { type: queryType.value, query: query.value } },
    );

    if (error) throw error;

    searchResults.value = data;
  } catch (error) {
    console.debug(error);
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="mx-32 my-16">
    <div class="join w-full">
      <input
        v-model="query"
        class="input input-bordered join-item w-full"
        placeholder="Search"
      >
      <select
        v-model="queryType"
        class="select select-bordered join-item"
      >
        <option value="film">
          Film
        </option>
        <option value="tv">
          TV
        </option>
      </select>
      <button class="btn btn-secondary join-item" @click="searchMovie">
        Search
      </button>
    </div>

    <div class="mt-16">
      <router-link
        v-for="result in searchResults"
        :key="result.id"
        :to="{
          name: 'import-production',
          params: {
            type: result.type,
            tmdbid: result.id,
          }
        }"
        class="flex mt-8 bg-base-300 rounded-md"
      >
        <figure class="shrink-0 w-40 h-60">
          <lazy-img
            class="overflow-hidden rounded-md"
            bucket="productions"
            :src="result.poster_url"
            :alt="result.original_title"
          />
        </figure>

        <div class="flex flex-col gap-4 p-6">
          <h2 class="flex items-center justify-between text-2xl">
            {{ result.original_title }} ({{ result.release_date.slice(0, 4) }})
            <div class="badge badge-success badge-lg">
              {{ result.original_language }}
            </div>
          </h2>
          <p class="line-clamp-3">
            {{ result.overview }}
          </p>
        </div>
      </router-link>
    </div>

    <div v-if="errorMessage" class="alert alert-error mt-8">
      <AlertBoxOutlineIcon />
      <span>{{ errorMessage }}</span>
    </div>
  </div>
</template>
