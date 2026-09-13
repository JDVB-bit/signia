/** Base comun para cualquier pagina de SignIA: fondo + Header + <main> con el
 * ancho/espaciado estandar del sitio. Cada pagina construye su contenido
 * (titulo, secciones, etc.) como children, para no perder libertad sobre
 * como se ve el titulo de cada una (por ejemplo el efecto "polvo" de la home). */
import Header from "./Header"

export default function PageLayout({ children }) {
    return (
        <div className="min-h-screen bg-bg text-slate-900 transition-colors dark:text-slate-100">
            <Header />
            <main className="mx-auto max-w-[110rem] space-y-14 px-6 py-14 sm:px-10 lg:px-16">
                {children}
            </main>
        </div>
    )
}
