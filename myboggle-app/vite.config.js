import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  server: {
    allowedHosts: [
      "graphcomedy-tropicgregory-5173.codio.io"
    ],
    proxy: {
      '/api': {
        target: 'https://graphcomedy-tropicgregory-8000.codio.io',
        changeOrigin: true,
        secure: false
      }
    }
  },
  plugins: [react()],
})