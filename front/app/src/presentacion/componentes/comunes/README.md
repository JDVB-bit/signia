# 🔘 `componentes/comunes/` — Piezas que usa todo el sitio

## 📖 Introducción

Componentes transversales, sin tema propio. Hoy solo hay uno, pero es el que
aparece en todas las páginas: el **botón**.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `Button.jsx` | 🔘 Botón del sistema: dos variantes de color, dos tamaños y estado deshabilitado |

---

## 🎯 Qué problema resuelve

1. **Botones distintos en cada página.** Sin una pieza común, cada vista acaba
   con su propio `className` y el sitio pierde identidad.
2. **Enviar formularios sin querer.** Un `<button>` sin `type` dentro de un
   formulario hace `submit` por defecto: un fallo clásico y difícil de ver.
3. **Deshabilitar de verdad.** Un botón apagado tiene que *parecerlo* (opacidad,
   cursor) y además **no responder**.

---

## 🔗 Qué dependencias tiene

Ninguna: React y las clases de Tailwind con la paleta de `src/index.css`.

---

## 🧠 Cómo soluciona el problema

### 🎨 Variantes atadas a la paleta

| Variante | Fondo | Texto | Cuándo |
|---|---|---|---|
| `primary` | `bg-secondary` | `text-brand-inverso` | Acción principal (*Entrenar*, *Traducir*) |
| `secondary` | `bg-surface` | `text-brand` | Acción de apoyo (*Enviar*) |

Los colores salen de las cinco variables del tema, así que el botón se adapta
solo al modo claro y al oscuro.

### 📏 Dos tamaños, con una razón

| Tamaño | Clases | Uso |
|---|---|---|
| `md` | `px-8 py-4 text-base` | Por defecto |
| `lg` | `px-[2.2rem] py-[1.1rem] text-[1.1rem]` | ~10 % mayor: el *Traducir* de la página principal del producto |

### 🚫 Siempre `type="button"`

Está fijado dentro del componente, no se puede olvidar desde fuera.

---

## 🔍 Qué tiene el archivo

```js
const ESTILOS_POR_VARIANTE = { primary: …, secondary: … }
const ESTILOS_POR_TAMANO   = { md: …, lg: … }
const ESTILOS_HABILITADO    = 'hover:opacity-90'
const ESTILOS_DESHABILITADO = 'cursor-not-allowed opacity-50'
```

| Prop | Por defecto | Para qué |
|---|---|---|
| `children` | — | Contenido del botón |
| `variant` | `'primary'` | Color |
| `size` | `'md'` | Tamaño |
| `onClick` | — | Acción |
| `disabled` | `false` | Apaga el botón y cambia su aspecto |

---

## 💡 Ejemplos de uso

```jsx
<Button variant="primary" onClick={alternarGrabacion} disabled={!detectorListo}>
    {grabando ? 'Detener' : 'Entrenar'}
</Button>

<Button variant="secondary" onClick={enviar} disabled={!hayMuestras}>
    Enviar
</Button>

<Button variant="primary" size="lg" disabled>
    Traducir
</Button>
```

> 💡 Si un control necesita otro aspecto (por ejemplo, el enlace *Borrar última
> muestra*, que es texto subrayado), **no** se añade una variante nueva por un
> único uso: se escribe ese control en su página. Las variantes son para lo que
> se repite.
