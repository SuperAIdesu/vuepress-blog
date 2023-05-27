import { navbar } from "vuepress-theme-hope";

export const zhNavbar = navbar([
  "/zh/",
  {
    text: "文章",
    icon: "edit",
    link: "/posts/",
  },
  {
    text: "標籤",
    icon: "tag",
    link: "/tag/",
  },
  {
    text: "關於",
    icon: "info",
    link: "/intro.html",
  }
]);
