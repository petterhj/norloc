import { computed, ref } from 'vue';
import { defineStore } from 'pinia';
import { supabase } from '../lib/supabase';

export const useUserStore = defineStore('user', () => {
  const session = ref(null);
  const role = ref(null);
  const permissions = ref([]);
  
  const isSignedIn = computed(() => {
    return !!session.value;
  });

  const user = computed(() => {
    if (session.value) {
      const { id, email } = session.value.user;
      return {
        id,
        email,
        role: role.value,
        permissions: permissions.value,
      };
    }
    return null;
  });

  function setSession(sessionData) {
    console.debug('Updating session data...');
    session.value = sessionData;
    fetchUserPermissions();
  }

  async function fetchUserPermissions() {
    if (!user.value) {
      role.value = null;
      permissions.value = [];
      return;
    }

    try {
      let { data: {
        role: userRole,
        permissions: userPermissions,
      }, error } = await supabase
        .from('user_permissions')
        .select('role, permissions')
        .eq('id', user.value.id)
        .single();

      if (error) throw error;

      role.value = userRole;
      permissions.value = userPermissions.filter((p) => p);
    } catch (error) {
      console.error('Could not fetch user role');
      console.debug(error.message);
      await signOut();
    }
  }

  async function signOut() {
    console.warn('Signing out!');
    try {
      let { error } = await supabase.auth.signOut();
      if (error) throw error;
    } catch (error) {
      console.error(error);
    }
    session.value = null;
    role.value = null;
    permissions.value = [];
  }

  return {
    session,
    user,
    isSignedIn,
    setSession,
    signOut,
  };
});

// if (sessionData) {
//   try {
//     let { data, error } = await supabase
//       .from('users')
//       .select('first_name, last_name, role')
//       .eq('id', sessionData.user.id)
//       .single();
//     if (error) throw error;
//     console.warn('user', data, error, status);
//     profile.value = data;
//     session.value = sessionData;
//     console.warn('DONE UPDATING SESSION DATA');
//     return;
//   } catch (error) {
//     console.error('Could not load user profile');
//     console.debug(error.message);
//     await signOut();
//   }
// }