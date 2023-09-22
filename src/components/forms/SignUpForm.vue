<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useForm } from 'vee-validate';
import * as yup from 'yup';
import { supabase } from '@/lib/supabase';

const router = useRouter();
const { values, errors, meta, handleSubmit, defineInputBinds } = useForm({
  validationSchema: yup.object({
    email: yup.string().required().email(),
    password: yup.string().min(8).required(),
    firstName: yup.string().min(2).required(),
    lastName: yup.string().min(2).required(),
  }),
});

const loading = ref(false);
const handlerError = ref(null);

const email = defineInputBinds('email');
const password = defineInputBinds('password');
const firstName = defineInputBinds('firstName');
const lastName = defineInputBinds('lastName');


const handleSignUp = handleSubmit(async (values) => {
  
  try {
    loading.value = true;
    handlerError.value = null;

    const { email, password, firstName, lastName } = values;

    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          first_name: firstName,
          last_name: lastName,
        },
      },
    });

    if (error) throw error;
    
    await router.push({ name: 'profile' });
  } catch (error) {
    if (error instanceof Error) {
      console.error(error.message);
      handlerError.value = error;
    }
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <form @submit.prevent="handleSignUp">
    <div class="form-control w-full max-w-xs">
      <label for="email" class="label">
        <span class="label-text">{{ $t('auth.fields.email') }}</span>
      </label>
      <input
        id="email"
        type="email"
        required
        autocomplete="username"
        class="input input-bordered w-full max-w-xs"
        :class="{ 'input-error': errors.email }"
        v-bind="email"
      >
      <p v-if="errors.email" class="mt-1 text-sm leading-6 text-error">
        {{ errors.email }}
      </p>
    </div>

    <div class="form-control w-full max-w-xs">
      <label for="password" class="label">
        <span class="label-text">{{ $t('auth.fields.password') }}</span>
      </label>
      <input
        id="password"
        type="password"
        required
        autocomplete="current-password" 
        class="input input-bordered w-full max-w-xs"
        :class="{ 'input-error': errors.password }"
        v-bind="password"
      >
      <p v-if="errors.password" class="mt-1 text-sm leading-6 text-error">
        {{ errors.password }}
      </p>
    </div>

    <div class="form-control w-full max-w-xs mt-8">
      <label for="firstName" class="label">
        <span class="label-text">{{ $t('member.fields.firstName') }}</span>
      </label>
      <input
        id="firstName"
        type="text"
        required
        class="input input-bordered w-full max-w-xs"
        :class="{ 'input-error': errors.firstName }"
        v-bind="firstName"
      >
      <p v-if="errors.firstName" class="mt-1 text-sm leading-6 text-error">
        {{ errors.firstName }}
      </p>
    </div>
    <div class="form-control w-full max-w-xs">
      <label for="lastName" class="label">
        <span class="label-text">{{ $t('member.fields.lastName') }}</span>
      </label>
      <input
        id="lastName"
        type="text"
        required
        class="input input-bordered w-full max-w-xs"
        :class="{ 'input-error': errors.lastName }"
        v-bind="lastName"
      >
      <p v-if="errors.lastName" class="mt-1 text-sm leading-6 text-error">
        {{ errors.lastName }}
      </p>
    </div>

    <div class="flex gap-4 mt-6">
      <input
        type="submit"
        class="btn btn-primary"
        :value="$t('auth.signup')"
        :disabled="!meta.dirty || loading"
      >
    </div>
  </form>

  <div class="mt-8">
    <pre>values: {{ values }}</pre>
    <pre>errors: {{ errors }}</pre>
  </div>

  <div v-if="handlerError" class="alert alert-error mt-8">
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
    <span>{{ handlerError.message }}</span>
  </div>
</template>