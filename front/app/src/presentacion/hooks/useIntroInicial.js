/** 🎬 Decide si mostrar la intro: solo la primera vez que alguien entra al sitio. */

import { useCallback, useState } from 'react'

import { introYaVista, marcarIntroVista } from '../../infra/navegador/registroDeIntro.js'

export default function useIntroInicial() {
    const [mostrarIntro, setMostrarIntro] = useState(() => !introYaVista())

    const finalizarIntro = useCallback(() => {
        marcarIntroVista()
        setMostrarIntro(false)
    }, [])

    return { mostrarIntro, finalizarIntro }
}
