# Signia — Frontend

Frontend del proyecto **Signia**, construido con React + Vite y Tailwind CSS v4.

## Stack

- [React 19](https://react.dev/)
- [Vite 8](https://vite.dev/)
- [Tailwind CSS v4](https://tailwindcss.com/) (vía `@tailwindcss/vite`)
- [oxlint](https://oxc.rs/docs/guide/usage/linter) para linting

## Requisitos

- Node.js
- [pnpm](https://pnpm.io/)

## Scripts

```bash
pnpm install     # instalar dependencias
pnpm dev         # servidor de desarrollo
pnpm build       # build de producción (salida en dist/)
pnpm preview     # previsualizar el build de producción
pnpm lint        # lint con oxlint
```

## Estructura

```
src/
├── assets/    # imágenes, íconos, etc.
├── pages/     # páginas/vistas
├── App.jsx    # componente raíz
├── index.css  # estilos globales y variables de tema
└── main.jsx   # punto de entrada
```
