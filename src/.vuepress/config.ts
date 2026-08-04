import { viteBundler } from '@vuepress/bundler-vite'
import { defineUserConfig } from "vuepress";
import theme from "./theme.js";

export default defineUserConfig({
  base: "/",

  head: [
    ["link", { rel: "preconnect", href: "https://public-oss.sbeam.dev", crossorigin: "" }],
  ],

  locales: {
    "/": {
      lang: "en-US",
      title: "Sbeam.dev",
      description: "虚空への発信 Signals into the void",
    },
  },

  bundler: viteBundler({
    viteOptions: {},
    vuePluginOptions: {},
  }),

  theme,

  // Enable it with pwa
  // shouldPrefetch: false,
});
