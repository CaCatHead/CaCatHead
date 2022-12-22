import { defineConfig } from 'vite';

export default defineConfig({
  publicDir: '../app/public',
  server: {
    fs: {
      // Allow serving files from one level up to the project root
      allow: ['..'],
    },
  },
});
