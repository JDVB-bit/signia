# 🧪 `infra/canvas/__tests__/` — Tests del overlay

## 📖 Introducción

Comprueban el dibujo del esqueleto **sin navegador**: se le pasa un contexto 2D
falso (`vi.fn()`) y se verifica qué llamadas recibe y con qué valores.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Módulo que verifica | Casos cubiertos |
|---|---|---|
| `dibujarManos.test.js` | `dibujarManos.js` | Integridad de `CONEXIONES`, escalado y espejado, número de trazos, rótulos por lado, manos incompletas |

`pintarManosSobreVideo.js` no se testea aquí: su trabajo es leer propiedades de
un `<video>` real y se comprueba en el navegador.

---

## 🎯 Qué problema resuelve

El overlay es **una herramienta de control de calidad del dataset**: si dibuja
mal, se graban muestras malas creyendo que están bien. Un esqueleto desplazado o
un rótulo cambiado engañan al que graba.

Además, un error aquí es peligroso: este código corre **dentro del bucle de
vídeo**, 30 veces por segundo. Una excepción pararía la captura entera.

---

## 🔗 Qué dependencias tiene

- `vitest` (incluido `vi.fn()` para el contexto falso).
- `dibujarManos.js` y las constantes del dominio.

---

## 🧠 Cómo soluciona el problema

El contexto falso registra las llamadas y acumula los textos escritos:

```js
function ctxFalso() {
    return {
        textos: [],
        clearRect: vi.fn(), beginPath: vi.fn(), moveTo: vi.fn(), lineTo: vi.fn(),
        stroke: vi.fn(), arc: vi.fn(), fill: vi.fn(),
        fillText: vi.fn(function (texto) { this.textos.push(texto) }),
    }
}
```

Con eso se puede afirmar cosas concretas: "un `moveTo` y un `lineTo` por
conexión", "un `arc` por landmark", "los rótulos fueron `izquierda` y `derecha`".

---

## 🔍 Qué tienen los archivos

| Test | Lo que garantiza |
|---|---|
| `todas apuntan a landmarks que existen` | Ninguna conexión sale del rango `0..20` |
| `no hay ninguna repetida ni ningun punto consigo mismo` | El esqueleto no dibuja líneas duplicadas ni degeneradas |
| `todos los landmarks quedan conectados al esqueleto` | Los 21 puntos forman una sola mano, sin dedos sueltos |
| `escala el landmark normalizado al tamano del canvas` | La conversión `0..1` → píxeles es correcta |
| `espeja la x para que coincida con el video` | El esqueleto cae sobre la mano, no sobre la contraria |
| `limpia el canvas en cada repintado` | Sin `clearRect` quedaría un rastro de manos anteriores |
| `dibuja un hueso por conexion y un punto por landmark` | El dibujo está completo |
| `rotula el lado: es la verificacion del handedness` | El rótulo existe y dice lo que debe |
| `usa un color distinto por mano` | Se puede distinguir izquierda de derecha |
| `ignora una mano con landmarks incompletos en vez de reventar el bucle` | Un dato parcial no detiene la captura |

---

## 💡 Ejemplos de uso

```bash
pnpm test -- canvas
```

```js
const ctx = ctxFalso()
dibujarManos(ctx, [mano('izquierda'), mano('derecha')], { ancho: 640, alto: 480, espejado: true })

expect(ctx.textos).toEqual(['izquierda', 'derecha'])
expect(ctx.arc).toHaveBeenCalledTimes(21 * 2)
```
