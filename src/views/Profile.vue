<script setup>
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/store/user';
import ProfileForm from '@/components/forms/ProfileForm.vue';

const userStore = useUserStore();
const { user } = storeToRefs(userStore);
const { signOut } = userStore;
</script>

<template>
  <div v-if="user" class="flex gap-12 mb-12">
    <div class="basis-80">
      <div class="form-control w-full max-w-xs">
        <label for="id" class="label">
          <span class="label-text">{{ $t('auth.id') }}</span>
        </label>
        <input
          id="id"
          type="text"
          class="input input-bordered w-full max-w-xs"
          :value="user.id"
          disabled
        >
      </div>

      <div class="form-control w-full max-w-xs">
        <label for="email" class="label">
          <span class="label-text">{{ $t('auth.fields.email') }}:</span>
        </label>
        <input
          id="email"
          type="text"
          class="input input-bordered w-full max-w-xs"
          :value="user.email"
          disabled
        >
      </div>

      <div class="form-control w-full max-w-xs">
        <label for="role" class="label">
          <span class="label-text">{{ $t('auth.role') }}:</span>
        </label>
        <input
          id="role"
          type="text"
          class="input input-bordered w-full max-w-xs"
          :value="user.role"
          disabled
        >
      </div>

      <div class="form-control w-full max-w-xs">
        <label for="permissions" class="label">
          <span class="label-text">{{ $t('auth.permissions') }}:</span>
        </label>
        <textarea
          id="permissions"
          type="text"
          class="textarea textarea-bordered w-full max-w-xs"
          :rows="8"
          :value="JSON.stringify(user.permissions, null, 2)"
          disabled
        />
      </div>
    </div>
    <ProfileForm />
  </div>

  <button
    class="btn btn-warning mt-12"
    @click="signOut"
  >
    {{ $t('auth.signout') }}
  </button>
</template>
