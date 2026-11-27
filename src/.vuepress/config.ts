import { cpSync, mkdirSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { viteBundler } from "@vuepress/bundler-vite";
import { defineUserConfig } from "vuepress";
import theme from "./theme.js";

// The `/zh/` locale reuses the root articles, but VuePress needs real files
// under `src/zh/` so every page gets its own locale and metadata. Symlinks
// cannot be used because Vite resolves them to the root modules, making the
// `/zh/` pages inherit the root page data.
//
// This runs when the config is loaded, which is before VuePress scans pages.
// An `onInitialized` hook would be too late: pages are already resolved by then.
const postsSource = fileURLToPath(new URL("../posts/", import.meta.url));
const postsDestination = fileURLToPath(new URL("../zh/posts/", import.meta.url));

rmSync(postsDestination, { recursive: true, force: true });
mkdirSync(postsDestination, { recursive: true });
cpSync(postsSource, postsDestination, { recursive: true });

export default defineUserConfig({
  base: "/",

  head: [
    ["link", { rel: "preconnect", href: "https://public-oss.sbeam.dev", crossorigin: "" }],
  ],

  locales: {
    "/": {
      lang: "en-US",
      title: "Sbeam.dev",
      description: "",
    },
    "/zh/": {
      lang: "zh-TW",
      title: "Sbeam.dev",
      description: "",
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
