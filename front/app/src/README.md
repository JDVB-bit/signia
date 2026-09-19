# 🧬 `src/` — Código fuente del front

## 📖 Introducción

Toda la aplicación, organizada en las **cuatro capas de Clean Architecture**. La
regla es una sola y se cumple sin excepciones: *las capas de dentro no importan
nada de las de fuera*.

```
src/
├── dominio/        🎯 reglas del negocio        (JavaScript puro)
├── aplicacion/     ⚙️ casos de uso              (usa dominio)
├── infra/          🔌 adaptadores externos      (MediaPipe, canvas, navegador)
├── presentacion/   🎨 interfaz en React         (usa todo lo anterior)
├── assets/         🖼️ imágenes empaquetadas
├── main.jsx        ▶️ arranque
└── index.css       🎨 Tailwind + paleta de 5 colores
```

---

## 📂 Qué archivos y carpetas tiene

| Elemento | Qué hace |
|---|---|
| `main.jsx` | ▶️ Aplica el tema, monta `BrowserRouter` y `AplicacionRaiz`, carga los estilos |
| `index.css` | 🎨 Importa Tailwind, define la variante `dark` y las cinco variables de color |
| [`dominio/`](dominio/) | 🎯 Contrato, reglas de grabación, elección de mano, etiquetas |
| [`aplicacion/`](aplicacion/) | ⚙️ Remuestreo, tensor crudo, creación de muestras y lotes |
| [`infra/`](infra/) | 🔌 MediaPipe, canvas y APIs del navegador |
| [`presentacion/`](presentacion/) | 🎨 Páginas, componentes, hooks, estados, textos y estilos |
| [`assets/`](assets/) | 🖼️ Imágenes que importa la página de Inicio |

---

## 🎯 Qué problema resuelve

1. **Que la lógica no quede atrapada en la interfaz.** Con la captura metida en
   un `useEffect`, probar el preprocesado exigiría un navegador con cámara.
2. **Que cambiar de tecnología no sea rehacer la app.** MediaPipe se importa en
   un único archivo; el almacenamiento, en otro.
3. **Que el front y el modelo no se separen.** `dominio/` y `aplicacion/` son
   gemelos de sus equivalentes en Python, y un test de conformidad lo vigila.

---

## 🔗 Qué dependencias tiene

| Capa | Puede importar de… | Dependencias externas |
|---|---|---|
| `dominio/` | nada | — |
| `aplicacion/` | `dominio/` | — |
| `infra/` | `dominio/` | `@mediapipe/tasks-vision`, APIs del navegador |
| `presentacion/` | todas | `react`, `react-router-dom`, Tailwind |

---

## 🧠 Cómo soluciona el problema

### 🧅 Dependencias hacia dentro

```
presentacion ──► aplicacion ──► dominio
      │                            ▲
      └────────► infra ────────────┘
```

Nadie apunta hacia afuera. Por eso `dominio/` y `aplicacion/` se prueban en node
sin simular nada, y los 166 tests del front tardan menos de un segundo.

### 📸 El flujo de la captura, de punta a punta

```
CameraFeed (<video>)
      │
useCamara ──► flujo de la cámara
      │
useDetectorDeManos ──► infra/mediapipe/detectorDeManos
      │
useBucleDeDeteccion ──► detectForVideo por frame nuevo
      │
infra/mediapipe/frameDesdeDeteccion ──► { t, manos }  del contrato
      ├──► infra/canvas/pintarManosSobreVideo   (overlay)
      └──► useGrabacionDeMuestra ──► dominio/reglasDeGrabacion
                    │
            aplicacion/crearMuestra ──► muestra del contrato
                    │
            aplicacion/paqueteDeMuestras ──► JSON descargado
```

### 🎨 Tema sin parpadeo

`main.jsx` llama a `aplicarTemaInicial()` **antes** de `createRoot`: la pantalla
de carga y todo lo demás nacen ya con los colores correctos.

---

## 🔍 Qué tienen los archivos

### `main.jsx`

1. `import './index.css'` y `'./presentacion/estilos/animaciones.css'`.
2. `aplicarTemaInicial()` — antes de renderizar.
3. `createRoot(...).render(<StrictMode><BrowserRouter><AplicacionRaiz /></…>)`.

### `index.css`

| Bloque | Para qué |
|---|---|
| `@import "tailwindcss"` | Carga Tailwind v4 |
| `@source not "../public/mediapipe"` | Evita que Tailwind escanee el *glue code* de Emscripten y genere clases falsas |
| `@custom-variant dark (&:where(.dark, .dark *))` | El modo oscuro depende de la clase `.dark`, no del sistema |
| `@theme { … }` | Paleta clara |
| `.dark { … }` | Paleta oscura |

| Variable | Papel |
|---|---|
| `--color-brand` | Color del texto |
| `--color-bg` | Fondo de la página |
| `--color-surface` | Paneles y secciones |
| `--color-secondary` | Color alterno para resaltar |
| `--color-brand-inverso` | Texto sobre `secondary` (el brand de la paleta contraria) |

---

## 💡 Ejemplos de uso

```bash
pnpm dev     # http://localhost:5173
pnpm test    # 166 tests de dominio, aplicación, infra y textos
pnpm lint    # oxlint
```

Añadir una funcionalidad nueva, en orden:

```
1. dominio/       ¿hay una regla nueva?           → función pura + test
2. aplicacion/    ¿un caso de uso nuevo?          → composición + test
3. infra/         ¿hace falta una API externa?    → adaptador aislado
4. presentacion/  ¿cómo se ve y cuándo ocurre?    → hook + componente
```

> 📌 Si al escribir un componente hace falta una decisión de negocio
> (*“¿cuántos frames son pocos?”*), es señal de que esa decisión pertenece a
> `dominio/`, no al JSX.
