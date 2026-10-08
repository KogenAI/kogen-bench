import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://bench.kogen.dev',
  output: 'static',
  trailingSlash: 'always',
  build: { inlineStylesheets: 'always' },
});
