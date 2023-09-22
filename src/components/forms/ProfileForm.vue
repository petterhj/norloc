<script setup>
import { onMounted, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { supabase } from '@/lib/supabase';
import { useUserStore } from '@/store/user';

const userStore = useUserStore();
const { user } = storeToRefs(userStore);
const { signOut } = userStore;

const loading = ref(true);
const firstName = ref('');
const lastName = ref('');

onMounted(() => {
  getProfile();
});

async function getProfile() {
  try {
    loading.value = true;
    
    let { data, error, status } = await supabase
      .from('users')
      .select('first_name, last_name, role')
      .eq('id', user.value.id)
      .single();

    if (error) throw error;

    if (data) {
      firstName.value = data.first_name;
      lastName.value = data.last_name;
    }
  } catch (error) {
    console.error('Could not load user profile');
    console.debug(error.message);
    signOut();
  } finally {
    loading.value = false;
  }
}

async function updateProfile() {
  try {
    loading.value = true;

    const updates = {
      id: user.value.id,
      first_name: firstName.value,
      last_name: lastName.value,
      updated_at: new Date(),
    };

    let { error } = await supabase.from('user_profiles').upsert(updates);

    if (error) throw error;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <form v-if="user" class="flex flex-col gap-4 form-widget" @submit.prevent="updateProfile">
    <div class="form-control w-full max-w-xs">
      <label for="firstName" class="label">
        <span class="label-text">{{ $t('member.fields.firstName') }}</span>
      </label>
      <input
        id="firstName"
        type="text"
        class="input input-bordered w-full max-w-xs"
        :disabled="loading"
        v-model="firstName"
      >
    </div>

    <div class="form-control w-full max-w-xs">
      <label for="lastName" class="label">
        <span class="label-text">{{ $t('member.fields.lastName') }}</span>
      </label>
      <input
        id="lastName"
        type="text"
        class="input input-bordered w-full max-w-xs"
        :disabled="loading"
        v-model="lastName"
      >
    </div>

    <div class="mt-3">
      <input
        type="submit"
        class="btn btn-primary"
        :value="$t('form.save')"
        :disabled="loading"
      >
    </div>
  </form>
</template>
