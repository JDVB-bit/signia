/** 🗃️ Lote de muestras acumuladas en memoria del navegador durante la sesion. */

import { useCallback, useState } from 'react'

/** Coleccion de muestras con las operaciones que ofrece la pagina de Entrenamiento. */
export default function useMuestrasCapturadas() {
    const [muestras, setMuestras] = useState([])

    const agregar = useCallback((muestra) => setMuestras((previas) => [...previas, muestra]), [])
    const borrarUltima = useCallback(() => setMuestras((previas) => previas.slice(0, -1)), [])
    const limpiar = useCallback(() => setMuestras([]), [])

    return { muestras, agregar, borrarUltima, limpiar }
}
