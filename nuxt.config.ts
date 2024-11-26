// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  modules: [
    "nuxt-quasar-ui",
    "@nuxt/icon",
    "@nuxt/eslint",
    "@nuxtjs/tailwindcss",
    "@vueuse/nuxt",
  ],
  quasar: {
    plugins: ["Dialog", "Loading", "Notify"],
    extras: {
      font: "roboto-font",
      animations: "all",
    },
  },
  app: {
    head: {
      title: "Shock Bed",
    },
  },
  imports: {
    dirs: ["./composables", "./utils", "./types"],
  },
  icon: {
    serverBundle: {
      collections: ["mdi", "material-symbols", "twemoji"],
    },
  },
});
