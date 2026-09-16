# ⚛️ `front/app/` — Aplicación React de SignIA

Construida con **React 19 + Vite 8 + Tailwind CSS v4**, tests con **Vitest** y lint con **oxlint**.

## 📦 Requisitos

- Node.js 24 LTS
- pnpm 11 (fijado en `package.json → packageManager`; con `corepack enable` se usa solo)

## 🛠️ Scripts

```bash
pnpm install     # instala dependencias
pnpm dev         # servidor de desarrollo en http://localhost:5173
pnpm test        # tests unitarios (Vitest, entorno node)
pnpm lint        # lint con oxlint
pnpm build       # build de producción en dist/
pnpm preview     # sirve el build para revisarlo
```

## 📁 Archivos de esta carpeta

| Archivo | Para qué sirve |
|---|---|
| `index.html` | Documento raíz (idioma `es`, título, favicon) donde se monta React |
| `package.json` / `pnpm-lock.yaml` | Dependencias y scripts, con versión de pnpm fijada |
| `vite.config.js` | Plugins (React, Tailwind) y configuración de Vitest |
| `.oxlintrc.json` | Reglas de lint (hooks de React, exports de componentes) |
| `Dockerfile` | Imagen en dos etapas: compila con Node 24 y sirve con nginx |
| `nginx.conf` | Sirve la SPA, cachea `/assets/` y redirige rutas a `index.html` |
| `.dockerignore` / `.gitignore` | Lo que no entra en la imagen / en git |

## 🏛️ Arquitectura en capas (`src/`)

```
presentacion ──► aplicacion ──► dominio
     │                ▲
     └──► infra ──────┘
```

La **regla de dependencia**: las capas internas (`dominio`, `aplicacion`) no importan nada de React, del DOM ni de MediaPipe. Ver [`src/README.md`](src/README.md).

## 🐳 Docker

```bash
docker build -t signia-front .
docker run -p 8080:80 signia-front   # abre http://localhost:8080
```
