import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },
  preview: {
    host: '0.0.0.0',
    port: process.env.PORT || 3000,
    strictPort: false,
    allowedHosts: [
      'localhost',
      '.onrender.com',
      'social-media-agent-frontend-afwe.onrender.com'
    ]
  }
})
