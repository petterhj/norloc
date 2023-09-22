<script setup>
import { computed, defineAsyncComponent } from 'vue';
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/store/user';
import AccountCircleOutlineIcon from 'icons/AccountCircleOutline.vue';
import TelevisionIcon from 'icons/Television.vue';
import MovieOpenOutlineIcon from 'icons/MovieOpenOutline.vue';

const GravatarImg = defineAsyncComponent(
  () => import('@/components/img/GravatarImg.vue')
);
  
const route = useRoute();
const store = useUserStore();
const { isSignedIn, user } = storeToRefs(store);

const redirectFromQuery = computed(() => {
  return route.name !== 'signin' ? 
    { redirectFrom: route.fullPath } :
    null;
});
</script>

<template>
  <div class="navbar bg-base-100">
    <div class="flex-1">
      <router-link
        :to="{ name: 'home' }"
        class="btn btn-ghost normal-case text-xl"
        active-class="active"
      >
        {{ $t('app.title') }}
      </router-link>
    </div>

    <div class="flex-none mr-8">
      <ul class="menu menu-horizontal flex gap-2">
        <li>
          <router-link :to="{ name: 'productions' }" active-class="active">
            {{ $t('productions.productions') }}
          </router-link>
        </li>
        <li>
          <router-link
            :to="{ name: 'productions', params: { type: 'film' } }"
            class="tooltip tooltip-bottom"
            active-class="active"
            :data-tip="$t('productions.types.film')"
          >
            <MovieOpenOutlineIcon />
          </router-link>
        </li>
        <li>
          <router-link
            :to="{ name: 'productions', params: { type: 'tv' } }"
            class="tooltip tooltip-bottom"
            active-class="active"
            :data-tip="$t('productions.types.tv')"
          >
            <TelevisionIcon />
          </router-link>
        </li>
        <li>
          <router-link :to="{ name: 'people' }" active-class="active">
            {{ $t('people.people') }}
          </router-link>
        </li>
        <li>
          <router-link :to="{ name: 'members' }" active-class="active">
            {{ $t('member.members') }}
          </router-link>
        </li>
      </ul>
    </div>

    <div class="flex-none gap-2">
      <div class="form-control">
        <input
          type="text"
          :placeholder="$t('general.search')"
          class="input input-bordered w-24 md:w-auto"
        >
      </div>
      
      <router-link
        v-if="isSignedIn"
        :to="{ name: 'profile' }"
        role="button"
        tabindex="0"
        class="btn btn-ghost btn-circle avatar"
        active-class="active"
      >
        <div class="w-10 rounded-full">
          <gravatar-img :email="user.email" />
        </div>
      </router-link>

      <router-link
        v-else
        :to="{ name: 'signin', query: redirectFromQuery }"
        role="button"
        tabindex="0"
        class="btn btn-ghost btn-circle avatar"
        active-class="active"
      >
        <div class="w-10 rounded-full">
          <AccountCircleOutlineIcon class="text-3xl" />
        </div>
      </router-link>
    </div>
  </div>
</template>