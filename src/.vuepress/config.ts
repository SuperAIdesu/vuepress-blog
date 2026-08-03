import { viteBundler } from '@vuepress/bundler-vite'
import { defineUserConfig } from "vuepress";
import theme from "./theme.js";

export default defineUserConfig({
  base: "/",

  head: [
    ["link", { rel: "preconnect", href: "https://fonts.googleapis.com" }],
    [
      "link",
      { rel: "preconnect", href: "https://fonts.gstatic.com", crossorigin: "" },
    ],
    ["link", { rel: "preconnect", href: "https://cdn.jsdelivr.net" }],
    [
      "link",
      {
        rel: "preload",
        href: "https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@100..900&display=swap",
        as: "style",
        onload: "this.onload=null;this.rel='stylesheet'",
      },
    ],
    ["noscript", {}, `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@100..900&display=swap">`],
    [
      "link",
      {
        rel: "preload",
        href: "https://cdn.jsdelivr.net/npm/lxgw-wenkai-tc-web@latest/style.css",
        as: "style",
        onload: "this.onload=null;this.rel='stylesheet'",
      },
    ],
    ["noscript", {}, `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/lxgw-wenkai-tc-web@latest/style.css">`],
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
