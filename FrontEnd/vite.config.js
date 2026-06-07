import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
  build: {
    // Minificação e otimizações
    minify: "terser",
    terserOptions: {
      compress: {
        drop_console: true,
      },
    },
    // Code splitting para lazy loading
    rollupOptions: {
      output: {
        manualChunks: {
          leaflet: ["leaflet"],
        },
      },
    },
    // Reportar tamanho final
    reportCompressedSize: true,
  },
});