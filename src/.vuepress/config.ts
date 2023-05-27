import { defineUserConfig } from "vuepress";
import theme from "./theme.js";

export default defineUserConfig({
  base: "/",

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
