import { useState } from 'react'
import App from './App'
import IntroSplash from './utils/IntroSplash'

const INTRO_STORAGE_KEY = 'signia-intro-vista'

function yaSeVioLaIntro() {
    if (typeof window === 'undefined') return true
    return localStorage.getItem(INTRO_STORAGE_KEY) === '1'
}

/** Decide si mostrar la pantalla de carga o la app real. Mientras la
 * intro esta activa, App ni siquiera se monta: asi ninguna otra
 * animacion de la pagina corre al mismo tiempo que ella. Se muestra una
 * unica vez: recargar la pagina no la vuelve a disparar. */
export default function AppRoot() {
    const [mostrarIntro, setMostrarIntro] = useState(() => !yaSeVioLaIntro())

    const finalizarIntro = () => {
        localStorage.setItem(INTRO_STORAGE_KEY, '1')
        setMostrarIntro(false)
    }

    if (mostrarIntro) {
        return <IntroSplash onFinish={finalizarIntro} />
    }

    return <App />
}
