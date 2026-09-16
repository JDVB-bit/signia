import ThemeToggle from "../tema/ThemeToggle"
import BurgerMenu from "../navegacion/BurgerMenu"

/** Header comun a todas las paginas del sitio: titulo + lema, boton de
 * tema y burger menu. Se centraliza aca para que sea igual en todas
 * partes en vez de repetir el markup por pagina. */
export default function Header() {
    return (
        <header className="flex items-center justify-between gap-4 bg-surface px-6 py-4 sm:px-10">
            <section>
                <h1 className="text-3xl font-bold text-brand">SignIA</h1>
                <h3 className="text-sm opacity-80 text-brand">Manos que hablan. Tecnologia que escucha</h3>
            </section>
            <section className="flex items-center gap-3">
                <ThemeToggle />
                <BurgerMenu />
            </section>
        </header>
    )
}
