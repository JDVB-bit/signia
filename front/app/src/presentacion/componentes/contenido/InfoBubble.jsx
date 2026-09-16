import { useCallback, useId, useState } from 'react'

import useCerrarConEscape from '../../hooks/useCerrarConEscape'

/** Burbuja de informacion: abre un dialogo centrado, con el fondo difuminado, para leer el detalle.
 *
 * Se cierra con el boton ✕, con Escape o pulsando fuera del panel.
 */
export default function InfoBubble({ label = 'Más información', children }) {
    const [abierta, setAbierta] = useState(false)
    const panelId = useId()

    const cerrar = useCallback(() => setAbierta(false), [])
    useCerrarConEscape(abierta, cerrar)

    return (
        <>
            <button
                type="button"
                onClick={() => setAbierta(true)}
                aria-haspopup="dialog"
                aria-expanded={abierta}
                aria-controls={panelId}
                className="mt-4 flex items-center gap-2 rounded-md px-1 py-1 text-sm font-medium text-secondary transition-opacity hover:opacity-80"
            >
                <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-2 border-secondary text-xs font-bold">
                    i
                </span>
                {label}
            </button>

            {abierta && (
                <div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-sm"
                    onClick={cerrar}
                >
                    {/* stopPropagation: un click DENTRO del panel no debe cerrarlo */}
                    <div
                        id={panelId}
                        role="dialog"
                        aria-modal="true"
                        onClick={(evento) => evento.stopPropagation()}
                        className="animate-modal-drop-in relative max-h-[80vh] w-[min(40rem,92vw)] overflow-y-auto rounded-xl bg-surface p-8 text-lg leading-loose tracking-wide text-slate-900 shadow-2xl dark:text-slate-100 sm:p-10"
                    >
                        <button
                            type="button"
                            onClick={cerrar}
                            aria-label="Cerrar"
                            className="absolute right-4 top-4 text-secondary transition-opacity hover:opacity-70"
                        >
                            ✕
                        </button>
                        <div className="space-y-4 pr-4">{children}</div>
                    </div>
                </div>
            )}
        </>
    )
}
