import { useEffect, useId, useRef, useState } from 'react'

const DEFAULT_LINKS = [
    { label: 'Inicio', href: '/' },
    { label: 'Traductor', href: '/traduccion' },
    { label: 'Entrenamiento', href: '/entrenamiento' },
]

export default function BurgerMenu({ links = DEFAULT_LINKS }) {
    const [open, setOpen] = useState(false)
    const panelId = useId()
    const firstLinkRef = useRef(null)

    useEffect(() => {
        if (!open) return undefined

        firstLinkRef.current?.focus()

        const onKeyDown = (event) => {
            if (event.key === 'Escape') setOpen(false)
        }
        document.addEventListener('keydown', onKeyDown)
        return () => document.removeEventListener('keydown', onKeyDown)
    }, [open])

    return (
        <div className="relative">
            <button
                type="button"
                onClick={() => setOpen((prev) => !prev)}
                aria-expanded={open}
                aria-controls={panelId}
                aria-label={open ? 'Cerrar menu' : 'Abrir menu'}
                className="flex h-10 w-10 flex-col items-center justify-center gap-1.5 rounded-md transition-opacity hover:opacity-80"
            >
                <span
                    className={`h-0.5 w-5 rounded-full bg-secondary transition-transform ${
                        open ? 'translate-y-2 rotate-45' : ''
                    }`}
                />
                <span
                    className={`h-0.5 w-5 rounded-full bg-secondary transition-opacity ${
                        open ? 'opacity-0' : ''
                    }`}
                />
                <span
                    className={`h-0.5 w-5 rounded-full bg-secondary transition-transform ${
                        open ? '-translate-y-2 -rotate-45' : ''
                    }`}
                />
            </button>

            {open && (
                <>
                    <button
                        type="button"
                        aria-label="Cerrar menu"
                        onClick={() => setOpen(false)}
                        className="fixed inset-0 z-40 cursor-default bg-slate-900/40"
                    />
                    <nav
                        id={panelId}
                        aria-label="Menu principal"
                        className="absolute right-0 z-50 mt-2 w-48 overflow-hidden rounded-lg bg-surface shadow-lg"
                    >
                        <ul className="flex flex-col py-2">
                            {links.map((link, index) => (
                                <li key={link.href}>
                                    <a
                                        ref={index === 0 ? firstLinkRef : null}
                                        href={link.href}
                                        onClick={() => setOpen(false)}
                                        className="block px-4 py-2 text-sm font-medium text-brand transition-colors hover:bg-secondary/40"
                                    >
                                        {link.label}
                                    </a>
                                </li>
                            ))}
                        </ul>
                    </nav>
                </>
            )}
        </div>
    )
}
