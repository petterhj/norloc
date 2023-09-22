<script setup>
import { defineAsyncComponent, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { supabase } from '@/lib/supabase';

const GravatarImg = defineAsyncComponent(
  () => import('@/components/img/GravatarImg.vue')
);  
  
const { t } = useI18n();
const router = useRouter();
const route = useRoute();

const loading = ref(false);
const errorMessage = ref('');
const email = ref('');
const password = ref('');

const handleSignIn = async () => {
  try {
    loading.value = true;
    errorMessage.value = null;

    const { error } = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value,
    });

    if (error) throw error;
    
    const { redirectFrom } = route.query;

    if (redirectFrom) {
      await router.push({ path: redirectFrom });
    } else {
      await router.push({ name: 'profile' });
    }
  } catch (error) {
    if (error instanceof Error) {
      console.error(error);
      if (error.message === 'Invalid login credentials') {
        errorMessage.value = t('auth.states.invalidCredentials');
      } else {
        errorMessage.value = error.message;
      }
      
    }
  } finally {
    loading.value = false;
  }
};

const loginAs = (user) => {
  email.value = user.email;
  password.value = user.password;
};
</script>

<template>
  <div class="mb-8">
    <div
      v-for="user in [
        { email: 'admin@example.com', password: 'admin-password' },
        { email: 'contributor@example.com', password: 'contributor-password' },
        { email: 'user@example.com', password: 'user-password' },
      ]"
      :key="user.email"
      class="tooltip"
      :data-tip="user.email"
    >
      <div
        role="button"
        tabindex="0"
        class="btn btn-ghost btn-circle avatar"
        @click="loginAs(user)"
      >
        <div class="w-10 rounded-full">
          <gravatar-img :email="user.email" />
        </div>
      </div>
    </div>
  </div>

  <form @submit.prevent="handleSignIn">
    <div class="form-control w-full max-w-xs">
      <label for="email" class="label">
        <span class="label-text">{{ $t("auth.fields.email") }}</span>
      </label>
      <input
        id="email"
        type="email"
        required
        autocomplete="username"
        class="input input-bordered w-full max-w-xs"
        v-model="email"
      >
    </div>

    <div class="form-control w-full max-w-xs">
      <label for="password" class="label">
        <span class="label-text">{{ $t("auth.fields.password") }}</span>
      </label>
      <input
        id="password"
        type="password"
        required
        autocomplete="current-password" 
        class="input input-bordered w-full max-w-xs"
        v-model="password"
      >
    </div>

    <div class="flex gap-6 items-center mt-6">
      <input
        type="submit"
        class="btn btn-primary"
        :value="$t('auth.signin')"
        :disabled="loading"
      >
      <router-link
        :to="{ name: 'signup' }"
        class="link text-md"
      >
        {{ $t('auth.signup') }}
      </router-link>
    </div>
  </form>

  <div v-if="errorMessage" class="alert alert-error mt-8">
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