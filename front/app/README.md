# ⚛️ `front/app/` — Aplicación React de SignIA

## 📖 Introducción

La aplicación web completa: **React 19 + Vite 8 + Tailwind CSS v4**, tests con
**Vitest** y lint con **oxlint**. Tres páginas (Inicio, Traducción y
Entrenamiento), tema claro/oscuro y **captura de señas con MediaPipe**
ejecutándose por entero en el navegador.

Es el cliente de la etapa 1: detecta las manos, construye la muestra del
contrato y —hoy— la exporta como JSON; cuando exista el backend (Fase 5) solo
cambiará el transporte.

---

## 📂 Qué archivos tiene y qué hace cada uno

### Configuración y despliegue

| Archivo | Para qué sirve |
|---|---|
| `index.html` | 🚪 Documento raíz (idioma `es`, título, favicon) donde se monta React |
| `package.json` / `pnpm-lock.yaml` | 📦 Dependencias y scripts, con la versión de pnpm fijada |
| `vite.config.js` | ⚙️ Plugins (React, Tailwind) y configuración de Vitest |
| `.oxlintrc.json` | 🧹 Reglas de lint (hooks de React, exports de componentes) |
| `Dockerfile` | 🐳 Imagen en dos etapas: compila con Node 24, sirve con nginx |
| `nginx.conf` | 🌐 Sirve la SPA, cachea `/assets/` y redirige rutas a `index.html` |
| `.dockerignore` / `.gitignore` | 🚫 Lo que no entra en la imagen / en git |

### Código y recursos

| Carpeta | Qué contiene |
|---|---|
| [`src/`](src/) | 🧬 Todo el código, en cuatro capas (`dominio`, `aplicacion`, `infra`, `presentacion`) |
| [`public/`](public/) | 📁 Archivos servidos tal cual: favicon y assets de MediaPipe |

---

## 🎯 Qué problema resuelve

1. **Presentar el producto** sin tecnicismos a quien nunca ha oído hablar de LSE.
2. **Grabar dataset con una pulsación**, con realimentación inmediata: cuántas
   manos se ven, cuántos segundos llevas y por qué se descartó una muestra.
3. **No divergir del entrenamiento**: el tensor que construye este código es el
   mismo que construye Python, y hay un test que lo demuestra.
4. **Funcionar sin servidor**: detección, preprocesado y (en la Fase 6)
   inferencia ocurren en el navegador. El vídeo nunca sale del dispositivo.

---

## 🔗 Qué dependencias tiene

### Requisitos

- **Node.js 24 LTS**
- **pnpm 11** — fijado en `package.json → packageManager`; con `corepack enable`
  se usa la versión correcta sola.

### Paquetes

| Paquete | Para qué |
|---|---|
| `react` / `react-dom` 19 | Interfaz |
| `react-router-dom` 7 | Rutas `/`, `/traduccion`, `/entrenamiento` |
| `tailwindcss` 4 + `@tailwindcss/vite` | Estilos y variables de tema |
| `@mediapipe/tasks-vision` | Detección de manos (`HandLandmarker`) |
| `vite` 8 + `@vitejs/plugin-react` | Desarrollo y build |
| `vitest` 5 | Tests de lógica pura |
| `oxlint` | Linter |

Y el paquete [`model/`](../../model/) como contraparte: los fixtures de
`model/tests/fixtures/` los lee el test de conformidad de este proyecto.

---

## 🧠 Cómo soluciona el problema

### 🏛️ Arquitectura en capas

```
presentacion ──► aplicacion ──► dominio
     │                             ▲
     └──────► infra ───────────────┘
```

**Regla de dependencia:** las capas internas (`dominio`, `aplicacion`) no
importan nada de React, del DOM ni de MediaPipe. Por eso sus **166 tests** corren
en node en menos de un segundo. Detalle en [`src/README.md`](src/README.md).

### 🎨 Paleta de cinco colores

Definida en `src/index.css` y usada por todo el sitio:

| Variable | Papel |
|---|---|
| `--color-brand` | Color del texto |
| `--color-bg` | Fondo de la página |
| `--color-surface` | Paneles y secciones sobre el fondo |
| `--color-secondary` | Color alterno para resaltar |
| `--color-brand-inverso` | Texto sobre `secondary` (el brand de la paleta contraria) |

La paleta oscura no se eligió a ojo: cada color se pasó a HSL, se giró el matiz
+180° y se invirtió la luminosidad, manteniendo la saturación. El modo oscuro se
activa con la clase `.dark` en `<html>`, no con `prefers-color-scheme`, para que
el botón de tema mande sobre el sistema.

### 🧭 Arranque y rutas

```
main.jsx ──► aplicarTemaInicial() ──► BrowserRouter ──► AplicacionRaiz
                                                          ├── IntroSplash  (primera visita)
                                                          └── Routes
                                                              ├── /              → Inicio
                                                              ├── /traduccion    → Traducción
                                                              └── /entrenamiento → Entrenamiento
```

---

## 🔍 Qué tienen los archivos de configuración

### `vite.config.js`

```js
plugins: [react(), tailwindcss()],
test: { environment: 'node', include: ['src/**/__tests__/**/*.test.{js,jsx}'] }
```

Vitest corre en **node**, sin jsdom: lo que se prueba es lógica pura. Lo que
necesita cámara o DOM real se verifica en el navegador.

### `.oxlintrc.json`

| Regla | Efecto |
|---|---|
| `react/rules-of-hooks: error` | Impide hooks condicionales |
| `react/only-export-components: warn` | Permite exportar constantes junto al componente (`allowConstantExport`) |
| `ignorePatterns: public/mediapipe/**` | No se lintan los binarios de MediaPipe |

### `Dockerfile` y `nginx.conf`

1. **Etapa de compilación**: `node:24-alpine`, `corepack enable`,
   `pnpm install --frozen-lockfile` y `pnpm run build`.
2. **Etapa de servicio**: `nginx:alpine` con solo `dist/`.

`nginx.conf` cachea `/assets/` durante un año (`immutable`, porque Vite les pone
hash) y resuelve cualquier ruta desconocida con `try_files … /index.html`, que es
lo que evita el 404 al recargar en `/entrenamiento`.

---

## 💡 Ejemplos de uso

```bash
pnpm install       # instalar dependencias
pnpm dev           # desarrollo → http://localhost:5173
pnpm test          # 166 tests (Vitest, una pasada)
pnpm test:watch    # tests en modo vigilancia
pnpm lint          # oxlint
pnpm build         # build de producción → dist/
pnpm preview       # servir el build para comprobarlo
```

Despliegue con Docker:

```bash
docker build -t signia-front .
docker run --rm -p 8080:80 signia-front   # http://localhost:8080
```

> 📷 **La cámara necesita un origen seguro.** `getUserMedia` solo funciona en
> `https://` o en `localhost`: al servir el contenedor en una IP de la red local
> sin TLS, el navegador bloqueará el permiso.
