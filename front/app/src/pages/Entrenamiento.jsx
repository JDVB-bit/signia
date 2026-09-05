import Header from "../utils/Header"

export default function Entrenamiento() {

    return (
        <div className="min-h-screen bg-bg text-slate-900 transition-colors dark:text-slate-100">
            <Header />

            <main className="mx-auto max-w-[110rem] space-y-14 px-6 py-14 sm:px-10 lg:px-16">
                <h2 className="text-center text-4xl font-extrabold tracking-tight text-brand drop-shadow-sm sm:text-5xl lg:text-6xl">
                    Entrenamiento
                </h2>
                <section>
                    {/*Aca ira el modulo de entrenamiento/practica de senas.
                        Por ahora solo la estructura base.*/}
                </section>
            </main>
        </div>
    )
}
