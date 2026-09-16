import Header from './Header'

/** Base comun de cualquier pagina: fondo + Header + <main> con el ancho y espaciado del sitio.
 *
 * Cada pagina aporta su contenido (titulo incluido) como children, para no
 * perder libertad sobre como se ve, por ejemplo el efecto "polvo" de Inicio.
 */
export default function PageLayout({ children }) {
    return (
        <div className="min-h-screen bg-bg text-slate-900 transition-colors dark:text-slate-100">
            <Header />
            <main className="mx-auto max-w-[110rem] space-y-14 px-6 py-14 sm:px-10 lg:px-16">{children}</main>
        </div>
    )
}
