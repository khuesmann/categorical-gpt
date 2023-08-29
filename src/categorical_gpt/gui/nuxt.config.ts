import defaultEnv from './env';
const runtimeEnv = process.env;
const env = { ...defaultEnv, ...runtimeEnv };

export default defineNuxtConfig({
  ssr: false,
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/tailwindcss',
    'nuxt-icon',
    '@pinia/nuxt',
    '@pinia-plugin-persistedstate/nuxt',
  ],
  runtimeConfig: { public: { ...env } },
});
