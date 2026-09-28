// Configurazione condivisa del frontend.
// La base URL si puo' sovrascrivere con la variabile d'ambiente VITE_API_BASE_URL.
export const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
).replace(/\/+$/, "");

export const PAGE_SIZE = 50;
