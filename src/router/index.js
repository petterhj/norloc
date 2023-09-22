import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import * as routerGuards from './routerGuards';

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/produksjoner/:type(film|tv)?',
    name: 'productions',
    component: () => import('../views/Productions.vue'),
  },
  {
    path: '/produksjoner/:type(film|tv)/:slug',
    name: 'production',
    component: () => import('../views/Production.vue'),
  },
  {
    path: '/produksjoner/import',
    name: 'import',
    meta: { requiresAuth: true },
    component: () => import('../views/Import.vue'),
  },
  {
    path: '/produksjoner/:type(film|tv)/import/tmdb/:tmdbid(\\d+)',
    name: 'import-production',
    meta: { requiresAuth: true },
    beforeEnter: routerGuards.tmdbImport,
  },
  {
    path: '/folk',
    name: 'people',
    component: () => import('../views/People.vue'),
  },
  {
    path: '/medlemmer',
    name: 'members',
    component: () => import('../views/Members.vue'),
  },
  {
    path: '/logg-inn',
    name: 'signin',
    component: () => import('../views/SignIn.vue'),
  },
  {
    path: '/meg',
    name: 'profile',
    meta: { requiresAuth: true },
    component: () => import('../views/Profile.vue'),
  },
  {
    path: '/bli-medlem',
    name: 'signup',
    meta: { requiresAnon: true },
    component: () => import('../views/SignUp.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
