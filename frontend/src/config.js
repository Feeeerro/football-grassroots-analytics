// Configurazione condivisa del frontend.
// I dati sono file JSON statici in public/data/ (generati da export_static.py).
// BASE_URL di Vite rende gli URL indipendenti dal path di deploy.
export const DATA_BASE_URL = `${import.meta.env.BASE_URL}data/`;

export const PAGE_SIZE = 50;
