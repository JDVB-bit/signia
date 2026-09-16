import { Route, Routes } from 'react-router-dom'

import IntroSplash from './componentes/intro/IntroSplash'
import useIntroInicial from './hooks/useIntroInicial'
import Entrenamiento from './paginas/Entrenamiento'
import Inicio from './paginas/Inicio'
import Traduccion from './paginas/Traduccion'
import { RUTAS } from './rutas'

/** Raiz de la interfaz: la intro (solo la primera visita) o las rutas del sitio.
 *
 * Mientras la intro esta activa no se monta ninguna pagina, asi ninguna otra
 * animacion compite con ella.
 */
export default function AplicacionRaiz() {
    const { mostrarIntro, finalizarIntro } = useIntroInicial()

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
