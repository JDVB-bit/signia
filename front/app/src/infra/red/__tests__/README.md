# 🧪 `red/__tests__/` — Tests del adaptador de red

## 📖 Introducción

**12 tests** que comprueban la petición sin levantar ningún servidor: el `fetch`
se sustituye por una función de mentira y se inspecciona con qué se llamó.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Qué verifica |
|---|---|
| `urlDeLaApi.test.js` | De dónde sale la URL: variable de entorno, local, barra final, vacío |
| `clienteDeMuestras.test.js` | Método, cabeceras, cuerpo, respuesta y las tres formas de fallar |

---

## 🎯 Qué problema resuelve

Un error aquí es de los que **no se ven**: el lote se manda mal formado, el
backend lo rechaza y el usuario solo ve que "no funciona". Los tests fijan el
contrato de transporte:

- que el cuerpo sea el paquete **tal cual**, sin envolver ni renombrar;
- que se declare `Content-Type: application/json`, o FastAPI no lo parsea;
- que el motivo que devuelve el backend llegue al usuario y no se pierda.

---

## 🔗 Qué dependencias tiene

`vitest` y sus `vi.fn()`. Ni jsdom ni red real.

---

## 🧠 Cómo soluciona el problema

### 🎭 Un `fetch` que se puede mirar por dentro

```js
const peticion = vi.fn().mockResolvedValue(respuesta({ cuerpo: { guardadas: 1 } }))
await subirLote(PAQUETE, { peticion, entorno: {} })

const [url, opciones] = peticion.mock.calls[0]
expect(JSON.parse(opciones.body)).toEqual(PAQUETE)
```

### 💥 Las tres formas de fallar, por separado

| Test | Situación real |
|---|---|
| `lanza con el motivo que da el backend` | Un `422`: el lote no cumple el contrato |
| `tolera un error sin cuerpo JSON` | Un `502` de un proxy, que devuelve HTML |
| `deja subir el fallo de red` | El backend apagado (`Failed to fetch`) |

Las tres acaban en la capa de aplicación, que decide si descargar el respaldo.

### 🌐 El entorno también se inyecta

`entorno: {}` simula que no hay `VITE_API_URL`, así que el test no depende de
cómo esté configurada la máquina donde corre.

---

## 💡 Ejemplos de uso

```bash
pnpm test -- red            # solo estos
pnpm test:watch -- red      # mientras se programa
```
