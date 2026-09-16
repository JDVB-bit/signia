import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  // Los tests son de logica pura (preprocesado, construccion de muestras): no
  // tocan el DOM, asi que corren en node y no necesitan jsdom.
  test: {
    environment: 'node',
    include: ['src/**/__tests__/**/*.test.{js,jsx}'],
  },
})
