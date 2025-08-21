import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// Detectar entorno
const isProd = process.env.NODE_ENV === "production";
const backendUrl = isProd
  ? "https://videolink-backend.onrender.com"
  : "http://localhost:10000"; // puerto de desarrollo local

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    strictPort: true,
    proxy: {
      // Proxy para llamadas REST
      "/api": {
        target: backendUrl,
        changeOrigin: true,
        secure: true,
      },
      // Proxy para WebSockets
      "/ws": {
        target: backendUrl.replace("http", "ws"),
        ws: true,
        changeOrigin: true,
        secure: true,
      },
      "/socket.io": {
        target: backendUrl.replace("http", "ws"),
        ws: true,
        changeOrigin: true,
        secure: true,
      },
    },
  },
  build: {
    outDir: "dist", // requerido para deploy en Render
  },
});
