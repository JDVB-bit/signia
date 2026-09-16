import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  // Los tests son de logica pura (sin DOM): corren en node, sin jsdom
  test: {
    environment: 'node',
    include: ['src/**/__tests__/**/*.test.{js,jsx}'],
  },
})
