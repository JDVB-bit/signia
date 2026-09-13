# Lista de mejoras, implementaciones y sugerencias — SignIA

> Lista viva según la regla 3 de `.claude/claude.md`. Se actualiza en cada sesión.

## Hecho
- [x] Paleta de colores principal (brand/bg/surface/secondary) como CSS vars de Tailwind v4 en `front/app/src/index.css`.
- [x] Paleta oscura calculada por color complementario (matiz +180°) + luminosidad invertida.
- [x] Botón `ThemeToggle` con persistencia en `localStorage` y detección de preferencia del sistema.
- [x] `App.jsx` migrado a las clases de la nueva paleta.

## Hecho (sesión 2)
- [x] `BurgerMenu.jsx` — botón hamburguesa animado a X, panel con overlay, cierre con click fuera / Escape / al elegir un enlace, foco en el primer enlace al abrir.
- [x] Aplicado en `App.jsx` (sustituyendo el botón `*toolbar` placeholder) y en `Traduccion.jsx` (que no tenía cabecera con estilos ni `ThemeToggle`).

## Hecho (sesión 3)
- [x] Botones del header (`ThemeToggle`, `BurgerMenu`) sin caja/contorno; usan `text-secondary` / `bg-secondary` solo en los elementos internos (emoji, barras).
- [x] `App.jsx`: título "Traductor de lenguaje..." centrado y más grande (`text-3xl`/`sm:text-4xl`).
- [x] Layout responsivo en grid: sección "Que es?" (con la burbuja de información dentro) a la izquierda, sección reservada para imágenes/animaciones a la derecha; en móvil se apilan verticalmente.

## Hecho (sesión 4)
- [x] Layout mucho más ancho (`max-w-[110rem]`), secciones con más padding, mejor aprovechamiento de los bordes de pantalla.
- [x] Título principal más grande e imponente (`text-4xl`→`lg:text-6xl`, `font-extrabold`, `drop-shadow-sm`).
- [x] Animación de aparición "polvo" (`animate-dust-in` en `App.css`) aplicada palabra por palabra al título, con retraso escalonado.
- [x] Componente `Typewriter.jsx` — animación de escritura simple, usado en el párrafo de "Que es?".
- [x] Borrador de contenido para "Que es?" (descripción, herramientas, misión, autoría académica) en `.informacion-homepage.md`, ignorado en git — pendiente de que Snt lo corrobore antes de llevarlo al código.

## Hecho (sesión 5)
- [x] Expandido `.informacion-homepage.md`: contenido organizado en 3 secciones (Que es / Mision / Herramientas), cada una con texto **Breve** (tarjeta) y **Detalle** (burbuja de información propia por sección).

## Hecho (sesión 6)
- [x] `.informacion-homepage.md`: los textos "Breve" de las 3 secciones se ampliaron a párrafos generales que ocupan la tarjeta (ya no titulares de una línea); "Detalle" sigue siendo lo específico para la burbuja.

## Hecho (sesión 7)
- [x] `.informacion-homepage.md`: reescrito en punto medio de longitud y limpiado de todo detalle técnico (sin React, MediaPipe, PyTorch, FastAPI, "landmarks", frontend/backend); todo redactado en términos de experiencia de usuario.

## Hecho (sesión 8)
- [x] Contenido de `.informacion-homepage.md` aplicado a `App.jsx`: 3 secciones reales (Que es / Mision / Herramientas), cada una con su texto breve (con animación de escritura) y su propia burbuja de información.
- [x] `InfoBubble.jsx` — nuevo componente: la burbuja de información ahora despliega un panel dinámico (overlay + cierre con click fuera/Escape/botón ✕) para mejor lectura del detalle, en vez del placeholder de botón.
- [x] `SectionCard.jsx` — pequeño componente de tarjeta reutilizado por las 3 secciones.
- [x] Corregido bug: el título con efecto "polvo" perdía los espacios entre palabras (el `inline-block` recortaba el espacio final); ahora el espacio va como nodo de texto fuera del `span`.

## Hecho (sesión 9)
- [x] Corregido el título "Que es?" → "¿Qué es?" (tilde y signo de apertura).
- [x] Layout reordenado: "¿Qué es?" queda siempre junto a la sección de imágenes (fila 1, 2 columnas). Misión y Herramientas pasaron a una fila aparte, en 12 columnas (7/5) con Herramientas desplazada hacia abajo (`lg:mt-16`) y padding distinto, para que no se sienta como una grilla uniforme.
- [x] `InfoBubble.jsx` — ahora es un modal centrado en pantalla (`fixed inset-0 flex items-center justify-center`), con `backdrop-blur-sm` sobre el fondo, texto más grande (`text-lg`), interlineado amplio (`leading-loose`) y letras espaciadas (`tracking-wide`). Verificado por estilos computados (blur(8px), 18px, 36px de interlineado).
- [x] `SectionCard.jsx` acepta ahora `className` para variar tamaño/padding por sección.

## Hecho (sesión 10)
- [x] Quitado el desfase vertical (`lg:mt-16`) entre Misión y Herramientas; ahora tienen el mismo alto (verificado: 284px ambas, mismo `top`), manteniendo el ancho distinto (7/5 columnas).

## Hecho (sesión 11)
- [x] Animación de entrada del modal de `InfoBubble`: desciende desde arriba (`translateY(-32px)→0`), 500ms exactos con curva `cubic-bezier(0.16,1,0.3,1)` — verificado con `getAnimations()` que la duración es 500ms, dentro del límite pedido.
- [x] `CarouselImage.jsx` — componente que recibe la imagen por prop (`src`/`alt`) y solo se encarga de pintarla; separa "qué imagen mostrar" de "cómo animar el cinturón".
- [x] `ImageBelt.jsx` — efecto cinturón: cada imagen visible ~5s, la siguiente empuja a la anterior hacia la izquierda con transición fluida (700ms), loop infinito sin salto (clon de la primera imagen al final del cinturón + reset invisible).
- [x] 3 imágenes de `front/app/src/assets` (`senas-persona1/2/3.jpg`) integradas en el cinturón, reemplazando el placeholder de la sección de imágenes.

## Hecho (sesión 12)
- [x] Sección de imágenes reducida (`h-56`/`sm:h-64`, `max-w-md`) y centrada verticalmente respecto a la tarjeta "¿Qué es?" (`items-center` en el grid de la fila 1, en vez de estirarse a la misma altura).
- Nota: Snt ajustó por su cuenta los tiempos de animación (`dust-in` a 1500ms, `modal-drop-in` a 2000ms, `TIEMPO_VISIBLE_MS` del carrusel a 7500ms) — no se tocó nada de eso.

## Hecho (sesión 13)
- [x] Confirmado: no habrá cuarta imagen por ahora (se queda en 3).
- [x] Verificado el layout en móvil: con `grid-cols-1` (por debajo de `lg`), "¿Qué es?" ya queda arriba y la imagen debajo, centrada y en su tamaño reducido (224px de alto) — no hizo falta tocar código, ya se comportaba así.

## Hecho (sesión 14) — Pantalla de carga (intro)
- [x] `IntroSplash.jsx` + `IntroSplash.css` (componente aparte, en `utils/`): pantalla de carga con fondo `color-brand`, título "SignIA" + lema apareciendo centrados y grandes, luego "succionados" (2.8s, curva de aceleración) hasta la posición/tamaño aproximados del header real, con un crossfade final de color/fondo hacia los tonos reales de la app antes de desmontarse. Duración total ≈4.65s, bajo el límite de 6s.
- [x] Barra de carga con una mano-emoji que se desliza y cambia de "seña" (🖐️→🤟→🤙→👌) a los cortes de 25/75/99% del progreso — alternativa vía CSS/emoji ya que no hay assets de manos, tal como se autorizó.
- [x] `AppRoot.jsx` — orquestador nuevo: mientras la intro está activa, `App` ni se monta (así ninguna otra animación de la página corre en paralelo); al terminar (`onFinish`), guarda `signia-intro-vista=1` en `localStorage` y monta `App`. Un reload posterior ya no vuelve a mostrar la intro (verificado).
- [x] `utils/theme.js` — se extrajo la lógica de tema (antes solo en `ThemeToggle`) para aplicarse de forma sincrónica en `main.jsx` ANTES de montar React, evitando parpadeos de tema tanto en la intro como en la app real (verificado en claro y oscuro).
- [x] No se tocó ninguno de los tiempos/valores que Snt ajustó por su cuenta (`App.css`, `ImageBelt.jsx`).

## Hecho (sesión 15)
- [x] Quitada la regla de "no volver a salir si recargas": ahora **toda** carga muestra algo.
- [x] `IntroSplash.jsx` acepta `soloFade`: si ya se vio la animación completa antes (`localStorage`), no se repite — solo se ve el mismo fondo `color-brand` desvaneciéndose (500ms) hasta dejar ver la home, que ya está montada detrás.
- [x] `AppRoot.jsx` reestructurado: primera vez = animación completa sin montar `App` (regla 4 intacta); cualquier otra vez = `App` se monta de una vez y el velo rápido se superpone encima. Verificado ambos casos en el navegador (primera carga con animación completa, recarga con solo el velo).

## Hecho (sesión 16)
- [x] Revertido el velo de recarga (`soloFade`): la intro vuelve a ser exactamente "una sola vez, punto" — `AppRoot.jsx` e `IntroSplash.jsx`/`.css` de vuelta a como estaban antes de esa prueba.
- [x] Verificada la paleta: todo (incluida la intro) usa `var(--color-brand/bg/surface/secondary)`, así que ya refleja los valores actuales del disco sin necesidad de tocar nada.
- [x] Trabajo de frontend dividido en 4 commits en `main`:
  1. `d2067f2` chore: retirar scaffold antiguo `front/signia`.
  2. `f97eb25` feat: botones del header (`ThemeToggle`, `BurgerMenu`, `theme.js`).
  3. `557bd66` feat: estructura del proyecto, secciones y contenido de la home.
  4. `14e168c` feat: pantalla de carga inicial (animación).
- Nota: quedaron sin commitear (fuera del alcance de "frontend"): `.claude/launch.json`, `.gitignore` (raíz), `.claude/claude.md`, `.claude/mejoras.md` — pendiente de que Snt diga si quiere versionarlos.

## Hecho (sesión 17) — bug de color en la intro
- [x] `IntroSplash.css`: el fondo del overlay usaba `--color-brand`; se cambió a `--color-bg` (el fondo real del sitio). El título usa `--color-brand` desde el inicio (ya no blanco + crossfade), y la barra de carga pasó de blanco fijo a `--color-brand`/`--color-secondary` — todo coherente con la paleta activa. Verificado en claro y oscuro con estilos computados.

## Hecho (sesión 18)
- [x] `.claude/` agregado al tracking de git y commiteado (`760de5d`): `claude.md`, `mejoras.md`, `launch.json` actualizado.
- [x] `Header.jsx` — header común extraído (título+lema, tema, burger menu), usado ahora en `App.jsx` y en las páginas nuevas, para que sea idéntico en todo el sitio en vez de copiado.
- [x] `pages/Traduccion.jsx` y `pages/Entrenamiento.jsx` — estructura básica (header + fondo `bg-bg`) con su título de sección; contenido específico de cada una queda pendiente.
- [x] `BurgerMenu`: agregado el enlace a "Entrenamiento" junto a Inicio y Traductor.
- Todo esto en el commit `ddc4484`.

## Hecho (sesión 19)
- [x] Instalado `react-router-dom` y conectadas las 3 páginas de verdad: `BrowserRouter` en `main.jsx`, `Routes`/`Route` en `AppRoot.jsx` (`/`, `/traduccion`, `/entrenamiento`), y `BurgerMenu` usando `<Link>` en vez de `<a>` planos. Verificado navegando por el menú y recargando directo en `/traduccion` (fallback SPA de Vite).
- [x] Confirmado (por historial de git) que no se tocó la paleta de colores en ningún commit propio; solo se corrigió a qué variable apuntaba la intro.

## Hecho (sesión 20)
- [x] `PageLayout.jsx` — nuevo componente base en `utils/`: agrupa el wrapper comun a toda pagina de SignIA (div raiz `min-h-screen bg-bg...` + `<Header/>` + `<main className="mx-auto max-w-[110rem]...">`), recibiendo el contenido de cada pagina como `children` (asi cada una mantiene libertad sobre su propio titulo, incluido el efecto "polvo" de la home).
- [x] `App.jsx` migrado a `PageLayout` como base. Verificado en el navegador (screenshot + sin errores de consola/servidor): la home se ve identica a como estaba antes del cambio.

## Pendiente / próximos pasos
- [ ] Migrar `pages/Traduccion.jsx` y `pages/Entrenamiento.jsx` a `PageLayout.jsx` (por ahora solo se aplico en `App.jsx`, a pedido de Snt).
- [ ] Definir el contenido real de `Traduccion.jsx` (el traductor en si) y `Entrenamiento.jsx` (modulo de practica).
- [ ] Si más adelante se agregan assets reales de manos/señas, reemplazar los emojis de `IntroSplash.jsx` (`SENAS`) por esos assets.
- [ ] Revisar la intro en pantallas muy angostas (el docking usa `left: 1.5rem` / `sm:2.5rem`, igual que el header real, pero vale la pena confirmarlo en dispositivo).
- [ ] Snt sigue con los "Verificar" pendientes de `.informacion-homepage.md` para afinar el contenido si hace falta (aunque ya está aplicado).
- [ ] Integrar en `App.jsx`: 3 secciones separadas (ya no una sola tarjeta "Que es?"), cada una con su propia burbuja de información mostrando el texto "Detalle".
- [ ] **No hay router** (`react-router-dom` no está instalado). Los enlaces del burger menu ("Inicio" → `/`, "Traductor" → `/traduccion`) son visuales; al no existir rutas reales, no navegan entre `App.jsx` y `Traduccion.jsx` como páginas SPA. Falta decidir e instalar un router para conectarlas de verdad.
- [ ] `Sidebar.jsx` sigue vacío y sin usar — con el burger menu ya implementado, probablemente se pueda eliminar; a confirmar.
- [ ] `Button.jsx` tiene variantes (`primary`, `sidebar`, `burble`, `stop`, `default`) declaradas pero sin estilos ni uso real — unificarlo con la paleta nueva.
- [ ] Extraer estilos repetidos de botones a `Button.jsx` en vez de clases sueltas en `App.jsx`.
- [ ] Contraste de accesibilidad: revisar `secondary` con texto oscuro en fondos claros.
- [ ] `.claude/launch.json` se había borrado del repo; lo recreé solo para poder previsualizar con el navegador embebido — confirmar si se quiere versionado o no.

## Ideas futuras (bajo prioridad)
- [ ] Modo "sistema" explícito (además de claro/oscuro) en el toggle.
- [ ] Animación de transición al cambiar de tema.
