import { useEffect, useId, useState } from 'react'

/** Burbuja de informacion: abre un panel centrado en pantalla, con el
 * fondo difuminado, para dar mas espacio y legibilidad al detalle. */
export default function InfoBubble({ label = 'Mas informacion', children }) {
    const [open, setOpen] = useState(false)
    const panelId = useId()

    useEffect(() => {
        if (!open) return undefined

        const onKeyDown = (event) => {
            if (event.key === 'Escape') setOpen(false)
        }
        document.addEventListener('keydown', onKeyDown)
        return () => document.removeEventListener('keydown', onKeyDown)
    }, [open])

    return (
        <>
            <button
                type="button"
                onClick={() => setOpen(true)}
                aria-haspopup="dialog"
                aria-expanded={open}
                aria-controls={panelId}
                className="mt-4 flex items-center gap-2 rounded-md px-1 py-1 text-sm font-medium text-secondary transition-opacity hover:opacity-80"
            >
                <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-2 border-secondary text-xs font-bold">
                    i
                </span>
                {label}
            </button>

            {open && (
                <div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-sm"
                    onClick={() => setOpen(false)}
                >
                    <div
                        id={panelId}
                        role="dialog"
                        aria-modal="true"
                        onClick={(event) => event.stopPropagation()}
                        className="animate-modal-drop-in relative max-h-[80vh] w-[min(40rem,92vw)] overflow-y-auto rounded-xl bg-surface p-8 text-lg leading-loose tracking-wide text-slate-900 shadow-2xl dark:text-slate-100 sm:p-10"
                    >
                        <button
                            type="button"
                            onClick={() => setOpen(false)}
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
