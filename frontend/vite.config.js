import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  // 127.0.0.1 e non "localhost": su macOS/Windows Node risolve "localhost" a ::1
  // (IPv6), mentre uvicorn per default ascolta solo su IPv4 -> il proxy da' 502.
  const proxyTarget = env.API_PROXY_TARGET || "http://127.0.0.1:8000";

  return {
    plugins: [react()],
    server: {
      port: 5173,
      // Proxy opzionale: con VITE_API_BASE_URL=/api le chiamate passano dal dev
      // server e raggiungono il backend senza bisogno di CORS.
      proxy: {
        "/api": {
          target: proxyTarget,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
  };
});
