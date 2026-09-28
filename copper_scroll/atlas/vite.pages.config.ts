// Static build for GitHub Pages. Usage (from copper_scroll/atlas):
//   corepack pnpm exec vite build --config vite.pages.config.ts
// Output: ../atlas-site/, served at https://quadrin.github.io/AncientHebrewTexts/copper_scroll/atlas-site/
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const here = fileURLToPath(new URL(".", import.meta.url));

export default defineConfig({
  root: `${here}pages`,
  base: "/AncientHebrewTexts/copper_scroll/atlas-site/",
  publicDir: `${here}public`,
  plugins: [react()],
  resolve: { alias: { "@": here.replace(/\/$/, "") } },
  build: { outDir: process.env.ATLAS_SITE_OUT ?? `${here}../atlas-site`, emptyOutDir: true },
});
