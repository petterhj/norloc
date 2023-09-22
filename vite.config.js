/* eslint-disable no-undef */
import path from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: [
      {
        find: '@',
        replacement: path.resolve(__dirname, 'src'),
      },
      {
        find: 'icons',
        replacement: path.resolve(
          __dirname,
          'node_modules/vue-material-design-icons',
        ),
      }
    ],
  },
});
