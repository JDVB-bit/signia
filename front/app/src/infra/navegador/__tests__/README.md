# 🧪 `infra/navegador/__tests__/` — Tests de los adaptadores del navegador

## 📖 Introducción

Comprueban que el acceso al almacenamiento **nunca rompe la aplicación**, pase
lo que pase con el navegador. Es el único adaptador de esta capa que se puede
probar sin navegador real, y también el más peligroso si falla.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Módulo que verifica | Escenarios |
|---|---|---|
| `almacenamientoSeguro.test.js` | `almacenamientoSeguro.js` | Sin `window`, con almacén funcional, con almacén que lanza excepciones |

Los demás módulos de la carpeta (`camara.js`, `descargarJson.js`,
`preferenciaDeTema.js`…) dependen de APIs que solo existen de verdad en el
navegador: se verifican allí, no con dobles que acabarían probando el doble.

---

## 🎯 Qué problema resuelve

`localStorage` es traicionero: **no falla al escribir, falla al mirarlo**. En
modo privado, con las cookies de terceros bloqueadas o dentro de un iframe,
`window.localStorage` lanza una excepción con solo accederlo.

Si eso ocurriera sin protección, la app no arrancaría — y el fallo aparecería
solo en el navegador de un usuario concreto, imposible de reproducir.

---

## 🔗 Qué dependencias tiene

- `vitest` (con `vi.stubGlobal` para sustituir `window`).
- `almacenamientoSeguro.js`.

---

## 🧠 Cómo soluciona el problema

Se simulan los tres mundos posibles:

| Escenario | Simulación | Comportamiento esperado |
|---|---|---|
| **Sin `window`** | `window` sin definir (tests, SSR) | Leer devuelve `null`, guardar no lanza |
| **Almacén normal** | Objeto con `getItem`/`setItem` en memoria | Se lee lo que se guarda |
| **Almacén hostil** | `getItem`/`setItem` que lanzan | Se comporta como vacío, sin propagar el error |

---

## 🔍 Qué tienen los archivos

| Test | Lo que garantiza |
|---|---|
| `sin window (tests, SSR) lee null y guardar no lanza` | El módulo se puede importar fuera del navegador |
| `lee lo que guarda cuando el almacen funciona` | El camino feliz sigue siendo correcto |
| `si el almacen lanza (modo privado) se comporta como vacio` | Modo privado degrada la comodidad, no la funcionalidad |

---

## 💡 Ejemplos de uso

```bash
pnpm test -- navegador
```

```js
// Almacén que lanza, como el de un navegador en modo privado
vi.stubGlobal('window', {
    get localStorage() {
        throw new Error('bloqueado')
    },
})

expect(leerLocal('signia-theme')).toBeNull()
expect(() => guardarLocal('signia-theme', 'dark')).not.toThrow()
```
