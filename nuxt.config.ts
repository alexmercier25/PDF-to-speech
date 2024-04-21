// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["nuxt-primevue"],
  primevue: {
    /* Options */
  },
  css: ["primeicons/primeicons.css", "primeflex/primeflex.css"],
  appConfig: {
    pdfToTextApi: process.env.PDFTOTEXT_API
  },
});
