import { defineUserConfig } from "vuepress";
import theme from "./theme.js";

export default defineUserConfig({
  base: "/",

  head: [
    // ['link', { rel: 'stylesheet', href: '//unpkg.com/heti/umd/heti.min.css' }],
    // ['script', {}, 'var element = document.getElementsByClassName("theme-hope-content"); element[0].classList.add("heti");'],
    ['link', { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Noto+Sans+TC&display=swap' }],
    // ['link', { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Noto+Serif+TC&display=swap' }],
  ],

  locales: {
    "/": {
      lang: "en-US",
      title: "Sbeam.dev",
      description: "虚空への発信 Signals into the void",
    },
  },

  theme,
  templateDev: "./src/.vuepress/templates/index.html",
  templateBuild: "./src/.vuepress/templates/index.html",

  // Enable it with pwa
  // shouldPrefetch: false,
});
