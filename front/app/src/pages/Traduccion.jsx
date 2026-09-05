import ThemeToggle from "../utils/ThemeToggle"
import BurgerMenu from "../utils/BurgerMenu"

export default function Traduccion(){

    return (
        <div className="min-h-screen bg-bg text-slate-900 transition-colors dark:text-slate-100">
            <header className="flex items-center justify-between gap-4 bg-surface px-6 py-4">
                <h1 className="text-3xl font-bold text-brand">SignIA</h1>
                <div className="flex items-center gap-3">
                    <ThemeToggle />
                    <BurgerMenu />
                </div>
            </header>

            <main className="mx-auto max-w-4xl px-6 py-10">
                <section>

                </section>
            </main>
        </div>
    )
}
