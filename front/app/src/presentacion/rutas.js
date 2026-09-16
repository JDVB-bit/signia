/** 🧭 Unica fuente de las rutas del sitio: la usan el router y el menu de navegacion. */

export const RUTAS = Object.freeze({
    INICIO: '/',
    TRADUCCION: '/traduccion',
    ENTRENAMIENTO: '/entrenamiento',
})

/** Enlaces del menu principal, en el orden en que se muestran. */
export const ENLACES_DE_NAVEGACION = [
    { etiqueta: 'Inicio', ruta: RUTAS.INICIO },
    { etiqueta: 'Traductor', ruta: RUTAS.TRADUCCION },
    { etiqueta: 'Entrenamiento', ruta: RUTAS.ENTRENAMIENTO },
]
