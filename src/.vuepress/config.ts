import { defineUserConfig } from "vuepress";
import theme from "./theme.js";

export default defineUserConfig({
  base: "/",

  head: [
    ['link', { rel: 'stylesheet', href: '//unpkg.com/heti/umd/heti.min.css' }],
    ['script', {}, 'var element = document.getElementsByClassName("theme-hope-content"); element[0].classList.add("heti");'],
    ['link', { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Noto+Sans+TC&display=swap' }],
    ['script', {src: 'https://static.cloudflareinsights.com/beacon.min.js', "data-cf-beacon": '{"token": "500ee885fc984594bd06da5556209b60"}'}]
    // ['link', { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Noto+Serif+TC&display=swap' }],
    // ['script', {src: '//unpkg.com/heti/umd/heti-addon.min.js'}],
    // ['script', {}, "const heti = new Heti('.heti'); heti.autoSpacing();"]
  ],

  locales: {
    "/": {
      lang: "en-US",
      title: "Sbeam.dev",
      description: "Tech, life and open discussion",
    },
    // "/zh/": {
    //   lang: "zh-TW",
    //   title: "Sbeam.dev",
    //   description: "Tech, life and open discussion",
    // },
  },

  theme,

  // Enable it with pwa
  // shouldPrefetch: false,
});
