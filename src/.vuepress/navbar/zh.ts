import { navbar } from "vuepress-theme-hope";

export const zhNavbar = navbar([
  "/zh/",
  {
    text: "文章",
    icon: "edit",
    link: "/zh/posts/",
  },
  {
    text: "標籤",
    icon: "tag",
    link: "/zh/tag/",
  },
  {
    text: "關於",
    icon: "info",
    link: "/zh/intro.html",
  },
]);
