import { defineClientConfig } from "vuepress/client";

export default defineClientConfig({
  enhance({ router }) {
    // VuePress 2.0.0-rc.33 restores scroll through vue-router's
    // `ScrollRestoration` plugin. The theme still installs the old
    // `scrollBehavior` wrapper, which makes vue-router scroll to the current
    // hash whenever the scroll spy updates it. Removing the deprecated option
    // avoids that feedback loop (and the corresponding runtime warning).
    delete (router.options as { scrollBehavior?: unknown }).scrollBehavior;
  },
});
