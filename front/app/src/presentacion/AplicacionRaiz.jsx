import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import Inicio from './paginas/Inicio'
import Traduccion from './paginas/Traduccion'
import Entrenamiento from './paginas/Entrenamiento'
import IntroSplash from './componentes/intro/IntroSplash'
import { RUTAS } from './rutas'

const INTRO_STORAGE_KEY = 'signia-intro-vista'

function yaSeVioLaIntro() {
    if (typeof window === 'undefined') return true
    return localStorage.getItem(INTRO_STORAGE_KEY) === '1'
}

/** Decide si mostrar la pantalla de carga o las rutas reales del sitio.
 * Mientras la intro esta activa, nada de eso se monta: asi ninguna otra
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

    return (
        <Routes>
            <Route path={RUTAS.INICIO} element={<Inicio />} />
            <Route path={RUTAS.TRADUCCION} element={<Traduccion />} />
            <Route path={RUTAS.ENTRENAMIENTO} element={<Entrenamiento />} />
        </Routes>
    )
}
