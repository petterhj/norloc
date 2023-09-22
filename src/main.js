import { createApp } from 'vue';
import { storeToRefs } from 'pinia';
import { supabase } from './lib/supabase';
import router from './router';
import store from './store';
import i18n from './locale';
import { useUserStore } from '@/store/user';

import './style.css';
import 'vue-material-design-icons/styles.css';

import App from './App.vue';

const app = createApp(App);

app.use(router);
app.use(store);
app.use(i18n);

const userStore = useUserStore();

const { isSignedIn, user } = storeToRefs(userStore);
const { setSession } = userStore;

router.beforeEach((to, from, next) => {
  console.debug('to=', to.name, isSignedIn.value);
  const { requiresAuth, requiresAnon } = to.meta;
  console.log(user.value);

  if (requiresAuth && !isSignedIn.value) {
    next({ name: 'signin', query: { redirectFrom: to.fullPath } });
  }
  else if ((requiresAnon || to.name === 'signin') && isSignedIn.value) {
    next({ name: 'profile' });
  } else {
    next();
  }
});

// Returns the session, refreshing it if necessary.
// https://supabase.com/docs/reference/javascript/auth-getsession
supabase.auth.getSession().then(async ({ data }) => {
  // await new Promise(r => setTimeout(r, 2000));
  await setSession(data.session);
});

// Receive a notification every time an auth event happens.
// https://supabase.com/docs/reference/javascript/auth-onauthstatechange
supabase.auth.onAuthStateChange(async (event, session) => {
  await setSession(session);
  
  if (event === 'SIGNED_OUT' && router.currentRoute.value.meta?.requiresAuth) {
    router.push({ name: 'signin' });
  }
});


app.mount('#app');
