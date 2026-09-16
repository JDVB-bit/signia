import BurgerMenu from '../navegacion/BurgerMenu'
import ThemeToggle from '../tema/ThemeToggle'

/** Cabecera comun a todas las paginas: marca + lema, boton de tema y menu. */
export default function Header() {
    return (
        <header className="flex items-center justify-between gap-4 bg-surface px-6 py-4 sm:px-10">
            <div>
                <h1 className="text-3xl font-bold text-brand">SignIA</h1>
                {/* El lema es un subtitulo, no un encabezado: no debe romper la jerarquia h1 > h2 */}
                <p className="text-sm text-brand opacity-80">Manos que hablan. Tecnología que escucha</p>
            </div>
            <nav aria-label="Preferencias y navegación" className="flex items-center gap-3">
                <ThemeToggle />
                <BurgerMenu />
            </nav>
        </header>
    )
}
