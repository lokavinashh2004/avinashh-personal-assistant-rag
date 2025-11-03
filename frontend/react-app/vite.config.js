import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/chat': 'http://localhost:7860',
      '/health': 'http://localhost:7860'
    }
  },
  build: {
    outDir: '../static',
    emptyOutDir: true
  }
})

