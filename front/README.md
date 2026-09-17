# 🖥️ `front/` — Interfaz web de SignIA

## 📖 Introducción

Todo lo que corre en el **navegador** del usuario. Es la única parte del sistema
con acceso a la cámara y, por eso, hace dos trabajos muy distintos: **enseñar el
producto** y **capturar el dato** con el que se entrena el modelo.

---

## 📂 Qué carpetas tiene y qué hace cada una

| Carpeta | Qué es | Parte del sistema |
|---|---|---|
| [`app/`](app/) | La aplicación React + Vite + Tailwind | Web pública (Inicio), captura de señas (Entrenamiento) y traductor (Fase 6) |

Esta carpeta es un contenedor deliberado: si algún día hay un segundo cliente
—una app móvil, un panel de administración— entra aquí junto a `app/` sin
reorganizar el repositorio.

---

## 🎯 Qué problema resuelve

1. 👀 **Que cualquiera entienda qué es SignIA** en la primera pantalla, sin
   tecnicismos.
2. 🎥 **Que grabar una seña cueste una pulsación**, porque el dataset se graba a
   mano y cientos de veces (Fase 2).
3. 🧪 **Que una muestra mala se descarte antes de guardarse**, mostrando en vivo
   el esqueleto de la mano y el lado detectado.
4. ⚡ **Que traducir no dependa de un servidor**: la inferencia vivirá aquí.

---

## 🔗 Qué dependencias tiene

**Node.js 24 LTS** y **pnpm 11**. El detalle de paquetes está en
[`app/package.json`](app/package.json) y explicado en
[`app/README.md`](app/README.md).

Su contraparte es [`model/`](../model/): comparten el contrato de datos y los
fixtures del test de conformidad.

---

## 🧠 Cómo soluciona el problema

### 🧠 Por qué el front pesa tanto en SignIA

El plan decide que **la etapa 1 (señas → glosas) se ejecuta en el navegador** con
`onnxruntime-web`: predecir ~6 veces por segundo enviando landmarks por HTTP
sería inviable en latencia y en coste.

Consecuencia: aquí hay **lógica de dominio real**, no solo pantallas. Y por eso
el código está en capas, con su propio `dominio/` y `aplicacion/` gemelos de los
de Python.

### 🧅 Organización

```
front/
└── app/
    ├── src/
    │   ├── dominio/       reglas (JS puro)
    │   ├── aplicacion/    casos de uso
    │   ├── infra/         MediaPipe, canvas, navegador
    │   └── presentacion/  React
    └── public/            assets servidos tal cual
```

---

## 🔍 Qué hay en `app/`

| Elemento | Detalle |
|---|---|
| Stack | React 19, Vite 8, Tailwind v4, MediaPipe Tasks Vision |
| Tests | 105 con Vitest, en entorno node |
| Despliegue | `Dockerfile` en dos etapas + `nginx.conf` para la SPA |
| Assets propios | Modelo `.task` y runtime WASM self-hosted |

---

## 💡 Ejemplos de uso

```bash
cd front/app
pnpm install
pnpm dev       # http://localhost:5173
pnpm test      # tests de lógica pura
pnpm build     # build de producción en dist/
```

Desde la raíz del repositorio, sin cambiar de carpeta:

```bash
pnpm --dir front/app run dev
```

Es justo lo que hace `.claude/launch.json` para levantar el servidor de
desarrollo desde el editor.
