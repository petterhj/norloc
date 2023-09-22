<script setup>
import { ref, onMounted } from 'vue';
import { supabase } from '@/lib/supabase';

const users = ref([]);

async function getMembers() {
  const { data } = await supabase
    .from('users')
    .select();
  users.value = data;
}

onMounted(() => {
  getMembers();
});
</script>

<template>
  <div class="grid grid-flow-col auto-cols-max gap-6">
    <div
      v-for="user in users"
      :key="user.id"
      class="card w-96 bg-neutral text-neutral-content"
    >
      <div class="card-body">
        <h2 class="card-title">
          {{ user.first_name }} {{ user.last_name }}
          <span class="badge badge-secondary badge-sm">
            {{ $t(`auth.roles.${user.role.toLowerCase()}`).toUpperCase() }}
          </span>
        </h2>
      </div>
    </div>
  </div>
</template>
