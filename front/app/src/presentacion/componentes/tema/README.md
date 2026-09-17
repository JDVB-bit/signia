# 🌗 `componentes/tema/` — Cambiar la paleta

## 📖 Introducción

El botón del header que alterna entre la paleta clara y la oscura. Es la parte
visible de un mecanismo que empieza antes de que React se monte.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `ThemeToggle.jsx` | 🔆 Botón que alterna el tema y muestra el icono del modo **al que se pasa** |

---

## 🎯 Qué problema resuelve

1. **Leer cómodo a cualquier hora.** La paleta clara es cálida (beige) y la
   oscura es su complementaria; elegir es del usuario, no nuestro.
2. **Respetar el sistema sin imponerlo.** Si nunca eligió, manda la preferencia
   del sistema operativo; en cuanto elige, manda su decisión.
3. **El parpadeo inicial.** Si el tema se aplicara al montar el componente, la
   primera pantalla saldría con los colores contrarios durante un instante.

---

## 🔗 Qué dependencias tiene

- [`../../hooks/useTema`](../../hooks/) — estado y sincronización.
- Indirectamente,
  [`infra/navegador/preferenciaDeTema.js`](../../../infra/navegador/), que es
  quien lee, guarda y aplica.

El componente **no toca** `localStorage` ni el `<html>`: solo pide al hook que
alterne.

---

## 🧠 Cómo soluciona el problema

```
main.jsx ──► aplicarTemaInicial()  ──►  <html class="dark">  ──► React monta
                    │
                    └── localStorage['signia-theme'] ?? prefers-color-scheme
```

El tema ya está puesto **antes** del primer render; `ThemeToggle` solo lo cambia
después. Al alternar, `useTema` aplica la clase y guarda la preferencia en el
mismo efecto, así que la pantalla y el recuerdo nunca se separan.

### 🔆 El icono muestra el destino, no el estado

| Tema actual | Icono | Significado |
|---|---|---|
| Claro | 🌙 | "Pulsa para ir a oscuro" |
| Oscuro | ☀️ | "Pulsa para ir a claro" |

Es la convención más extendida y evita la duda de "¿me dice cómo estoy o a dónde
voy?". El estado real se comunica por `aria-pressed`, que es lo que leen las
tecnologías de apoyo.

---

## 🔍 Qué tiene el archivo

| Constante | Valor |
|---|---|
| `ICONO_PASAR_A_CLARO` | `☀️` |
| `ICONO_PASAR_A_OSCURO` | `🌙` |

| Atributo | Valor |
|---|---|
| `type` | `button` |
| `aria-pressed` | `oscuro` — el estado real |
| `aria-label` | `Cambiar paleta de colores` |

Sin props: se coloca y funciona.

---

## 💡 Ejemplos de uso

```jsx
// Header.jsx
<nav aria-label="Preferencias y navegación" className="flex items-center gap-3">
    <ThemeToggle />
    <BurgerMenu />
</nav>
```

Para usar el tema desde otro sitio, se pide al hook, no al componente:

```jsx
import useTema from '../../hooks/useTema'

const { oscuro, alternarTema } = useTema()
```

> 🎨 Los colores de cada paleta están en `src/index.css`. La oscura no se eligió
> a ojo: cada color se pasó a HSL, se giró el matiz +180° y se invirtió la
> luminosidad, manteniendo la saturación.
