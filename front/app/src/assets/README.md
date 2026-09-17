# 🖼️ `src/assets/` — Imágenes empaquetadas por Vite

## 📖 Introducción

Recursos estáticos que **forman parte del código**: se importan desde un
componente, Vite los procesa (les añade un hash al nombre y los optimiza) y
acaban en `dist/assets/`.

Es la diferencia con [`public/`](../../public/), cuyo contenido se sirve tal cual
y sin procesar.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Qué es | Dónde se usa |
|---|---|---|
| `senas-persona1.jpg` | Persona haciendo una seña en LSE | Carrusel de la página de Inicio |
| `senas-persona2.jpg` | Ídem | Ídem |
| `senas-persona3.jpg` | Ídem | Ídem |
| `.gitkeep` | Mantiene la carpeta en git cuando está vacía | — |

---

## 🎯 Qué problema resuelve

La página de Inicio necesita **mostrar de qué habla** antes de que nadie lea un
párrafo. Tres fotos en rotación explican "traductor de lengua de señas" más
rápido que el mejor texto.

Y técnicamente: si estas imágenes estuvieran en `public/`, el navegador podría
servir una versión cacheada antigua tras un despliegue. Al importarlas, cada
build genera una URL nueva.

---

## 🔗 Qué dependencias tiene

Ninguna propia. Las consume `presentacion/paginas/Inicio.jsx` a través de
[`ImageBelt`](../presentacion/componentes/contenido/) y `CarouselImage`.

---

## 🧠 Cómo soluciona el problema

```
import senasPersona1 from '../../assets/senas-persona1.jpg'
          │
          └──► Vite ──► /assets/senas-persona1-a1b2c3d4.jpg
```

Al importarse, Vite devuelve la **URL final ya versionada**: el navegador puede
cachearla de forma agresiva sin riesgo de servir una imagen obsoleta.

Cada imagen viaja con su texto alternativo en el array `IMAGENES_CARRUSEL` de la
página: el `alt` es parte del dato, no del componente.

---

## 🔍 Qué tienen los archivos

Tres fotografías en `.jpg`, con proporción apaisada, pensadas para un recuadro
de `h-56` (`sm:h-64`) y recortadas con `object-cover`.

El nombre sigue el patrón `senas-personaN.jpg`: describe **qué** se ve, no dónde
se usa, para que reordenar el carrusel no obligue a renombrarlas.

---

## 💡 Ejemplos de uso

```jsx
import senasPersona1 from '../../assets/senas-persona1.jpg'
import senasPersona2 from '../../assets/senas-persona2.jpg'
import senasPersona3 from '../../assets/senas-persona3.jpg'

const TEXTO_ALTERNATIVO_IMAGEN = 'Persona haciendo una seña en LSE'
const IMAGENES_CARRUSEL = [senasPersona1, senasPersona2, senasPersona3].map((src) => ({
    src,
    alt: TEXTO_ALTERNATIVO_IMAGEN,
}))

<ImageBelt images={IMAGENES_CARRUSEL} />
```

Para añadir una imagen: copiarla aquí con un nombre descriptivo, importarla y
añadirla al array.

> 📌 **Regla práctica:** si el archivo se importa desde JavaScript, va aquí. Si
> necesita una URL fija y estable (como el modelo `.task` de MediaPipe), va en
> [`public/`](../../public/).
