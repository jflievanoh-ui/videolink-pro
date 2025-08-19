import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "https://videolink-backend.onrender.com",
      "/ws": {
        target: "wss://videolink-backend.onrender.com",
        ws: true,
      },
    },
  },
  build: {
    outDir: "dist", // 👈 required for Render deployment
  },
});
