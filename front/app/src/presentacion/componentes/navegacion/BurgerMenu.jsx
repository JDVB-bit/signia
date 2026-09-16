import { useCallback, useEffect, useId, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

import useCerrarConEscape from '../../hooks/useCerrarConEscape'
import { ENLACES_DE_NAVEGACION } from '../../rutas'

/** Menu hamburguesa: el icono se anima a ✕ y abre un panel con los enlaces del sitio.
 *
 * Se cierra con click fuera, con Escape o al elegir un enlace, y al abrirse
 * lleva el foco al primer enlace para poder navegar con teclado.
 */
export default function BurgerMenu({ enlaces = ENLACES_DE_NAVEGACION }) {
    const [abierto, setAbierto] = useState(false)
    const panelId = useId()
    const primerEnlaceRef = useRef(null)

    const cerrar = useCallback(() => setAbierto(false), [])
    useCerrarConEscape(abierto, cerrar)

    // ♿ Foco al primer enlace: quien navega con teclado no tiene que buscar el panel
    useEffect(() => {
        if (abierto) primerEnlaceRef.current?.focus()
    }, [abierto])

    return (
        <div className="relative">
            <button
                type="button"
                onClick={() => setAbierto((previo) => !previo)}
                aria-expanded={abierto}
                aria-controls={panelId}
                aria-label={abierto ? 'Cerrar menú' : 'Abrir menú'}
                className="flex h-10 w-10 flex-col items-center justify-center gap-1.5 rounded-md transition-opacity hover:opacity-80"
            >
                <span
                    className={`h-0.5 w-5 rounded-full bg-secondary transition-transform ${
                        abierto ? 'translate-y-2 rotate-45' : ''
                    }`}
                />
                <span
                    className={`h-0.5 w-5 rounded-full bg-secondary transition-opacity ${
                        abierto ? 'opacity-0' : ''
                    }`}
                />
                <span
                    className={`h-0.5 w-5 rounded-full bg-secondary transition-transform ${
                        abierto ? '-translate-y-2 -rotate-45' : ''
                    }`}
                />
            </button>

            {abierto && (
                <>
                    {/* Fondo que cierra el menu al pulsar fuera del panel */}
                    <button
                        type="button"
                        aria-label="Cerrar menú"
                        onClick={cerrar}
                        className="fixed inset-0 z-40 cursor-default bg-slate-900/40"
                    />
                    <nav
                        id={panelId}
                        aria-label="Menú principal"
                        className="absolute right-0 z-50 mt-2 w-48 overflow-hidden rounded-lg bg-surface shadow-lg"
                    >
                        <ul className="flex flex-col py-2">
                            {enlaces.map((enlace, indice) => (
                                <li key={enlace.ruta}>
                                    <Link
                                        ref={indice === 0 ? primerEnlaceRef : null}
                                        to={enlace.ruta}
                                        onClick={cerrar}
                                        className="block px-4 py-2 text-sm font-medium text-brand transition-colors hover:bg-secondary/40"
                                    >
                                        {enlace.etiqueta}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </nav>
                </>
            )}
        </div>
    )
}
